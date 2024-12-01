from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.app import App

class PortraitButtonsLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # В портретном режиме кнопки будут внизу одна над другой
        self.test_button = Button(
            text='TEST',
            size_hint=(0.9, 0.08),  # 90% ширины
            pos_hint={'center_x': 0.5, 'y': 0.11}  # Чуть выше от низа
        )
        self.test_button.bind(on_release=self.on_test_press)
        
        self.settings_button = Button(
            text='SETTINGS',
            size_hint=(0.9, 0.08),  # 90% ширины
            pos_hint={'center_x': 0.5, 'y': 0.01}  # У самого низа
        )
        self.settings_button.bind(on_release=self.on_settings_press)
        
        self.add_widget(self.test_button)
        self.add_widget(self.settings_button)

    def on_test_press(self, instance):
        app = App.get_running_app()
        if hasattr(app, 'toggle_test_window'):
            app.toggle_test_window()
            
    def on_settings_press(self, instance):
        pass  # Для будущей реализации
