from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QTableWidget, QTableWidgetItem, QMessageBox)
from PyQt5.QtCore import pyqtSignal, QTimer
import subprocess
import re

class DeviceManagerWidget(QWidget):
    # Signal emitted when a device is connected (passes device_id)
    device_connected = pyqtSignal(str)
    # Signal emitted when a device is disconnected
    device_disconnected = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.devices = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_devices)
        # Start a polling timer that re-runs `refresh_devices()` every 2000 ms
        # This uses ADB in the background to keep the device list up-to-date.
        self.timer.start(2000)  # Refresh every 2 seconds
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        self.status_label = QLabel("Status: Waiting for devices...")
        header.addWidget(self.status_label)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        # When pressed, `handle_refresh` will first disconnect any currently
        # connected device and then refresh the ADB device list for a fresh start.
        refresh_btn.clicked.connect(self.handle_refresh)
        header.addWidget(refresh_btn)
        
        layout.addLayout(header)
        
        # Devices table
        self.devices_table = QTableWidget()
        self.devices_table.setColumnCount(4)
        self.devices_table.setHorizontalHeaderLabels(["Device ID", "Model", "Status", "Actions"])
        layout.addWidget(self.devices_table)
        
        self.setLayout(layout)
        
    def refresh_devices(self):
        """Query ADB for connected devices and update the UI table.

        Steps:
        - Run `adb devices -l` to get current devices
        - Parse output into `current_devices` dict
        - Update the table with Connect/Disconnect buttons
        - If a previously connected device disappeared, emit disconnect
        """
        try:
            # Get list of devices using adb
            result = subprocess.run(['adb', 'devices', '-l'], 
                                 capture_output=True, text=True)
            
            # Parse the output
            lines = result.stdout.strip().split('\n')[1:]  # Skip first line
            current_devices = {}
            
            # Each non-empty line represents a device; parse device id, status and model
            for line in lines:
                if line.strip():
                    parts = line.split()
                    device_id = parts[0]
                    status = parts[-1]
                    # Try to read a `model:XYZ` token from adb output; fallback to 'Unknown'
                    model = next((p.split(':')[1] for p in parts[1:] if 'model:' in p), 'Unknown')
                    current_devices[device_id] = {'model': model, 'status': status}
            
            # Check if previously connected device is no longer available
            if hasattr(self, 'connected_device_id') and self.connected_device_id:
                if self.connected_device_id not in current_devices:
                    self.disconnect_device(self.connected_device_id, emit_signal=True)
                    self.connected_device_id = None
            
            # Update table
            self.devices_table.setRowCount(len(current_devices))
            for row, (device_id, info) in enumerate(current_devices.items()):
                self.devices_table.setItem(row, 0, QTableWidgetItem(device_id))
                self.devices_table.setItem(row, 1, QTableWidgetItem(info['model']))
                
                # Check if this is the connected device
                # If this device is marked as connected in the UI, show Disconnect
                if hasattr(self, 'connected_device_id') and self.connected_device_id == device_id:
                    self.devices_table.setItem(row, 2, QTableWidgetItem("Connected"))
                    # Add disconnect button
                    disconnect_btn = QPushButton("Disconnect")
                    disconnect_btn.clicked.connect(lambda checked, d=device_id: self.disconnect_device(d, emit_signal=True))
                    self.devices_table.setCellWidget(row, 3, disconnect_btn)
                else:
                    self.devices_table.setItem(row, 2, QTableWidgetItem(info['status']))
                    # Add connect button
                    connect_btn = QPushButton("Connect")
                    connect_btn.clicked.connect(lambda checked, d=device_id: self.connect_device(d))
                    self.devices_table.setCellWidget(row, 3, connect_btn)
            
            # Update status
            if current_devices:
                if hasattr(self, 'connected_device_id') and self.connected_device_id:
                    connected_device = current_devices.get(self.connected_device_id, {})
                    model = connected_device.get('model', 'Unknown')
                    self.status_label.setText(f"Status: Connected to {model} ({self.connected_device_id})")
                else:
                    self.status_label.setText(f"Status: Found {len(current_devices)} device(s)")
            else:
                self.status_label.setText("Status: No devices found")
                # Clear connected device if no devices are found
                if hasattr(self, 'connected_device_id') and self.connected_device_id:
                    self.disconnect_device(self.connected_device_id, emit_signal=True)
                    self.connected_device_id = None
                
            self.devices = current_devices
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to refresh devices: {str(e)}")

    def handle_refresh(self):
        """Handler for Refresh button: disconnect any connected device, then refresh list"""
        try:
            if hasattr(self, 'connected_device_id') and self.connected_device_id:
                # Disconnect currently connected device for a fresh start
                self.disconnect_device(self.connected_device_id, emit_signal=True)
                self.connected_device_id = None
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to disconnect device before refresh: {str(e)}")

        # Now refresh the device list
        self.refresh_devices()
            
    def connect_device(self, device_id):
        """Attempt to mark a device as connected.

        Checks device state via `adb -s <id> get-state` and, if responsive,
        updates UI and emits `device_connected` signal.
        """
        try:
            # Check if device is authorized
            result = subprocess.run(['adb', '-s', device_id, 'get-state'], 
                                 capture_output=True, text=True)
            
            if 'device' in result.stdout:
                # Update the status in the table first
                for row in range(self.devices_table.rowCount()):
                    if self.devices_table.item(row, 0).text() == device_id:
                        # Update status to "Connected"
                        self.devices_table.setItem(row, 2, QTableWidgetItem("Connected"))
                        
                        # Change the connect button to a disconnect button
                        disconnect_btn = QPushButton("Disconnect")
                        disconnect_btn.clicked.connect(lambda checked, d=device_id: self.disconnect_device(d, emit_signal=True))
                        self.devices_table.setCellWidget(row, 3, disconnect_btn)
                        break
                
                # Store the connected device ID
                self.connected_device_id = device_id
                
                # Update status label with device info
                device_info = self.devices.get(device_id, {})
                model = device_info.get('model', 'Unknown')
                self.status_label.setText(f"Status: Connected to {model} ({device_id})")
                
                # Emit the signal after updating the UI
                self.device_connected.emit(device_id)
                
                QMessageBox.information(self, "Success", f"Connected to device {device_id}")
            else:
                QMessageBox.warning(self, "Error", "Device not authorized. Please accept the USB debugging prompt on your device.")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to connect to device: {str(e)}")

    def disconnect_device(self, device_id, emit_signal=True):
        """Disconnect the device in the UI and emit `device_disconnected` if requested."""
        try:
            # Update the status in the table first
            for row in range(self.devices_table.rowCount()):
                if self.devices_table.item(row, 0).text() == device_id:
                    # Update status back to device state
                    device_status = self.devices.get(device_id, {}).get('status', 'device')
                    self.devices_table.setItem(row, 2, QTableWidgetItem(device_status))
                    
                    # Change the disconnect button back to a connect button
                    connect_btn = QPushButton("Connect")
                    connect_btn.clicked.connect(lambda checked, d=device_id: self.connect_device(d))
                    self.devices_table.setCellWidget(row, 3, connect_btn)
                    break
            
            # Clear the connected device ID
            self.connected_device_id = None
            
            # Update status label
            self.status_label.setText("Status: Waiting for devices...")
            
            # Emit the disconnected signal if requested
            if emit_signal:
                self.device_disconnected.emit()
                QMessageBox.information(self, "Success", f"Disconnected from device {device_id}")
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to disconnect from device: {str(e)}") 