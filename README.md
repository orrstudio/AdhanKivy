 # AdhanKivy

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

Adaptive digital clock with a modern minimalist design, developed using the Kivy Framework.

## Features

- Automatic interface adaptation for portrait and landscape orientation
- Smooth animations when changing orientation and updating time
- Customizable color scheme with 9 preset colors
- Minimalist design with black background
- Optimized performance using hysteresis for orientation detection

## Applications and Capabilities

AdhanKivy is not just a clock, it's a multifunctional time display application that can be used in various scenarios:

### Home Use
- As a desktop clock on your computer or laptop
- As a clock for presentations or online meetings
- As a fullscreen clock for home theater

### Professional Use
- In TV studios for current time display
- On information displays in offices and public spaces
- In educational institutions for time control

### Advantages
- Adaptive design allows using the application on screens of any orientation
- High readability thanks to contrasting colors and minimalist design
- Customizable colors allow adapting the clock to any interior or corporate style

### Customization
The application is easily customizable:
- Choice of color schemes
- Adaptation to portrait or landscape mode

## Technologies

- Python 3
- Kivy 2.2.1
- Modular architecture with UI component separation

## Project Structure
```
AdhanKivy/
├── main.py                 # Main application file
├── ui/                     # UI components
│   ├── base_clock.py       # Base clock class
│   ├── landscape_clock.py  # Landscape orientation
│   ├── portrait_clock.py   # Portrait orientation
│   └── settings_window.py  # Settings window
├── data/                   # Additional data
├── fonts/                  # Fonts
└── requirements.txt        # Dependencies
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/orrstudio/AdhanKivy.git
cd AdhanKivy
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # for Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python main.py
```

## System Requirements

- Python 3.8 or higher
- Kivy 2.2.1
- Minimum 512MB RAM
- Any operating system supporting Python and Kivy (Windows, Linux, macOS)

## Building APK for Android with Buildozer

To build an APK using Buildozer, follow these steps:

1. **Install Buildozer**:
   Follow the installation instructions from the [Buildozer Documentation](https://buildozer.readthedocs.io/en/latest/installation.html).

2. **Build the APK**:
   Run the following command to build the APK:
   ```bash
   buildozer android debug
   ```
   The built APK will be located in the `bin/` directory of your project.

3. **Deploy to a device** (optional):
   If you have an Android device connected, you can deploy the APK directly using:
   ```bash
   buildozer android deploy run
   ```

## Building Standalone Executables and Packages

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

### Windows Packaging

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
