from PyQt6.QtWidgets import QApplication
import ctypes

def get_windows_scroll_mode():
    try:
        lines = ctypes.c_uint()
        ctypes.windll.user32.SystemParametersInfoW(0x0068, 0, ctypes.byref(lines), 0)
        
        if lines.value == 0xFFFFFFFF or lines.value >= 0xFFFFFFFF:
            return (3, True) 
        else:
            return (lines.value, False)  
    except:
        qt_lines = QApplication.wheelScrollLines()
        return (qt_lines, False)

def configure_scroll_area(scroll_area):
    lines, is_page_scroll = get_windows_scroll_mode()
    
    scroll_area._scroll_lines = lines
    scroll_area._is_page_scroll = is_page_scroll
    
    original_wheelEvent = scroll_area.wheelEvent
    
    def custom_wheelEvent(event):
        scrollbar = scroll_area.verticalScrollBar()
        if not scrollbar:
            original_wheelEvent(event)
            return
        
        delta = event.angleDelta().y()
        
        if scroll_area._is_page_scroll:
            page_step = scrollbar.pageStep()
            
            if delta > 0:
                scrollbar.setValue(scrollbar.value() - page_step)
            else:
                scrollbar.setValue(scrollbar.value() + page_step)
            
            event.accept()
        else:
            step = scroll_area._scroll_lines * 20  
            
            if delta > 0:
                scrollbar.setValue(scrollbar.value() - step)
            else:
                scrollbar.setValue(scrollbar.value() + step)
            
            event.accept()
    
    scroll_area.wheelEvent = custom_wheelEvent
