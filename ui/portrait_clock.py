# ui/portrait_clock.py

"""
Модуль отвечает за отображение часов в портретном режиме.
Реализует виджет часов с автоматической загрузкой цвета из базы данных
и возможностью его обновления через настройки.
"""

from ui.base_clock import BaseClockLabel
from logic.time_handler import TimeHandler
from data.database import SettingsDatabase
from ui.settings_window import SettingsWindow

class PortraitClockLabel(BaseClockLabel):
    """
    Виджет часов для портретной ориентации.
    Наследуется от BaseClockLabel и добавляет:
    - Загрузку цвета из базы данных
    - Управление видимостью двоеточия
    - Специфичное позиционирование для портретного режима
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
        Настройка стиля для портретной ориентации.
        Размещает часы вверху экрана по центру.
        """
        super().setup_style()
        self.valign = 'top'  # Выравнивание по верхнему краю
        self.pos_hint = {'center_x': 0.5, 'top': 1}  # Центрирование по горизонтали и прижатие к верху

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
