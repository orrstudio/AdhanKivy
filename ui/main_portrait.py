from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window

def create_portrait_prayer_times_table(self):
    """
    Создает таблицу молитв для портретной ориентации
    """
    prayer_times_table = GridLayout(
        cols=2,  
        spacing=(10, 10),
        size_hint=(0.9, None),
        pos_hint={'center_x': 0.5}
    )
    
    base_font_size = self.calculate_font_size(scale_factor=0.15)
    
    prayer_times = [
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
    ]
    
    for item in prayer_times:
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
            prayer, time = item
            prayer_font_size = base_font_size * max(1, Window.width / 600)
            time_font_size = base_font_size * max(1, Window.width / 600)
            
            prayer_label = Label(
                text=prayer,
                font_size=prayer_font_size * 0.35, 
                font_name='PrayerNameFont',
                size_hint_x=None,
                size_hint_y=None,
                width=Window.width * 0.6,
                height=prayer_font_size * 0.35,
                halign='left',
                valign='middle',
                text_size=(Window.width * 0.52, None),
                color=(1, 1, 1, 1)
            )
            time_label = Label(
                text=time,
                font_size=time_font_size * 0.40,
                font_name='PrayerTimeFont',
                size_hint_x=None,
                size_hint_y=None,
                width=Window.width * 0.28,
                height=time_font_size * 0.5,
                halign='right',
                valign='middle',
                text_size=(Window.width * 0.42, None),
                color=(1, 1, 1, 1)
            )
        
        prayer_times_table.add_widget(prayer_label)
        prayer_times_table.add_widget(time_label)
    
    return prayer_times_table
