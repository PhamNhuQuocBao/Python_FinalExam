import sys
from PyQt5.QtWidgets import QApplication, QWidget,  QVBoxLayout,QStackedWidget

from screens.auth_app import LoginForm, RegisterForm
from screens.football_club import FootballClubManager

class AuthApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ứng dụng Đăng nhập")
        self.resize(300, 250)

        self.stack = QStackedWidget(self)

        self.login_form = LoginForm(self.show_register, self.go_to_manager)
        self.register_form = RegisterForm(self.show_login)

        self.stack.addWidget(self.login_form)
        self.stack.addWidget(self.register_form)

        layout = QVBoxLayout()
        layout.addWidget(self.stack)
        self.setLayout(layout)

        self.show_login()

    def show_login(self):
        self.stack.setCurrentWidget(self.login_form)

    def show_register(self):
        self.stack.setCurrentWidget(self.register_form)

    def go_to_manager(self):
        self.manager_window = FootballClubManager()
        self.manager_window.show()
        self.close()  # Ẩn cửa sổ login


# ============ Chạy app ============
if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth_window = AuthApp()
    auth_window.show()
    sys.exit(app.exec_())