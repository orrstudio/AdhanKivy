# Настройка двойного касания в Kivy

## Описание
В этой документации описывается, как настроить обработку двойного касания (double tap) для перехода между окнами в приложении Kivy.

## Пример реализации
Рассмотрим пример реализации на основе класса `TestWindow`, где двойное касание используется для возврата в главное окно.

### 1. Импорт необходимых модулей
```python
from kivy.input.motionevent import MotionEvent  # Для обработки касаний
from kivy.app import App  # Для доступа к основному приложению
```

### 2. Реализация метода on_touch_down
```python
def on_touch_down(self, touch: MotionEvent, *args) -> bool:
    """
    Обработчик касания экрана.
    Закрывает текущее окно при двойном касании внутри него.
    
    Args:
        touch (MotionEvent): Событие касания с координатами
        *args: Дополнительные аргументы Kivy

    Returns:
        bool: True если касание обработано, False если нет
    """
    # Сначала передаем касание родительскому классу
    ret = super().on_touch_down(touch)
    
    # Проверяем условия для двойного касания
    if isinstance(touch, MotionEvent) and \
       self.collide_point(*touch.pos) and \
       hasattr(touch, 'is_double_tap') and \
       touch.is_double_tap:
        
        app = App.get_running_app()
        if hasattr(app, 'switch_to_main'):
            app.switch_to_main()
        return True
    
    return ret
```

### 3. Важные компоненты
1. **Проверка типа касания**:
   ```python
   isinstance(touch, MotionEvent)
   ```
   Убеждаемся, что объект касания правильного типа.

2. **Проверка области касания**:
   ```python
   self.collide_point(*touch.pos)
   ```
   Проверяем, что касание произошло внутри виджета.

3. **Проверка двойного касания**:
   ```python
   hasattr(touch, 'is_double_tap') and touch.is_double_tap
   ```
   Проверяем наличие и значение атрибута is_double_tap.

4. **Переключение окна**:
   ```python
   app = App.get_running_app()
   if hasattr(app, 'switch_to_main'):
       app.switch_to_main()
   ```
   Получаем экземпляр приложения и вызываем метод переключения.

### 4. Метод переключения в главном приложении
```python
def switch_to_main(self):
    """Переключение на главное окно"""
    if self.current_window == 'test':
        self.layout.remove_widget(self.test_window)
        self.layout.add_widget(self.clock_widget)
        self.layout.add_widget(self.buttons_widget)
        self.current_window = 'main'
```

## Как применить к другим окнам

1. **Импортируйте необходимые модули**:
   ```python
   from kivy.input.motionevent import MotionEvent
   from kivy.app import App
   ```

2. **Добавьте метод on_touch_down**:
   - Скопируйте базовую структуру метода
   - Измените название метода переключения (например, `switch_to_main` на `switch_to_other`)
   - При необходимости добавьте дополнительную логику

3. **Добавьте метод переключения в главное приложение**:
   ```python
   def switch_to_other(self):
       """Переключение на другое окно"""
       if self.current_window == 'current':
           self.layout.remove_widget(self.current_window)
           self.layout.add_widget(self.other_window)
           self.current_window = 'other'
   ```

## Важные замечания

1. Всегда вызывайте `super().on_touch_down(touch)` в начале метода для сохранения базовой функциональности.
2. Сохраняйте результат вызова родительского метода и возвращайте его, если двойное касание не обработано.
3. Проверяйте все условия перед обработкой двойного касания.
4. Убедитесь, что метод переключения существует в главном приложении.

## Отладка

Если возникают проблемы, проверьте:
1. Правильность импорта всех необходимых модулей
2. Наличие всех проверок в методе `on_touch_down`
3. Существование метода переключения в главном приложении
4. Правильность названий виджетов и методов

## Пример использования

```python
class MyCustomWindow(Widget):
    def on_touch_down(self, touch: MotionEvent, *args) -> bool:
        ret = super().on_touch_down(touch)
        
        if isinstance(touch, MotionEvent) and \
           self.collide_point(*touch.pos) and \
           hasattr(touch, 'is_double_tap') and \
           touch.is_double_tap:
            
            app = App.get_running_app()
            if hasattr(app, 'switch_to_other'):
                app.switch_to_other()
            return True
        
        return ret
```
