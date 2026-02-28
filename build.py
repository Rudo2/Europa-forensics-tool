import os
import subprocess
import shutil
import sys

def build_executable():
    print("Building executable...")
    
    # Create dist directory if it doesn't exist
    if not os.path.exists("dist"):
        os.makedirs("dist")
    
    # Get the Python executable path
    python_path = sys.executable
    
    # Build the executable with all necessary resources
    subprocess.run([
        "pyinstaller",
        "--name=MobileForensicTool",
        "--onefile",
        "--windowed",
        "--add-data=src/ui/assets;src/ui/assets",
        "--add-data=requirements.txt;.",
        "--hidden-import=PyQt5",
        "--hidden-import=PyQt5.QtCore",
        "--hidden-import=PyQt5.QtGui",
        "--hidden-import=PyQt5.QtWidgets",
        "--hidden-import=src.ui.assets",
        "--clean",
        "main.py"
    ])
    
    print("Build complete! Executable is in the dist folder.")
    
    # Create a copy of the source code for development
    print("Creating development copy...")
    dev_copy_dir = "MobileForensicTool_Dev"
    if os.path.exists(dev_copy_dir):
        shutil.rmtree(dev_copy_dir)
    
    # Copy all files except dist and build directories
    ignore_patterns = shutil.ignore_patterns('dist', 'build', '__pycache__', '*.pyc')
    shutil.copytree('.', dev_copy_dir, ignore=ignore_patterns)
    
    print(f"Development copy created in {dev_copy_dir}")
    
    # Verify the executable
    exe_path = os.path.join("dist", "MobileForensicTool.exe")
    if os.path.exists(exe_path):
        print(f"\nExecutable created successfully at: {exe_path}")
        print("You can now run the executable by double-clicking it.")
    else:
        print("\nError: Executable was not created successfully.")

if __name__ == "__main__":
    build_executable() 