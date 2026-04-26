# EasyClass
✨ A lightweight, user-friendly class schedule application built with Python and Tkinter

## Overview
EasyClass is a simple yet powerful desktop timetable tool designed for students. It offers a clean graphical interface, local data storage, iCalendar export, and can be compiled into a standalone executable for cross-platform use.

## Features
- 📅 Clean and intuitive weekly timetable interface
- 🎨 Fully customizable course colors and detailed information
- 💾 Stable local data persistence
- 📤 Export schedules to standard iCalendar (.ics) format
- 🖥️ Easy-to-use GUI with zero learning cost
- 🚀 Compilable into a standalone executable via Nuitka
- 📝 Support add, edit, and delete operations for all classes
- 🎯 Stable, lightweight, and no internet required

## Tech Stack
- Development Language: Python 3
- GUI Framework: Tkinter (built-in)
- Image Processing: Pillow (PIL)
- Calendar Export: icalendar
- Compiler: Nuitka

## Installation Steps
### 1. Clone the repository
git clone https://github.com/your-username/EasyClass.git
cd EasyClass

### 2. Install required dependencies
pip install -r requirements.txt

## Run from Source Code
python main.py

## Compile to Standalone Executable
### For Windows
nuitka --onefile --windows-icon-from-ico=app.ico --disable-console --output-filename=EasyClass main.py

### For macOS / Linux
nuitka --onefile --disable-console --output-filename=EasyClass main.py

## How to Use
1. Add class: click any timetable slot to fill in course details
2. Edit class: double-click an existing class to modify information
3. Delete class: select and remove any class with one click
4. Export schedule: export to .ics and import to calendar apps
5. Customize: set different colors for each course

## Project Structure
EasyClass/
├── main.py                 # Main application entry
├── core/                   # Core schedule logic
├── ui/                     # Tkinter interface components
├── utils/                  # Export and helper functions
├── assets/                 # Icons, images, resources
└── requirements.txt        # Dependency list

## requirements.txt
Pillow>=10.0.0
icalendar>=5.0.0

## Contributing
1. Fork this repository
2. Create a new feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License
This project is released under the MIT License.

## Feedback & Support
If you encounter bugs or have feature requests, please create an Issue in the repository.
"
