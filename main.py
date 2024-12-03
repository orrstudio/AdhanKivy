"""
Структура проекта

📁 AdhanKivy/
│
├── ⏰ main.py
│   └── 🏛️ MainWindowApp (Основной класс приложения)
│       ├── __init__()
│       │   - Инициализация параметров
│       │
│       ├── build()
│       │   - Настройка окна
│       │   - Создание основного layout
│       │   - Добавление виджетов:
│       │     • ClockWidget (часы)
│       │     • SettingsManager
│       │
│       ├── Методы адаптивности
│       │   - calculate_font_size()
│       │   - create_prayer_labels()
│       │   - on_width_change()
│       │
│       ├── Методы обновления времени
│       │   - update_time_with_colon()
│       │   - get_current_time()
│       │
│       └── Методы управления цветом
│           - update_title_color()
│           - update_title_font_size()
│
├── � ui/
│   ├── 🕰️ clock_widget.py
│   │   └── ClockWidget
│   │       - Виджет часов с обновлением времени
│   │
│   ├── 🕰️ clock_functions.py
│   │   └── BaseClockLabel
│   │       - Адаптивный Label для часов
│   │
│   ├── 🔧 settings_manager.py
│   │   └── SettingsManager
│   │       - Управление настройками
│   │
│   └── 🖥️ settings_window.py
│       └── SettingsWindow
│           - Окно настроек
│
├── 📁 data/
│   └── 📊 database.py
│       └── SettingsDatabase
│           - Работа с базой настроек
│
└── 📁 logic/
    └── ⏰ time_handler.py
        └── TimeHandler
            - Логика работы с временем

- prayer_times_table.spacing = (10, 10):
  - Это горизонтальный и вертикальный отступ между ячейками таблицы (GridLayout)
  - Первое число (10) - расстояние между столбцами
  - Второе число (10) - расстояние между строками
  - Измеряется в пикселях
  - Чем больше число, тем больше расстояние между ячейками
  - Если поставить (0, 0), ячейки будут вплотную друг к другу

- size_hint=(0.9, 0.8):
  - Относительный размер виджета внутри родительского контейнера
  - Первое число (0.9) означает 90% ширины родительского контейнера
  - Второе число (0.8) означает 80% высоты родительского контейнера
  - Диапазон от 0 до 1
  - Позволяет адаптивно масштабировать элемент под разные размеры экрана
"""

