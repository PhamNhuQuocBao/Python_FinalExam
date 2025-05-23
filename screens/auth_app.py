from PyQt5.QtWidgets import (
     QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
     QMessageBox
)
from bson import ObjectId
from database import MongoManager
from models.club import Club

# ============ Giao diện Đăng nhập/Đăng ký =============
class LoginForm(QWidget):
    def __init__(self, switch_to_register, login_success_callback):
        super().__init__()
        # Init database
        self.crud = MongoManager()

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

        user_exists = self.crud.find_one("users", {"username": username})

        if not user_exists:
            QMessageBox.warning(self, "Thất bại", "Tài khoản không tìm thấy!")
            return
        
        if not user_exists.get("password", None) == password:
            QMessageBox.warning(self, "Thất bại", "Mật khẩu không đúng!")
            return

        QMessageBox.information(self, "Thành công", "Đăng nhập thành công!")
        self.login_success_callback()


class RegisterForm(QWidget):
    def __init__(self, switch_to_login):
        super().__init__()
        self.crud = MongoManager()

        self.setWindowTitle("Đăng ký")

        self.label_user = QLabel("Username:")
        self.input_user = QLineEdit()

        self.label_pass = QLabel("Password:")
        self.input_pass = QLineEdit()
        self.input_pass.setEchoMode(QLineEdit.Password)

        self.label_confirm = QLabel("Nhập lại Password:")
        self.input_confirm = QLineEdit()
        self.input_confirm.setEchoMode(QLineEdit.Password)

        self.label_city = QLabel("City:")
        self.input_city = QLineEdit()

        self.label_country = QLabel("Country:")
        self.input_country = QLineEdit()

        self.label_name = QLabel("Name:")
        self.input_name = QLineEdit()

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
        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.label_city)
        layout.addWidget(self.input_city)
        layout.addWidget(self.label_country)
        layout.addWidget(self.input_country)
        layout.addWidget(self.register_button)
        layout.addWidget(self.switch_button)

        self.setLayout(layout)

    def register(self):
        username = self.input_user.text()
        password = self.input_pass.text()
        confirm = self.input_confirm.text()
        name = self.input_name.text()
        city = self.input_city.text()
        country = self.input_country.text()

        if not username or not password or not confirm or not name or not city or not country:
            QMessageBox.warning(self, "Lỗi", "Vui lòng điền đầy đủ thông tin.")
        elif password != confirm:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu không khớp.")
        else:
            user_exists = self.crud.find_one("users", {"username": username})

            if user_exists:
                QMessageBox.warning(self, "Lỗi", "Tài khoản đã tồn tại!")
                return
            
            club = Club(name, city, country)
            club_document = self.crud.insert("clubs", club.to_dict())
            club_id = str(club_document.inserted_id)
            
            self.crud.insert("users", {"username": username, "password": password, "club_id": ObjectId(club_id)})
            QMessageBox.information(self, "Thành công", "Đăng ký thành công!")

            return True
        
        return False