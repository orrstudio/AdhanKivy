"""
Структура проекта

📁 AdhanKivy/
│
├── ⏰ main.py
│   └── 🏛️ MainWindowApp (Основной класс приложения)
│       ├── Инициализация и настройка окна
│       │   - Регистрация шрифтов
│       │   - Создание основного layout
│       │   - Настройка заголовка с часами
│       │
│       ├── Методы ориентации
│       │   - get_current_orientation()
│       │   - on_window_resize()
│       │
│       ├── Методы адаптивности
│       │   - calculate_font_size()
│       │   - update_title_font_size()
│       │   - update_title_height()
│       │
│       └── Методы управления временем
│           - get_current_time()
│           - update_time_with_colon()
│
├── 🖼️ ui/
│   ├── 🕰️ main_portrait.py - Таблица молитв для портретной ориентации
│   │   Генерирует полную таблицу молитв с адаптацией под вертикальный экран
│   │
│   ├── 🕰️ main_landscape.py - Таблица молитв для ландшафтной ориентации
│   │   Возвращает пустой layout для горизонтального экрана
│   │
│   ├── 🕰️ main_square.py - Таблица молитв для квадратной ориентации
│   │   Возвращает пустой layout для квадратного экрана
│   │
│   ├── 🕰️ clock_widget.py - Виджет часов
│   ├── 🕰️ clock_functions.py - Вспомогательные функции для работы с часами
│   ├── 🔧 settings_manager.py - Управление настройками приложения
│   └── 🖥️ settings_window.py - Окно настроек
│
├── 📁 data/
│   └── 📊 database.py
│
└── 📁 logic/
    └── ⏰ time_handler.py

"""

# main.py
import kivy
from datetime import datetime
import math
kivy.require('2.2.1')

# Импорты базовых классов Kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.input.motionevent import MotionEvent
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.metrics import sp
from kivy.uix.anchorlayout import AnchorLayout

# Импорты локальных модулей приложения
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
