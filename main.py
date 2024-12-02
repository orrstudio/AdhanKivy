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

from ui.settings_window import SettingsWindow
from ui.settings_manager import SettingsManager
from ui.clock_widget import ClockWidget
from data.database import SettingsDatabase
from logic.time_handler import TimeHandler

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
            spacing=0,
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
        
        # Добавляем заголовок в начало макета
        self.layout.add_widget(self.title_label)

        # Создаем таблицу молитв
        prayer_times_table = GridLayout(
            cols=2,  # Две колонки: время и название молитвы
            spacing=(0, 0),  # Без отступов между ячейками
            size_hint=(0.9, 0.8),  # 90% ширины и 80% высоты родительского контейнера
            pos_hint={'center_x': 0.5, 'top': 1},  # По центру по горизонтали и прижато к верху
            padding=(0, 0)  # Без отступов от краев
        )
        
        # Привязываем обработчик изменения размера
        prayer_times_table.bind(width=self.on_width_change)
        
        # Создаем метки при инициализации
        self.create_prayer_labels(prayer_times_table, [
            ('Təhəccüd -', '05:30'),
            ('İmsak ----', '05:30'),
            ('Günəş ----', '05:30'),
            ('Günorta --', '13:00'),
            ('İkindi ---', '15:00'),
            ('Axşam ----', '16:30'),
            ('Gecə -----', '20:30')
        ])

        # Добавляем таблицу молитв в основной layout
        self.layout.add_widget(prayer_times_table)

        # Запускаем таймер обновления времени и мигания точек каждые 0.5 секунды
        self.is_colon_visible = True
        Clock.schedule_interval(self.update_time_with_colon, 0.5)

        # Устанавливаем текущее окно
        self.current_window = 'main'
        
        return self.layout
        
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
        
        for prayer, time in prayer_times:
            # Динамический расчет размера шрифта для названия молитвы
            prayer_font_size = base_font_size * max(1, Window.width / 500)  # Уменьшаем коэффициент
            
            # Динамический расчет размера шрифта для времени
            time_font_size = base_font_size * max(1, Window.width / 500)  # Уменьшаем коэффициент
            
            prayer_label = Label(
                text=prayer,
                font_size=prayer_font_size * 0.45,
                font_name='PrayerNameFont',
                size_hint_x=None,  # Отключаем относительные размеры по горизонтали
                size_hint_y=None,  # Отключаем относительные размеры по вертикали
                width=Window.width * 0.55,  # Абсолютная ширина
                height=prayer_font_size * 0.5,  # Динамическая высота
                halign='left',
                valign='middle',
                text_size=(Window.width * 0.58, None),  # Указываем размер текста
                color=(1, 1, 1, 1)  # Белый цвет
            )
            time_label = Label(
                text=time,
                font_size=time_font_size * 0.6,
                font_name='PrayerTimeFont',
                size_hint_x=None,  # Отключаем относительные размеры по горизонтали
                size_hint_y=None,  # Отключаем относительные размеры по вертикали
                width=Window.width * 0.35,  # Абсолютная ширина
                height=time_font_size * 0.6,  # Динамическая высота
                halign='right',
                valign='middle',
                text_size=(Window.width * 0.52, None),  # Указываем размер текста
                color=(1, 1, 1, 1)  # Белый цвет
            )
            
            prayer_times_table.add_widget(prayer_label)
            prayer_times_table.add_widget(time_label)

    def on_width_change(self, instance, width):
        # Перересовываем метки при изменении ширины
        self.create_prayer_labels(instance, [
            ('Təhəccüd -', '05:30'),
            ('İmsak ----', '05:30'),
            ('Günəş ----', '05:30'),
            ('Günorta --', '13:00'),
            ('İkindi ---', '15:00'),
            ('Axşam ----', '16:30'),
            ('Gecə -----', '20:30')
        ])
        
if __name__ == "__main__":
    MainWindowApp().run()
