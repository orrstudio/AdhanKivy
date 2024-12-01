from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.core.window import Window
from ui.settings_window import SettingsWindow
from data.database import SettingsDatabase

class PortraitButtonsLayout(FloatLayout):
    def __init__(self, clock_label, **kwargs):
        super().__init__(**kwargs)
        self.db = SettingsDatabase()
        self.clock_label = clock_label
        
        # Применяем сохраненные настройки
        saved_color = self.db.get_setting('color')
        if saved_color and hasattr(self.clock_label, 'color'):
            self.clock_label.color = SettingsWindow.get_color_tuple(saved_color)

    def open_settings_window(self, *args):
        """Показать окно настроек"""
        settings_window = SettingsWindow(self.db, self, self.apply_settings)
        settings_window.open()
            
    def apply_settings(self, color_tuple):
        """Применить настройки цвета к часам
        
        Args:
            color_tuple: Кортеж (r, g, b, a) с значениями цвета
        """
        if hasattr(self.clock_label, 'color'):
            self.clock_label.color = color_tuple
