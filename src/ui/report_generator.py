from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QFileDialog, QMessageBox)
from PyQt5.QtCore import pyqtSlot
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
import os
from datetime import datetime
from src.utils.helpers import format_timestamp

class ReportGeneratorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.extracted_data = None
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Format selection
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Report Format:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["PDF", "Excel", "Text"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)
        
        # Generate button
        self.generate_btn = QPushButton("Generate Report")
        self.generate_btn.clicked.connect(self.generate_report)
        self.generate_btn.setEnabled(False)
        layout.addWidget(self.generate_btn)
        
        self.setLayout(layout)
        
    @pyqtSlot(dict)
    def on_data_available(self, data):
        self.extracted_data = data
        self.generate_btn.setEnabled(True)
    
    def _format_data_timestamps(self, data):
        """Format timestamps in data for readable dates."""
        if isinstance(data, list):
            return [
                {**item, 'date': format_timestamp(item.get('date', ''))} 
                if 'date' in item else item 
                for item in data
            ]
        return data
        
    def generate_report(self):
        if not self.extracted_data:
            QMessageBox.warning(self, "Warning", "No data available for report generation")
            return
            
        format_type = self.format_combo.currentText()
        
        try:
            # Get save location from user
            file_filter = ""
            if format_type == "PDF":
                file_filter = "PDF Files (*.pdf)"
                default_ext = ".pdf"
            elif format_type == "Excel":
                file_filter = "Excel Files (*.xlsx)"
                default_ext = ".xlsx"
            else:
                file_filter = "Text Files (*.txt)"
                default_ext = ".txt"
                
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Report",
                f"forensic_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}{default_ext}",
                file_filter
            )
            
            if filename:
                if format_type == "PDF":
                    self.generate_pdf_report(filename)
                elif format_type == "Excel":
                    self.generate_excel_report(filename)
                else:
                    self.generate_text_report(filename)
                    
                QMessageBox.information(self, "Success", "Report generated successfully!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")
            
    def generate_pdf_report(self, filename):
        try:
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            # Add title
            styles = getSampleStyleSheet()
            title = Paragraph("Mobile Forensic Report", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            
            if not self.extracted_data:
                raise ValueError("No data available to generate report")
            
            # Create tables for each data type
            for data_type, data in self.extracted_data.items():
                if not data:  # Skip if data is empty
                    continue

                # Add section header
                section_title = Paragraph(f"{data_type.upper()} Data", styles['Heading1'])
                elements.append(section_title)
                elements.append(Spacer(1, 12))

                table_data = []
                try:
                    if data_type == "sms":
                        table_data = [["Number", "Date", "Message"]]
                        for sms in data:
                            number = sms.get('address') or sms.get('number') or 'Unknown'
                            date_str = format_timestamp(sms.get('date', ''))
                            table_data.append([str(number), date_str, str(sms.get('body', ''))])

                    elif data_type == "calls":
                        # Helper to format duration
                        def _format_duration(sec_val):
                            try:
                                s = int(sec_val)
                            except Exception:
                                return str(sec_val)
                            if s < 60:
                                return f"{s} sec"
                            elif s < 3600:
                                m = s // 60
                                rs = s % 60
                                return f"{m}m {rs}s"
                            else:
                                h = s // 3600
                                m = (s % 3600) // 60
                                return f"{h}h {m}m"

                        table_data = [["Number", "Date", "Duration", "Type"]]
                        for call in data:
                            number = call.get('number') or call.get('address') or 'Unknown'
                            date_str = format_timestamp(call.get('date', ''))
                            duration = _format_duration(call.get('duration', 0))
                            call_type = call.get('type', 'Unknown')
                            table_data.append([str(number), date_str, duration, str(call_type)])

                    elif data_type == "browser":
                        table_data = [["Title", "URL", "Date"]]
                        for entry in data:
                            table_data.append([
                                str(entry.get('title', '')),
                                str(entry.get('url', '')),
                                format_timestamp(entry.get('date', ''))
                            ])

                    elif data_type == "media":
                        table_data = [["Type", "Path"]]
                        for img in data.get('images', []):
                            path = img.get('path') if isinstance(img, dict) else str(img)
                            table_data.append(["Image", str(path)])
                        for vid in data.get('videos', []):
                            path = vid.get('path') if isinstance(vid, dict) else str(vid)
                            table_data.append(["Video", str(path)])

                    elif data_type == "documents":
                        if isinstance(data, list) and data and isinstance(data[0], dict):
                            table_data = [["Path", "Type", "Size", "Modified"]]
                            for doc in data:
                                table_data.append([
                                    str(doc.get('path', '')),
                                    str(doc.get('type', '')),
                                    str(doc.get('size', '')),
                                    format_timestamp(doc.get('modified', ''))
                                ])
                        else:
                            table_data = [["Document Path"]]
                            for doc in data:
                                table_data.append([str(doc)])

                    if len(table_data) > 1:
                        table = Table(table_data)
                        table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), 14),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), 12),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ]))
                        elements.append(table)
                        elements.append(Spacer(1, 20))
                except Exception as e:
                    print(f"Error processing {data_type}: {str(e)}")
                    continue

            # Add timestamp at the bottom
            timestamp = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
            elements.append(timestamp)

            # Build the document
            doc.build(elements)

        except Exception as e:
            raise Exception(f"Failed to generate PDF report: {str(e)}")

    def generate_excel_report(self, filename):
        # Write Excel sheets with formatted dates and clear columns
        def _format_duration(sec_val):
            try:
                s = int(sec_val)
            except Exception:
                return str(sec_val)
            if s < 60:
                return f"{s} sec"
            elif s < 3600:
                m = s // 60
                rs = s % 60
                return f"{m}m {rs}s"
            else:
                h = s // 3600
                m = (s % 3600) // 60
                return f"{h}h {m}m"

        with pd.ExcelWriter(filename) as writer:
            for data_type, data in self.extracted_data.items():
                if data_type == "sms":
                    rows = []
                    for sms in data:
                        rows.append({
                            'Number': sms.get('address') or sms.get('number') or 'Unknown',
                            'Date': format_timestamp(sms.get('date', '')),
                            'Message': sms.get('body', '')
                        })
                    pd.DataFrame(rows).to_excel(writer, sheet_name='SMS Logs', index=False)

                elif data_type == "calls":
                    rows = []
                    for call in data:
                        rows.append({
                            'Number': call.get('number') or call.get('address') or 'Unknown',
                            'Date': format_timestamp(call.get('date', '')),
                            'Duration': _format_duration(call.get('duration', 0)),
                            'Type': call.get('type', 'Unknown')
                        })
                    pd.DataFrame(rows).to_excel(writer, sheet_name='Call Logs', index=False)

                elif data_type == "browser":
                    rows = []
                    for entry in data:
                        rows.append({
                            'Title': entry.get('title', ''),
                            'URL': entry.get('url', ''),
                            'Date': format_timestamp(entry.get('date', ''))
                        })
                    pd.DataFrame(rows).to_excel(writer, sheet_name='Browser History', index=False)

                elif data_type == "media":
                    imgs = []
                    for img in data.get('images', []):
                        path = img.get('path') if isinstance(img, dict) else str(img)
                        imgs.append({'Path': path})
                    vids = []
                    for vid in data.get('videos', []):
                        path = vid.get('path') if isinstance(vid, dict) else str(vid)
                        vids.append({'Path': path})
                    if imgs:
                        pd.DataFrame(imgs).to_excel(writer, sheet_name='Images', index=False)
                    if vids:
                        pd.DataFrame(vids).to_excel(writer, sheet_name='Videos', index=False)

                elif data_type == "documents":
                    # Documents may be list of dicts or paths
                    if isinstance(data, list) and data and isinstance(data[0], dict):
                        rows = []
                        for doc in data:
                            rows.append({
                                'Path': doc.get('path', ''),
                                'Type': doc.get('type', ''),
                                'Size': doc.get('size', ''),
                                'Modified': format_timestamp(doc.get('modified', ''))
                            })
                        pd.DataFrame(rows).to_excel(writer, sheet_name='Documents', index=False)
                    else:
                        pd.DataFrame([{'Path': str(p)} for p in data]).to_excel(writer, sheet_name='Documents', index=False)

    def generate_text_report(self, filename):
        def _format_duration(sec_val):
            try:
                s = int(sec_val)
            except Exception:
                return str(sec_val)
            if s < 60:
                return f"{s} sec"
            elif s < 3600:
                m = s // 60
                rs = s % 60
                return f"{m}m {rs}s"
            else:
                h = s // 3600
                m = (s % 3600) // 60
                return f"{h}h {m}m"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Mobile Forensic Report\n")
            f.write("=" * 50 + "\n\n")

            for data_type, data in self.extracted_data.items():
                f.write(f"\n{data_type.upper()} DATA\n")
                f.write("-" * 30 + "\n")

                if data_type == "sms":
                    for sms in data:
                        number = sms.get('address') or sms.get('number') or 'Unknown'
                        f.write(f"From: {number}\n")
                        f.write(f"Date: {format_timestamp(sms.get('date', ''))}\n")
                        f.write(f"Message: {sms.get('body', '')}\n")
                        f.write("-" * 20 + "\n")

                elif data_type == "calls":
                    for call in data:
                        number = call.get('number') or call.get('address') or 'Unknown'
                        f.write(f"Number: {number}\n")
                        f.write(f"Date: {format_timestamp(call.get('date', ''))}\n")
                        f.write(f"Duration: {_format_duration(call.get('duration', 0))}\n")
                        f.write(f"Type: {call.get('type', 'Unknown')}\n")
                        f.write("-" * 20 + "\n")

                elif data_type == "browser":
                    for entry in data:
                        f.write(f"URL: {entry.get('url', '')}\n")
                        f.write(f"Title: {entry.get('title', '')}\n")
                        f.write(f"Date: {format_timestamp(entry.get('date', ''))}\n")
                        f.write("-" * 20 + "\n")

                elif data_type == "media":
                    f.write("\nImages:\n")
                    for img in data.get('images', []):
                        path = img.get('path') if isinstance(img, dict) else str(img)
                        f.write(f"{path}\n")
                    f.write("\nVideos:\n")
                    for vid in data.get('videos', []):
                        path = vid.get('path') if isinstance(vid, dict) else str(vid)
                        f.write(f"{path}\n")

                elif data_type == "documents":
                    if isinstance(data, list) and data and isinstance(data[0], dict):
                        for doc in data:
                            f.write(f"Path: {doc.get('path', '')}\n")
                            f.write(f"Type: {doc.get('type', '')}\n")
                            f.write(f"Size: {doc.get('size', '')}\n")
                            f.write(f"Modified: {format_timestamp(doc.get('modified', ''))}\n")
                            f.write("-" * 20 + "\n")
                    else:
                        for doc in data:
                            f.write(f"{doc}\n")

                f.write("\n")

