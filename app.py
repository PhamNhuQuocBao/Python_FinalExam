import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application Basic")
        self.resize(300, 200)

        # Tạo giao diện
        self.label = QLabel("Chào bạn!", self)
        self.button = QPushButton("Nhấn vào đây", self)
        self.button.clicked.connect(self.on_click)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_click(self):
        self.label.setText("Bạn vừa nhấn nút!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
