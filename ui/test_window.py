from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.app import App

class TestWindow(FloatLayout):
    """
    Тестовое окно для разработки и тестирования новых функций.
    После успешного тестирования функции могут быть перенесены в основное приложение.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Заголовок окна
        self.title_label = Label(
            text='Тестовое окно',
            size_hint=(1, 0.1),
            pos_hint={'top': 1},
            font_size=dp(24)
        )
        self.add_widget(self.title_label)
        
        # Кнопка возврата к основному окну
        self.back_button = Button(
            text='Вернуться к часам',
            size_hint=(0.3, 0.1),
            pos_hint={'x': 0.05, 'top': 0.95}
        )
        self.back_button.bind(on_press=self.on_back_button_press)
        self.add_widget(self.back_button)
        
        # Тестовая кнопка
        self.test_button = Button(
            text='Тестовая кнопка',
            size_hint=(0.3, 0.1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.test_button.bind(on_press=self.on_test_button_press)
        self.add_widget(self.test_button)
        
        # Метка для отображения результатов тестов
        self.result_label = Label(
            text='',
            size_hint=(0.8, 0.3),
            pos_hint={'center_x': 0.5, 'y': 0.1}
        )
        self.add_widget(self.result_label)
    
    def on_test_button_press(self, instance):
        """Обработчик нажатия тестовой кнопки"""
        print("Тестовая кнопка нажата!")
        self.result_label.text = "Тестовая кнопка была нажата!"
    
    def on_back_button_press(self, instance):
        """Обработчик кнопки возврата к основному окну"""
        if hasattr(App.get_running_app(), 'toggle_test_window'):
            App.get_running_app().toggle_test_window()
