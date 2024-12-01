 # AdhanKivy: Времена молитвы

<div align="center">
  <img src="images/logo.png" alt="Adhan Logo" width="400"/>
</div>

<div align="center">
  
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Kivy-2.2.1-brightgreen)](https://kivy.org/)
[![GitHub release](https://img.shields.io/badge/Release-v1.0.0-blue)](https://github.com/OrrStudio/AdhanKivy/releases)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/OrrStudio/AdhanKivy/graphs/commit-activity)
[![GitHub issues](https://img.shields.io/github/issues/OrrStudio/AdhanKivy)](https://github.com/OrrStudio/AdhanKivy/issues)

</div>

## 🕰️ О Проекте

AdhanKivy - это приложение для отображения и напоминания о времени молитвы.

## ✨ Ключевые Особенности

- 🌓 Адаптивный интерфейс для портретной и ландшафтной ориентации
- 🎨 Настраиваемая цветовая схема для цифровых часов
- 🕌 Функционал расчета времени намаза
- 🔇 Настраиваемые звуковые уведомления

## 🛠 Технологии

- **Язык**: Python 3.8+
- **Фреймворк**: Kivy 2.2.1
- **Платформы**: Cross-platform (Linux, Android)

## 🚀 Быстрый Старт

1. Клонируйте репозиторий
2. Установите зависимости: `pip install -r requirements.txt`
3. Запустите приложение: `python main.py`

## 📦 Установка

Чтобы создать APK с помощью Buildozer, выполните следующие действия:

1. **Установите Buildozer**:
   Следуйте инструкциям по установке из [Документации Buildozer](https://buildozer.readthedocs.io/en/latest/installation.html).

2. **Создайте APK**:
   Запустите следующую команду для сборки APK:
   ```bash
   buildozer android debug
   ```
   Собранный APK будет находиться в директории `bin/` вашего проекта.

3. **Развертывание на устройстве** (optional):
   Если у вас подключен устройство Android, вы можете развернуть APK напрямую с помощью:
   ```bash
   buildozer android deploy run
   ```

## Создание автономных исполняемых файлов и пакетов

### Linux Packaging

#### PyInstaller (Standalone Executable)
1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create executable:
```bash
pyinstaller --onefile --windowed --add-data "fonts:fonts" --add-data "icons:icons" main.py
```

#### AppImage
1. Install `appimagetool`:
```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
```

2. Create AppDir structure:
```bash
mkdir -p AdhanKivy.AppDir/usr/bin
mkdir -p AdhanKivy.AppDir/usr/share/applications
mkdir -p AdhanKivy.AppDir/usr/share/icons
```

3. Copy files and create .desktop file
```bash
cp dist/main AdhanKivy.AppDir/usr/bin/adhankivy
cp icons/iconEzanClock.svg AdhanKivy.AppDir/usr/share/icons/adhankivy.svg
```

4. Create AdhanKivy.desktop:
```
[Desktop Entry]
Name=Adhan
Exec=adhankivy
Icon=adhankivy
Type=Application
Categories=Utility;Adhan;
```

5. Generate AppImage:
```bash
./appimagetool-x86_64.AppImage AdhanKivy.AppDir
```

### Упаковка для Windows

#### PyInstaller (Executable)
1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Create executable:
```bash
pyinstaller --onefile --windowed --add-data "fonts;fonts" --add-data "icons;icons" main.py
```

#### Inno Setup (Installer)
1. Download and install [Inno Setup](https://jrsoftware.org/isdl.php)
2. Create a script (AdhanKivy_Installer.iss):
```
[Setup]
AppName=AdhanKivy
AppVersion=1.0.0
DefaultDirName={pf}\AdhanKivy
DefaultGroupName=AdhanKivy
OutputBaseFilename=AdhanKivy_Installer

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; DestName: "AdhanKivy.exe"
Source: "icons\*"; DestDir: "{app}\icons"
Source: "fonts\*"; DestDir: "{app}\fonts"

[Icons]
Name: "{group}\AdhanKivy"; Filename: "{app}\AdhanKivy.exe"
```

3. Compile the installer using Inno Setup Compiler

## License

MIT License

## Author

Oruc Qafar - Python Developer
- GitHub: [OrrStudio](https://github.com/OrrStudio)
- Email: orr888@gmail.com
