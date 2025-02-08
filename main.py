from PyQt5.QtWidgets import QApplication
import sys
from View.app import MainWindow
from Controller.product_controller import ProductController

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    controller = ProductController(main_window)
    main_window.set_controller(controller)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()