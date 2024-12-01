# main.py
import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout

from ui.test_window import TestWindow
from ui.clock_widget import ClockWidget
from ui.buttons_widget import ButtonsWidget
from ui.portrait_clock import PortraitClockLayout

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
        
        # Добавляем кнопки
        self.buttons_widget = None  # Инициализируем как None
        
        def on_clock_widget_created():
            # Получаем clock_label из текущего clock_widget
            clock_label = (self.clock_widget.clock_widget.clock_label 
                         if isinstance(self.clock_widget.clock_widget, PortraitClockLayout)
                         else self.clock_widget.clock_widget)
            
            # Создаем buttons_widget если его еще нет, или обновляем clock_label если он уже есть
            if self.buttons_widget is None:
                self.buttons_widget = ButtonsWidget(clock_label=clock_label)
                self.layout.add_widget(self.buttons_widget)
            else:
                self.buttons_widget.clock_label = clock_label
        
        self.clock_widget.bind_on_clock_widget_created(on_clock_widget_created)
        
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
            self.layout.add_widget(self.buttons_widget)
            self.current_window = 'main'

if __name__ == "__main__":
    MainWindowApp().run()
