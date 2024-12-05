from datetime import datetime
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

# Словари для конвертации в римские цифры
WEEKDAY_TO_ROMAN = {
    0: 'I',     # Понедельник
    1: 'II',    # Вторник
    2: 'III',   # Среда
    3: 'IV',    # Четверг
    4: 'V',     # Пятница
    5: 'VI',    # Суббота
    6: 'VII'    # Воскресенье
}

MONTH_TO_ROMAN = {
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
    6: 'VI',
    7: 'VII',
    8: 'VIII',
    9: 'IX',
    10: 'X',
    11: 'XI',
    12: 'XII'
}

def get_formatted_dates():
    """
    Возвращает отформатированные даты
    Returns:
        dict: Словарь с частями даты и их шрифтами
    """
    current_date = datetime.now()
    
    # Григорианская дата в формате IV - 05.XII.2024
    weekday = current_date.weekday()
    month = current_date.month
    
    # Части даты с указанием шрифтов
    date_parts = {
        'weekday': {
            'text': f"{WEEKDAY_TO_ROMAN[weekday]} -",
            'font': 'FontSourceCodePro-Light',
            'font_size': 40
        },
        'day': {
            'text': current_date.strftime('%d'),
            'font': 'FontDSEG7-Light',
        },
        'month': {
            'text': f".{MONTH_TO_ROMAN[month]}.",
            'font': 'FontSourceCodePro-Light'
        },
        'year': {
            'text': current_date.strftime('%Y'),
            'font': 'FontDSEG7-Light'
        },
        'full_gregorian': f"{WEEKDAY_TO_ROMAN[weekday]} - {current_date.strftime('%d')}.{MONTH_TO_ROMAN[month]}.{current_date.strftime('%Y')}"
    }
    
    # Дата хиджры (пока в старом формате)
    date_parts['hijri'] = current_date.strftime('%d %B %Y').capitalize()
    
    return date_parts

def create_gregorian_date_label(base_font_size):
    """
    Создает Label для григорианской даты с разными шрифтами и размерами
    
    Args:
        base_font_size (float): Базовый размер шрифта
    
    Returns:
        GridLayout: Layout с Label для частей даты
    """
    formatted_dates = get_formatted_dates()
    
    # Извлекаем размеры шрифтов для каждой части, с значениями по умолчанию
    weekday_font_size = formatted_dates["weekday"].get('font_size', base_font_size * 0.2)
    day_font_size = formatted_dates["day"].get('font_size', base_font_size * 0.2)
    month_font_size = formatted_dates["month"].get('font_size', base_font_size * 0.2)
    year_font_size = formatted_dates["year"].get('font_size', base_font_size * 0.2)
    
    print(f"Debug: font_sizes - Weekday: {weekday_font_size}, Day: {day_font_size}, Month: {month_font_size}, Year: {year_font_size}")
    
    # Создаем Label для каждой части даты
    weekday_label = Label(
        text=formatted_dates["weekday"]["text"],
        font_name=formatted_dates["weekday"]["font"],
        font_size=weekday_font_size,
        color=(1, 1, 1, 1),
        size_hint_x=1,
        size_hint_y=None,
        height=weekday_font_size * 1.2,
        halign='center',
        valign='middle'
    )
    
    day_label = Label(
        text=formatted_dates["day"]["text"],
        font_name=formatted_dates["day"]["font"],
        font_size=day_font_size,
        color=(1, 1, 1, 1),
        size_hint_x=1,
        size_hint_y=None,
        height=day_font_size * 1.2,
        halign='center',
        valign='middle'
    )
    
    month_label = Label(
        text=formatted_dates["month"]["text"],
        font_name=formatted_dates["month"]["font"],
        font_size=month_font_size,
        color=(1, 1, 1, 1),
        size_hint_x=1,
        size_hint_y=None,
        height=month_font_size * 1.2,
        halign='center',
        valign='middle'
    )
    
    year_label = Label(
        text=formatted_dates["year"]["text"],
        font_name=formatted_dates["year"]["font"],
        font_size=year_font_size,
        color=(1, 1, 1, 1),
        size_hint_x=1,
        size_hint_y=None,
        height=year_font_size * 1.2,
        halign='center',
        valign='middle'
    )
    
    # Создаем GridLayout для размещения Label
    date_layout = GridLayout(
        cols=4,
        size_hint_y=None,
        height=max(weekday_font_size, day_font_size, month_font_size, year_font_size) * 1.2
    )
    date_layout.add_widget(weekday_label)
    date_layout.add_widget(day_label)
    date_layout.add_widget(month_label)
    date_layout.add_widget(year_label)
    
    return date_layout

def create_hijri_date_label(base_font_size):
    """
    Создает Label для даты Хиджры
    
    Args:
        base_font_size (float): Базовый размер шрифта
    
    Returns:
        Label: Label с датой Хиджры
    """
    formatted_dates = get_formatted_dates()
    
    return Label(
        text=formatted_dates['hijri'],
        font_name='FontSourceCodePro-Regular',
        font_size=base_font_size * 0.2,  # Размер шрифта
        color=(1, 1, 1, 1),  # Белый цвет
        size_hint_x=1,  # Занимает всю ширину
        size_hint_y=None,  # Фиксированная высота
        height=base_font_size * 0.25,  # Фиксированная высота
        halign='center',  # Центр по горизонтали
        valign='middle',  # Центр по вертикали
    )