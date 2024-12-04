"""
Модуль генерации таблицы молитв для портретной ориентации.

Функционал:
- Создание полной таблицы молитв
- Адаптация под портретную ориентацию экрана
- Сохранение оригинального дизайна и логики отображения

Особенности:
- Динамический расчет размеров шрифта
"""

from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from ui.date_widget_portrait import create_date_widget_portrait

def create_portrait_prayer_times_table(self):
    """
    Создает таблицу молитв для портретной ориентации
    Адаптивная сетка с двумя колонками для названий и времени молитв
    """
    # Создаем общий контейнер
    portrait_layout = GridLayout(
        cols=1,  # Один столбец
        spacing=(10, 10),  # Отступы между элементами
        size_hint=(0.9, None),  # Занимаем 90% ширины, высота авто
        pos_hint={'center_x': 0.5}  # Центрируем по горизонтали
    )
    
    # Создаем и добавляем виджеты
    space1_widget, date_widget, date_hijri_widget, line1_widget, day_hello_widget = create_date_widget_portrait(self)
    portrait_layout.add_widget(space1_widget)
    portrait_layout.add_widget(date_widget)
    portrait_layout.add_widget(date_hijri_widget)
    portrait_layout.add_widget(line1_widget)
    portrait_layout.add_widget(day_hello_widget)
    
    # Создаем GridLayout для таблицы молитв с двумя колонками
    prayer_times_table = GridLayout(
        cols=2,  # Две колонки: название молитвы и время
        spacing=(10, 10),  # Отступы между элементами сетки
        size_hint=(0.9, None),  # Занимаем 90% ширины, высота авто
        pos_hint={'center_x': 0.5}  # Центрируем по горизонтали
    )
    
    # Расчет базового размера шрифта с учетом размера экрана
    base_font_size = self.calculate_font_size(scale_factor=5)
    
    # Список молитв с временами (статический для демонстрации)
    prayer_times = [
        #('', '', {}),  # Пустая строка для отступа
        ('=====>>>>>', '00:00'),  # Специальная строка
        (' ', ' ', {}),  # Еще один отступ
        ('Təhəccüd -', '00:30'),  # Ночная молитва
        ('İmsak ----', '05:30'),  # Утренняя молитва до восхода
        ('Günəş ----', '05:30'),  # Молитва восхода
        ('Günorta --', '13:00'),  # Полуденная молитва
        ('İkindi ---', '15:00'),  # Послеполуденная молитва
        ('Axşam ----', '16:30'),  # Вечерняя молитва
        ('Gecə -----', '20:30')   # Ночная молитва
    ]
    
    # Итерация по каждой молитве для создания Label
    for item in prayer_times:
        # Проверка на наличие дополнительных параметров
        if len(item) == 3 and isinstance(item[2], dict):
            # Распаковка элемента с параметрами
            prayer, time, params = item
            # Создание Label для названия молитвы с особыми параметрами
            prayer_label = Label(
                text=prayer,
                font_size=params.get('font_size', 1),  # Размер шрифта из параметров
                font_name=params.get('font_name', 'PrayerNameFont'),  # Шрифт из параметров
                size_hint_x=None,  # Фиксированная ширина
                size_hint_y=None,  # Фиксированная высота
                height=base_font_size * 0.01,  # Маленькая высота
                color=(1, 1, 1, 0)  # Прозрачный цвет
            )
            # Создание Label для времени молитвы с особыми параметрами
            time_label = Label(
                text=time,
                font_size=params.get('font_size', 1),
                font_name=params.get('font_name', 'PrayerNameFont'),
                size_hint_x=None,
                size_hint_y=None,
                height=base_font_size * 0.01,
                color=(1, 1, 1, 0)
            )
        else:
            # Стандартная обработка элементов без параметров
            prayer, time = item
            # Динамический расчет размера шрифта в зависимости от ширины экрана
            prayer_font_size = base_font_size * max(1, Window.width / 600)
            time_font_size = base_font_size * max(1, Window.width / 600)
            
            # Создание Label для названия молитвы
            prayer_label = Label(
                text=prayer,
                font_size=prayer_font_size * 0.25,  # Уменьшаем размер шрифта
                font_name='PrayerNameFont',  # Специальный шрифт
                size_hint_x=None,  # Фиксированная ширина
                size_hint_y=None,  # Фиксированная высота
                width=Window.width * 0.6,  # Ширина 60% от экрана
                height=prayer_font_size * 0.38,  # Высота пропорциональна шрифту
                halign='left',  # Выравнивание по левому краю
                valign='middle',  # Вертикальное центрирование
                text_size=(Window.width * 0.45, None),  # Размер текста
                color=(1, 1, 1, 1)  # Белый цвет
            )
            
            # Создание Label для времени молитвы
            time_label = Label(
                text=time,
                font_size=time_font_size * 0.35,  # Уменьшаем размер шрифта
                font_name='PrayerTimeFont',  # Специальный шрифт для времени
                size_hint_x=None,  # Фиксированная ширина
                size_hint_y=None,  # Фиксированная высота
                width=Window.width * 0.25,  # Ширина 28% от экрана
                height=time_font_size * 0.38,  # Высота пропорциональна шрифту
                halign='right',  # Выравнивание по правому краю
                valign='middle',  # Вертикальное центрирование
                text_size=(Window.width * 0.35, None),  # Размер текста
                color=(1, 1, 1, 1)  # Белый цвет
            )
        
        # Добавление Label в таблицу молитв
        prayer_times_table.add_widget(prayer_label)
        prayer_times_table.add_widget(time_label)
    
    # Добавляем таблицу молитв в общий контейнер
    portrait_layout.add_widget(prayer_times_table)
    
    # Возвращаем общий контейнер с датой и таблицей
    return portrait_layout
