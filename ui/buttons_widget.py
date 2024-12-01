from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.core.window import Window

from .portrait_buttons import PortraitButtonsLayout
from .landscape_buttons import LandscapeButtonsLayout

class ButtonsWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_orientation = None
        self.check_and_set_orientation()
        Window.bind(on_resize=self.on_window_resize)

    def on_window_resize(self, instance, width, height):
        if hasattr(self, '_resize_trigger'):
            Clock.unschedule(self._resize_trigger)
        self._resize_trigger = Clock.schedule_once(
            lambda dt: self.check_and_set_orientation(), 0.1)

    def check_and_set_orientation(self, *args):
        aspect_ratio = Window.width / Window.height
        LANDSCAPE_THRESHOLD = 1.1
        PORTRAIT_THRESHOLD = 0.9
        
        new_orientation = None
        if aspect_ratio > LANDSCAPE_THRESHOLD:
            new_orientation = 'landscape'
        elif aspect_ratio < PORTRAIT_THRESHOLD:
            new_orientation = 'portrait'
        else:
            return
        
        if new_orientation == self.current_orientation:
            return
            
        self.switch_orientation(new_orientation)

    def switch_orientation(self, new_orientation):
        # Создаем новый виджет в соответствии с ориентацией
        new_widget = (LandscapeButtonsLayout() if new_orientation == 'landscape' 
                     else PortraitButtonsLayout())
        
        # Если есть предыдущий виджет, удаляем его
        if hasattr(self, 'buttons_layout'):
            self.remove_widget(self.buttons_layout)
        
        # Добавляем новый виджет
        self.buttons_layout = new_widget
        self.add_widget(new_widget)
        
        self.current_orientation = new_orientation
