# ui/portrait_clock.py

"""
Модуль отвечает за отображение часов в портретном режиме.
Содержит два основных класса:
- PortraitClockLayout: контейнер для размещения часов
- PortraitClockLabel: сами часы с настройками отображения

Часы автоматически загружают свой цвет из базы данных при создании
и могут обновлять его через метод apply_settings.
"""

from kivy.uix.floatlayout import FloatLayout
from ui.base_clock import BaseClockLabel
from logic.time_handler import TimeHandler
from data.database import SettingsDatabase
from ui.settings_window import SettingsWindow

class PortraitClockLayout(FloatLayout):
    """
    Контейнер для размещения часов в портретном режиме.
    Наследуется от FloatLayout для поддержки свободного позиционирования виджетов.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Создаем метку времени и добавляем её в контейнер
        self.clock_label = PortraitClockLabel()
        self.add_widget(self.clock_label)

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
