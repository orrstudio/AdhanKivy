from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from datetime import datetime
import locale

def create_date_widget_portrait(self):
    """
    Создает виджет даты для портретной ориентации
    
    Returns:
        Label: Виджет с отформатированной датой
    """
    # Устанавливаем локаль для корректного отображения даты
    locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')
    
    # Получаем текущую дату
    current_date = datetime.now()
    
    # Форматируем дату
    formatted_date = current_date.strftime('%d %B %Y').capitalize()
    
    # Расчет базового размера шрифта
    base_font_size = self.calculate_font_size(scale_factor=0.15)

    # Создаем Space 1 Label
    space1_label = Label(
        text=' ',
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.1,  # Размер шрифта пропорционально базовому
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.1,  # Высота пропорциональна базовому шрифту
        halign='center',  # Центрирование по горизонтали
        valign='middle',  # Центрирование по вертикали
        text_size=(Window.width * 0.9, None)  # Размер текста на всю ширину
    )


    # Создаем Label для даты
    date_label = Label(
        text=formatted_date,
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.25,  # Размер шрифта пропорционально базовому
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.1,  # Высота пропорциональна базовому шрифту
        halign='center',  # Центрирование по горизонтали
        valign='middle',  # Центрирование по вертикали
        text_size=(Window.width * 0.9, None)  # Размер текста на всю ширину
    )
    
    # Создаем Label для второй строки даты
    date_hijri_label = Label(
        text=current_date.strftime('%A').capitalize(),
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.2,  # Размер шрифта пропорционально базовому
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.1,  # Высота пропорциональна базовому шрифту
        halign='center',  # Центрирование по горизонтали
        valign='middle',  # Центрирование по вертикали
        text_size=(Window.width * 0.9, None)  # Размер текста на всю ширину
    )

    # Создаем GridLayout для дня недели и "Привет"
    day_hello_layout = GridLayout(
        cols=2,  # Два столбца
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.3,  # Высота как у большего виджета
        spacing=(10, 0)  # Небольшой отступ между элементами
    )

    # Создаем Label для дня недели
    day_label = Label(
        text='next time --',
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.2,  # Маленький размер
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        halign='right',  # Выравнивание вправо
    )

    # Создаем Label 
    hello_label = Label(
        text='00:00',
        font_name='PrayerTimeFont',  # Шрифт как у часиков
        font_size=base_font_size * 0.5,  # Большой размер шрифта
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        halign='left',  # Выравнивание влево
    )

    # Добавляем Label в GridLayout
    day_hello_layout.add_widget(day_label)
    day_hello_layout.add_widget(hello_label)

    # Создаем Line 1 Label
    line1_label = Label(
        text='---------------------------',
        font_name='PrayerNameFont',
        font_size=base_font_size * 0.1,  # Размер шрифта пропорционально базовому
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.1,  # Высота пропорциональна базовому шрифту
        halign='center',  # Центрирование по горизонтали
        valign='middle',  # Центрирование по вертикали
        text_size=(Window.width * 0.9, None)  # Размер текста на всю ширину
    )

    # Возвращаем виджеты
    return space1_label, date_label, date_hijri_label, line1_label, day_hello_layout
