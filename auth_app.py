from PyQt5.QtWidgets import (
     QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
     QMessageBox
)

# ============ Giao diện Đăng nhập/Đăng ký =============
class LoginForm(QWidget):
    def __init__(self, switch_to_register, login_success_callback):
        super().__init__()
        self.setWindowTitle("Đăng nhập")
        self.login_success_callback = login_success_callback

        self.label_user = QLabel("Username:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Password:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Đăng nhập")
        self.login_button.clicked.connect(self.login)

        self.switch_button = QPushButton("Chưa có tài khoản? Đăng ký")
        self.switch_button.clicked.connect(switch_to_register)

        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.login_button)
        layout.addWidget(self.switch_button)

        self.setLayout(layout)

    def login(self):
        username = self.input_user.text()
        password = self.input_pass.text()

        if username == "admin" and password == "123":
            QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")
            self.login_success_callback()
        else:
            QMessageBox.warning(self, "Thất bại", "Sai thông tin đăng nhập!")


class RegisterForm(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.setWindowTitle("Đăng ký")

        self.label_user = QLabel("Username:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Password:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.label_confirm = QLabel("Nhập lại Password:")
        self.input_confirm = QLineEdit()
        self.input_confirm.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Đăng ký")
        self.register_button.clicked.connect(self.register)

        self.switch_button = QPushButton("Đã có tài khoản? Đăng nhập")
        self.switch_button.clicked.connect(switch_to_login)

        layout = QVBoxLayout()
        layout.addWidget(self.label_user)
        layout.addWidget(self.input_user)
        layout.addWidget(self.label_pass)
        layout.addWidget(self.input_pass)
        layout.addWidget(self.label_confirm)
        layout.addWidget(self.input_confirm)
        layout.addWidget(self.register_button)
        layout.addWidget(self.switch_button)

        self.setLayout(layout)

    def register(self):
        username = self.input_user.text()
        password = self.input_pass.text()
        confirm = self.input_confirm.text()

        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin.")
        elif password != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu không khớp.")
        else:
            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")
