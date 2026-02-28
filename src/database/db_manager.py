from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from datetime import datetime
from .models import Base, Device, SMSMessage, CallLog, BrowserHistory, MediaFile, Document

class DatabaseManager:
    def __init__(self, db_path="forensic_data.db"):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def add_device(self, device_id, model, android_version, serial):
        """Add a new device to the database."""
        try:
            device = Device(
                device_id=device_id,
                model=model,
                android_version=android_version,
                serial=serial
            )
            self.session.add(device)
            self.session.commit()
            return device
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to add device: {str(e)}")
            
    def add_sms_messages(self, device_id, messages):
        """Add SMS messages to the database."""
        try:
            for msg in messages:
                sms = SMSMessage(
                    device_id=device_id,
                    address=msg['address'],
                    date=datetime.fromtimestamp(int(msg['date']) / 1000),
                    body=msg['body']
                )
                self.session.add(sms)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to add SMS messages: {str(e)}")
            
    def add_call_logs(self, device_id, calls):
        """Add call logs to the database."""
        try:
            for call in calls:
                call_log = CallLog(
                    device_id=device_id,
                    number=call['number'],
                    date=datetime.fromtimestamp(int(call['date']) / 1000),
                    duration=call['duration'],
                    call_type=call['type']
                )
                self.session.add(call_log)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to add call logs: {str(e)}")
            
    def add_browser_history(self, device_id, history):
        """Add browser history to the database."""
        try:
            for entry in history:
                browser_entry = BrowserHistory(
                    device_id=device_id,
                    url=entry['url'],
                    title=entry['title'],
                    date=datetime.fromtimestamp(int(entry['date']) / 1000) if entry['date'] else None
                )
                self.session.add(browser_entry)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to add browser history: {str(e)}")
            
    def add_media_files(self, device_id, media_data):
        """Add media files to the database."""
        try:
            # Add images
            for img_path in media_data['images']:
                media_file = MediaFile(
                    device_id=device_id,
                    file_path=img_path,
                    file_type='image',
                    file_name=os.path.basename(img_path),
                    file_size=0  # Size will be updated when file is downloaded
                )
                self.session.add(media_file)
                
            # Add videos
            for vid_path in media_data['videos']:
                media_file = MediaFile(
                    device_id=device_id,
                    file_path=vid_path,
                    file_type='video',
                    file_name=os.path.basename(vid_path),
                    file_size=0  # Size will be updated when file is downloaded
                )
                self.session.add(media_file)
                
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to add media files: {str(e)}")
            
    def add_documents(self, device_id, documents):
        """Add documents to the database."""
        try:
            for doc_path in documents:
                doc = Document(
                    device_id=device_id,
                    file_path=doc_path,
                    file_name=os.path.basename(doc_path),
                    file_type=os.path.splitext(doc_path)[1][1:],
                    file_size=0  # Size will be updated when file is downloaded
                )
                self.session.add(doc)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to add documents: {str(e)}")
            
    def get_device(self, device_id):
        """Get device information from the database."""
        return self.session.query(Device).filter_by(device_id=device_id).first()
        
    def get_sms_messages(self, device_id):
        """Get SMS messages for a device."""
        return self.session.query(SMSMessage).filter_by(device_id=device_id).all()
        
    def get_call_logs(self, device_id):
        """Get call logs for a device."""
        return self.session.query(CallLog).filter_by(device_id=device_id).all()
        
    def get_browser_history(self, device_id):
        """Get browser history for a device."""
        return self.session.query(BrowserHistory).filter_by(device_id=device_id).all()
        
    def get_media_files(self, device_id):
        """Get media files for a device."""
        return self.session.query(MediaFile).filter_by(device_id=device_id).all()
        
    def get_documents(self, device_id):
        """Get documents for a device."""
        return self.session.query(Document).filter_by(device_id=device_id).all()
        
    def update_file_size(self, file_path, size):
        """Update the file size for a media file or document."""
        try:
            # Check if it's a media file
            media_file = self.session.query(MediaFile).filter_by(file_path=file_path).first()
            if media_file:
                media_file.file_size = size
                self.session.commit()
                return
                
            # Check if it's a document
            document = self.session.query(Document).filter_by(file_path=file_path).first()
            if document:
                document.file_size = size
                self.session.commit()
                return
                
        except SQLAlchemyError as e:
            self.session.rollback()
            raise Exception(f"Failed to update file size: {str(e)}")
            
    def close(self):
        """Close the database session."""
        self.session.close() 