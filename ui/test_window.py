"""
TestWindow (GridLayout)
│
├── Свойства:
│   ├── cols = 2 (две колонки)
│   ├── spacing = (0, 0) (без отступов между ячейками)
│   ├── size_hint = (None, None) (фиксированный размер)
│   ├── size = (Window.width * 0.9, Window.height * 0.8) (относительный размер)
│   ├── pos_hint = {'center_x': 0.5, 'top': 1} (по центру по горизонтали и прижато к верху)
│   └── pos_hint = {'top': 1} (прижато к верху)
│
├── Данные:
│   └── prayer_times - список времен молитв
│       ├── Тахаджуд (05:30)
│       ├── Имсак (05:30)
│       ├── Восход солнца (05:30)
│       ├── Полуденная молитва (13:00)
│       ├── Послеполуденная молитва (15:00)
│       ├── Вечерняя молитва (16:30)
│       └── Ночная молитва (20:30)
│
├── Методы:
│   ├── __init__(): Инициализация окна
│   ├── calculate_font_size(): Расчет размера шрифта
│   ├── create_labels(): Создание меток времени молитв
│   ├── on_window_resize(): Обработка изменения размера окна
│   └── on_touch_down(): Обработка двойного касания для закрытия окна
│
└── Особенности:
    ├── Использует два пользовательских шрифта
    ├── Адаптивный размер шрифта
    ├── Двухколоночный макет (название молитвы | время)
    └── Закрытие окна по двойному касанию

Основные характеристики:

1. Окно представляет собой таблицу с двумя колонками
2. Шрифты:
    - PrayerNameFont для названий молитв
    - PrayerTimeFont для времени
3. Размер шрифта динамически меняется в зависимости от ширины окна
4. Поддерживает закрытие по двойному касанию

Это тестовое окно для отображения времен молитв с адаптивным дизайном.


"""

# Импорты из Kivy фреймворка
import math
from kivy.uix.label import Label  # Для текстовых меток в таблице
from kivy.uix.gridlayout import GridLayout  # Для создания табличной структуры
from kivy.core.text import LabelBase  # Для регистрации шрифтов
from kivy.input.motionevent import MotionEvent  # Для обработки касаний

