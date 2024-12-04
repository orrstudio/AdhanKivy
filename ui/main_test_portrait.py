from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from datetime import datetime
import locale

def create_line_label(base_font_size):
    return Label(
        text='―' * 150,  # Много тире
        font_name='PrayerNameFont',
        height=base_font_size * 0.1, # Высота пропорциональна базовому шрифту
        size_hint_x=1, # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        color=(1, 1, 1, 1),  # Белый цвет
        halign='center',  # Центрирование по горизонтали
        valign='middle',  # Центрирование по вертикали
        #font_size=base_font_size * 0.1,  # Размер шрифта пропорционально базовому
    )

def create_space_label(base_font_size):
    return Label(text=' ', height=base_font_size * 0.2)

def create_portrait_widgets(self):
    """
    Создает виджет даты для портретной ориентации
    
    Returns:
        Label: Виджет с отформатированной датой
    """
    # Устанавливаем локаль для корректного отображения даты
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    
    # Расчет базового размера шрифта
    base_font_size = self.calculate_font_size(scale_factor=0.15)

    # Получаем текущую дату
    current_date = datetime.now()
    
    # Форматируем даты
    formatted_date_xijri = current_date.strftime('%d %B %Y').capitalize()
    formatted_date_gregorian = current_date.strftime('%d %B %Y').capitalize()

    # Создаем Label для даты Хиджри
    date_hijri_label = Label(
        text=formatted_date_xijri,
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.25,  # Размер шрифта пропорционально базовому
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.3,  # Высота пропорциональна базовому шрифту
        halign='center',  # Центрирование по горизонтали
        valign='middle',  # Центрирование по вертикали
    )

    # Создаем Label для даты Григорианской
    date_gregorian_label = Label(
        text=formatted_date_gregorian,
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.25,  # Размер шрифта пропорционально базовому
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.3,  # Высота пропорциональна базовому шрифту
        halign='center',  # Центрирование по горизонтали
        valign='middle',  # Центрирование по вертикали
    )
    
    # Создаем GridLayout для NextTimeName и NextTimeNumbers
    nex_time_layout = GridLayout(
        cols=2,  # Два столбца
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.6,  # Высота пропорциональна базовому шрифту
        spacing=(10, 0)  # Небольшой отступ между элементами
    )

    # Создаем Label для NextTimeName
    next_time_name_label = Label(
        text='NextTime -',
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.3,  # Маленький размер
        color=(1, 1, 1, 1),  # Белый цвет
        halign='left',  # Выравнивание вправо
    )

    # Создаем Label для NextTimeNumbers
    next_time_numbers_label = Label(
        text='00:00',
        font_name='PrayerTimeFont',  # Шрифт как у часиков
        font_size=base_font_size * 0.5,  # Большой размер шрифта
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        height=base_font_size * 0.6,  # Высота пропорциональна базовому шрифту
        halign='right',  # Выравнивание влево
    )

    # Добавляем Label в GridLayout
    nex_time_layout.add_widget(next_time_name_label)
    nex_time_layout.add_widget(next_time_numbers_label)

    # Возвращаем виджеты
    return (
        #create_space_label(base_font_size), 
        create_line_label(base_font_size), 
        date_hijri_label, 
        date_gregorian_label, 
        create_line_label(base_font_size), 
        nex_time_layout, 
        create_line_label(base_font_size), 
        create_space_label(base_font_size)
    )
