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
kivy.require('2.2.1')

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.input.motionevent import MotionEvent

from ui.test_window import TestWindow
from ui.clock_widget import ClockWidget
from ui.settings_manager import SettingsManager

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
        
        # Добавляем часы
        self.clock_widget = ClockWidget()
        
        # Устанавливаем коллбэк для обновления виджета часов
        self.clock_widget.bind_on_clock_widget_created(self._on_clock_widget_created)
        
        self.layout.add_widget(self.clock_widget)
        
        # Создаем менеджер настроек
        self.settings_manager = SettingsManager(self.clock_widget.clock_widget)
        self.settings_manager.apply_saved_color()
        
        # Привязываем обработчики свайпа
        Window.bind(on_touch_down=self.on_window_touch_down)
        Window.bind(on_touch_up=self.on_window_touch_up)
        
        # Привязываем обработчик двойного клика к окну
        Window.bind(on_touch_down=self.on_window_touch_down_double_tap)
        
        # Создаем тестовое окно, но пока не показываем
        self.test_window = TestWindow()
        
        return self.layout

    def switch_to_test(self):
        """Переключение на тестовое окно"""
        if self.current_window == 'main':
            self.layout.remove_widget(self.clock_widget)
            self.layout.add_widget(self.test_window)
            self.current_window = 'test'
        
    def switch_to_main(self):
        """Переключение на главное окно"""
        if self.current_window == 'test':
            self.layout.remove_widget(self.test_window)
            self.layout.add_widget(self.clock_widget)
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
