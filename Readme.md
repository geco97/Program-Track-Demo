# Program Tracker README

## Introduction
This program is an **Active Program Tracker**, designed to monitor and categorize the applications running on a Windows system. It provides valuable insights into software usage, helps improve productivity, and offers focus mode to minimize distractions.

## Features
- **Real-time program tracking**: Monitors the currently active application.
- **Categorization of programs**: Groups applications into categories such as Work, Social Media, Entertainment, etc.
- **Focus Mode**: Blocks specific applications to improve focus.
- **Alerts for excessive usage**: Notifies when an application has been used beyond a defined threshold.
- **Data visualization**: Displays usage statistics in bar charts and pie charts.
- **Weekly summary report**: Provides an overview of app usage per week.
- **Productivity Score**: Calculates the ratio of work-related activities to total screen time.
- **Updated Byte Version**: A lightweight version with refined features.

## Libraries Used
### **1. os**
- Used for system-level operations, including sending notifications.

### **2. time**
- Provides timestamping and tracking elapsed time for each application.

### **3. pygame**
- Used for creating a graphical user interface (GUI) to display active program tracking results.

### **4. json**
- Handles data storage and retrieval for tracking historical program usage.

### **5. psutil**
- Retrieves process information such as application names and execution times.

### **6. win32gui & win32process**
- Extracts the currently active window title and process information.

### **7. collections.defaultdict**
- Ensures easy management of application tracking data.

## How the Code Works
### **1. Program Tracking**
- The `get_active_window()` function extracts the currently active program’s name and title.
- `ProcessTracker` class logs the duration of each application's usage.
- If the application changes, the system logs the previous app’s duration and switches to the new one.

### **2. Focus Mode**
- The system tracks program usage time and blocks distractions such as YouTube, Netflix, Twitter, and Facebook when enabled.
- Press **F** to enable or disable focus mode dynamically.

### **3. Data Storage & Visualization**
- The `history.json` file is used to store tracked data persistently.
- The updated Byte Version improves efficiency by simplifying tracking mechanisms.

### **4. GUI with Pygame**
- A simple interface displays the active program and usage statistics.
- Keyboard shortcuts:
  - **R**: Reset history
  - **Q**: Quit the application
  - **F**: Enable/disable Focus Mode

## Updated Byte Version - Buy for $20
The new Byte Version enhances efficiency, improves tracking accuracy, and refines the user interface. Get access to the full source code for **$20**. Contact us for purchase details at **geco97@gmail.com** .

## Benefits of This Application
- **Improves productivity** by tracking and limiting time spent on distractions.
- **Provides insights** into daily application usage.
- **Encourages better focus** through alerts and focus mode.
- **Helps users balance** work and leisure time.

## Installation and Usage
### **1. Install Dependencies**
Ensure Python and the required libraries are installed:
```sh
pip install pygame psutil pywin32
```
### **2. Run the Application**
```sh
python main.py
```
### **3. Control the Application**
- Use keyboard shortcuts for different functionalities.
- Review productivity reports and alerts for self-improvement.

## Command List
- **R** - Reset history
- **Q** - Quit application
- **F** - Enable/disable focus mode

---
This program is a powerful tool for managing time effectively, staying productive, and maintaining a balance between work and leisure.

