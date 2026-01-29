import winreg
import os
import subprocess
import re
from typing import Dict, List, Set
from settings_manager import settings_manager
from PyQt6.QtCore import QThread, pyqtSignal


class SystemScanner:
    """Сканер установленных программ и драйверов в системе"""
    
    def __init__(self):
        self.installed_programs = set()
        self.installed_drivers = set()
        self.program_versions = {}
        self.driver_versions = {}
    
    def scan_installed_programs(self) -> Set[str]:
        """Сканирование установленных программ через реестр Windows"""
        programs = set()
        versions = {}
        
        registry_paths = [
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
            (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall")
        ]
        
        for hkey, path in registry_paths:
            try:
                with winreg.OpenKey(hkey, path) as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if display_name and len(display_name.strip()) > 2:
                                        programs.add(display_name.strip())
                                        
                                        try:
                                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                                            if version:
                                                versions[display_name.strip()] = version.strip()
                                        except FileNotFoundError:
                                            pass
                                            
                                except FileNotFoundError:
                                    pass
                        except (OSError, FileNotFoundError):
                            continue
            except (OSError, FileNotFoundError):
                continue
        
        self.installed_programs = programs
        self.program_versions = versions
        return programs
    
    def scan_installed_drivers(self) -> Set[str]:
        """Сканирование установленных драйверов через PowerShell"""
        drivers = set()
        versions = {}
        
        try:
            powershell_command = """
            Get-WmiObject Win32_PnPSignedDriver | Where-Object {
                $_.DeviceName -and 
                $_.DriverVersion -and 
                $_.DeviceName -notlike "*Generic*" -and
                $_.DeviceName -notlike "*Standard*" -and
                $_.DeviceName -notlike "*Basic*" -and
                $_.DeviceName -notlike "*Microsoft*" -and
                $_.DeviceName -notlike "*Windows*"
            } | Select-Object DeviceName, DriverVersion, DriverDate | 
            ConvertTo-Json
            """
            
            result = subprocess.run(
                ["powershell", "-Command", powershell_command],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if result.returncode == 0 and result.stdout.strip():
                import json
                try:
                    driver_data = json.loads(result.stdout)
                    if isinstance(driver_data, list):
                        for driver in driver_data:
                            if driver.get("DeviceName"):
                                device_name = driver["DeviceName"].strip()
                                drivers.add(device_name)
                                if driver.get("DriverVersion"):
                                    versions[device_name] = driver["DriverVersion"].strip()
                    elif isinstance(driver_data, dict) and driver_data.get("DeviceName"):
                        device_name = driver_data["DeviceName"].strip()
                        drivers.add(device_name)
                        if driver_data.get("DriverVersion"):
                            versions[device_name] = driver_data["DriverVersion"].strip()
                except json.JSONDecodeError:
                    pass
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, FileNotFoundError):
            pass
        
        self.installed_drivers = drivers
        self.driver_versions = versions
        return drivers
    
    def check_program_installed(self, program_name: str) -> Dict[str, any]:
        """Проверка установлена ли конкретная программа"""
        program_name_lower = program_name.lower()
        
        for installed_program in self.installed_programs:
            installed_lower = installed_program.lower()
            
            if self._is_program_match(program_name_lower, installed_lower):
                return {
                    "installed": True,
                    "exact_name": installed_program,
                    "version": self.program_versions.get(installed_program, "Неизвестно")
                }
        
        return {"installed": False, "exact_name": None, "version": None}
    
    def check_driver_installed(self, driver_name: str) -> Dict[str, any]:
        """Проверка установлен ли конкретный драйвер или программа"""
        driver_name_lower = driver_name.lower()
        
        if 'directx' in driver_name_lower:
            if self._check_directx_installed():
                return {
                    "installed": True,
                    "exact_name": "DirectX (системный)",
                    "version": "Установлен"
                }
        
        program_result = self._check_in_programs(driver_name)
        if program_result["installed"]:
            return program_result
        
        driver_result = self._check_in_drivers(driver_name)
        if driver_result["installed"]:
            return driver_result
        
        return {"installed": False, "exact_name": None, "version": None}
    
    def _check_in_programs(self, driver_name: str) -> Dict[str, any]:
        """Проверка драйвера среди установленных программ"""
        driver_name_lower = driver_name.lower()
        driver_words = set(self._extract_key_words(driver_name_lower))
        
        candidates = []  
        
        for installed_program in self.installed_programs:
            installed_lower = installed_program.lower()
            
            if ('.net' in driver_name_lower or 'dotnet' in driver_name_lower) and '.net' in installed_lower:
                if not self._has_exclusions(installed_lower, driver_name_lower):
                    candidates.append({
                        "program": installed_program,
                        "score": self._calculate_relevance_score(driver_name_lower, installed_lower)
                    })
                    continue
            
            if any(word in installed_lower for word in driver_words if len(word) > 2):
                if not self._has_exclusions(installed_lower, driver_name_lower):
                    if self._is_relevant_match(driver_name_lower, installed_lower):
                        candidates.append({
                            "program": installed_program,
                            "score": self._calculate_relevance_score(driver_name_lower, installed_lower)
                        })
        
        if candidates:
            best_candidate = max(candidates, key=lambda x: x["score"])
            return {
                "installed": True,
                "exact_name": best_candidate["program"],
                "version": self.program_versions.get(best_candidate["program"], "Неизвестно")
            }
        
        return {"installed": False, "exact_name": None, "version": None}
    
    def _check_in_drivers(self, driver_name: str) -> Dict[str, any]:
        """Проверка драйвера среди системных драйверов"""
        driver_name_lower = driver_name.lower()
        driver_words = set(self._extract_key_words(driver_name_lower))
        
        for installed_driver in self.installed_drivers:
            installed_lower = installed_driver.lower()
            
            if any(word in installed_lower for word in driver_words if len(word) > 2):
                if not self._has_exclusions(installed_lower, driver_name_lower):
                    if self._is_relevant_match(driver_name_lower, installed_lower):
                        return {
                            "installed": True,
                            "exact_name": installed_driver,
                            "version": self.driver_versions.get(installed_driver, "Неизвестно")
                        }
        
        return {"installed": False, "exact_name": None, "version": None}
    
    def _is_relevant_match(self, driver_name: str, installed_name: str) -> bool:
        """Проверка релевантности совпадения"""
        driver_words = set(self._extract_key_words(driver_name))
        installed_words = set(self._extract_key_words(installed_name))
        
        common_words = driver_words.intersection(installed_words)
        
        if 'amd' in driver_name and 'adrenalin' in driver_name:
            return 'amd' in installed_name and ('settings' in installed_name or 'software' in installed_name)
        
        if 'visual' in driver_name and ('cpp' in driver_words or 'c++' in driver_name):
            return 'visual' in installed_name and ('c++' in installed_name or 'redistributable' in installed_name)
        
        if 'dotnet' in driver_words or 'framework' in driver_words or '.net' in driver_name:
            return '.net' in installed_name or 'dotnet' in installed_name
        
        if 'java' in driver_words:
            return 'java' in installed_name
        
        if len(driver_words) <= 2:
            return len(common_words) >= 1
        
        key_brands = {'java', 'nvidia', 'amd', 'intel', 'microsoft', 'directx', 'visual', 'net'}
        driver_brands = driver_words.intersection(key_brands)
        installed_brands = installed_words.intersection(key_brands)
        
        if driver_brands and installed_brands and driver_brands.intersection(installed_brands):
            return True
        
        return len(common_words) >= max(1, len(driver_words) * 0.4)
    
    def _extract_key_words(self, name: str) -> List[str]:
        """Извлечение ключевых слов из названия драйвера"""
        common_words = {'driver', 'drivers', 'suite', 'package', 'tool', 'tools', 
                       'utility', 'support', 'assistant', 'experience', 'control', 'panel',
                       'center', 'manager', 'application', 'program', 'system', 'windows'}
        
        name = name.replace('c++', 'cpp').replace('.net', 'dotnet')
        
        cleaned = re.sub(r'[^\w\s]', ' ', name)
        words = [word.strip() for word in cleaned.split() if len(word) > 1 and word not in common_words]
        
        return words
    
    def _has_exclusions(self, installed_name: str, driver_name: str) -> bool:
        """Проверка на исключения для избежания ложных срабатываний"""
        general_exclusions = ['basic', 'standard', 'generic', 'pnp']
        
        if not ('visual' in driver_name or '.net' in driver_name or 'dotnet' in driver_name):
            general_exclusions.extend(['microsoft', 'windows'])
        
        brand_exclusions = {
            'amd': ['processor', 'chipset', 'gpio', 'pci', 'smbus', 'balanced', 'dvr64', 'wvr64', 'crash defender'],
            'intel': ['management', 'mei', 'serial', 'thermal', 'platform'],
            'nvidia': ['audio', 'usb', 'serial']
        }
        
        if any(exclusion in installed_name for exclusion in general_exclusions):
            return True
        
        for brand, exclusions in brand_exclusions.items():
            if brand in driver_name and any(exclusion in installed_name for exclusion in exclusions):
                return True
        
        return False
    
    def _calculate_relevance_score(self, driver_name: str, installed_name: str) -> float:
        """Вычисление оценки релевантности для приоритизации результатов"""
        score = 0.0
        
        if driver_name in installed_name:
            score += 10.0
        
        driver_words = set(self._extract_key_words(driver_name))
        installed_words = set(self._extract_key_words(installed_name))
        common_words = driver_words.intersection(installed_words)
        score += len(common_words) * 2.0
        
        extra_words = len(installed_words) - len(common_words)
        score -= extra_words * 0.5
        
        penalty_words = ['auto', 'updater', 'update', 'launcher', 'installer', 'setup']
        for word in penalty_words:
            if word in installed_name:
                score -= 2.0
        
        bonus_words = ['runtime', 'framework', 'redistributable', 'sdk']
        for word in bonus_words:
            if word in installed_name:
                score += 1.0
        
        return score
    
    def _is_program_match(self, target_name: str, installed_name: str) -> bool:
        """Проверка соответствия названий программ"""
        target_clean = self._clean_program_name(target_name)
        installed_clean = self._clean_program_name(installed_name)
        
        if target_clean == "opera" and "gx" in installed_clean.lower():
            return False  
        if "opera gx" in target_clean.lower() and "gx" not in installed_clean.lower():
            return False  
        
        if target_clean == installed_clean:
            return True
        
        target_words = set(target_clean.split())
        installed_words = set(installed_clean.split())
        
        if len(target_words) <= 2:
            return target_words.issubset(installed_words)
        else:
            common_words = target_words.intersection(installed_words)
            return len(common_words) >= max(2, len(target_words) * 0.6)
    
    def _is_driver_match(self, target_name: str, installed_name: str) -> bool:
        """Проверка соответствия названий драйверов"""
        target_clean = self._clean_driver_name(target_name)
        installed_clean = self._clean_driver_name(installed_name)
        
        if target_clean.lower() in installed_clean.lower() or installed_clean.lower() in target_clean.lower():
            return True
        
        target_words = set(target_clean.lower().split())
        installed_words = set(installed_clean.lower().split())
        
        key_brands = {'nvidia', 'amd', 'intel', 'realtek', 'qualcomm', 'broadcom', 'via', 'asus', 'msi', 'gigabyte'}
        target_brands = target_words.intersection(key_brands)
        installed_brands = installed_words.intersection(key_brands)
        
        if target_brands and installed_brands and target_brands.intersection(installed_brands):
            return True
        
        common_words = target_words.intersection(installed_words)
        if len(common_words) >= 1 and any(len(word) > 3 for word in common_words):
            return True
        
        return False
    
    def _clean_program_name(self, name: str) -> str:
        """Очистка названия программы от лишних символов"""
        name = re.sub(r'\([^)]*\)', '', name)
        name = re.sub(r'\[[^\]]*\]', '', name)
        name = re.sub(r'\d+\.\d+[\.\d]*', '', name)
        name = re.sub(r'\b(x64|x86|32-bit|64-bit|32bit|64bit)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\b(version|ver|v)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[^\w\s]', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
    
    def _clean_driver_name(self, name: str) -> str:
        """Очистка названия драйвера от лишних символов"""
        name = re.sub(r'\([^)]*\)', '', name)
        name = re.sub(r'\[[^\]]*\]', '', name)
        name = re.sub(r'\b(driver|drivers|device|adapter|controller|software|suite|package)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\b(adrenalin|geforce|experience|control|panel|center|utility|tool|tools)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\d+\.\d+[\.\d]*', '', name)
        name = re.sub(r'\b(x64|x86|32-bit|64-bit|32bit|64bit|win10|win11|windows)\b', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[^\w\s]', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        return name.strip()
    
    def _check_directx_installed(self) -> bool:
        """Проверка установки DirectX через системные файлы"""
        try:
            import os
            system32_path = os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'System32')
            directx_files = ['d3d11.dll', 'd3d12.dll', 'dxgi.dll', 'xinput1_4.dll']
            
            for file in directx_files:
                if os.path.exists(os.path.join(system32_path, file)):
                    return True
            return False
        except:
            return False
    
    def get_scan_summary(self) -> Dict[str, int]:
        """Получить сводку по сканированию"""
        return {
            "programs_found": len(self.installed_programs),
            "drivers_found": len(self.installed_drivers)
        }


class InstallationStatusManager:
    """Менеджер статусов установки программ и драйверов"""
    
    def __init__(self):
        self.scanner = SystemScanner()
        self.scan_completed = False
        self.program_statuses = {}
        self.driver_statuses = {}
    
    def perform_system_scan(self) -> bool:
        """Выполнить полное сканирование системы"""
        try:
            print("Сканирование установленных программ...")
            self.scanner.scan_installed_programs()
            
            print("Сканирование установленных драйверов...")
            self.scanner.scan_installed_drivers()
            
            self.scan_completed = True
            print(f"Сканирование завершено: найдено {len(self.scanner.installed_programs)} программ и {len(self.scanner.installed_drivers)} драйверов")
            return True
            
        except Exception as e:
            print(f"Ошибка сканирования: {e}")
            return False
    
    def check_programs_status(self, programs_data: List[Dict]) -> Dict[str, Dict]:
        """Проверить статус установки для списка программ"""
        if not self.scan_completed:
            return {}
        
        statuses = {}
        for program in programs_data:
            program_name = program.get("name", "")
            if program_name:
                status = self.scanner.check_program_installed(program_name)
                statuses[program_name] = status
        
        self.program_statuses = statuses
        return statuses
    
    def check_drivers_status(self, drivers_data: List[Dict]) -> Dict[str, Dict]:
        """Проверить статус установки для списка драйверов"""
        if not self.scan_completed:
            return {}
        
        statuses = {}
        for driver in drivers_data:
            driver_name = driver.get("name", "")
            if driver_name:
                status = self.scanner.check_driver_installed(driver_name)
                statuses[driver_name] = status
        
        self.driver_statuses = statuses
        return statuses
    
    def get_program_status(self, program_name: str) -> Dict[str, any]:
        """Получить статус конкретной программы"""
        return self.program_statuses.get(program_name, {"installed": False, "exact_name": None, "version": None})
    
    def get_driver_status(self, driver_name: str) -> Dict[str, any]:
        """Получить статус конкретного драйвера"""
        return self.driver_statuses.get(driver_name, {"installed": False, "exact_name": None, "version": None})


class BackgroundScanner(QThread):
    """Фоновый сканер системы"""
    
    scan_completed = pyqtSignal(dict, dict, dict)  
    scan_progress = pyqtSignal(str)  
    
    def __init__(self, programs_data=None, drivers_data=None):
        super().__init__()
        self.programs_data = programs_data or []
        self.drivers_data = drivers_data or []
        self.status_manager = InstallationStatusManager()
    
    def run(self):
        """Выполнение сканирования в фоновом потоке"""
        try:
            self.scan_progress.emit("Сканирование программ...")
            success = self.status_manager.perform_system_scan()
            
            if success:
                programs_status = {}
                drivers_status = {}
                
                if self.programs_data:
                    self.scan_progress.emit("Проверка статуса программ...")
                    programs_status = self.status_manager.check_programs_status(self.programs_data)
                
                if self.drivers_data:
                    self.scan_progress.emit("Проверка статуса драйверов...")
                    drivers_status = self.status_manager.check_drivers_status(self.drivers_data)
                
                summary = self.status_manager.scanner.get_scan_summary()
                
                settings_manager.save_scan_cache(programs_status, drivers_status, summary)
                
                self.scan_completed.emit(programs_status, drivers_status, summary)
            else:
                self.scan_completed.emit({}, {}, {"programs_found": 0, "drivers_found": 0})
                
        except Exception as e:
            print(f"Ошибка фонового сканирования: {e}")
            self.scan_completed.emit({}, {}, {"programs_found": 0, "drivers_found": 0})


class CachedInstallationStatusManager(InstallationStatusManager):
    """Менеджер статусов с поддержкой кеширования"""
    def __init__(self):
        super().__init__()
        self.use_cache = True
    
    def get_program_status(self, program_name: str) -> Dict[str, any]:
        """Получить статус программы"""
        if self.use_cache and settings_manager.is_cache_valid():
            cached_status = settings_manager.get_cached_status(program_name, "programs")
            if cached_status.get("installed") is not False or cached_status.get("exact_name"):
                return cached_status
        
        return super().get_program_status(program_name)
    
    def get_driver_status(self, driver_name: str) -> Dict[str, any]:
        """Получить статус драйвера"""
        if self.use_cache and settings_manager.is_cache_valid():
            cached_status = settings_manager.get_cached_status(driver_name, "drivers")
            if cached_status.get("installed") is not False or cached_status.get("exact_name"):
                return cached_status
        
        return super().get_driver_status(driver_name)
    
    def force_refresh(self):
        """Принудительное обновление без кеша"""
        self.use_cache = False
        self.scan_completed = False
    
    def refresh_cache(self):
        """Обновить кеш - перезагрузить данные из settings_manager"""
        settings_manager.scan_cache = settings_manager.load_scan_cache()
        self.use_cache = True