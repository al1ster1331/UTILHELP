import os
import sys
import json
import requests
import subprocess
import tempfile
from packaging import version
from PyQt6.QtWidgets import QMessageBox, QApplication
from PyQt6.QtCore import QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QIcon, QTextBlockFormat


class UpdateChecker:
    """Класс для проверки обновлений с GitHub"""
    def __init__(self):
        self.current_version = "1.0"  
        self.github_repo = "al1ster13/UTILHELP"  
        self.github_api_url = f"https://api.github.com/repos/{self.github_repo}/releases/latest"
        
    def get_current_version(self):
        """Получить текущую версию программы"""
        try:
            version_file = os.path.join(os.path.dirname(__file__), "version.txt")
            if os.path.exists(version_file):
                with open(version_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except:
            pass
        
        return self.current_version
    
    def check_for_updates(self):
        """Проверить наличие обновлений на GitHub"""
        try:
            from temp_manager import debug_log
            debug_log("Checking for updates on GitHub...")
            
            response = requests.get(self.github_api_url, timeout=10)
            response.raise_for_status()
            release_data = response.json()
            latest_version = release_data.get('tag_name', '').lstrip('v')
            
            if latest_version.startswith('utilhelp-'):
                latest_version = latest_version[9:]  
            elif latest_version.startswith('v'):
                latest_version = latest_version[1:]   
            
            if not latest_version or not latest_version.replace('.', '').isdigit():
                debug_log(f"Invalid version format: {latest_version}")
                return {
                    'error': f'Неправильный формат версии: {latest_version}',
                    'update_available': False
                }
            release_name = release_data.get('name', '')
            release_notes = release_data.get('body', '')
            release_url = release_data.get('html_url', '')
            
            installer_url = None
            installer_name = None
            
            for asset in release_data.get('assets', []):
                asset_name = asset.get('name', '').lower()
                if 'setup' in asset_name and asset_name.endswith('.exe'):
                    installer_url = asset.get('browser_download_url')
                    installer_name = asset.get('name')
                    break
            
            current_ver = self.get_current_version()
            
            debug_log(f"Current version: {current_ver}")
            debug_log(f"Latest version: {latest_version}")
            
            try:
                if version.parse(latest_version) > version.parse(current_ver):
                    debug_log("New version available!")
                    return {
                        'update_available': True,
                        'latest_version': latest_version,
                        'current_version': current_ver,
                        'release_name': release_name,
                        'release_notes': release_notes,
                        'release_url': release_url,
                        'installer_url': installer_url,
                        'installer_name': installer_name
                    }
                else:
                    debug_log("No updates available")
                    return {
                        'update_available': False,
                        'latest_version': latest_version,
                        'current_version': current_ver
                    }
            except Exception as version_error:
                debug_log(f"Version comparison error: {version_error}")
                return {
                    'error': f'Ошибка сравнения версий: {str(version_error)}',
                    'update_available': False
                }
                
        except requests.exceptions.RequestException as e:
            from temp_manager import debug_log
            debug_log(f"Network error checking for updates: {e}")
            return {
                'error': f'Ошибка сети: {str(e)}',
                'update_available': False
            }
        except Exception as e:
            from temp_manager import debug_log
            debug_log(f"Error checking for updates: {e}")
            return {
                'error': f'Ошибка проверки обновлений: {str(e)}',
                'update_available': False
            }


class UpdateDownloader(QThread):
    """Поток для скачивания обновления"""
    
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(str)  
    download_failed = pyqtSignal(str)    
    
    def __init__(self, installer_url, installer_name):
        super().__init__()
        self.installer_url = installer_url
        self.installer_name = installer_name
        self.cancelled = False
        
    def run(self):
        """Скачивание установщика"""
        try:
            from temp_manager import debug_log
            debug_log(f"Starting download: {self.installer_url}")
            
            temp_dir = tempfile.gettempdir()
            installer_path = os.path.join(temp_dir, self.installer_name)
            
            response = requests.get(self.installer_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded_size = 0
            
            with open(installer_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if self.cancelled:
                        f.close()
                        if os.path.exists(installer_path):
                            os.remove(installer_path)
                        return
                    
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded_size / total_size) * 100)
                            self.progress_updated.emit(progress)
            
            debug_log(f"Download completed: {installer_path}")
            self.download_finished.emit(installer_path)
            
        except Exception as e:
            from temp_manager import debug_log
            debug_log(f"Download failed: {e}")
            self.download_failed.emit(str(e))
    
    def cancel(self):
        """Отменить скачивание"""
        self.cancelled = True


class UpdateManager:
    """Менеджер обновлений"""
    
    def __init__(self, parent_window=None):
        self.parent_window = parent_window
        self.checker = UpdateChecker()
        self.downloader = None
        self.progress_dialog = None
        
    def check_for_updates_silent(self):
        """Тихая проверка обновлений (без UI)"""
        return self.checker.check_for_updates()
    
    def check_for_updates_interactive(self):
        """Интерактивная проверка обновлений с UI"""
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QPixmap
            
            check_dialog = QDialog(self.parent_window)
            check_dialog.setWindowTitle("Проверка обновлений")
            check_dialog.setFixedSize(400, 180)
            check_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            
            check_dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
            check_dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            
            main_container = QFrame(check_dialog)
            main_container.setGeometry(10, 10, 380, 160)
            main_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #2d2d2d, stop: 1 #1a1a1a);
                    border-radius: 12px;
                    border: 1px solid #404040;
                }
            """)
            
            layout = QVBoxLayout(main_container)
            layout.setContentsMargins(25, 20, 25, 20)
            layout.setSpacing(15)
            
            header_layout = QHBoxLayout()
            
            icon_label = QLabel()
            try:
                from resource_path import get_icon_path
                logo_icon_path = get_icon_path("logo64x64.png")
                if logo_icon_path:
                    pixmap = QPixmap(logo_icon_path)
                    scaled_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    icon_label.setPixmap(scaled_pixmap)
            except:
                icon_label.setText("🔄")
                icon_label.setStyleSheet("font-size: 24px; background: transparent; border: none;")
            
            icon_label.setStyleSheet("""
                QLabel {
                    background: transparent;
                    border: none;
                    padding: 0px;
                    margin: 0px;
                }
            """)
            icon_label.setFixedSize(40, 40)
            header_layout.addWidget(icon_label)
            
            title_label = QLabel("UTILHELP - Обновления")
            title_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                    margin-left: 10px;
                }
            """)
            header_layout.addWidget(title_label)
            header_layout.addStretch()
            
            close_btn = QPushButton()
            close_btn.setFixedSize(30, 30)
            
            from resource_path import get_icon_path
            from PyQt6.QtGui import QIcon
            from PyQt6.QtCore import QSize
            
            close_icon_path = get_icon_path("closemenu.png")
            if close_icon_path:
                close_btn.setIcon(QIcon(close_icon_path))
                close_btn.setIconSize(QSize(16, 16))
                close_btn.setFlat(True)
            else:
                close_btn.setText("×")
            
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #a0aec0;
                    border: none;
                    border-radius: 15px;
                    font-size: 18px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e53e3e;
                    color: white;
                }
            """)
            close_btn.clicked.connect(check_dialog.reject)
            header_layout.addWidget(close_btn)
            
            layout.addLayout(header_layout)
            
            check_label = QLabel("Проверка обновлений...")
            check_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """)
            check_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(check_label)
            
            layout.addStretch()
            
            cancel_btn = QPushButton("Отмена")
            cancel_btn.setFixedHeight(35)
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(64, 64, 64, 0.3);
                    color: #ffffff;
                    border: 1px solid #404040;
                    border-radius: 6px;
                    font-size: 13px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    padding: 0 20px;
                }
                QPushButton:hover {
                    background-color: rgba(64, 64, 64, 0.5);
                }
            """)
            cancel_btn.clicked.connect(check_dialog.reject)
            layout.addWidget(cancel_btn)
            
            if self.parent_window:
                parent_geometry = self.parent_window.geometry()
                x = parent_geometry.x() + (parent_geometry.width() - check_dialog.width()) // 2
                y = parent_geometry.y() + (parent_geometry.height() - check_dialog.height()) // 2
                check_dialog.move(x, y)
            
            check_dialog.show()
            QApplication.processEvents()
            
            update_info = self.checker.check_for_updates()
            
            check_dialog.close()
            
            if 'error' in update_info:
                QMessageBox.warning(
                    self.parent_window,
                    "Ошибка проверки обновлений",
                    f"Не удалось проверить обновления:\n{update_info['error']}"
                )
                return False
            
            if update_info['update_available']:
                self.show_update_dialog(update_info)
                return True
            else:
                return False
                
        except Exception as e:
            QMessageBox.critical(
                self.parent_window,
                "Ошибка",
                f"Произошла ошибка при проверке обновлений:\n{str(e)}"
            )
            return False
    
    def show_update_dialog(self, update_info):
        """Показать диалог с предложением обновления"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
        from PyQt6.QtCore import Qt, QSize
        from PyQt6.QtGui import QFont, QPixmap, QIcon
        
        dialog = QDialog(self.parent_window)
        dialog.setWindowTitle("Обновление UTILHELP")
        dialog.setFixedSize(600, 500)
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        
        dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        main_container = QFrame(dialog)
        main_container.setGeometry(10, 10, 580, 480)
        main_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2d2d2d, stop: 1 #1a1a1a);
                border-radius: 16px;
                border: 1px solid #404040;
            }
        """)
        
        layout = QVBoxLayout(main_container)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel()
        try:
            from resource_path import get_icon_path
            logo_icon_path = get_icon_path("logo64x64.png")
            if logo_icon_path:
                pixmap = QPixmap(logo_icon_path)
                scaled_pixmap = pixmap.scaled(56, 56, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                icon_label.setPixmap(scaled_pixmap)
        except:
            icon_label.setText("🔄")
            icon_label.setStyleSheet("font-size: 48px; background: transparent; border: none;")
        
        icon_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
        """)
        icon_label.setFixedSize(64, 64)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel("Доступно обновление UTILHELP")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 20px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                border: none;
                margin-left: 10px;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        close_btn = QPushButton()
        close_btn.setFixedSize(28, 28)  
        
        close_icon_path = get_icon_path("closemenu.png")
        if close_icon_path:
            close_btn.setIcon(QIcon(close_icon_path))
            close_btn.setIconSize(QSize(16, 16))
            close_btn.setFlat(True)
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #666666;
                    border: none;
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 0px;
                    margin: 0px;
                    text-align: center;
                    line-height: 21px;
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #777777;
                }
                QPushButton:pressed {
                    background-color: #555555;
                }
                QPushButton:focus {
                    outline: none;
                    border: none;
                }
            """)
        else:
            close_btn.setText("✕")
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #666666;
                    border: none;
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 12px;
                    padding: 0px;
                    margin: 0px;
                    text-align: center;
                    line-height: 21px;
                    outline: none;
                }
                QPushButton:hover {
                    background-color: #777777;
                }
                QPushButton:pressed {
                    background-color: #555555;
                }
                QPushButton:focus {
                    outline: none;
                    border: none;
                }
            """)
        close_btn.clicked.connect(dialog.reject)
        header_layout.addWidget(close_btn)
        
        layout.addLayout(header_layout)
        
        version_container = QFrame()
        version_container.setStyleSheet("""
            QFrame {
                background-color: rgba(64, 64, 64, 0.3);
                border-radius: 12px;
                border: 1px solid rgba(64, 64, 64, 0.5);
            }
        """)
        version_layout = QVBoxLayout(version_container)
        version_layout.setSpacing(8)
        version_layout.setContentsMargins(15, 15, 15, 15)
        version_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        new_version_label = QLabel(f"Новая версия: {update_info['latest_version']}")
        new_version_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        new_version_label.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                border: none;
                text-align: left;
                qproperty-alignment: AlignLeft;
                margin-left: -2px;
            }
        """)
        version_layout.addWidget(new_version_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        if update_info.get('release_name'):
            release_name_label = QLabel(f"Релиз: {update_info['release_name']}")
            release_name_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            release_name_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                    font-weight: 500;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                    margin-top: 5px;
                    text-align: left;
                    qproperty-alignment: AlignLeft;
                    margin-left: -4px;
                }
            """)
            version_layout.addWidget(release_name_label, 0, Qt.AlignmentFlag.AlignLeft)
        
        layout.addWidget(version_container)
        
        if update_info.get('release_notes'):
            notes_label = QLabel("Что нового:")
            notes_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                    margin-bottom: 5px;
                }
            """)
            layout.addWidget(notes_label)
            
            from PyQt6.QtWidgets import QTextBrowser
            
            notes_text = QTextBrowser()
            notes_text.setMaximumHeight(120)
            notes_text.setReadOnly(True)
            
            formatted_text = f"""
            <div style="text-align: left; margin: 0; padding: 0; line-height: 1.4;">
                {update_info['release_notes'].replace(chr(10), '<br>')}
            </div>
            """
            notes_text.setHtml(formatted_text)
            
            notes_text.setStyleSheet("""
                QTextBrowser {
                    background-color: rgba(26, 26, 26, 0.8);
                    color: #ffffff;
                    border: 1px solid #404040;
                    border-radius: 8px;
                    padding: 8px;
                    font-size: 13px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QScrollBar:vertical {
                    background-color: #2d2d2d;
                    width: 8px;
                    border-radius: 4px;
                }
                QScrollBar::handle:vertical {
                    background-color: #404040;
                    border-radius: 4px;
                    min-height: 20px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #4a4a4a;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    border: none;
                    background: none;
                }
            """)
            
            layout.addWidget(notes_text)
        
        layout.addStretch()
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        update_btn = QPushButton("Обновить сейчас")
        update_btn.setFixedHeight(45)
        update_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4CAF50, stop: 1 #45a049);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 0 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5CBF60, stop: 1 #4CAF50);
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #45a049, stop: 1 #3d8b40);
            }
        """)
        
        later_btn = QPushButton("Позже")
        later_btn.setFixedHeight(45)
        later_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(64, 64, 64, 0.3);
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: rgba(64, 64, 64, 0.5);
                border: 1px solid #4a4a4a;
            }
            QPushButton:pressed {
                background-color: rgba(64, 64, 64, 0.7);
            }
        """)
        
        buttons_layout.addWidget(update_btn)
        buttons_layout.addWidget(later_btn)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        def on_update():
            dialog.accept()
            if update_info.get('installer_url'):
                self.download_and_install_update(update_info)
            else:
                from PyQt6.QtWidgets import QMessageBox
                msg = QMessageBox(self.parent_window)
                msg.setWindowTitle("Ошибка")
                msg.setText("Установщик не найден в релизе. Пожалуйста, скачайте обновление вручную.")
                msg.setIcon(QMessageBox.Icon.Warning)
                msg.exec()
        
        def on_later():
            dialog.reject()
        
        update_btn.clicked.connect(on_update)
        later_btn.clicked.connect(on_later)
        
        if self.parent_window:
            parent_geometry = self.parent_window.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - dialog.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - dialog.height()) // 2
            dialog.move(x, y)
        
        dialog.exec()
    
    def download_and_install_update(self, update_info):
        """Скачать и установить обновление"""
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar, QFrame
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QFont
            
            self.progress_dialog = QDialog(self.parent_window)
            self.progress_dialog.setWindowTitle("Скачивание обновления")
            self.progress_dialog.setFixedSize(450, 200)
            self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            
            self.progress_dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
            self.progress_dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            
            main_container = QFrame(self.progress_dialog)
            main_container.setGeometry(10, 10, 430, 180)
            main_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #2d2d2d, stop: 1 #1a1a1a);
                    border-radius: 12px;
                    border: 1px solid #404040;
                }
            """)
            
            layout = QVBoxLayout(main_container)
            layout.setContentsMargins(25, 20, 25, 20)
            layout.setSpacing(15)
            
            title_label = QLabel("Скачивание обновления...")
            title_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 16px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)
            
            file_label = QLabel(f"Файл: {update_info.get('installer_name', 'Установщик UTILHELP')}")
            file_label.setStyleSheet("""
                QLabel {
                    color: #a0aec0;
                    font-size: 12px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """)
            file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(file_label)
            
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            progress_bar.setFixedHeight(8)
            progress_bar.setStyleSheet("""
                QProgressBar {
                    background-color: rgba(64, 64, 64, 0.3);
                    border: none;
                    border-radius: 4px;
                }
                QProgressBar::chunk {
                    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0,
                        stop: 0 #4CAF50, stop: 1 #5CBF60);
                    border-radius: 4px;
                }
            """)
            layout.addWidget(progress_bar)
            
            percent_label = QLabel("0%")
            percent_label.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """)
            percent_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(percent_label)
            
            layout.addStretch()
            
            cancel_btn = QPushButton("Отмена")
            cancel_btn.setFixedHeight(35)
            cancel_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(229, 62, 62, 0.2);
                    color: #fc8181;
                    border: 1px solid rgba(229, 62, 62, 0.3);
                    border-radius: 6px;
                    font-size: 13px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    padding: 0 20px;
                }
                QPushButton:hover {
                    background-color: rgba(229, 62, 62, 0.3);
                    border: 1px solid rgba(229, 62, 62, 0.5);
                }
            """)
            layout.addWidget(cancel_btn)
            
            self.downloader = UpdateDownloader(
                update_info['installer_url'],
                update_info['installer_name']
            )
            
            def update_progress(value):
                progress_bar.setValue(value)
                percent_label.setText(f"{value}%")
            
            self.downloader.progress_updated.connect(update_progress)
            self.downloader.download_finished.connect(self.on_download_finished)
            self.downloader.download_failed.connect(self.on_download_failed)
            cancel_btn.clicked.connect(self.downloader.cancel)
            cancel_btn.clicked.connect(self.progress_dialog.close)
            
            self.downloader.start()
            self.progress_dialog.show()
            
            if self.parent_window:
                parent_geometry = self.parent_window.geometry()
                x = parent_geometry.x() + (parent_geometry.width() - self.progress_dialog.width()) // 2
                y = parent_geometry.y() + (parent_geometry.height() - self.progress_dialog.height()) // 2
                self.progress_dialog.move(x, y)
            
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self.parent_window,
                "Ошибка",
                f"Не удалось начать скачивание обновления:\n{str(e)}"
            )
    
    def on_download_finished(self, installer_path):
        """Обработка завершения скачивания"""
        try:
            if self.progress_dialog:
                self.progress_dialog.close()
            
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
            from PyQt6.QtCore import Qt
            from PyQt6.QtGui import QPixmap
            
            dialog = QDialog(self.parent_window)
            dialog.setWindowTitle("Обновление готово")
            dialog.setFixedSize(450, 250)
            dialog.setWindowModality(Qt.WindowModality.WindowModal)
            
            dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
            dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            
            main_container = QFrame(dialog)
            main_container.setGeometry(10, 10, 430, 230)
            main_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #2d2d2d, stop: 1 #1a1a1a);
                    border-radius: 12px;
                    border: 1px solid #404040;
                }
            """)
            
            layout = QVBoxLayout(main_container)
            layout.setContentsMargins(30, 25, 30, 25)
            layout.setSpacing(20)
            
            icon_label = QLabel()
            try:
                from resource_path import get_icon_path
                complete_icon_path = get_icon_path("complete.png")
                if complete_icon_path:
                    pixmap = QPixmap(complete_icon_path)
                    scaled_pixmap = pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    icon_label.setPixmap(scaled_pixmap)
                else:
                    icon_label.setText("✅")
                    icon_label.setStyleSheet("font-size: 48px;")
            except:
                icon_label.setText("✅")
                icon_label.setStyleSheet("font-size: 48px;")
            
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(icon_label)
            
            title_label = QLabel("Обновление скачано!")
            title_label.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    font-size: 18px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                }
            """)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(title_label)
            
            desc_label = QLabel("Запустить установку?\n\nПрограмма будет закрыта для установки обновления.")
            desc_label.setStyleSheet("""
                QLabel {
                    color: #ffffff;
                    font-size: 14px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: transparent;
                    border: none;
                    line-height: 1.4;
                }
            """)
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(desc_label)
            
            layout.addStretch()
            
            buttons_layout = QHBoxLayout()
            buttons_layout.setSpacing(15)
            
            install_btn = QPushButton("Установить сейчас")
            install_btn.setFixedHeight(40)
            install_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #4CAF50, stop: 1 #45a049);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: bold;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    padding: 0 25px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                        stop: 0 #5CBF60, stop: 1 #4CAF50);
                }
            """)
            
            later_btn = QPushButton("Позже")
            later_btn.setFixedHeight(40)
            later_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(64, 64, 64, 0.3);
                    color: #ffffff;
                    border: 1px solid #404040;
                    border-radius: 8px;
                    font-size: 14px;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    padding: 0 25px;
                }
                QPushButton:hover {
                    background-color: rgba(64, 64, 64, 0.5);
                }
            """)
            
            buttons_layout.addWidget(install_btn)
            buttons_layout.addWidget(later_btn)
            layout.addLayout(buttons_layout)
            
            def on_install():
                dialog.accept()
                self.run_installer(installer_path)
            
            def on_later():
                dialog.reject()
                from PyQt6.QtWidgets import QMessageBox
                msg = QMessageBox(self.parent_window)
                msg.setWindowTitle("Установщик сохранен")
                msg.setText(f"Установщик сохранен в:\n{installer_path}\n\nВы можете запустить его позже для обновления программы.")
                msg.setIcon(QMessageBox.Icon.Information)
                msg.exec()
            
            install_btn.clicked.connect(on_install)
            later_btn.clicked.connect(on_later)
            
            if self.parent_window:
                parent_geometry = self.parent_window.geometry()
                x = parent_geometry.x() + (parent_geometry.width() - dialog.width()) // 2
                y = parent_geometry.y() + (parent_geometry.height() - dialog.height()) // 2
                dialog.move(x, y)
            
            dialog.exec()
                
        except Exception as e:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(
                self.parent_window,
                "Ошибка",
                f"Ошибка при обработке скачанного файла:\n{str(e)}"
            )
    
    def on_download_failed(self, error_message):
        """Обработка ошибки скачивания"""
        if self.progress_dialog:
            self.progress_dialog.close()
        
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
        from PyQt6.QtCore import Qt
        from PyQt6.QtGui import QPixmap
        
        dialog = QDialog(self.parent_window)
        dialog.setWindowTitle("Ошибка скачивания")
        dialog.setFixedSize(450, 280)
        dialog.setWindowModality(Qt.WindowModality.WindowModal)
        
        dialog.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        dialog.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        main_container = QFrame(dialog)
        main_container.setGeometry(10, 10, 430, 260)
        main_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #2d2d2d, stop: 1 #1a1a1a);
                border-radius: 12px;
                border: 1px solid #404040;
            }
        """)
        
        layout = QVBoxLayout(main_container)
        layout.setContentsMargins(30, 25, 30, 25)
        layout.setSpacing(20)
        
        header_layout = QHBoxLayout()
        
        icon_label = QLabel()
        try:
            from resource_path import get_icon_path
            error_icon_path = get_icon_path("error.png")
            if error_icon_path:
                pixmap = QPixmap(error_icon_path)
                scaled_pixmap = pixmap.scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                icon_label.setPixmap(scaled_pixmap)
            else:
                icon_label.setText("❌")
                icon_label.setStyleSheet("font-size: 32px;")
        except:
            icon_label.setText("❌")
            icon_label.setStyleSheet("font-size: 32px;")
        
        icon_label.setFixedSize(40, 40)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel("Ошибка скачивания")
        title_label.setStyleSheet("""
            QLabel {
                color: #fc8181;
                font-size: 20px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                border: none;
                margin-left: 10px;
            }
        """)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        close_btn = QPushButton("×")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #a0aec0;
                border: none;
                border-radius: 15px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e53e3e;
                color: white;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        header_layout.addWidget(close_btn)
        
        layout.addLayout(header_layout)
        
        error_container = QFrame()
        error_container.setStyleSheet("""
            QFrame {
                background-color: rgba(229, 62, 62, 0.1);
                border-radius: 12px;
                border: 1px solid rgba(229, 62, 62, 0.3);
                padding: 15px;
            }
        """)
        error_layout = QVBoxLayout(error_container)
        error_layout.setSpacing(10)
        
        main_message_label = QLabel("Не удалось скачать обновление")
        main_message_label.setStyleSheet("""
            QLabel {
                color: #fc8181;
                font-size: 16px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                border: none;
            }
        """)
        error_layout.addWidget(main_message_label)
        
        error_details_label = QLabel(f"Детали ошибки:\n{error_message}")
        error_details_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                border: none;
                line-height: 1.4;
            }
        """)
        error_details_label.setWordWrap(True)
        error_layout.addWidget(error_details_label)
        
        layout.addWidget(error_container)
        
        suggestions_label = QLabel("Возможные решения:")
        suggestions_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                border: none;
                margin-top: 5px;
            }
        """)
        layout.addWidget(suggestions_label)
        
        suggestions_text = QLabel("• Проверьте подключение к интернету\n• Попробуйте позже\n• Скачайте обновление вручную с GitHub")
        suggestions_text.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                border: none;
                line-height: 1.5;
            }
        """)
        layout.addWidget(suggestions_text)
        
        layout.addStretch()
        
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        
        retry_btn = QPushButton("Повторить")
        retry_btn.setFixedHeight(40)
        retry_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #4CAF50, stop: 1 #45a049);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 0 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #5CBF60, stop: 1 #4CAF50);
            }
        """)
        
        close_dialog_btn = QPushButton("Закрыть")
        close_dialog_btn.setFixedHeight(40)
        close_dialog_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(64, 64, 64, 0.3);
                color: #ffffff;
                border: 1px solid #404040;
                border-radius: 8px;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                padding: 0 25px;
            }
            QPushButton:hover {
                background-color: rgba(64, 64, 64, 0.5);
            }
        """)
        
        buttons_layout.addWidget(retry_btn)
        buttons_layout.addWidget(close_dialog_btn)
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        def on_retry():
            dialog.accept()
        
        def on_close():
            dialog.reject()
        
        retry_btn.clicked.connect(on_retry)
        close_dialog_btn.clicked.connect(on_close)
        
        if self.parent_window:
            parent_geometry = self.parent_window.geometry()
            x = parent_geometry.x() + (parent_geometry.width() - dialog.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - dialog.height()) // 2
            dialog.move(x, y)
        
        dialog.exec()
    
    def run_installer(self, installer_path):
        try:
            from temp_manager import debug_log
            debug_log(f"Running installer: {installer_path}")
            
            subprocess.Popen([installer_path], shell=True)
            
            QApplication.quit()
            
        except Exception as e:
            QMessageBox.critical(
                self.parent_window,
                "Ошибка запуска установщика",
                f"Не удалось запустить установщик:\n{str(e)}"
            )
    

update_manager = None


def get_update_manager(parent_window=None):
    """Получить экземпляр менеджера обновлений"""
    global update_manager
    if update_manager is None:
        update_manager = UpdateManager(parent_window)
    elif parent_window and update_manager.parent_window != parent_window:
        update_manager.parent_window = parent_window
    return update_manager