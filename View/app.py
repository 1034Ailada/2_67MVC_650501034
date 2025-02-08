from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QComboBox, QTextEdit, QGridLayout, QFrame
from PyQt5.QtGui import QColor, QFont
import sys
from Controller.product_controller import ProductController
from datetime import datetime

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.setWindowTitle("ระบบคลังสินค้า")
        self.setGeometry(100, 100, 500, 600)

        layout = QGridLayout()
        
        self.product_id_label = QLabel("รหัสสินค้า:")
        self.product_id_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.product_id_label, 0, 0)
        
        self.product_id_input = QLineEdit(self)
        self.product_id_input.setPlaceholderText("กรอกรหัสสินค้า (6 หลัก)")
        layout.addWidget(self.product_id_input, 0, 1)
        
        self.category_label = QLabel("ประเภทสินค้า:")
        self.category_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.category_label, 1, 0)
        
        self.category_input = QComboBox(self)
        self.category_input.addItems(["อาหาร", "อิเล็กทรอนิกส์", "เสื้อผ้า"])
        layout.addWidget(self.category_input, 1, 1)

        self.expiration_date_label = QLabel("วันที่หมดอายุ:")
        self.expiration_date_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.expiration_date_label, 2, 0)
        
        self.expiration_date_input = QLineEdit(self)
        self.expiration_date_input.setPlaceholderText("YYYY-MM-DD")
        layout.addWidget(self.expiration_date_input, 2, 1)
        
        self.condition_label = QLabel("สภาพสินค้า:")
        self.condition_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.condition_label, 3, 0)
        
        self.condition_input = QComboBox(self)
        self.condition_input.addItems(["ปกติ", "เสียหาย", "ต้องตรวจสอบเพิ่มเติม"])
        layout.addWidget(self.condition_input, 3, 1)

        self.add_button = QPushButton("เพิ่มสินค้า", self)
        self.add_button.setFont(QFont("Arial", 12, QFont.Bold))
        self.add_button.clicked.connect(self.add_product)
        layout.addWidget(self.add_button, 4, 0, 1, 2)

        self.log_label = QLabel("Log:")
        self.log_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.log_label, 5, 0, 1, 2)
        
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)
        layout.addWidget(self.log_window, 6, 0, 1, 2)
        
        self.stats_label = QLabel("สถิติการรับสินค้า:")
        self.stats_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.stats_label, 7, 0, 1, 2)
        
        self.stats_window = QTextEdit(self)
        self.stats_window.setReadOnly(True)
        self.stats_window.setFrameShape(QFrame.Panel)
        self.stats_window.setFrameShadow(QFrame.Sunken)
        self.stats_window.setFont(QFont("Arial", 10))
        layout.addWidget(self.stats_window, 8, 0, 1, 2)
        
        self.setLayout(layout)

    def set_controller(self, controller):
        #กำหนด Controller ให้ View
        self.controller = controller
        self.update_stats()

    def add_product(self):
        #เรียกเมื่อกดปุ่มเพิ่มสินค้า
        product_id = self.product_id_input.text().strip()
        category = self.category_input.currentText()
        expiration_date = self.expiration_date_input.text().strip()
        condition = self.condition_input.currentText()

        if self.controller:
            message = self.controller.add_product(product_id, category, expiration_date, condition)
            self.update_stats()
            QApplication.processEvents()

    def append_log(self, message):
        #แสดงข้อความ Log ในหน้าต่าง Log Window
        self.log_window.setTextColor(QColor("black"))  # เปลี่ยนข้อความเป็นสีดำเสมอ (ตอนแรกจะแยกสี ; - ;)
        self.log_window.append(message)
        
    def display_message(self, message):
        #แสดงข้อความแจ้งเตือนใน Log Window
        self.append_log(message)

    def update_stats(self):
        #อัปเดตสถิติการรับและปฏิเสธสินค้า
        if self.controller:
            stats = self.controller.load_statistics()
            if stats:
                self.display_statistics(stats)

    def display_statistics(self, stats):
        #แสดงข้อมูลสถิติสินค้าในหน้าจอ
        self.stats_window.clear()
        if stats:
            for stat in stats:
                self.stats_window.append(f"{stat['category']}: รับเข้า {stat['accepted']} | ปฏิเสธ {stat['rejected']}")
        else:
            self.stats_window.append("ไม่มีข้อมูลสถิติ")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    controller = ProductController(window)
    window.set_controller(controller)
    window.show()
    sys.exit(app.exec())