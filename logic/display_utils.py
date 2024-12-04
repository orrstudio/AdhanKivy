import logging
import platform
from kivy.core.window import Window
from kivy.utils import platform as kivy_platform
import subprocess
import json

def get_monitor_info():
    """
    Возвращает базовую информацию о размере экрана
    """
    return [{
        'id': 0,
        'name': 'Screen',
        'width': Window.system_size[0],
        'height': Window.system_size[1],
        'x': Window.left,
        'y': Window.top,
        'is_primary': True
    }]

def find_current_monitor():
    """
    Возвращает текущий монитор (всегда один)
    """
    return get_monitor_info()[0]

def get_window_info():
    """
    Возвращает текущие координаты и размеры окна
    """
    return {
        'x': Window.left,
        'y': Window.top,
        'width': Window.width,
        'height': Window.height
    }

def is_mobile_device():
    """
    Определяет, является ли устройство мобильным.
    
    Returns:
        bool: True, если устройство считается мобильным
    """
    return kivy_platform in ['android', 'ios']

def log_display_info():
    """
    Логирует подробную информацию о текущем дисплее.
    """
    monitor = find_current_monitor()
    window_info = get_window_info()
    
    logging.info(f"Platform: {platform.platform()}")
    logging.info(f"Python Platform: {platform.system()}")
    logging.info(f"Kivy Platform: {kivy_platform}")
    logging.info(f"Window Size: {window_info['width']}x{window_info['height']}")
    logging.info(f"Is Mobile Device: {is_mobile_device()}")
    logging.info(f"Machine: {platform.machine()}")
    logging.info(f"Processor: {platform.processor()}")
    
    logging.info("Monitor:")
    logging.info(f"  Monitor {monitor['id']} ({monitor['name']}): "
                 f"{monitor['width']}x{monitor['height']} "
                 f"at ({monitor['x']}, {monitor['y']}) "
                 f"{'(Primary)' if monitor['is_primary'] else ''}")
    
    logging.info(f"Window Position: ({window_info['x']}, {window_info['y']})")
    logging.info(f"Window Size: {window_info['width']}x{window_info['height']}")
