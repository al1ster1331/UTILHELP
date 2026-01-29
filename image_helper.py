from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from resource_path import get_program_image_path


def load_program_image(image_name):
    """Загрузить изображение программы/драйвера"""
    if not image_name:
        return None
    
    image_path = get_program_image_path(image_name)
    
    if not image_path:
        return None
    
    pixmap = QPixmap(image_path)
    
    if pixmap.isNull():
        return None
    
    return pixmap


def create_program_icon(image_name, size=(24, 24)):
    """Создать иконку для кнопки из изображения программы"""
    from PyQt6.QtGui import QIcon
    
    pixmap = load_program_image(image_name)
    
    if not pixmap or pixmap.isNull():
        return None
    
    scaled_pixmap = pixmap.scaled(
        size[0], size[1], 
        Qt.AspectRatioMode.KeepAspectRatio, 
        Qt.TransformationMode.SmoothTransformation
    )
    
    return QIcon(scaled_pixmap)