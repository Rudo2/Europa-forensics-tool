import os
import sys
from datetime import datetime

# Ensure project src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt5.QtWidgets import QApplication
from src.ui.report_generator import ReportGeneratorWidget

out_dir = os.path.join(os.path.dirname(__file__), '..', 'output', 'test_reports')
os.makedirs(out_dir, exist_ok=True)

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
text_path = os.path.join(out_dir, f'test_report_{timestamp}.txt')
xlsx_path = os.path.join(out_dir, f'test_report_{timestamp}.xlsx')

now_ms = lambda: str(int(datetime.now().timestamp() * 1000))

sample = {
    'sms': [
        {'address': '+1234567890', 'date': now_ms(), 'body': 'Test message 1'},
        {'address': '+1987654321', 'date': now_ms(), 'body': 'Another test'}
    ],
    'calls': [
        {'number': '+1234567890', 'date': now_ms(), 'duration': '65', 'type': 'Incoming'},
        {'number': '+1987654321', 'date': now_ms(), 'duration': '3665', 'type': 'Outgoing'},
        # Entry using 'address' instead of 'number' to test fallback handling
        {'address': '+1112223333', 'date': now_ms(), 'duration': '30', 'type': 'Outgoing'}
    ],
    'browser': [
        {'title': 'Example', 'url': 'http://example.com', 'date': now_ms()}
    ],
    'media': {
        'images': [{'path': '/path/to/image.jpg'}],
        'videos': [{'path': '/path/to/video.mp4'}]
    },
    'documents': [
        {'path': '/path/to/doc.pdf', 'type': 'pdf', 'size': '12345', 'modified': now_ms()}
    ]
}

app = QApplication([])
rg = ReportGeneratorWidget()
rg.extracted_data = sample

print('Generating text report ->', text_path)
rg.generate_text_report(text_path)
print('Generating excel report ->', xlsx_path)
rg.generate_excel_report(xlsx_path)

print('\nDone. Created files:')
print(text_path)
print(xlsx_path)
app.quit()
