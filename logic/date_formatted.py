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

HIJRI_MONTH_TO_ROMAN = {
    1: 'I',     # Мухаррам
    2: 'II',    # Сафар
    3: 'III',   # Раби аль-авваль
    4: 'IV',    # Раби ас-сани
    5: 'V',     # Джумада аль-уля
    6: 'VI',    # Джумада ас-сани
    7: 'VII',   # Раджаб
    8: 'VIII',  # Шаабан
    9: 'IX',    # Рамадан
    10: 'X',    # Шавваль
    11: 'XI',   # Зу-ль-када
    12: 'XII'   # Зу-ль-хиджа
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
            'text': f"/{MONTH_TO_ROMAN[month]}/",
            'font': 'FontSourceCodePro-Light'
        },
        'year': {
            'text': current_date.strftime('%Y'),
            'font': 'FontDSEG7-Light'
        },
        'full_gregorian': f"{WEEKDAY_TO_ROMAN[weekday]} - {current_date.strftime('%d')}.{MONTH_TO_ROMAN[month]}.{current_date.strftime('%Y')}",
        
        # Добавляем части для даты хиджры
        'hijri_day': {
            'text': '15',
            'font': 'FontDSEG7-Light'
        },
        'hijri_month': {
            'text': f"/{HIJRI_MONTH_TO_ROMAN[5]}/",  # Используем римские цифры для месяца
            'font': 'FontSourceCodePro-Light'
        },
        'hijri_year': {
            'text': '1445',
            'font': 'FontDSEG7-Light'
        }
    }
    
    return date_parts

def create_gregorian_date_label(base_font_size):
    """
    Создает Label для григорианской даты с разными шрифтами и размерами в одной строке
    
    Args:
        base_font_size (float): Базовый размер шрифта
    
    Returns:
        Label: Label с датой в одной строке
    """
    formatted_dates = get_formatted_dates()
    
    # Определяем размеры для каждой части и округляем их до целых чисел
    weekday_size = int(base_font_size * 0.24)    # Размер для "VI -"
    day_size = int(base_font_size * 0.19)       # Размер для "14"
    month_size = int(base_font_size * 0.24)      # Размер для ".XII."
    year_size = int(base_font_size * 0.19)      # Размер для "2024"
    
    # Формируем текст с разметкой для разных шрифтов и размеров
    marked_text = (
        f'[size={weekday_size}][font=FontSourceCodePro-Light]{formatted_dates["weekday"]["text"]}[/font][/size] '
        f'[size={day_size}][font=FontDSEG7-Light]{formatted_dates["day"]["text"]}[/font][/size]'
        f'[size={month_size}][font=FontSourceCodePro-Light]{formatted_dates["month"]["text"]}[/font][/size]'
        f'[size={year_size}][font=FontDSEG7-Light]{formatted_dates["year"]["text"]}[/font][/size]'
    )
    
    # Создаем Label с поддержкой разметки
    date_label = Label(
        text=marked_text,
        markup=True,  # Включаем поддержку разметки
        color=(1, 1, 1, 1),
        size_hint_x=1,
        size_hint_y=None,
        height=base_font_size * 0.3,  # Увеличиваем высоту для разных размеров
        halign='center',
        valign='middle'
    )
    
    return date_label

def create_hijri_date_label(base_font_size):
    """
    Создает Label с датами хиджры и григорианской в одной строке
    
    Args:
        base_font_size (float): Базовый размер шрифта
    
    Returns:
        Label: Label с обеими датами в одной строке
    """
    formatted_dates = get_formatted_dates()
    
    # Определяем размеры для каждой части и округляем их до целых чисел
    size = int(base_font_size * 0.19)
    month_size = int(base_font_size * 0.24)
    
    # Формируем текст с разметкой для обеих дат
    marked_text = (
        # Дата хиджры
        f'[size={size}][font=FontDSEG7-Light]{formatted_dates["hijri_day"]["text"]}[/font][/size]'
        f'[size={month_size}][font=FontSourceCodePro-Light]{formatted_dates["hijri_month"]["text"]}[/font][/size]'
        f'[size={size}][font=FontDSEG7-Light]{formatted_dates["hijri_year"]["text"]}[/font][/size]'
        # Разделитель
        f'[size={size}][font=FontSourceCodePro-Light] - [/font][/size]'
        # Григорианская дата
        f'[size={size}][font=FontSourceCodePro-Light]{formatted_dates["weekday"]["text"]}[/font][/size] '
        f'[size={size}][font=FontDSEG7-Light]{formatted_dates["day"]["text"]}[/font][/size]'
        f'[size={month_size}][font=FontSourceCodePro-Light]{formatted_dates["month"]["text"]}[/font][/size]'
        f'[size={size}][font=FontDSEG7-Light]{formatted_dates["year"]["text"]}[/font][/size]'
    )
    
    # Создаем Label с поддержкой разметки
    date_label = Label(
        text=marked_text,
        markup=True,
        color=(1, 1, 1, 1),
        size_hint_x=1,
        size_hint_y=None,
        height=base_font_size * 0.3,
        halign='center',
        valign='middle'
    )
    
    return date_label