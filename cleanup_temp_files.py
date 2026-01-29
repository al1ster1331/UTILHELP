"""
Скрипт для ручной очистки временных файлов UTILHELP
"""

import os
import tempfile
import shutil
from temp_manager import get_temp_manager

def cleanup_temp_files():
    print("=== ОЧИСТКА ВРЕМЕННЫХ ФАЙЛОВ UTILHELP ===")
    system_temp = tempfile.gettempdir()
    print(f"Системная temp: {system_temp}")
    print()

    temp_manager = get_temp_manager()
    
    print("1. Текущие временные файлы:")
    
    utilhelp_folders = []
    for folder_name in ["UTILHELPTEMP", "UTILHELP", "UH"]:
        folder_path = os.path.join(system_temp, folder_name)
        if os.path.exists(folder_path):
            try:
                files = os.listdir(folder_path)
                utilhelp_folders.append((folder_name, len(files)))
                print(f"   Папка {folder_name}: {len(files)} файлов")
            except:
                print(f"   Папка {folder_name}: ошибка чтения")
    
    temp_files = []
    try:
        for file in os.listdir(system_temp):
            if (file.startswith("utilhelp") or 
                file.endswith("_temp.png") or
                "temp.png" in file):
                temp_files.append(file)
        
        if temp_files:
            print(f"   Отдельные файлы в Temp: {len(temp_files)}")
            for file in temp_files[:5]:  # Показываем первые 5
                print(f"     - {file}")
            if len(temp_files) > 5:
                print(f"     ... и еще {len(temp_files) - 5} файлов")
    except Exception as e:
        print(f"   Ошибка чтения системной temp: {e}")
    
    if not utilhelp_folders and not temp_files:
        print("   Временные файлы UTILHELP не найдены")
        print()
        print("=== ОЧИСТКА НЕ ТРЕБУЕТСЯ ===")
        return
    
    print()

    print("2. Выполнение очистки:")
    
    cleaned_count = 0

    for folder_name in ["UTILHELPTEMP", "UTILHELP", "UH"]:
        folder_path = os.path.join(system_temp, folder_name)
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path, ignore_errors=True)
                print(f"   ✓ Удалена папка: {folder_name}")
                cleaned_count += 1
            except Exception as e:
                print(f"   ✗ Ошибка удаления папки {folder_name}: {e}")

    removed_files = 0
    try:
        for file in os.listdir(system_temp):
            file_path = os.path.join(system_temp, file)
            
            if (file.startswith("utilhelp") or 
                file.endswith("_temp.png") or
                "temp.png" in file):
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        removed_files += 1
                except:
                    pass
        
        if removed_files > 0:
            print(f"   ✓ Удалено файлов: {removed_files}")
            cleaned_count += removed_files
    except Exception as e:
        print(f"   ✗ Ошибка очистки файлов: {e}")
    
    print()
    
    print("3. Проверка результата:")
    remaining_items = 0
    
    for folder_name in ["UTILHELPTEMP", "UTILHELP", "UH"]:
        folder_path = os.path.join(system_temp, folder_name)
        if os.path.exists(folder_path):
            remaining_items += 1
            print(f"   ⚠️  Папка {folder_name} все еще существует")
    
    try:
        remaining_files = []
        for file in os.listdir(system_temp):
            if (file.startswith("utilhelp") or 
                file.endswith("_temp.png") or
                "temp.png" in file):
                remaining_files.append(file)
        
        if remaining_files:
            remaining_items += len(remaining_files)
            print(f"   ⚠️  Осталось файлов: {len(remaining_files)}")
    except:
        pass
    
    if remaining_items == 0:
        print("   ✓ Все временные файлы UTILHELP удалены")
    
    print()
    print(f"=== ОЧИСТКА ЗАВЕРШЕНА (обработано элементов: {cleaned_count}) ===")

if __name__ == "__main__":
    cleanup_temp_files()