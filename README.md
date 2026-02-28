<<<<<<< HEAD
# Europa-forensics-tool
An emerging forensics tool
=======
# Mobile Forensic Tool

A comprehensive mobile forensic tool for extracting and analyzing data from mobile devices.

## Features

- Device detection and connection via USB
- Extraction of:
  - SMS logs
  - Call logs
  - Browsing history
  - Images
  - Videos
  - Documents
- Data visualization in tabular format
- Report generation in multiple formats (PDF, Excel, TXT)

## Requirements

- Python 3.8 or higher
- ADB (Android Debug Bridge)
- USB debugging enabled on target device

## Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install ADB and add it to your system PATH
4. Enable USB debugging on your target device

## Usage

1. Run the application:
   ```
   python main.py
   ```
2. Connect your device via USB
3. Select the data you want to extract
4. View the extracted data in the application
5. Generate reports in your preferred format

## Setup script (Windows)

For convenience there is a `setup.bat` that creates a virtual environment and installs dependencies on Windows:

```
call setup.bat
```

This will create `venv` and install packages from `requirements.txt`.

## Project Structure

```
mobile_forensic_tool/
├── main.py                 # Main application entry point
├── requirements.txt        # Project dependencies
├── src/
│   ├── ui/                # UI components
│   ├── extractors/        # Data extraction modules
│   ├── database/          # Database models and operations
│   └── utils/             # Utility functions
└── reports/               # Generated reports directory
``` 
>>>>>>> 7d91a13 (Initial commit - Europa Forensics Tool)
