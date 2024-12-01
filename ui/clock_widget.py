from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.core.window import Window

from .portrait_clock import PortraitClockLabel
from .landscape_clock import LandscapeClockLabel

class ClockWidget(FloatLayout):
    colors = {
        'lime': (0, 1, 0, 1),
        'aqua': (0, 1, 1, 1),
        'blue': (0, 0, 1, 1),
        'red': (1, 0, 0, 1),
        'yellow': (1, 1, 0, 1),
        'magenta': (1, 0, 1, 1),
        'pink': (1, 0.75, 0.8, 1),
        'grey': (0.7, 0.7, 0.7, 1),
        'white': (1, 1, 1, 1)
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_orientation = None
        self._on_clock_widget_created = None
        
        print("ClockWidget __init__ START")  
        print(f"Initial window size: {Window.width}x{Window.height}")  
        
        self.check_and_set_orientation()
        
        Window.bind(on_resize=self.on_window_resize)
        Clock.schedule_interval(self.update_time, 0.5)
        
        print("ClockWidget __init__ END")  

    def bind_on_clock_widget_created(self, callback):
        print("bind_on_clock_widget_created called!")  # Отладочная печать
        print(f"Callback: {callback}")  # Отладочная печать
        
        # Устанавливаем коллбэк
        self._on_clock_widget_created = callback
        
        # Если виджет уже создан, вызываем коллбэк немедленно
        if hasattr(self, 'clock_widget') and self.clock_widget is not None:
            print("Immediately calling _on_clock_widget_created")  # Отладочная печать
            Clock.schedule_once(lambda dt: self._on_clock_widget_created(self.clock_widget), 0)

    def on_window_resize(self, instance, width, height):
        if hasattr(self, '_resize_trigger'):
            Clock.unschedule(self._resize_trigger)
        self._resize_trigger = Clock.schedule_once(
            lambda dt: self.check_and_set_orientation(), 0.1)

    def check_and_set_orientation(self, *args):
        aspect_ratio = Window.width / Window.height
        LANDSCAPE_THRESHOLD = 1.1
        PORTRAIT_THRESHOLD = 0.9
        
        print(f"check_and_set_orientation START")  
        print(f"Window size: {Window.width}x{Window.height}, aspect ratio: {aspect_ratio}")  
        
        new_orientation = None
        if aspect_ratio > LANDSCAPE_THRESHOLD:
            new_orientation = 'landscape'
        elif aspect_ratio < PORTRAIT_THRESHOLD:
            new_orientation = 'portrait'
        else:
            print("Orientation not determined")  
            return
        
        print(f"Detected orientation: {new_orientation}")  
        
        if new_orientation == self.current_orientation:
            print("Orientation unchanged")  
            return
            
        self.switch_orientation(new_orientation)
        
        print(f"check_and_set_orientation END")  

    def switch_orientation(self, new_orientation):
        new_widget = (LandscapeClockLabel() if new_orientation == 'landscape' 
                     else PortraitClockLabel())
        new_widget.opacity = 0
        
        self.add_widget(new_widget)
        
        if hasattr(self, 'clock_widget'):
            new_widget.color = self.clock_widget.color
                
            anim_old = Animation(opacity=0, duration=0.15)
            
            def on_complete(*args):
                self.remove_widget(self.clock_widget)
                self.clock_widget = new_widget
                print("Before _on_clock_widget_created call")  
                print(f"_on_clock_widget_created: {self._on_clock_widget_created}")  
                if self._on_clock_widget_created:
                    print("Calling _on_clock_widget_created")  
                    self._on_clock_widget_created(self.clock_widget)
            
            anim_old.bind(on_complete=on_complete)
            anim_old.start(self.clock_widget)
        else:
            self.clock_widget = new_widget
            print("Before _on_clock_widget_created call (else)")  
            print(f"_on_clock_widget_created: {self._on_clock_widget_created}")  
            if self._on_clock_widget_created:
                print("Calling _on_clock_widget_created (else)")  
                self._on_clock_widget_created(self.clock_widget)
        
        anim_new = Animation(opacity=1, duration=0.15)
        anim_new.start(new_widget)
        
        self.current_orientation = new_orientation

    def update_time(self, dt):
        if hasattr(self, 'clock_widget'):
            self.clock_widget.toggle_colon_visibility()

    def update_color(self, color_name):
        if hasattr(self, 'clock_widget'):
            color_key = color_name.lower()
            color_tuple = self.colors.get(color_key, (1, 1, 1, 1))
            
            self.clock_widget.color = color_tuple