class TestWindow(GridLayout):
    """
    Окно для отображения времен молитв в табличном формате.
    Использует двухколоночную структуру, где первая колонка - время,
    вторая - название молитвы. Закрывается по двойному касанию в любом месте окна.
    """
    def __init__(self, 
                 prayer_name_font='fonts/SourceCodePro/SourceCodePro-ExtraLight.ttf', 
                 prayer_time_font='fonts/DSEG-Classic/DSEG14Classic-Regular.ttf',
                 prayer_times=None,
                 on_double_tap=None,
                 text_config=None,
                 **kwargs):
        # Регистрация шрифтов
        LabelBase.register(name='PrayerNameFont', fn_regular=prayer_name_font)
        LabelBase.register(name='PrayerTimeFont', fn_regular=prayer_time_font)
        
        # Сохраняем коллбэк
        self.on_double_tap = on_double_tap
        
        # Конфигурация по умолчанию
        self.default_text_config = {
            'prayer_name': {
                'scale_factor': 0.15,  # Возвращаем прежний коэффициент
                'height_factor': 2.0,  # Высота метки
                'font_scale': 1.5,     # Дополнительный множитель размера шрифта
                'halign': 'left',
                'valign': 'middle',
                'color': (1, 1, 1, 1)  # Белый цвет
            },
            'prayer_time': {
                'scale_factor': 0.15,
                'height_factor': 2.0,
                'font_scale': 1.5,
                'halign': 'right',
                'valign': 'middle',
                'color': (1, 1, 1, 1)  # Белый цвет
            }
        }
        
        # Обновляем конфигурацию если передана
        if text_config:
            for key in ['prayer_name', 'prayer_time']:
                if key in text_config:
                    self.default_text_config[key].update(text_config[key])
        
        super().__init__(**kwargs)
        
        # Устанавливаем цвет фона
        self.background_color = (0, 0, 0, 1)  # Темно-серый фон
        self.background = True
        
        # Настраиваем таблицу
        self.cols = 2  # Две колонки: время и название молитвы
        self.spacing = (0, 0)  # Без отступов между ячейками
        
        # Адаптивные параметры
        self.size_hint = (0.9, 0.8)  # 90% ширины и 80% высоты родительского контейнера
        self.pos_hint = {'center_x': 0.5, 'top': 1}  # По центру по горизонтали и прижато к верху
        
        self.padding = (0, 0)  # Без отступов от краев
        
        # Тестовые данные времен молитв, если не переданы
        self.prayer_times = prayer_times or [
            ('Təhəccüd -', '05:30'),  # Тахаджуд (ночная молитва)
            ('İmsak ----', '05:30'),  # Имсак (начало поста)
            ('Günəş ----', '05:30'),  # Восход солнца
            ('Günorta --', '13:00'),  # Полуденная молитва
            ('İkindi ---', '15:00'),  # Послеполуденная молитва
            ('Axşam ----', '16:30'),  # Вечерняя молитва
            ('Gecə -----', '20:30')   # Ночная молитва
        ]
        
        # Сохраняем начальную ширину как базовую
        self.initial_width = self.width
        
        # Привязываем обработчик изменения размера
        self.bind(width=self.on_width_change)
        
        # Создаем метки при инициализации
        self.create_labels()
            
        # Включаем обработку касаний
        self.bind(on_touch_down=self.on_touch_down)

    def calculate_font_size(self, scale_factor=0.1):
        # Логарифмическая шкала для более плавного масштабирования
        base_size = min(self.width, self.height)
        
        # Используем логарифмическую функцию для более естественного масштабирования
        logarithmic_scale = math.log(base_size + 1, 10)  # +1 чтобы избежать деления на ноль
        
        # Применяем нелинейное масштабирование
        font_size = logarithmic_scale * base_size * scale_factor
        
        # Устанавливаем жесткие границы
        return max(min(font_size, base_size * 0.2), 10)

    def create_labels(self):
        self.clear_widgets()
        
        # Базовый размер шрифта
        base_font_size = self.calculate_font_size(scale_factor=0.15)
        
        # Устанавливаем равномерное распределение колонок
        self.cols = 2
        self.spacing = (10, 10)  # Небольшой отступ
        
        for prayer, time in self.prayer_times:
            # Динамический расчет размера шрифта для названия молитвы
            prayer_font_size = base_font_size * max(1, self.width / 500)  # Уменьшаем коэффициент
            
            # Динамический расчет размера шрифта для времени
            time_font_size = base_font_size * max(1, self.width / 500)  # Уменьшаем коэффициент
            
            prayer_label = Label(
                text=prayer,
                font_size=prayer_font_size * 0.45,
                font_name='PrayerNameFont',
                size_hint_x=None,  # Отключаем относительные размеры по горизонтали
                size_hint_y=None,  # Отключаем относительные размеры по вертикали
                width=self.width * 0.55,  # Абсолютная ширина
                height=prayer_font_size * 0.5,  # Динамическая высота
                halign='left',
                valign='middle',
                text_size=(self.width * 0.58, None),  # Указываем размер текста
                color=(1, 1, 1, 1)  # Белый цвет
            )
            time_label = Label(
                text=time,
                font_size=time_font_size * 0.6,
                font_name='PrayerTimeFont',
                size_hint_x=None,  # Отключаем относительные размеры по горизонтали
                size_hint_y=None,  # Отключаем относительные размеры по вертикали
                width=self.width * 0.35,  # Абсолютная ширина
                height=time_font_size * 0.6,  # Динамическая высота
                halign='right',
                valign='middle',
                text_size=(self.width * 0.52, None),  # Указываем размер текста
                color=(1, 1, 1, 1)  # Белый цвет
            )
            
            self.add_widget(prayer_label)
            self.add_widget(time_label)

    def on_window_resize(self, instance, width, height):
        """
        Обработчик изменения размера виджета.
        Пересоздает метки с учетом новых собственных размеров.
        """
        # Пересоздаем метки с текущими размерами виджета
        self.create_labels()

    def on_width_change(self, instance, width):
        # Перересовываем метки при изменении ширины
        self.create_labels()

    def on_touch_down(self, touch: MotionEvent, *args) -> bool:
        """
        Обработчик касания экрана.
        Закрывает тестовое окно при двойном касании внутри него.
        
        Args:
            touch (MotionEvent): Событие касания с координатами
            *args: Дополнительные аргументы Kivy

        Returns:
            bool: True если касание обработано, False если нет
        """
        # Сначала передаем касание родительскому классу для обработки базовой функциональности
        ret = super().on_touch_down(touch)
        
        # Проверяем, что touch - это объект касания и было двойное касание внутри окна
        if isinstance(touch, MotionEvent) and self.collide_point(*touch.pos) and hasattr(touch, 'is_double_tap') and touch.is_double_tap:
            if self.on_double_tap:
                self.on_double_tap()
            return True
        
        return ret
