from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window

from .portrait_buttons import PortraitButtonsLayout
from .landscape_buttons import LandscapeButtonsLayout

class ButtonsWidget(FloatLayout):
    def __init__(self, clock_label, **kwargs):
        super().__init__(**kwargs)
        self.clock_label = clock_label
        self.current_orientation = None
        
        print("ButtonsWidget __init__ START")  # Отладочная печать
        print(f"Initial window size: {Window.width}x{Window.height}")  # Отладочная печать
        
        # Принудительная установка ориентации при инициализации
        self.check_and_set_orientation()
        
        Window.bind(on_resize=self.on_window_resize)

        print("ButtonsWidget __init__ END")  # Отладочная печать

    @property
    def clock_label(self):
        return self._clock_label

    @clock_label.setter
    def clock_label(self, value):
        self._clock_label = value
        if hasattr(self, 'buttons_layout'):
            self.buttons_layout.clock_label = value

    def on_window_resize(self, instance, width, height):
        if hasattr(self, '_resize_trigger'):
            Clock.unschedule(self._resize_trigger)
        self._resize_trigger = Clock.schedule_once(
            lambda dt: self.check_and_set_orientation(), 0.1)

    def check_and_set_orientation(self, *args):
        aspect_ratio = Window.width / Window.height
        LANDSCAPE_THRESHOLD = 1.1
        PORTRAIT_THRESHOLD = 0.9
        
        print(f"ButtonsWidget check_and_set_orientation START")  # Отладочная печать
        print(f"Window size: {Window.width}x{Window.height}, aspect ratio: {aspect_ratio}")  # Отладочная печать
        
        new_orientation = None
        if aspect_ratio > LANDSCAPE_THRESHOLD:
            new_orientation = 'landscape'
        elif aspect_ratio < PORTRAIT_THRESHOLD:
            new_orientation = 'portrait'
        else:
            print("Orientation not determined")  # Отладочная печать
            return
        
        print(f"Detected orientation: {new_orientation}")  # Отладочная печать
        
        if new_orientation == self.current_orientation:
            print("Orientation unchanged")  # Отладочная печать
            return
            
        self.switch_orientation(new_orientation)
        
        print(f"ButtonsWidget check_and_set_orientation END")  # Отладочная печать

    def switch_orientation(self, new_orientation):
        # Создаем новый виджет в соответствии с ориентацией
        print(f"Switching to orientation: {new_orientation}")  # Отладочная печать
        new_widget = (LandscapeButtonsLayout(clock_label=self.clock_label) if new_orientation == 'landscape' 
                     else PortraitButtonsLayout(clock_label=self.clock_label))
        
        # Если есть предыдущий виджет, удаляем его
        if hasattr(self, 'buttons_layout'):
            self.remove_widget(self.buttons_layout)
        
        # Добавляем новый виджет
        self.buttons_layout = new_widget
        self.add_widget(new_widget)
        
        self.current_orientation = new_orientation
        print(f"Current buttons_layout: {type(self.buttons_layout).__name__}")  # Отладочная печать
