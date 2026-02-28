import os
import subprocess
from datetime import datetime

def check_adb_available():
    """Check if ADB is available in the system."""
    try:
        subprocess.run(['adb', 'version'], capture_output=True, check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_device_info(device_id):
    """Get detailed information about a connected device."""
    try:
        # Get device model
        model = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.model'],
            capture_output=True, text=True
        ).stdout.strip()
        
        # Get Android version
        android_version = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'getprop', 'ro.build.version.release'],
            capture_output=True, text=True
        ).stdout.strip()
        
        # Get device serial number
        serial = subprocess.run(
            ['adb', '-s', device_id, 'shell', 'getprop', 'ro.serialno'],
            capture_output=True, text=True
        ).stdout.strip()
        
        return {
            'model': model,
            'android_version': android_version,
            'serial': serial,
            'connection_time': datetime.now().isoformat()
        }
    except Exception as e:
        raise Exception(f"Failed to get device info: {str(e)}")

def ensure_directory(path):
    """Ensure a directory exists, create if it doesn't."""
    if not os.path.exists(path):
        os.makedirs(path)

def format_timestamp(timestamp):
    """Format timestamp to human-readable format."""
    try:
        dt = datetime.fromtimestamp(int(timestamp) / 1000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, TypeError):
        return str(timestamp)

def sanitize_filename(filename):
    """Sanitize filename to be safe for all operating systems."""
    # Replace invalid characters with underscore
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_file_size(path):
    """Get file size in human-readable format."""
    try:
        size_bytes = os.path.getsize(path)
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    except Exception:
        return "Unknown size" 