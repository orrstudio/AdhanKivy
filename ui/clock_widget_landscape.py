# ui/landscape_clock.py

"""
Модуль отвечает за отображение часов в ландшафтном режиме.
Реализует виджет часов с автоматической загрузкой цвета из базы данных
и возможностью его обновления через настройки.
"""

from ui.clock_functions import BaseClockLabel
from logic.time_handler import TimeHandler
from data.database import SettingsDatabase
from ui.settings_window import SettingsWindow

class LandscapeClockLabel(BaseClockLabel):
    """
    Виджет часов для ландшафтной ориентации.
    Наследуется от BaseClockLabel и добавляет:
    - Загрузку цвета из базы данных
    - Управление видимостью двоеточия
    - Специфичное позиционирование для ландшафтного режима
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_colon_visible = True  # Флаг видимости двоеточия для мигания
        
        # Инициализация базы данных и загрузка сохраненного цвета
        self.db = SettingsDatabase()
        saved_color = self.db.get_setting('color')
        if saved_color:
            self.color = SettingsWindow.get_color_tuple(saved_color)
        
    def setup_style(self):
        """
        Настройка стиля для ландшафтной ориентации.
        Размещает часы по центру экрана как по вертикали, так и по горизонтали.
        """
        super().setup_style()
        self.valign = 'middle'  # Центрирование по вертикали
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Центрирование по обеим осям
        
    def toggle_colon_visibility(self):
        """
        Переключает видимость двоеточия для создания эффекта мигания.
        Вызывается периодически для обновления отображения времени.
        """
        self.is_colon_visible = not self.is_colon_visible
        self.text = TimeHandler.get_formatted_time(self.is_colon_visible)
        
    def apply_settings(self, color):
        """
        Применяет новые настройки цвета к часам.
        
        Args:
            color: Кортеж (r, g, b, a) с компонентами цвета
                  r, g, b - красный, зеленый, синий (0-1)
                  a - прозрачность (0-1)
        """
        self.color = color