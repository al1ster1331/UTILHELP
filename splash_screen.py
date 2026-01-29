from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QPixmap


class SplashScreen(QWidget):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Загрузка...")
        self.setFixedSize(400, 300)  
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.background = QWidget()
        
        self.gradient_position = 0
        self.gradient_timer = QTimer()
        self.gradient_timer.timeout.connect(self.update_gradient)
        self.gradient_timer.start(100)  

        self.update_gradient()
        
        bg_layout = QVBoxLayout(self.background)
        bg_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        title_label = QLabel("UTILHELP")
        title_label.setObjectName("title_label")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 28px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                letter-spacing: 2px;
                background: transparent;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scrolling_text = QLabel()
        self.scrolling_text.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 14px;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: transparent;
                min-height: 20px;
            }
        """)
        self.scrolling_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.scroll_messages = [
            "Добро пожаловать в UTILHELP"
        ]
        self.current_message_index = 0
        self.scroll_position = 0
        self.scroll_direction = 1
        
        self.scroll_timer = QTimer()
        self.scroll_timer.timeout.connect(self.update_scrolling_text)
        self.scroll_timer.start(50)  
        
        self.status_label = QLabel("Инициализация системы...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-weight: bold;
                background: transparent;
            }
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.original_title = "UTILHELP"
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(220)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border-radius: 10px;
                background-color: #404040;
                text-align: center;
                color: #ffffff;
                font-weight: bold;
                font-size: 10px;
            }
            QProgressBar::chunk {
                background-color: #666666;
                border-radius: 8px;
                margin: 1px;
                min-width: 20px;
            }
        """)
        
        bg_layout.addWidget(title_label)
        bg_layout.addSpacing(10)
        bg_layout.addWidget(self.scrolling_text)
        bg_layout.addSpacing(20)
        
        actions_container = QWidget()
        actions_container.setFixedHeight(25)
        actions_container.setStyleSheet("background: transparent;")
        actions_layout = QVBoxLayout(actions_container)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        bg_layout.addWidget(actions_container)
        
        bg_layout.addSpacing(25)
        
        progress_container = QWidget()
        progress_container.setFixedHeight(30)
        progress_container.setStyleSheet("background: transparent;")
        progress_layout = QVBoxLayout(progress_container)
        progress_layout.setContentsMargins(0, 0, 0, 0)
        progress_layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        bg_layout.addWidget(progress_container)
        
        layout.addWidget(self.background)
        self.setLayout(layout)
        
        screen = self.screen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
        self.progress_animation = QPropertyAnimation(self.progress_bar, b"value")
        self.progress_animation.setDuration(2000)  
        self.progress_animation.setStartValue(0)
        self.progress_animation.setEndValue(100)
        self.progress_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        
        self.status_messages = [
            "Инициализация системы...",
            "Загрузка компонентов интерфейса...",
            "Подключение к базам данных...",
            "Проверка конфигурации...",
            "Подготовка рабочего пространства...",
            "Загрузка ресурсов...",
            "Финализация запуска...",
            "Готово!"
        ]
        self.current_status = 0

    def update_gradient(self):
        self.gradient_position = (self.gradient_position + 1) % 100
        
        progress = self.gradient_position / 100.0
        
        colors = [
            "#1a1a1a",  
            "#2d2d2d",  
            "#353535",  
            "#404040",  
            "#2a2a2a"   
        ]
        
        pos1 = int(progress * 2) % len(colors)
        pos2 = (pos1 + 1) % len(colors)
        pos3 = (pos1 + 2) % len(colors)
        
        gradient_style = f"""
            background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                stop: 0 {colors[pos1]}, 
                stop: 0.5 {colors[pos2]}, 
                stop: 1 {colors[pos3]});
            border-radius: 15px;
        """
        
        self.background.setStyleSheet(gradient_style)

    def update_scrolling_text(self):
        if not hasattr(self, 'scroll_messages'):
            return
            
        current_message = self.scroll_messages[0]  
        
        if self.scroll_position <= len(current_message):
            if self.scroll_position < len(current_message):
                visible_text = current_message[:self.scroll_position + 1]
                visible_text += "█"  
            else:
                visible_text = current_message  
            
            self.scrolling_text.setText(visible_text)
            self.scroll_position += 1

    def start_animation(self):
        """Запуск анимации загрузки"""
        self.status_timer.start(200)  
        self.progress_animation.start()
        
        self.progress_animation.finished.connect(self.close_with_cleanup)

    def close_with_cleanup(self):
        """Закрытие с очисткой таймеров"""
        if hasattr(self, 'gradient_timer'):
            self.gradient_timer.stop()
        if hasattr(self, 'scroll_timer'):
            self.scroll_timer.stop()
        if hasattr(self, 'status_timer'):
            self.status_timer.stop()
        
        self.close()

    def update_status(self):
        """Обновление статуса загрузки"""
        if self.current_status < len(self.status_messages):
            self.status_label.setText(self.status_messages[self.current_status])
            self.current_status += 1
        else:
            self.status_timer.stop()