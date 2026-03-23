# 🚀 Camera System Launchers

Multiple ways to start the Camera System application.

## 📋 Available Launchers

### 1. **run.bat** (Simple & Fast)
- **Purpose**: Quick start with basic setup
- **Usage**: Double-click `run.bat`
- **Features**:
  - Automatic dependency installation
  - Basic error handling
  - Shows login credentials
  - Simple and straightforward

### 2. **start.bat** (Advanced)
- **Purpose**: Advanced launcher with multiple options
- **Usage**: Double-click `start.bat`
- **Features**:
  - Menu-driven interface
  - Normal/Debug mode options
  - Dependency installation
  - Database status check
  - Better error handling

### 3. **launcher.py** (Python Launcher)
- **Purpose**: Full-featured Python launcher
- **Usage**: Run `python launcher.py`
- **Features**:
  - Interactive menu
  - System status checking
  - Browser auto-open
  - Debug mode toggle
  - Dependency management
  - Colorful interface

## 🎯 Recommended Usage

### For Quick Start:
```bash
# Double-click this file
run.bat
```

### For Advanced Options:
```bash
# Double-click this file for menu
start.bat
```

### For Full Control:
```bash
# Run in terminal
python launcher.py
```

## 📱 Access Information

- **URL**: http://localhost:5000
- **Admin**: admin / admin123
- **Technician**: fn1 / tech123

## 🔧 Troubleshooting

### If application doesn't start:
1. Run `start.bat` and choose option 3 (Install dependencies)
2. Check Python installation: `python --version`
3. Verify requirements.txt exists

### If database errors occur:
1. Run `start.bat` and choose option 4 (Check database)
2. Ensure `camera_system.db` file exists
3. Check file permissions

### If port 5000 is busy:
1. Close other applications using port 5000
2. Or modify port in `app.py`

## 📝 Notes

- All launchers automatically set environment variables
- Debug mode shows detailed error messages
- Database is automatically created on first run
- All launchers support Arabic/English interface

## 🚀 Quick Start Commands

```cmd
# Option 1: Simple start
run.bat

# Option 2: Advanced menu
start.bat

# Option 3: Python launcher
python launcher.py

# Option 4: Direct Python
python app.py
```

Choose the launcher that best fits your needs! 🎉