# main.py
import kivy
from datetime import datetime
import math
kivy.require('2.2.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.input.motionevent import MotionEvent
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.uix.anchorlayout import AnchorLayout

from ui.settings_window import SettingsWindow
from ui.settings_manager import SettingsManager
from ui.clock_widget import ClockWidget
from data.database import SettingsDatabase
from logic.time_handler import TimeHandler
from ui.main_portrait import create_portrait_prayer_times_table
from ui.main_landscape import create_landscape_prayer_times_table
from ui.main_square import create_square_prayer_times_table

class MainWindowApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_window = 'main'
        self.touch_start_x = None
        self.touch_start_y = None
        self.SWIPE_THRESHOLD = 200  # Минимальная длина свайпа в пикселях
        
    def build(self):
        # Регистрация шрифтов
        LabelBase.register(
            name='PrayerNameFont', 
            fn_regular='fonts/SourceCodePro/SourceCodePro-ExtraLight.ttf'
        )
        LabelBase.register(
            name='PrayerTimeFont', 
            fn_regular='fonts/DSEG-Classic/DSEG14Classic-Regular.ttf'
        )

        # Черный фон
        Window.clearcolor = (0, 0, 0, 1)
        
        # Привязываем обработчик двойного касания
        Window.bind(on_touch_down=self.on_window_touch_down_double_tap)
        
        # Основной layout - GridLayout
        self.layout = GridLayout(
            cols=1,  # Один столбец
            spacing=Window.height * 0.01,  # Увеличить отступ между виджетами
            padding=0
        )
        
        # Создаем заголовок
        self.title_label = Label(
            text=self.get_current_time(), 
            font_name="fonts/DSEG-Classic/DSEG7Classic-Bold.ttf",
            color=(0, 1, 0, 1),  # зеленый цвет как у часов
            size_hint_x=1,  # занимает всю ширину
            size_hint_y=None,  # отключаем автоматическую высоту
            height=str(Window.width * 0.3) + 'dp',  # высота зависит от ширины
            pos_hint={'top': 1},  # прижат к верху
            font_size=str(Window.width // 3.5) + 'sp',  # начальный размер шрифта
            halign='center'  # центрирование текста
        )
        
        # Привязываем обновление размера шрифта и высоты к изменению размера окна
        Window.bind(width=self.update_title_font_size)
        Window.bind(height=self.update_title_height)
        Window.bind(on_resize=self.on_window_resize)
        
        # Добавляем заголовок в начало макета
        self.layout.add_widget(self.title_label)

        # Определение ориентации и создание соответствующей таблицы молитв
        current_orientation = self.get_current_orientation()
        
        if current_orientation == 'portrait':
            prayer_times_table = create_portrait_prayer_times_table(self)
        elif current_orientation == 'landscape':
            prayer_times_table = create_landscape_prayer_times_table(self)
        else:  # square
            prayer_times_table = create_square_prayer_times_table(self)
        
        # Добавление таблицы молитв, если она не None
        if prayer_times_table:
            self.layout.add_widget(prayer_times_table)

        # Запускаем таймер обновления времени и мигания точек каждые 0.5 секунды
        self.is_colon_visible = True
        Clock.schedule_interval(self.update_time_with_colon, 0.5)

        # Устанавливаем текущее окно
        self.current_window = 'main'
        
        return self.layout

    def get_current_orientation(self):
        """
        Точное определение ориентации экрана
        """
        width, height = Window.size
        
        if width > height * 1.2:
            return 'landscape'
        elif height > width * 1.2:
            return 'portrait'
        else:
            return 'square'

    def on_window_touch_down_double_tap(self, window, touch):
        """Обработчик двойного касания"""
        if touch.is_double_tap:
            # Открываем окно настроек
            self.settings_manager = SettingsManager(None, self)
            self.settings_manager.open_settings_window()
        return False

    def update_title_font_size(self, instance, width):
        """Обновляем размер шрифта в зависимости от ширины окна"""
        self.title_label.font_size = str(width // 3.5) + 'sp'

    def update_title_height(self, instance, height):
        """Обновляем высоту заголовка в зависимости от ширины окна"""
        self.title_label.height = str(Window.width * 0.3) + 'dp'

    def get_current_time(self, show_colon=True):
        """Получаем текущее время с возможностью скрыть двоеточие"""
        return TimeHandler.get_formatted_time(show_colon)
    
    def update_time_with_colon(self, dt):
        """Обновляем время с мигающим двоеточием"""
        self.is_colon_visible = not self.is_colon_visible
        self.title_label.text = self.get_current_time(self.is_colon_visible)

    def _on_clock_widget_created(self, clock_widget=None):
        """
        Обновляем ссылку на виджет часов в менеджере настроек
        """
        # Если clock_widget не передан, используем текущий виджет часов
        if clock_widget is None and hasattr(self.clock_widget, 'clock_widget'):
            clock_widget = self.clock_widget.clock_widget
        
        self.settings_manager.clock_label = clock_widget
        self.settings_manager.apply_saved_color()

    def apply_initial_color(self, dt):
        """Применение начального цвета после инициализации"""
        initial_color = self.settings_manager.db.get_setting('color')
        if initial_color:
            color_tuple = SettingsWindow.get_color_tuple(initial_color)
            self.update_title_color(color_tuple)
        
    def update_title_color(self, color):
        """Обновляем цвет заголовка"""
        self.title_label.color = color
        
    def update_color(self, color_name):
        """Обновляем цвет по имени"""
        color_tuple = SettingsWindow.get_color_tuple(color_name)
        self.update_title_color(color_tuple)

    def calculate_font_size(self, scale_factor=0.1):
        # Логарифмическая шкала для более плавного масштабирования
        base_size = min(Window.width, Window.height)
        
        # Используем логарифмическую функцию для более естественного масштабирования
        logarithmic_scale = math.log(base_size + 1, 10)  # +1 чтобы избежать деления на ноль
        
        # Применяем нелинейное масштабирование
        font_size = logarithmic_scale * base_size * scale_factor
        
        # Устанавливаем жесткие границы
        return max(min(font_size, base_size * 0.2), 10)

    def create_prayer_labels(self, prayer_times_table, prayer_times):
        prayer_times_table.clear_widgets()
        
        # Базовый размер шрифта
        base_font_size = self.calculate_font_size(scale_factor=0.15)
        
        # Устанавливаем равномерное распределение колонок
        prayer_times_table.cols = 2
        prayer_times_table.spacing = (10, 10)  # Небольшой отступ
        
        for item in prayer_times:
            # Если элемент содержит 3 параметра - это особый случай (разделитель)
            if len(item) == 3 and isinstance(item[2], dict):
                prayer, time, params = item
                prayer_label = Label(
                    text=prayer,
                    font_size=params.get('font_size', 1),
                    font_name=params.get('font_name', 'PrayerNameFont'),
                    size_hint_x=None,
                    size_hint_y=None,
                    height=base_font_size * 0.01,
                    color=(1, 1, 1, 0)
                )
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
                # Стандартный случай для обычных строк
                prayer, time = item
                prayer_font_size = base_font_size * max(1, Window.width / 600)
                time_font_size = base_font_size * max(1, Window.width / 600)
                
                prayer_label = Label(
                    text=prayer,
                    font_size=prayer_font_size * 0.35, 
                    font_name='PrayerNameFont',
                size_hint_x=None,  # Отключаем относительные размеры по горизонтали
                size_hint_y=None,  # Отключаем относительные размеры по вертикали
                width=Window.width * 0.6,  # Абсолютная ширина
                height=prayer_font_size * 0.35,  # Динамическая высота
                    halign='left',
                    valign='middle',
                text_size=(Window.width * 0.52, None),  # Указываем размер текста
                color=(1, 1, 1, 1)  # Белый цвет
                )
                time_label = Label(
                    text=time,
                    font_size=time_font_size * 0.40,
                    font_name='PrayerTimeFont',
                size_hint_x=None,  # Отключаем относительные размеры по горизонтали
                size_hint_y=None,  # Отключаем относительные размеры по вертикали
                width=Window.width * 0.28,  # Абсолютная ширина
                height=time_font_size * 0.5,  # Динамическая высота
                    halign='right',
                    valign='middle',
                text_size=(Window.width * 0.42, None),  # Указываем размер текста
                color=(1, 1, 1, 1)  # Белый цвет
                )
            
            prayer_times_table.add_widget(prayer_label)
            prayer_times_table.add_widget(time_label)

    def on_width_change(self, instance, width):
        # Перересовываем метки при изменении ширины
        self.create_prayer_labels(instance, [
            ('', '', {}),
            ('===>>> ---', '00:00'),
            (' ', ' ', {}),
            ('Təhəccüd -', '00:30'),
            ('İmsak ----', '05:30'),
            ('Günəş ----', '05:30'),
            ('Günorta --', '13:00'),
            ('İkindi ---', '15:00'),
            ('Axşam ----', '16:30'),
            ('Gecə -----', '20:30')
        ])

    def on_window_resize(self, instance, width, height):
        """
        Обработчик изменения размера окна
        """
        # Удаляем старую таблицу
        for child in self.layout.children[:]:
            if isinstance(child, GridLayout) and child != self.title_label:
                self.layout.remove_widget(child)
        
        # Определяем новую ориентацию
        current_orientation = self.get_current_orientation()
        
        # Создаем новую таблицу
        if current_orientation == 'portrait':
            prayer_times_table = create_portrait_prayer_times_table(self)
        elif current_orientation == 'landscape':
            prayer_times_table = create_landscape_prayer_times_table(self)
        else:  # square
            prayer_times_table = create_square_prayer_times_table(self)
        
        # Добавляем таблицу, если она не None
        if prayer_times_table:
            self.layout.add_widget(prayer_times_table)

    def classify_block_orientation(self, block):
        """
        Классифицирует блок по его ориентации
        
        :param block: Kivy виджет
        :return: 'portrait', 'landscape', или 'square'
        """
        # Получаем размеры блока
        width = block.width
        height = block.height
        
        # Определяем ориентацию с некоторым допуском
        tolerance = 0.1  # 10% погрешности
        
        if abs(width - height) / max(width, height) <= tolerance:
            return 'square'
        elif width > height * (1 + tolerance):
            return 'landscape'
        elif height > width * (1 + tolerance):
            return 'portrait'
        else:
            return 'square'

    def separate_blocks_by_orientation(self, layout):
        """
        Разделяет блоки layout по ориентации
        
        :param layout: Kivy layout
        :return: Словарь с разделенными блоками
        """
        orientations = {
            'portrait': [],
            'landscape': [],
            'square': []
        }
        
        for child in layout.children:
            orientation = self.classify_block_orientation(child)
            orientations[orientation].append(child)
        
        return orientations

if __name__ == "__main__":
    MainWindowApp().run()
