# main.py
import kivy
kivy.require('2.2.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.input.motionevent import MotionEvent

from ui.test_window import TestWindow
from ui.clock_widget import ClockWidget
from ui.buttons_widget import ButtonsWidget

class MainWindowApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_window = 'main'
        self.touch_start_x = None
        self.touch_start_y = None
        self.SWIPE_THRESHOLD = 200  # Минимальная длина свайпа в пикселях
        
    def build(self):
        # Черный фон
        Window.clearcolor = (0, 0, 0, 1)
        
        # Основной layout
        self.layout = FloatLayout()
        
        # Инициализируем buttons_widget как None перед определением коллбэка
        self.buttons_widget = None
        
        # Добавляем часы
        self.clock_widget = ClockWidget()
        
        # Определяем коллбэк ПЕРЕД добавлением виджета
        def on_clock_widget_created():
            # Получаем clock_label из текущего clock_widget
            clock_label = self.clock_widget.clock_widget
            
            print("on_clock_widget_created START")  # Отладочная печать
            print(f"clock_label: {clock_label}")  # Отладочная печать
            
            # Создаем buttons_widget если его еще нет, или обновляем clock_label если он уже есть
            print("Creating buttons_widget")  # Отладочная печать
            self.buttons_widget = ButtonsWidget(clock_label=clock_label)
            self.layout.add_widget(self.buttons_widget)
            
            print("on_clock_widget_created END")  # Отладочная печать
        
        # Устанавливаем коллбэк
        self.clock_widget.bind_on_clock_widget_created(on_clock_widget_created)
        
        # Добавляем часы в layout
        self.layout.add_widget(self.clock_widget)
        
        print("build method: before return")  # Отладочная печать
        
        # Создаем тестовое окно, но пока не показываем
        self.test_window = TestWindow()
        
        # Привязываем обработчики свайпа
        Window.bind(on_touch_down=self.on_window_touch_down)
        Window.bind(on_touch_up=self.on_window_touch_up)
        
        # Привязываем обработчик двойного клика к окну
        Window.bind(on_touch_down=self.on_window_touch_down_double_tap)
        
        return self.layout

    def switch_to_test(self):
        """Переключение на тестовое окно"""
        if self.current_window == 'main':
            self.layout.remove_widget(self.clock_widget)
            self.layout.remove_widget(self.buttons_widget)
            self.layout.add_widget(self.test_window)
            self.current_window = 'test'
        
    def switch_to_main(self):
        """Переключение на главное окно"""
        if self.current_window == 'test':
            self.layout.remove_widget(self.test_window)
            self.layout.add_widget(self.clock_widget)
            self.layout.add_widget(self.buttons_widget)
            self.current_window = 'main'

    def on_window_touch_down(self, window, touch):
        # Сохраняем начальную позицию свайпа
        self.touch_start_x = touch.x
        self.touch_start_y = touch.y
        return False

    def on_window_touch_up(self, window, touch):
        if self.touch_start_x is None or self.touch_start_y is None:
            return False

        # Вычисляем смещение свайпа
        dx = touch.x - self.touch_start_x
        dy = touch.y - self.touch_start_y

        # Сбрасываем начальную позицию
        self.touch_start_x = None
        self.touch_start_y = None

        # Проверяем горизонтальный свайп вправо
        if dx > self.SWIPE_THRESHOLD and abs(dy) < 100:
            print("Свайп вправо - переключение на тестовый экран")
            self.switch_to_test()
            return True

        return False

    def on_window_touch_down_double_tap(self, instance, touch):
        """
        Обработчик касания окна.
        Открывает окно настроек при двойном касании только в основном окне.
        """
        print(f"Touch event: {touch}, is_double_tap: {hasattr(touch, 'is_double_tap')}")  # Отладочная печать
        if isinstance(touch, MotionEvent) and hasattr(touch, 'is_double_tap') and touch.is_double_tap:
            print("Double tap detected!")  # Отладочная печать
            # Проверяем, что мы находимся в основном окне
            if self.current_window == 'main':
                print("Current window is main")  # Отладочная печать
                print(f"Buttons widget: {self.buttons_widget}")  # Отладочная печать
                print(f"Buttons widget type: {type(self.buttons_widget)}")  # Отладочная печать
                # Получаем текущий виджет кнопок
                if hasattr(self, 'buttons_widget') and hasattr(self.buttons_widget, 'buttons_layout'):
                    buttons_layout = self.buttons_widget.buttons_layout
                    print(f"Buttons layout: {buttons_layout}")  # Отладочная печать
                    print(f"Buttons layout type: {type(buttons_layout)}")  # Отладочная печать
                    if hasattr(buttons_layout, 'open_settings_window'):
                        buttons_layout.open_settings_window()
                return True
        return False

if __name__ == "__main__":
    MainWindowApp().run()
