# Импорты из Kivy фреймворка
from kivy.uix.floatlayout import FloatLayout  # Для основного layout окна
from kivy.uix.button import Button  # Для кнопки "назад"
from kivy.uix.label import Label  # Для текстовых меток в таблице
from kivy.core.window import Window  # Для работы с окном приложения
from kivy.metrics import dp  # Для работы с независимыми от устройства пикселями
from kivy.app import App  # Для доступа к основному приложению
from kivy.uix.gridlayout import GridLayout  # Для создания табличной структуры
from kivy.core.text import LabelBase  # Для регистрации шрифтов

# Регистрируем пользовательские шрифты
LabelBase.register(name='PrayerNameFont', 
                  fn_regular='fonts/SourceCodePro/SourceCodePro-ExtraLight.ttf')
LabelBase.register(name='PrayerTimeFont', 
                  fn_regular='fonts/DSEG14Classic-Regular.ttf')

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
        # Формат: (название молитвы, время)
        self.prayer_times = [
            ('Təhəccüd -', '05:30'),
            ('İmsak ----', '05:30'),
            ('Günəş ----', '05:30'),
            ('Günorta --', '13:00'),
            ('İkindi ---', '15:00'), 
            ('Axşam ----', '16:30'),
            ('Gecə -----', '20:30')
        ]
        
        # Создаем метки для всех времен молитв
        self.create_labels()
            
        # Добавляем таблицу в окно
        self.add_widget(self.table)
        
        # Создаем кнопку "BACK" для возврата к основному окну
        self.back_button = Button(
            text='BACK',
            size_hint=(None, None),  # Фиксированный размер
            size=(120, 50),  # Размер кнопки в пикселях
            pos_hint={'center_x': 0.5, 'y': 0.05},  # Позиция внизу по центру
            background_color=(0.6, 0.6, 0.6, 1),  # Серый фон
            color=(0.9, 0.9, 0.9, 1),  # Светло-серый текст
            font_size='16sp'  # Размер шрифта
        )
        # Привязываем обработчик нажатия
        self.back_button.bind(on_release=self.on_back_button_press)
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
        time_font_size = self.calculate_font_size()  # Размер для времени
        prayer_font_size = time_font_size * 1  # Размер для названий (70% от размера времени)
        
        # Создаем метки для каждого времени молитвы
        for prayer, time in self.prayer_times:
            # Метка для названия молитвы (левая колонка)
            prayer_label = Label(
                text=prayer,
                font_size=prayer_font_size,  # Используем меньший размер для названий
                font_name='PrayerNameFont',  # Используем шрифт PrayerNameFont
                size_hint=(0.65, None),
                height=time_font_size * 1.5,  # Высота остается как у времени для выравнивания
                halign='left',  # Выравнивание текста влево
                valign='middle',
                text_size=(Window.width*0.65, time_font_size * 2.5)
            )
            # Метка для времени (правая колонка)
            time_label = Label(
                text=time,
                font_size=time_font_size,  # Больший размер для времени
                font_name='PrayerTimeFont',  # Используем шрифт PrayerTimeFont
                size_hint=(0.35, None),
                height=time_font_size * 1.5,  # Высота зависит от размера шрифта
                halign='right',  # Выравнивание текста вправо
                valign='middle',  # Вертикально по центру
                text_size=(Window.width*0.35, time_font_size * 1.5)  # Область текста
            )
            # Добавляем метки в таблицу
            self.table.add_widget(prayer_label)
            self.table.add_widget(time_label)
    
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
