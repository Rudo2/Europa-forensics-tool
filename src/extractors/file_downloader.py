import os
import subprocess
from PyQt5.QtCore import QObject, pyqtSignal
import shutil
from datetime import datetime

class FileDownloader(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, device_id, output_dir="downloads"):
        super().__init__()
        self.device_id = device_id
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
    def download_file(self, remote_path, file_type):
        """Download a file from the device to the local machine."""
        try:
            # Create a subdirectory for the file type
            type_dir = os.path.join(self.output_dir, file_type)
            if not os.path.exists(type_dir):
                os.makedirs(type_dir)
                
            # Generate a unique filename
            filename = os.path.basename(remote_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            local_path = os.path.join(type_dir, f"{timestamp}_{filename}")
            
            # Use adb pull to download the file
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'pull', remote_path, local_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.finished.emit(local_path)
                return local_path
            else:
                raise Exception(f"Failed to download file: {result.stderr}")
                
        except Exception as e:
            self.error.emit(str(e))
            return None
            
    def download_files(self, file_list, file_type):
        """Download multiple files from the device."""
        total_files = len(file_list)
        downloaded_files = []
        
        for i, file_path in enumerate(file_list):
            try:
                local_path = self.download_file(file_path, file_type)
                if local_path:
                    downloaded_files.append(local_path)
                    
                # Update progress
                progress = int((i + 1) / total_files * 100)
                self.progress.emit(progress)
                
            except Exception as e:
                self.error.emit(f"Failed to download {file_path}: {str(e)}")
                
        return downloaded_files
        
    def download_media_files(self, media_data):
        """Download media files (images and videos) from the device."""
        all_files = []
        
        # Download images
        if 'images' in media_data and media_data['images']:
            image_files = self.download_files(media_data['images'], 'images')
            all_files.extend(image_files)
            
        # Download videos
        if 'videos' in media_data and media_data['videos']:
            video_files = self.download_files(media_data['videos'], 'videos')
            all_files.extend(video_files)
            
        return all_files
        
    def download_documents(self, documents):
        """Download documents from the device."""
        return self.download_files(documents, 'documents')
        
    def get_file_size(self, file_path):
        """Get the size of a file on the device."""
        try:
            result = subprocess.run(
                ['adb', '-s', self.device_id, 'shell', 'stat', '-c', '%s', file_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return int(result.stdout.strip())
            else:
                return 0
                
        except Exception:
            return 0 