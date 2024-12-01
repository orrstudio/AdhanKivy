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
        
        # В портретном режиме кнопки будут внизу одна над другой
        self.test_button = Button(
            text='TEST',
            size_hint=(None, None),
            size=(120, 50),
            background_color=(0.6, 0.6, 0.6, 1),
            pos_hint={'center_x': 0.5, 'y': 0.05 + 50/Window.height},
            color=(0.9, 0.9, 0.9, 1),
            font_size='16sp'
        )
        self.test_button.bind(on_release=self.on_test_press)
        
        self.settings_button = Button(
            text='SETTINGS',
            size_hint=(None, None),
            size=(120, 50),
            background_color=(0.6, 0.6, 0.6, 1),
            pos_hint={'center_x': 0.5, 'y': 0.05},
            color=(0.9, 0.9, 0.9, 1),
            font_size='16sp'
        )
        self.settings_button.bind(on_release=self.on_settings_press)
        
        self.add_widget(self.test_button)
        self.add_widget(self.settings_button)
        
        # Применяем сохраненные настройки
        saved_color = self.db.get_setting('color')
        if saved_color and hasattr(self.clock_label, 'color'):
            self.clock_label.color = SettingsWindow.get_color_tuple(saved_color)

    def on_test_press(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'switch_to_test'):
            app.switch_to_test()
            
    def on_settings_press(self, instance):
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
