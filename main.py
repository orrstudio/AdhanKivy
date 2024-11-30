# main.py
import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from ui.test_window import TestWindow
from ui.clock_widget import ClockWidget

class MainWindowApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_window = 'main'
        
    def build(self):
        # Черный фон
        Window.clearcolor = (0, 0, 0, 1)
        
        # Основной layout
        self.layout = FloatLayout()
        
        # Добавляем часы
        self.clock_widget = ClockWidget()
        self.layout.add_widget(self.clock_widget)
        
        # Создаем тестовое окно, но пока не показываем
        self.test_window = TestWindow()
        
        return self.layout

    def toggle_test_window(self):
        self.layout.clear_widgets()
        if self.current_window == 'main':
            self.layout.add_widget(self.test_window)
            self.current_window = 'test'
        else:
            self.layout.add_widget(self.clock_widget)
            self.current_window = 'main'

if __name__ == "__main__":
    MainWindowApp().run()
