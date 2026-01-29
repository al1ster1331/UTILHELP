import sys
import os

def resource_path(relative_path):
    """Получить абсолютный путь к ресурсу, работает для dev и для PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

def get_icon_path(icon_name):
    """Получить путь к системной иконке UTILHELP с fallback и диагностикой"""
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    
    search_paths = []
    
    if getattr(sys, 'frozen', False):
        search_paths.extend([
            os.path.join(exe_dir, 'assets', 'icons', icon_name),
            os.path.join(exe_dir, 'Icons', icon_name),  
        ])
    
    search_paths.extend([
        os.path.join(exe_dir, 'Icons', icon_name),
    ])
    
    try:
        search_paths.extend([
            resource_path(f"Icons/{icon_name}"),
            resource_path(f"assets/icons/{icon_name}"),
        ])
    except:
        pass
    
    for path in search_paths:
        # try:
        #     from temp_manager import debug_log
        #     debug_log(f"Checking system icon path: {path}")
        # except:
        #     pass
        
        if path and os.path.exists(path):
            # try:
            #     from temp_manager import debug_log
            #     debug_log(f"Found system icon at: {path}")
            # except:
            #     pass
            return path
    
    # try:
    #     from temp_manager import debug_log
    #     debug_log(f"System icon not found: {icon_name}. Checked paths: {search_paths}")
    # except:
    #     pass
    
    return None

def get_program_image_path(image_name):
    """Получить путь к картинке программы для скачивания с расширенной диагностикой"""
    # try:
    #     from temp_manager import debug_log
    #     debug_log(f"Looking for program image: {image_name}")
    # except:
    #     pass
    
    if image_name and ('/' in image_name or '\\' in image_name):
        image_name = os.path.basename(image_name)
        # try:
        #     from temp_manager import debug_log
        #     debug_log(f"Extracted filename from path: {image_name}")
        # except:
        #     pass
    
    if os.path.isabs(image_name) and os.path.exists(image_name):
        return image_name
    
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(os.path.abspath(sys.executable))
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    
    search_paths = []
    
    if getattr(sys, 'frozen', False):
        search_paths.extend([
            os.path.join(exe_dir, 'assets', 'programs', image_name),
            os.path.join(exe_dir, 'ProgramImages', image_name),    # Fallback на старую структуру
            os.path.join(exe_dir, 'assets', 'icons', image_name),  # Fallback на системные иконки
        ])
    
    search_paths.extend([
        os.path.join(exe_dir, 'ProgramImages', image_name),
        os.path.join(exe_dir, 'Icons', image_name),  # Fallback на системные иконки
    ])
    
    try:
        search_paths.extend([
            resource_path(f"ProgramImages/{image_name}"),
            resource_path(f"assets/programs/{image_name}"),
            resource_path(f"Icons/{image_name}"),
            resource_path(f"assets/icons/{image_name}"),
        ])
    except:
        pass
    
    for path in search_paths:
        # try:
        #     from temp_manager import debug_log
        #     debug_log(f"Checking program image path: {path}")
        # except:
        #     pass
        
        if path and os.path.exists(path):
            # try:
            #     from temp_manager import debug_log
            #     debug_log(f"Found program image at: {path}")
            # except:
            #     pass
            return path
    
    # try:
    #     from temp_manager import debug_log
    #     debug_log(f"Program image not found: {image_name}. Checked paths: {search_paths}")
    # except:
    #     pass
    
    return None

def get_db_path(db_name):
    """Получить путь к базе данных"""
    exe_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
    
    if getattr(sys, 'frozen', False):
        db_path = os.path.join(exe_dir, 'data', db_name)
        if os.path.exists(db_path):
            return db_path
        else:
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            return db_path
    
    dev_path = os.path.join(exe_dir, db_name)
    if os.path.exists(dev_path):
        return dev_path
    
    try:
        fallback_path = resource_path(db_name)
        if os.path.exists(fallback_path):
            return fallback_path
    except:
        pass
    
    return db_name  