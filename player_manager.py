from pymongo import MongoClient
from bson.objectid import ObjectId
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QSpinBox, QComboBox, QMessageBox, QLineEdit, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QLabel, QHeaderView
)

class PlayerManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["football_club"]
        self.players_col = self.db["players"]

        # Các input cũ
        self.name_input = QLineEdit()
        self.age_input = QSpinBox()
        self.age_input.setRange(10, 60)
        self.position_input = QComboBox()
        self.position_input.addItems(["Thủ môn", "Hậu vệ", "Tiền vệ", "Tiền đạo"])
        self.number_input = QSpinBox()
        self.number_input.setRange(1, 99)

        # Các input mới
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Số điện thoại")
        self.cccd_input = QLineEdit()
        self.cccd_input.setPlaceholderText("CCCD")
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("Địa chỉ")

        self.add_btn = QPushButton("Thêm")
        self.update_btn = QPushButton("Sửa")
        self.delete_btn = QPushButton("Xoá")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm tên...")

        self.table = QTableWidget()
        self.table.setColumnCount(8)  # Tăng số cột để chứa các trường mới
        self.table.setHorizontalHeaderLabels(["ID", "Tên", "Tuổi", "Vị trí", "Số áo", "SĐT", "CCCD", "Địa chỉ"])
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.cellClicked.connect(self.load_to_form)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Layout form cập nhật
        form = QHBoxLayout()
        form.addWidget(QLabel("Tên:")); form.addWidget(self.name_input)
        form.addWidget(QLabel("Tuổi:")); form.addWidget(self.age_input)
        form.addWidget(QLabel("Vị trí:")); form.addWidget(self.position_input)
        form.addWidget(QLabel("Số áo:")); form.addWidget(self.number_input)
        form.addWidget(QLabel("SĐT:")); form.addWidget(self.phone_input)
        form.addWidget(QLabel("CCCD:")); form.addWidget(self.cccd_input)
        form.addWidget(QLabel("Địa chỉ:")); form.addWidget(self.address_input)

        buttons = QHBoxLayout()
        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.update_btn)
        buttons.addWidget(self.delete_btn)

        search = QHBoxLayout()
        search.addWidget(QLabel("Tìm kiếm:"))
        search.addWidget(self.search_input)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addLayout(search)
        layout.addWidget(self.table)

        self.add_btn.clicked.connect(self.add_player)
        self.update_btn.clicked.connect(self.update_player)
        self.delete_btn.clicked.connect(self.delete_player)
        self.search_input.textChanged.connect(self.load_players)

        self.selected_id = None
        self.load_players()

    def load_players(self):
        keyword = self.search_input.text()
        query = {"name": {"$regex": keyword, "$options": "i"}} if keyword else {}
        players = list(self.players_col.find(query))

        self.table.setRowCount(len(players))
        for row, p in enumerate(players):
            self.table.setItem(row, 0, QTableWidgetItem(str(p["_id"])))
            self.table.setItem(row, 1, QTableWidgetItem(p["name"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(p["age"])))
            self.table.setItem(row, 3, QTableWidgetItem(p["position"]))
            self.table.setItem(row, 4, QTableWidgetItem(str(p["number"])))
            self.table.setItem(row, 5, QTableWidgetItem(p.get("phone", "")))
            self.table.setItem(row, 6, QTableWidgetItem(p.get("cccd", "")))
            self.table.setItem(row, 7, QTableWidgetItem(p.get("address", "")))

    def load_to_form(self, row, _):
        self.selected_id = self.table.item(row, 0).text()
        self.name_input.setText(self.table.item(row, 1).text())
        self.age_input.setValue(int(self.table.item(row, 2).text()))
        self.position_input.setCurrentText(self.table.item(row, 3).text())
        self.number_input.setValue(int(self.table.item(row, 4).text()))
        self.phone_input.setText(self.table.item(row, 5).text())
        self.cccd_input.setText(self.table.item(row, 6).text())
        self.address_input.setText(self.table.item(row, 7).text())

    def add_player(self):
        player = {
            "name": self.name_input.text(),
            "age": self.age_input.value(),
            "position": self.position_input.currentText(),
            "number": self.number_input.value(),
            "phone": self.phone_input.text(),
            "cccd": self.cccd_input.text(),
            "address": self.address_input.text(),
        }
        if not player["name"]:
            QMessageBox.warning(self, "Thiếu tên", "Vui lòng nhập tên cầu thủ.")
            return
        self.players_col.insert_one(player)
        self.clear_form()
        self.load_players()

    def update_player(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Chọn cầu thủ", "Vui lòng chọn cầu thủ.")
            return
        update = {
            "name": self.name_input.text(),
            "age": self.age_input.value(),
            "position": self.position_input.currentText(),
            "number": self.number_input.value(),
            "phone": self.phone_input.text(),
            "cccd": self.cccd_input.text(),
            "address": self.address_input.text(),
        }
        self.players_col.update_one({"_id": ObjectId(self.selected_id)}, {"$set": update})
        self.clear_form()
        self.load_players()

    def delete_player(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Chọn cầu thủ", "Vui lòng chọn cầu thủ.")
            return
        self.players_col.delete_one({"_id": ObjectId(self.selected_id)})
        self.clear_form()
        self.load_players()

    def clear_form(self):
        self.name_input.clear()
        self.age_input.setValue(18)
        self.position_input.setCurrentIndex(0)
        self.number_input.setValue(1)
        self.phone_input.clear()
        self.cccd_input.clear()
        self.address_input.clear()
        self.selected_id = None
