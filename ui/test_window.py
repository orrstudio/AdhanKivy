# Импорты из Kivy фреймворка
from kivy.uix.floatlayout import FloatLayout  # Для основного layout окна
from kivy.uix.button import Button  # Для кнопки "назад"
from kivy.uix.label import Label  # Для текстовых меток в таблице
from kivy.core.window import Window  # Для работы с окном приложения
from kivy.metrics import dp  # Для работы с независимыми от устройства пикселями
from kivy.app import App  # Для доступа к основному приложению
from kivy.uix.gridlayout import GridLayout  # Для создания табличной структуры

class TestWindow(FloatLayout):
    """
    Окно для отображения времен молитв в табличном формате.
    Использует GridLayout для создания двухколоночной таблицы,
    где первая колонка - время, вторая - название молитвы.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Создаем таблицу с двумя колонками
        # Таблица занимает всю ширину окна и имеет фиксированную высоту
        self.table = GridLayout(
            cols=2,  # Две колонки: время и название молитвы
            spacing=(0, 0),  # Без отступов между ячейками
            size_hint=(1, None),  # Ширина 100%, высота фиксированная
            height=200,  # Общая высота таблицы
            pos_hint={'top': 1},  # Прижимаем к верхнему краю окна
            padding=(0, 0)  # Без отступов от краев
        )
        
        # Тестовые данные времен молитв
        # Формат: (время, название молитвы)
        self.prayer_times = [
            ('05:30', 'Фаджр'),
            ('13:00', 'Зухр'),
            ('16:30', 'Аср'),
            ('19:00', 'Магриб'),
            ('20:30', 'Иша')
        ]
        
        # Создаем метки для всех времен молитв
        self.create_labels()
            
        # Добавляем таблицу в окно
        self.add_widget(self.table)
        
        # Создаем кнопку "назад" для возврата к основному окну
        self.back_button = Button(
            text='BACK',
            size_hint=(None, None),  # Фиксированный размер
            size=(120, 50),  # Размер кнопки в пикселях
            pos_hint={'center_x': 0.5, 'y': 0.05},  # Позиция внизу по центру
            background_color=(0.2, 0.2, 0.2, 1),  # Темно-серый фон
            color=(0.9, 0.9, 0.9, 1),  # Светло-серый текст
            font_size='16sp'  # Размер шрифта
        )
        # Привязываем обработчик нажатия
        self.back_button.bind(on_press=self.on_back_button_press)
        self.add_widget(self.back_button)
        
        # Привязываем обработчик изменения размера окна
        Window.bind(on_resize=self.on_window_resize)

    def calculate_font_size(self):
        """
        Рассчитывает размер шрифта на основе ширины окна.
        Размер шрифта = 10% от ширины окна, что обеспечивает
        адаптивность текста под разные размеры экрана.
        """
        return Window.width * 0.1  # 10% от ширины окна
    
    def create_labels(self):
        """
        Создает и размещает метки для всех времен молитв.
        Каждая строка состоит из двух меток: время и название молитвы.
        Метки автоматически подстраиваются под размер шрифта.
        """
        self.table.clear_widgets()  # Очищаем старые метки
        
        # Получаем размер шрифта на основе текущей ширины окна
        font_size = self.calculate_font_size()
        
        # Создаем метки для каждого времени молитвы
        for time, prayer in self.prayer_times:
            # Метка для времени (левая колонка)
            time_label = Label(
                text=time,
                font_size=font_size,  # Адаптивный размер шрифта
                size_hint=(0.5, None),  # 50% ширины, высота по контенту
                height=font_size * 1.5,  # Высота зависит от размера шрифта
                halign='left',  # Выравнивание текста влево
                valign='middle',  # Вертикально по центру
                text_size=(Window.width/2, font_size * 1.5)  # Область текста
            )
            # Метка для названия молитвы (правая колонка)
            prayer_label = Label(
                text=prayer,
                font_size=font_size,
                size_hint=(0.5, None),
                height=font_size * 1.5,
                halign='right',  # Выравнивание текста вправо
                valign='middle',
                text_size=(Window.width/2, font_size * 1.5)
            )
            # Добавляем метки в таблицу
            self.table.add_widget(time_label)
            self.table.add_widget(prayer_label)
    
    def on_window_resize(self, instance, width, height):
        """
        Обработчик изменения размера окна.
        Пересоздает все метки с новым размером шрифта,
        обеспечивая адаптивность интерфейса.
        """
        self.create_labels()
    
    def on_back_button_press(self, instance):
        """
        Обработчик нажатия кнопки "назад".
        Возвращает пользователя к основному окну приложения.
        """
        if hasattr(App.get_running_app(), 'toggle_test_window'):
            App.get_running_app().toggle_test_window()
