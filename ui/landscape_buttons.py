from kivy.uix.floatlayout import FloatLayout
from ui.settings_window import SettingsWindow
from data.database import SettingsDatabase

class LandscapeButtonsLayout(FloatLayout):
    def __init__(self, clock_label=None, **kwargs):
        super().__init__(**kwargs)
        self.db = SettingsDatabase()
        self.clock_label = clock_label

    def open_settings_window(self, *args):
        """Показать окно настроек"""
        print("Landscape open_settings_window called!")  # Отладочная печать
        settings_window = SettingsWindow(self.db, self, self.apply_settings)
        settings_window.open()

    def apply_settings(self, color_tuple):
        """Применить настройки цвета к часам"""
        if hasattr(self.clock_label, 'color'):
            self.clock_label.color = color_tuple
