import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QStackedWidget, QMessageBox, QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import Qt

from screens.player_manager import PlayerManagerWidget


# ============ Giao diện Quản lý CLB =============
class FootballClubManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quản lý Câu lạc bộ Bóng đá")
        self.resize(1700, 800)

        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setAlignment(Qt.AlignTop)

        self.btn_players = QPushButton("Cầu thủ")
        self.btn_coach = QPushButton("Huấn luyện viên")
        self.btn_matches = QPushButton("Trận đấu")

        for btn in [self.btn_players, self.btn_coach, self.btn_matches]:
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sidebar.addWidget(btn)

        # Nội dung chính
        self.content_stack = QStackedWidget()
        self.page_players = PlayerManagerWidget()
        # self.page_players.setAlignment(Qt.AlignCenter)

        self.page_coach = QLabel("Thông tin HLV")
        self.page_coach.setAlignment(Qt.AlignCenter)

        self.page_matches = QLabel("Lịch thi đấu")
        self.page_matches.setAlignment(Qt.AlignCenter)

        self.content_stack.addWidget(self.page_players)
        self.content_stack.addWidget(self.page_coach)
        self.content_stack.addWidget(self.page_matches)

        # Kết nối
        self.btn_players.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.page_players))
        self.btn_coach.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.page_coach))
        self.btn_matches.clicked.connect(lambda: self.content_stack.setCurrentWidget(self.page_matches))

        # Sidebar 1/5
        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(self.width() // 5)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(self.content_stack)