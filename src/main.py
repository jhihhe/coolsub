# -*- coding: utf-8 -*-
# Copyright (c) 2026 jhihhe. All rights reserved.
# Project: coolsub

import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QListWidget, QListWidgetItem, 
                             QPushButton, QFileDialog, QMessageBox, QFrame, QSplitter)
from PySide6.QtCore import Qt, QMimeData, QSize
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QFont, QColor, QPalette, QPainter, QPainterPath, QPen

from src.engine import process_subtitle
from src.styles import STYLES

class PreviewWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.style_config = STYLES["immersive_serif"]
        self.setStyleSheet("background-color: #1a1a1a; border-radius: 10px; border: 1px solid #333;")
        
    def set_style(self, style_key):
        self.style_config = STYLES.get(style_key, STYLES["immersive_serif"])
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        text = "这就是高级沉浸式字幕预览\nThis is a premium subtitle preview."
        
        # Setup font
        font = QFont(self.style_config.font_name.split(",")[0].strip())
        font.setPointSizeF(20) # Fixed size for preview
        font.setBold(self.style_config.bold)
        painter.setFont(font)

        # Calculate position
        rect = self.contentsRect()
        
        # Create text path for outline
        path = QPainterPath()
        # Center the text
        fm = painter.fontMetrics()
        lines = text.split("\n")
        total_h = len(lines) * fm.height()
        curr_y = (rect.height() - total_h) / 2 + fm.ascent()
        
        for line in lines:
            line_w = fm.horizontalAdvance(line)
            curr_x = (rect.width() - line_w) / 2
            path.addText(curr_x, curr_y, font, line)
            curr_y += fm.height()

        # Draw shadow if needed
        if self.style_config.shadow_width > 0:
            painter.save()
            painter.translate(self.style_config.shadow_width, self.style_config.shadow_width)
            painter.fillPath(path, QColor(0, 0, 0, 150))
            painter.restore()

        # Draw outline
        if self.style_config.outline_width > 0:
            pen = QPen(self.style_config.get_qcolor(self.style_config.outline_color), self.style_config.outline_width * 2)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.strokePath(path, pen)

        # Draw fill
        painter.fillPath(path, self.style_config.get_qcolor(self.style_config.primary_color))

class DropArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setMinimumHeight(200)
        self.setStyleSheet("""
            DropArea {
                border: 2px dashed #666;
                border-radius: 15px;
                background-color: #f8f9fa;
            }
            DropArea:hover {
                background-color: #e9ecef;
                border-color: #007aff;
            }
        """)
        
        layout = QVBoxLayout(self)
        self.label = QLabel("将字幕文件拖放到此处\n(支持 .srt, .ass, .vtt, .ssa)")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: #666; font-size: 16px;")
        layout.addWidget(self.label)
        
        self.files = []

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet("""
                DropArea {
                    border: 2px dashed #007aff;
                    border-radius: 15px;
                    background-color: #e3f2fd;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            DropArea {
                border: 2px dashed #666;
                border-radius: 15px;
                background-color: #f8f9fa;
            }
        """)

    def dropEvent(self, event: QDropEvent):
        self.files = [url.toLocalFile() for url in event.mimeData().urls()]
        if self.files:
            file_names = [os.path.basename(f) for f in self.files]
            self.label.setText(f"已就绪: {', '.join(file_names)}")
        self.dragLeaveEvent(None)
        event.accept()

class CoolSubApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("coolsub - 高级字幕风格转换器")
        self.setMinimumSize(600, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QVBoxLayout()
        header = QLabel("coolsub")
        header.setStyleSheet("font-size: 24px; font-weight: bold; color: #1d1d1f;")
        subheader = QLabel("拖放文件并选择高级视觉风格")
        subheader.setStyleSheet("font-size: 13px; color: #86868b;")
        header_layout.addWidget(header)
        header_layout.addWidget(subheader)
        main_layout.addLayout(header_layout)

        content_layout = QHBoxLayout()
        
        self.drop_area = DropArea()
        content_layout.addWidget(self.drop_area, 2)

        right_layout = QVBoxLayout()
        
        style_label = QLabel("视觉风格选择")
        style_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #1d1d1f;")
        right_layout.addWidget(style_label)

        self.style_list = QListWidget()
        self.style_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #d2d2d7;
                border-radius: 10px;
                background: white;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f5f5f7;
            }
            QListWidget::item:selected {
                background-color: #0071e3;
                color: white;
            }
        """)
        
        for key, style in STYLES.items():
            item = QListWidgetItem()
            item.setText(f"{style.name}")
            item.setToolTip(style.description)
            item.setData(Qt.UserRole, key)
            self.style_list.addItem(item)
        
        self.style_list.currentRowChanged.connect(self.update_preview)
        right_layout.addWidget(self.style_list)

        preview_label = QLabel("实时效果预览")
        preview_label.setStyleSheet("font-size: 13px; font-weight: 600; color: #1d1d1f; margin-top: 10px;")
        right_layout.addWidget(preview_label)
        
        self.preview_area = PreviewWidget()
        right_layout.addWidget(self.preview_area)
        
        content_layout.addLayout(right_layout, 3)
        main_layout.addLayout(content_layout)

        bottom_layout = QHBoxLayout()
        
        self.status_label = QLabel("就绪")
        self.status_label.setStyleSheet("color: #86868b; font-size: 12px;")
        bottom_layout.addWidget(self.status_label)
        
        bottom_layout.addStretch()

        self.btn_process = QPushButton("立即生成高级字幕")
        self.btn_process.setMinimumSize(180, 40)
        self.btn_process.setCursor(Qt.PointingHandCursor)
        self.btn_process.setStyleSheet("""
            QPushButton {
                background-color: #0071e3;
                color: white;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 600;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #0077ed;
            }
            QPushButton:pressed {
                background-color: #006edb;
            }
            QPushButton:disabled {
                background-color: #d2d2d7;
                color: #86868b;
            }
        """)
        self.btn_process.clicked.connect(self.run_conversion)
        bottom_layout.addWidget(self.btn_process)
        
        main_layout.addLayout(bottom_layout)
        
        self.style_list.setCurrentRow(0)

    def update_preview(self, index):
        item = self.style_list.item(index)
        if item:
            style_key = item.data(Qt.UserRole)
            self.preview_area.set_style(style_key)

    def run_conversion(self):
        if not self.drop_area.files:
            QMessageBox.warning(self, "提醒", "请先拖入字幕文件")
            return
        
        selected_item = self.style_list.currentItem()
        if not selected_item:
            return
        
        style_key = selected_item.data(Qt.UserRole)
        success_count = 0
        
        self.btn_process.setEnabled(False)
        self.status_label.setText("正在处理...")
        QApplication.processEvents()

        for file_path in self.drop_area.files:
            success, result = process_subtitle(file_path, style_key)
            if success:
                success_count += 1
            else:
                QMessageBox.critical(self, "错误", f"处理失败: {os.path.basename(file_path)}\n{result}")

        self.btn_process.setEnabled(True)
        self.status_label.setText(f"处理完成: 成功 {success_count} / 总计 {len(self.drop_area.files)}")
        
        if success_count > 0:
            QMessageBox.information(self, "成功", f"已生成 {success_count} 个高级样式字幕，保存在源文件夹中。")
            self.drop_area.files = []
            self.drop_area.label.setText("将字幕文件拖放到此处\n(支持 .srt, .ass, .vtt, .ssa)")

def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = CoolSubApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

