from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from datetime import datetime

Base = declarative_base()

class Device(Base):
    __tablename__ = 'devices'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), unique=True, nullable=False)
    model = Column(String(100))
    android_version = Column(String(20))
    serial = Column(String(50))
    connection_time = Column(DateTime, default=datetime.now)
    
    # Relationships
    sms_messages = relationship("SMSMessage", back_populates="device")
    call_logs = relationship("CallLog", back_populates="device")
    browser_history = relationship("BrowserHistory", back_populates="device")
    media_files = relationship("MediaFile", back_populates="device")
    documents = relationship("Document", back_populates="device")

class SMSMessage(Base):
    __tablename__ = 'sms_messages'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), ForeignKey('devices.device_id'))
    address = Column(String(50))
    date = Column(DateTime)
    body = Column(Text)
    
    # Relationship
    device = relationship("Device", back_populates="sms_messages")

class CallLog(Base):
    __tablename__ = 'call_logs'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), ForeignKey('devices.device_id'))
    number = Column(String(50))
    date = Column(DateTime)
    duration = Column(Integer)  # in seconds
    call_type = Column(String(20))  # incoming, outgoing, missed
    
    # Relationship
    device = relationship("Device", back_populates="call_logs")

class BrowserHistory(Base):
    __tablename__ = 'browser_history'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), ForeignKey('devices.device_id'))
    url = Column(String(500))
    title = Column(String(200))
    date = Column(DateTime)
    
    # Relationship
    device = relationship("Device", back_populates="browser_history")

class MediaFile(Base):
    __tablename__ = 'media_files'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), ForeignKey('devices.device_id'))
    file_path = Column(String(500))
    file_type = Column(String(20))  # image, video
    file_name = Column(String(200))
    file_size = Column(Integer)  # in bytes
    extraction_date = Column(DateTime, default=datetime.now)
    
    # Relationship
    device = relationship("Device", back_populates="media_files")

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), ForeignKey('devices.device_id'))
    file_path = Column(String(500))
    file_name = Column(String(200))
    file_type = Column(String(20))  # pdf, doc, docx
    file_size = Column(Integer)  # in bytes
    extraction_date = Column(DateTime, default=datetime.now)
    
    # Relationship
    device = relationship("Device", back_populates="documents") 