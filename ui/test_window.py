# Импорты из Kivy фреймворка
from kivy.uix.label import Label  # Для текстовых меток в таблице
from kivy.core.window import Window  # Для работы с окном приложения
from kivy.app import App  # Для доступа к основному приложению
from kivy.uix.gridlayout import GridLayout  # Для создания табличной структуры
from kivy.core.text import LabelBase  # Для регистрации шрифтов
from kivy.input.motionevent import MotionEvent  # Для обработки касаний

# Регистрируем пользовательские шрифты
LabelBase.register(name='PrayerNameFont',  # Шрифт для названий молитв
                  fn_regular='fonts/SourceCodePro/SourceCodePro-ExtraLight.ttf')
LabelBase.register(name='PrayerTimeFont',  # Шрифт для времени
                  fn_regular='fonts/DSEG-Classic/DSEG14Classic-Regular.ttf')

class TestWindow(GridLayout):
    """
    Окно для отображения времен молитв в табличном формате.
    Использует двухколоночную структуру, где первая колонка - время,
    вторая - название молитвы. Закрывается по касанию в любом месте окна.
    """
    def __init__(self, **kwargs):
        # Инициализация родительского класса
        super().__init__(**kwargs)
        
        # Настраиваем таблицу
        self.cols = 2  # Две колонки: время и название молитвы
        self.spacing = (0, 0)  # Без отступов между ячейками
        self.size_hint = (1, None)  # Ширина 100%, высота фиксированная
        self.height = Window.height  # Высота на весь экран
        self.pos_hint = {'top': 1}  # Прижимаем к верхнему краю окна
        self.padding = (0, 0)  # Без отступов от краев
        
        # Тестовые данные времен молитв
        # Формат: (название молитвы, время)
        self.prayer_times = [
            ('Təhəccüd -', '05:30'),  # Тахаджуд (ночная молитва)
            ('İmsak ----', '05:30'),  # Имсак (начало поста)
            ('Günəş ----', '05:30'),  # Восход солнца
            ('Günorta --', '13:00'),  # Полуденная молитва
            ('İkindi ---', '15:00'),  # Послеполуденная молитва
            ('Axşam ----', '16:30'),  # Вечерняя молитва
            ('Gecə -----', '20:30')   # Ночная молитва
        ]
        
        # Создаем метки для всех времен молитв
        self.create_labels()
            
        # Привязываем обработчик изменения размера окна
        Window.bind(on_resize=self.on_window_resize)
        
        # Включаем обработку касаний
        self.bind(on_touch_down=self.on_touch_down)

    def calculate_font_size(self):
        """
        Рассчитывает размер шрифта на основе ширины окна.
        Размер шрифта = 10% от ширины окна, что обеспечивает
        адаптивность текста под разные размеры экрана.
        """
        return Window.width * 0.1  # 10% от ширины окна
    
    def create_labels(self):
        """
        Создает и размещает метки для всех времен молитв.
        Каждая строка состоит из двух меток: время и название молитвы.
        Метки автоматически подстраиваются под размер шрифта.
        """
        # Очищаем старые метки перед созданием новых
        self.clear_widgets()
        
        # Получаем размер шрифта на основе текущей ширины окна
        time_font_size = self.calculate_font_size()  # Размер для времени
        prayer_font_size = time_font_size * 1  # Размер для названий
        
        # Создаем метки для каждого времени молитвы
        for prayer, time in self.prayer_times:
            # Метка для названия молитвы (левая колонка)
            prayer_label = Label(
                text=prayer,  # Текст с названием молитвы
                font_size=prayer_font_size,  # Размер шрифта
                font_name='PrayerNameFont',  # Специальный шрифт для названий
                size_hint=(0.65, None),  # 65% ширины, высота по контенту
                height=time_font_size * 1.5,  # Высота зависит от размера шрифта
                halign='left',  # Выравнивание текста влево
                valign='middle',  # Вертикальное выравнивание по центру
                text_size=(Window.width*0.65, time_font_size * 2.5)  # Область текста
            )
            # Метка для времени (правая колонка)
            time_label = Label(
                text=time,  # Текст со временем
                font_size=time_font_size,  # Размер шрифта
                font_name='PrayerTimeFont',  # Специальный шрифт для времени
                size_hint=(0.35, None),  # 35% ширины, высота по контенту
                height=time_font_size * 1.5,  # Высота зависит от размера шрифта
                halign='right',  # Выравнивание текста вправо
                valign='middle',  # Вертикальное выравнивание по центру
                text_size=(Window.width*0.35, time_font_size * 1.5)  # Область текста
            )
            # Добавляем метки в таблицу
            self.add_widget(prayer_label)  # Сначала название молитвы
            self.add_widget(time_label)    # Затем время
    
    def on_window_resize(self, instance, width, height):
        """
        Обработчик изменения размера окна.
        Пересоздает все метки с новым размером шрифта,
        обеспечивая адаптивность интерфейса.
        """
        # При изменении размера окна пересоздаем все метки
        self.height = height  # Обновляем высоту таблицы
        self.create_labels()  # Пересоздаем метки с новыми размерами
    
    def on_touch_down(self, touch: MotionEvent, *args) -> bool:
        """
        Обработчик касания экрана.
        Закрывает тестовое окно при любом касании внутри него.
        
        Args:
            touch (MotionEvent): Событие касания с координатами
            *args: Дополнительные аргументы Kivy

        Returns:
            bool: True если касание обработано, False если нет
        """
        # Проверяем, было ли касание внутри окна
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            # Проверяем наличие метода переключения окон
            if hasattr(app, 'switch_to_main'):
                app.switch_to_main()  # Переключаемся на главное окно
                return True  # Касание обработано
        # Если касание не в нашей области, передаем его дальше
        return super().on_touch_down(touch, *args)
