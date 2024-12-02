"""
Структура проекта

📁 AdhanKivy/
│
├── 🐍 main.py
│   └── 🏛️ MainWindowApp (Основной класс приложения)
│       ├── __init__()
│       │   - Инициализация параметров свайпа
│       │   - Установка начальных значений
│       │
│       ├── build()
│       │   - Настройка окна
│       │   - Создание основного layout
│       │   - Добавление виджетов:
│       │     • ClockWidget
│       │     • SettingsManager
│       │     • TestWindow
│       │   - Привязка обработчиков событий
│       │
│       ├── Методы переключения окон
│       │   - switch_to_test()
│       │   - switch_to_main()
│       │
│       ├── Обработчики событий
│       │   - on_window_touch_down()
│       │   - on_window_touch_up()
│       │   - on_window_touch_down_double_tap()
│       │
│       └── Служебные методы
│           - _on_clock_widget_created()
│
└── 📂 ui/
    ├── 🕰️ clock_widget.py
    ├── 🔧 settings_manager.py
    └── 🧪 test_window.py

Структура класса MainWindowApp:

MainWindowApp
│
├── Атрибуты
│   - current_window: текущее активное окно
│   - touch_start_x, touch_start_y: координаты начала свайпа
│   - SWIPE_THRESHOLD: порог длины свайпа
│
├── Методы создания интерфейса
│   - build(): основной метод создания интерфейса
│   - _on_clock_widget_created(): обновление виджета часов
│
├── Методы навигации
│   - switch_to_test(): переход в тестовый режим
│   - switch_to_main(): возврат в главный экран
│
└── Обработчики событий
    - on_window_touch_down(): начало касания
    - on_window_touch_up(): обработка свайпа
    - on_window_touch_down_double_tap(): обработка двойного тапа

🔍 Основные компоненты:

1. Главное окно с часами
2. Тестовое окно
3. Окно настроек
4. Система навигации жестами

Интересные особенности:
- Использует Kivy для создания кроссплатформенного интерфейса
- Реализована навигация через свайпы и двойные тапы
- Гибкая система переключения между экранами

"""

# main.py
import kivy
from datetime import datetime
kivy.require('2.2.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.input.motionevent import MotionEvent
from kivy.clock import Clock

from ui.test_window import TestWindow
from ui.settings_manager import SettingsManager
from logic.time_handler import TimeHandler

class MainWindowApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_window = 'main'
        self.touch_start_x = None
        self.touch_start_y = None
        self.SWIPE_THRESHOLD = 200  # Минимальная длина свайпа в пикселях
        
    def build(self):
        # Черный фон
        Window.clearcolor = (0, 0, 0, 1)
        
        # Основной layout
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
        
        # Создаем тестовое окно
        self.test_window = TestWindow(
            on_double_tap=self.switch_to_main  # Привязываем двойное касание к возврату в главное окно
        )
        
        # Добавляем тестовое окно в основной layout
        self.layout.add_widget(self.test_window)
        
        # Запускаем таймер обновления времени и мигания точек каждые 0.5 секунды
        self.is_colon_visible = True
        Clock.schedule_interval(self.update_time_with_colon, 0.5)
        
        # Создаем менеджер настроек
        self.settings_manager = SettingsManager(None)
        self.settings_manager.apply_saved_color()
        
        # Привязываем обработчики свайпа
        Window.bind(on_touch_down=self.on_window_touch_down)
        Window.bind(on_touch_up=self.on_window_touch_up)
        
        # Привязываем обработчик двойного клика к окну
        Window.bind(on_touch_down=self.on_window_touch_down_double_tap)
        
        return self.layout

    def switch_to_test(self):
        """Переключение на тестовое окно"""
        if self.current_window == 'main':
            self.layout.remove_widget(self.title_label)
            self.current_window = 'test'
        
    def switch_to_main(self):
        """Переключение на главное окно"""
        if self.current_window == 'test':
            self.layout.add_widget(self.title_label)
            self.current_window = 'main'

    def on_window_touch_down(self, window, touch):
        # Сохраняем начальную позицию свайпа
        self.touch_start_x = touch.x
        self.touch_start_y = touch.y
        return False

    def on_window_touch_up(self, window, touch):
        if self.touch_start_x is None or self.touch_start_y is None:
            return False

        # Вычисляем смещение свайпа
        dx = touch.x - self.touch_start_x
        dy = touch.y - self.touch_start_y

        # Сбрасываем начальную позицию
        self.touch_start_x = None
        self.touch_start_y = None

        # Определяем пороги для свайпа
        SWIPE_THRESHOLD = 200  # Минимальная длина свайпа в пикселях

        # Проверяем свайп в любом направлении
        if (abs(dx) > SWIPE_THRESHOLD or abs(dy) > SWIPE_THRESHOLD):
            self.switch_to_test()
            return True

        return False

    def on_window_touch_down_double_tap(self, instance, touch):
        """
        Обработчик касания окна.
        Открывает окно настроек или возвращается в основное окно.
        """
        # Проверяем количество касаний
        if touch.is_double_tap or getattr(touch, 'tap_count', 0) == 2:
            
            # Если текущее окно - тестовое, возвращаемся в основное
            if self.current_window == 'test':
                self.switch_to_main()
                return True
            
            # Если основное окно, открываем настройки
            elif self.current_window == 'main':
                self.settings_manager.open_settings_window()
                return True
        
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

if __name__ == "__main__":
    MainWindowApp().run()
