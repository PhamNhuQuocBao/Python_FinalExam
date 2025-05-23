from pymongo import MongoClient
from bson.objectid import ObjectId
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QSpinBox, QComboBox, QMessageBox, QLineEdit, QPushButton, 
    QVBoxLayout, QWidget, QHBoxLayout, QLabel, QHeaderView, QDoubleSpinBox, QDateEdit, 
    QGroupBox, QGridLayout, QTabWidget, QTextEdit, QCheckBox, QFrame, QSplitter
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPalette, QColor
from datetime import datetime, date
import json

# Import the Player class from the previous artifact
from models.player import Player

class PlayerManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["football_club"]
        self.players_col = self.db["players"]
        
        self.selected_id = None
        self.setup_ui()
        self.connect_signals()
        self.load_players()


    def create_form_widget(self):
        """Create the form widget for player input"""
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Create tabs for different information groups
        tab_widget = QTabWidget()
        
        # Basic Info Tab
        basic_tab = QWidget()
        basic_layout = QGridLayout(basic_tab)
        
        # Basic player information
        basic_layout.addWidget(QLabel("Tên cầu thủ:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên cầu thủ...")
        basic_layout.addWidget(self.name_input, 0, 1)
        
        basic_layout.addWidget(QLabel("Tuổi:"), 1, 0)
        self.age_input = QSpinBox()
        self.age_input.setRange(16, 45)
        self.age_input.setValue(20)
        basic_layout.addWidget(self.age_input, 1, 1)
        
        basic_layout.addWidget(QLabel("Vị trí:"), 2, 0)
        self.position_input = QComboBox()
        positions = ["GK", "CB", "LB", "RB", "LWB", "RWB", "SW", "CDM", "CM", "CAM", "LM", "RM", "LW", "RW", "CF", "ST", "LF", "RF"]
        self.position_input.addItems(positions)
        basic_layout.addWidget(self.position_input, 2, 1)
        
        basic_layout.addWidget(QLabel("Số áo:"), 3, 0)
        self.jersey_number_input = QSpinBox()
        self.jersey_number_input.setRange(1, 99)
        self.jersey_number_input.setValue(1)
        basic_layout.addWidget(self.jersey_number_input, 3, 1)
        
        basic_layout.addWidget(QLabel("Quốc tịch:"), 4, 0)
        self.nationality_input = QLineEdit()
        self.nationality_input.setPlaceholderText("VD: Việt Nam, Brazil...")
        basic_layout.addWidget(self.nationality_input, 4, 1)
        
        tab_widget.addTab(basic_tab, "Thông tin cơ bản")
        
        # Physical Info Tab
        physical_tab = QWidget()
        physical_layout = QGridLayout(physical_tab)
        
        physical_layout.addWidget(QLabel("Chiều cao (cm):"), 0, 0)
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(150.0, 220.0)
        self.height_input.setValue(175.0)
        self.height_input.setSuffix(" cm")
        physical_layout.addWidget(self.height_input, 0, 1)
        
        physical_layout.addWidget(QLabel("Cân nặng (kg):"), 1, 0)
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(50.0, 120.0)
        self.weight_input.setValue(70.0)
        self.weight_input.setSuffix(" kg")
        physical_layout.addWidget(self.weight_input, 1, 1)
        
        tab_widget.addTab(physical_tab, "Thông tin thể hình")
        
        # Contract Info Tab
        contract_tab = QWidget()
        contract_layout = QGridLayout(contract_tab)
        
        contract_layout.addWidget(QLabel("Ngày bắt đầu HĐ:"), 0, 0)
        self.contract_start_input = QDateEdit()
        self.contract_start_input.setDate(QDate.currentDate())
        self.contract_start_input.setCalendarPopup(True)
        contract_layout.addWidget(self.contract_start_input, 0, 1)
        
        contract_layout.addWidget(QLabel("Ngày kết thúc HĐ:"), 1, 0)
        self.contract_end_input = QDateEdit()
        self.contract_end_input.setDate(QDate.currentDate().addYears(2))
        self.contract_end_input.setCalendarPopup(True)
        contract_layout.addWidget(self.contract_end_input, 1, 1)
        
        contract_layout.addWidget(QLabel("Lương (USD):"), 2, 0)
        self.salary_input = QDoubleSpinBox()
        self.salary_input.setRange(0, 100000000)
        self.salary_input.setValue(0)
        self.salary_input.setPrefix("$ ")
        contract_layout.addWidget(self.salary_input, 2, 1)
        
        contract_layout.addWidget(QLabel("Giá trị TN (USD):"), 3, 0)
        self.market_value_input = QDoubleSpinBox()
        self.market_value_input.setRange(0, 500000000)
        self.market_value_input.setValue(0)
        self.market_value_input.setPrefix("$ ")
        contract_layout.addWidget(self.market_value_input, 3, 1)
        
        contract_layout.addWidget(QLabel("CLB trước đây:"), 4, 0)
        self.previous_clubs_input = QTextEdit()
        self.previous_clubs_input.setMaximumHeight(60)
        self.previous_clubs_input.setPlaceholderText("VD: Manchester United, Liverpool...")
        contract_layout.addWidget(self.previous_clubs_input, 4, 1)
        
        tab_widget.addTab(contract_tab, "Hợp đồng")
        
        # Performance Tab
        performance_tab = QWidget()
        performance_layout = QGridLayout(performance_tab)
        
        performance_layout.addWidget(QLabel("Số trận đã chơi:"), 0, 0)
        self.matches_played_input = QSpinBox()
        self.matches_played_input.setRange(0, 1000)
        performance_layout.addWidget(self.matches_played_input, 0, 1)
        
        performance_layout.addWidget(QLabel("Số bàn thắng:"), 1, 0)
        self.goals_input = QSpinBox()
        self.goals_input.setRange(0, 1000)
        performance_layout.addWidget(self.goals_input, 1, 1)
        
        performance_layout.addWidget(QLabel("Số kiến tạo:"), 2, 0)
        self.assists_input = QSpinBox()
        self.assists_input.setRange(0, 1000)
        performance_layout.addWidget(self.assists_input, 2, 1)
        
        performance_layout.addWidget(QLabel("Thẻ vàng:"), 3, 0)
        self.yellow_cards_input = QSpinBox()
        self.yellow_cards_input.setRange(0, 100)
        performance_layout.addWidget(self.yellow_cards_input, 3, 1)
        
        performance_layout.addWidget(QLabel("Thẻ đỏ:"), 4, 0)
        self.red_cards_input = QSpinBox()
        self.red_cards_input.setRange(0, 50)
        performance_layout.addWidget(self.red_cards_input, 4, 1)
        
        tab_widget.addTab(performance_tab, "Thống kê")
        
        # Contact Info Tab
        contact_tab = QWidget()
        contact_layout = QGridLayout(contact_tab)
        
        contact_layout.addWidget(QLabel("Số điện thoại:"), 0, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("VD: 0123456789")
        contact_layout.addWidget(self.phone_input, 0, 1)
        
        contact_layout.addWidget(QLabel("CCCD:"), 1, 0)
        self.cccd_input = QLineEdit()
        self.cccd_input.setPlaceholderText("Số căn cướ công dân")
        contact_layout.addWidget(self.cccd_input, 1, 1)
        
        contact_layout.addWidget(QLabel("Địa chỉ:"), 2, 0)
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.address_input.setPlaceholderText("Địa chỉ đầy đủ...")
        contact_layout.addWidget(self.address_input, 2, 1)
        
        tab_widget.addTab(contact_tab, "Liên hệ")
        
        form_layout.addWidget(tab_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Thêm cầu thủ")
        self.add_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; padding: 8px; font-weight: bold; }")
        
        self.update_btn = QPushButton("✏️ Cập nhật")
        self.update_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; padding: 8px; font-weight: bold; }")
        
        self.delete_btn = QPushButton("🗑️ Xóa")
        self.delete_btn.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; padding: 8px; font-weight: bold; }")
        
        self.clear_btn = QPushButton("🔄 Làm mới")
        self.clear_btn.setStyleSheet("QPushButton { background-color: #95a5a6; color: white; padding: 8px; font-weight: bold; }")
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.clear_btn)
        
        form_layout.addLayout(button_layout)
        
        return form_widget

    def create_table_widget(self):
        """Create the table widget for displaying players"""
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        
        # Search and filter controls
        search_group = QGroupBox("🔍 Tìm kiếm & Lọc")
        search_layout = QHBoxLayout(search_group)
        
        search_layout.addWidget(QLabel("Tên:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên...")
        search_layout.addWidget(self.search_input)
        
        search_layout.addWidget(QLabel("Vị trí:"))
        self.position_filter = QComboBox()
        self.position_filter.addItem("Tất cả vị trí")
        positions = ["GK", "CB", "LB", "RB", "LWB", "RWB", "SW", "CDM", "CM", "CAM", "LM", "RM", "LW", "RW", "CF", "ST", "LF", "RF"]
        self.position_filter.addItems(positions)
        search_layout.addWidget(self.position_filter)
        
        search_layout.addWidget(QLabel("Quốc tịch:"))
        self.nationality_filter = QComboBox()
        self.nationality_filter.addItem("Tất cả quốc gia")
        search_layout.addWidget(self.nationality_filter)
        
        self.refresh_btn = QPushButton("🔄 Làm mới danh sách")
        self.refresh_btn.setStyleSheet("QPushButton { background-color: #34495e; color: white; padding: 5px; }")
        search_layout.addWidget(self.refresh_btn)
        
        table_layout.addWidget(search_group)
        
        # Players table
        self.table = QTableWidget()
        self.table.setColumnCount(15)
        headers = [
            "ID", "Tên", "Tuổi", "Vị trí", "Số áo", "Quốc tịch", 
            "Chiều cao", "Cân nặng", "Trận", "Bàn thắng", "Kiến tạo", 
            "Thẻ vàng", "Thẻ đỏ", "Lương", "Giá trị TN"
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Name
        for i in range(2, 15):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        # Hide ID column
        self.table.setColumnHidden(0, True)
        
        table_layout.addWidget(self.table)
        
        # Statistics panel
        stats_group = QGroupBox("📊 Thống kê")
        stats_layout = QHBoxLayout(stats_group)
        
        self.total_players_label = QLabel("Tổng cầu thủ: 0")
        self.avg_age_label = QLabel("Tuổi TB: 0")
        self.total_goals_label = QLabel("Tổng bàn thắng: 0")
        self.total_matches_label = QLabel("Tổng trận: 0")
        
        stats_layout.addWidget(self.total_players_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.avg_age_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.total_goals_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.total_matches_label)
        stats_layout.addStretch()
        
        table_layout.addWidget(stats_group)
        
        return table_widget

    def connect_signals(self):
        """Connect signals to slots"""
        self.add_btn.clicked.connect(self.add_player)
        self.update_btn.clicked.connect(self.update_player)
        self.delete_btn.clicked.connect(self.delete_player)
        self.clear_btn.clicked.connect(self.clear_form)
        self.refresh_btn.clicked.connect(self.load_players)
        
        self.search_input.textChanged.connect(self.filter_players)
        self.position_filter.currentTextChanged.connect(self.filter_players)
        self.nationality_filter.currentTextChanged.connect(self.filter_players)
        
        self.table.cellClicked.connect(self.load_to_form)
        self.table.cellDoubleClicked.connect(self.show_player_details)

    def load_players(self):
        """Load all players from database"""
        try:
            players_data = list(self.players_col.find())
            self.all_players = [Player.from_dict(p) for p in players_data]
            self.update_nationality_filter()
            self.display_players(self.all_players)
            self.update_statistics()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def update_nationality_filter(self):
        """Update nationality filter options"""
        nationalities = set()
        for player in self.all_players:
            if player.nationality:
                nationalities.add(player.nationality)
        
        current_text = self.nationality_filter.currentText()
        self.nationality_filter.clear()
        self.nationality_filter.addItem("Tất cả quốc gia")
        self.nationality_filter.addItems(sorted(nationalities))
        
        # Restore previous selection if possible
        index = self.nationality_filter.findText(current_text)
        if index >= 0:
            self.nationality_filter.setCurrentIndex(index)

    def filter_players(self):
        """Filter players based on search criteria"""
        if not hasattr(self, 'all_players'):
            return
            
        filtered_players = []
        search_text = self.search_input.text().lower()
        position_filter = self.position_filter.currentText()
        nationality_filter = self.nationality_filter.currentText()
        
        for player in self.all_players:
            # Name filter
            if search_text and search_text not in player.name.lower():
                continue
                
            # Position filter
            if position_filter != "Tất cả vị trí" and player.position != position_filter:
                continue
                
            # Nationality filter
            if nationality_filter != "Tất cả quốc gia" and player.nationality != nationality_filter:
                continue
                
            filtered_players.append(player)
        
        self.display_players(filtered_players)

    def display_players(self, players):
        """Display players in the table"""
        self.table.setRowCount(len(players))
        
        for row, player in enumerate(players):
            self.table.setItem(row, 0, QTableWidgetItem(str(player.id or "")))
            self.table.setItem(row, 1, QTableWidgetItem(player.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(player.age)))
            self.table.setItem(row, 3, QTableWidgetItem(player.position))
            self.table.setItem(row, 4, QTableWidgetItem(str(player.jersey_number)))
            self.table.setItem(row, 5, QTableWidgetItem(player.nationality))
            self.table.setItem(row, 6, QTableWidgetItem(f"{player.height:.1f} cm" if player.height > 0 else "N/A"))
            self.table.setItem(row, 7, QTableWidgetItem(f"{player.weight:.1f} kg" if player.weight > 0 else "N/A"))
            self.table.setItem(row, 8, QTableWidgetItem(str(player.matches_played)))
            self.table.setItem(row, 9, QTableWidgetItem(str(player.goals)))
            self.table.setItem(row, 10, QTableWidgetItem(str(player.assists)))
            self.table.setItem(row, 11, QTableWidgetItem(str(player.yellow_cards)))
            self.table.setItem(row, 12, QTableWidgetItem(str(player.red_cards)))
            self.table.setItem(row, 13, QTableWidgetItem(f"${player.salary:,.0f}" if player.salary > 0 else "N/A"))
            self.table.setItem(row, 14, QTableWidgetItem(player.get_market_value_formatted()))

    def update_statistics(self):
        """Update statistics panel"""
        if not hasattr(self, 'all_players'):
            return
            
        total_players = len(self.all_players)
        avg_age = sum(p.age for p in self.all_players) / total_players if total_players > 0 else 0
        total_goals = sum(p.goals for p in self.all_players)
        total_matches = sum(p.matches_played for p in self.all_players)
        
        self.total_players_label.setText(f"Tổng cầu thủ: {total_players}")
        self.avg_age_label.setText(f"Tuổi TB: {avg_age:.1f}")
        self.total_goals_label.setText(f"Tổng bàn thắng: {total_goals}")
        self.total_matches_label.setText(f"Tổng trận: {total_matches}")

    def load_to_form(self, row, column):
        """Load selected player data to form"""
        if row < 0:
            return
            
        self.selected_id = self.table.item(row, 0).text()
        
        # Find the player object
        player = None
        for p in self.all_players:
            if str(p.id) == self.selected_id:
                player = p
                break
        
        if not player:
            return
        
        # Load basic info
        self.name_input.setText(player.name)
        self.age_input.setValue(player.age)
        
        # Set position
        pos_index = self.position_input.findText(player.position)
        if pos_index >= 0:
            self.position_input.setCurrentIndex(pos_index)
            
        self.jersey_number_input.setValue(player.jersey_number)
        self.nationality_input.setText(player.nationality)
        
        # Physical info
        self.height_input.setValue(player.height)
        self.weight_input.setValue(player.weight)
        
        # Contract info
        if player.contract_start:
            self.contract_start_input.setDate(QDate(player.contract_start))
        if player.contract_end:
            self.contract_end_input.setDate(QDate(player.contract_end))
            
        self.salary_input.setValue(player.salary)
        self.market_value_input.setValue(player.market_value)
        self.previous_clubs_input.setPlainText(player.previous_clubs)
        
        # Performance info
        self.matches_played_input.setValue(player.matches_played)
        self.goals_input.setValue(player.goals)
        self.assists_input.setValue(player.assists)
        self.yellow_cards_input.setValue(player.yellow_cards)
        self.red_cards_input.setValue(player.red_cards)
        
        # Contact info
        self.phone_input.setText(player.phone)
        self.cccd_input.setText(player.cccd)
        self.address_input.setPlainText(player.address)

    def create_player_from_form(self):
        """Create Player object from form data"""
        return Player(
            name=self.name_input.text().strip(),
            age=self.age_input.value(),
            position=self.position_input.currentText(),
            jersey_number=self.jersey_number_input.value(),
            height=self.height_input.value(),
            weight=self.weight_input.value(),
            nationality=self.nationality_input.text().strip(),
            contract_start=self.contract_start_input.date().toPyDate(),
            contract_end=self.contract_end_input.date().toPyDate(),
            salary=self.salary_input.value(),
            market_value=self.market_value_input.value(),
            previous_clubs=self.previous_clubs_input.toPlainText().strip(),
            goals=self.goals_input.value(),
            assists=self.assists_input.value(),
            yellow_cards=self.yellow_cards_input.value(),
            red_cards=self.red_cards_input.value(),
            matches_played=self.matches_played_input.value(),
            phone=self.phone_input.text().strip(),
            cccd=self.cccd_input.text().strip(),
            address=self.address_input.toPlainText().strip()
        )

    def validate_player_data(self, player):
        """Validate player data before saving"""
        if not player.name:
            QMessageBox.warning(self, "Lỗi", "Tên cầu thủ không được để trống!")
            return False
            
        # Check for duplicate jersey number
        query = {"jersey_number": player.jersey_number}
        if self.selected_id:
            query["_id"] = {"$ne": ObjectId(self.selected_id)}
            
        if self.players_col.find_one(query):
            QMessageBox.warning(self, "Lỗi", f"Số áo {player.jersey_number} đã được sử dụng!")
            return False
            
        return True

    def add_player(self):
        """Add new player"""
        try:
            player = self.create_player_from_form()
            
            if not self.validate_player_data(player):
                print(f"ERROR")
                return
                
            result = self.players_col.insert_one(player.to_dict())
            
            if result.inserted_id:
                QMessageBox.information(self, "Thành công", "Thêm cầu thủ thành công!")
                self.clear_form()
                self.load_players()
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể thêm cầu thủ!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm cầu thủ: {str(e)}")

    def update_player(self):
        """Update selected player"""
        if not self.selected_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cầu thủ cần cập nhật!")
            return
            
        try:
            player = self.create_player_from_form()
            
            if not self.validate_player_data(player):
                return
                
            result = self.players_col.update_one(
                {"_id": ObjectId(self.selected_id)},
                {"$set": player.to_dict()}
            )
            
            if result.modified_count > 0:
                QMessageBox.information(self, "Thành công", "Cập nhật cầu thủ thành công!")
                self.clear_form()
                self.load_players()
            else:
                QMessageBox.warning(self, "Lỗi", "Không có thay đổi nào được thực hiện!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật cầu thủ: {str(e)}")

    def delete_player(self):
        """Delete selected player"""
        if not self.selected_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cầu thủ cần xóa!")
            return
            
        # Confirm deletion
        player_name = self.name_input.text()
        reply = QMessageBox.question(
            self, "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa cầu thủ '{player_name}'?\n\nHành động này không thể hoàn tác!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                result = self.players_col.delete_one({"_id": ObjectId(self.selected_id)})
                
                if result.deleted_count > 0:
                    QMessageBox.information(self, "Thành công", "Xóa cầu thủ thành công!")
                    self.clear_form()
                    self.load_players()
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể xóa cầu thủ!")
                    
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa cầu thủ: {str(e)}")
from pymongo import MongoClient
from bson.objectid import ObjectId
from PyQt5.QtWidgets import (
    QTableWidget, QTableWidgetItem, QSpinBox, QComboBox, QMessageBox, QLineEdit, QPushButton, 
    QVBoxLayout, QWidget, QHBoxLayout, QLabel, QHeaderView, QDoubleSpinBox, QDateEdit, 
    QGroupBox, QGridLayout, QTabWidget, QTextEdit, QCheckBox, QFrame, QSplitter
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QPalette, QColor
from datetime import datetime, date
import json

# Import the Player class from the previous artifact
from models.player import Player

class PlayerManagerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client["football_club"]
        self.players_col = self.db["players"]
        
        self.selected_id = None
        self.setup_ui()
        self.connect_signals()
        self.load_players()

    def setup_ui(self):
        """Setup the user interface"""
        self.setWindowTitle("Football Player Management System")
        self.setMinimumSize(1400, 800)
        
        # Main layout with splitter
        main_layout = QVBoxLayout(self)
        
        # Title Container
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("⚽ FOOTBALL PLAYER MANAGEMENT SYSTEM")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                background-color: #ecf0f1;
                border-radius: 8px;
                padding: 20px;
            }
        """)
        title_container.setMaximumHeight(200)  # Giới hạn chiều cao ở đây

        title_layout.addWidget(title)
        main_layout.addWidget(title_container)
        
        # Create splitter for form and table
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Form
        form_widget = self.create_form_widget()
        splitter.addWidget(form_widget)
        
        # Right side - Table and controls
        table_widget = self.create_table_widget()
        splitter.addWidget(table_widget)
        
        # Set splitter proportions
        splitter.setSizes([500, 900])
        main_layout.addWidget(splitter)

    def create_form_widget(self):
        """Create the form widget for player input"""
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        
        # Create tabs for different information groups
        tab_widget = QTabWidget()
        
        # Basic Info Tab
        basic_tab = QWidget()
        basic_layout = QGridLayout(basic_tab)
        
        # Basic player information
        basic_layout.addWidget(QLabel("Tên cầu thủ:"), 0, 0)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nhập tên cầu thủ...")
        basic_layout.addWidget(self.name_input, 0, 1)
        
        basic_layout.addWidget(QLabel("Tuổi:"), 1, 0)
        self.age_input = QSpinBox()
        self.age_input.setRange(16, 45)
        self.age_input.setValue(20)
        basic_layout.addWidget(self.age_input, 1, 1)
        
        basic_layout.addWidget(QLabel("Vị trí:"), 2, 0)
        self.position_input = QComboBox()
        positions = ["GK", "CB", "LB", "RB", "LWB", "RWB", "SW", "CDM", "CM", "CAM", "LM", "RM", "LW", "RW", "CF", "ST", "LF", "RF"]
        self.position_input.addItems(positions)
        basic_layout.addWidget(self.position_input, 2, 1)
        
        basic_layout.addWidget(QLabel("Số áo:"), 3, 0)
        self.jersey_number_input = QSpinBox()
        self.jersey_number_input.setRange(1, 99)
        self.jersey_number_input.setValue(1)
        basic_layout.addWidget(self.jersey_number_input, 3, 1)
        
        basic_layout.addWidget(QLabel("Quốc tịch:"), 4, 0)
        self.nationality_input = QLineEdit()
        self.nationality_input.setPlaceholderText("VD: Việt Nam, Brazil...")
        basic_layout.addWidget(self.nationality_input, 4, 1)
        
        tab_widget.addTab(basic_tab, "Thông tin cơ bản")
        
        # Physical Info Tab
        physical_tab = QWidget()
        physical_layout = QGridLayout(physical_tab)
        
        physical_layout.addWidget(QLabel("Chiều cao (cm):"), 0, 0)
        self.height_input = QDoubleSpinBox()
        self.height_input.setRange(150.0, 220.0)
        self.height_input.setValue(175.0)
        self.height_input.setSuffix(" cm")
        physical_layout.addWidget(self.height_input, 0, 1)
        
        physical_layout.addWidget(QLabel("Cân nặng (kg):"), 1, 0)
        self.weight_input = QDoubleSpinBox()
        self.weight_input.setRange(50.0, 120.0)
        self.weight_input.setValue(70.0)
        self.weight_input.setSuffix(" kg")
        physical_layout.addWidget(self.weight_input, 1, 1)
        
        tab_widget.addTab(physical_tab, "Thông tin thể hình")
        
        # Contract Info Tab
        contract_tab = QWidget()
        contract_layout = QGridLayout(contract_tab)
        
        contract_layout.addWidget(QLabel("Ngày bắt đầu HĐ:"), 0, 0)
        self.contract_start_input = QDateEdit()
        self.contract_start_input.setDate(QDate.currentDate())
        self.contract_start_input.setCalendarPopup(True)
        contract_layout.addWidget(self.contract_start_input, 0, 1)
        
        contract_layout.addWidget(QLabel("Ngày kết thúc HĐ:"), 1, 0)
        self.contract_end_input = QDateEdit()
        self.contract_end_input.setDate(QDate.currentDate().addYears(2))
        self.contract_end_input.setCalendarPopup(True)
        contract_layout.addWidget(self.contract_end_input, 1, 1)
        
        contract_layout.addWidget(QLabel("Lương (USD):"), 2, 0)
        self.salary_input = QDoubleSpinBox()
        self.salary_input.setRange(0, 100000000)
        self.salary_input.setValue(50000)
        self.salary_input.setPrefix("$ ")
        contract_layout.addWidget(self.salary_input, 2, 1)
        
        contract_layout.addWidget(QLabel("Giá trị TN (USD):"), 3, 0)
        self.market_value_input = QDoubleSpinBox()
        self.market_value_input.setRange(0, 500000000)
        self.market_value_input.setValue(100000)
        self.market_value_input.setPrefix("$ ")
        contract_layout.addWidget(self.market_value_input, 3, 1)
        
        contract_layout.addWidget(QLabel("CLB trước đây:"), 4, 0)
        self.previous_clubs_input = QTextEdit()
        self.previous_clubs_input.setMaximumHeight(60)
        self.previous_clubs_input.setPlaceholderText("VD: Manchester United, Liverpool...")
        contract_layout.addWidget(self.previous_clubs_input, 4, 1)
        
        tab_widget.addTab(contract_tab, "Hợp đồng")
        
        # Performance Tab
        performance_tab = QWidget()
        performance_layout = QGridLayout(performance_tab)
        
        performance_layout.addWidget(QLabel("Số trận đã chơi:"), 0, 0)
        self.matches_played_input = QSpinBox()
        self.matches_played_input.setRange(0, 1000)
        performance_layout.addWidget(self.matches_played_input, 0, 1)
        
        performance_layout.addWidget(QLabel("Số bàn thắng:"), 1, 0)
        self.goals_input = QSpinBox()
        self.goals_input.setRange(0, 1000)
        performance_layout.addWidget(self.goals_input, 1, 1)
        
        performance_layout.addWidget(QLabel("Số kiến tạo:"), 2, 0)
        self.assists_input = QSpinBox()
        self.assists_input.setRange(0, 1000)
        performance_layout.addWidget(self.assists_input, 2, 1)
        
        performance_layout.addWidget(QLabel("Thẻ vàng:"), 3, 0)
        self.yellow_cards_input = QSpinBox()
        self.yellow_cards_input.setRange(0, 100)
        performance_layout.addWidget(self.yellow_cards_input, 3, 1)
        
        performance_layout.addWidget(QLabel("Thẻ đỏ:"), 4, 0)
        self.red_cards_input = QSpinBox()
        self.red_cards_input.setRange(0, 50)
        performance_layout.addWidget(self.red_cards_input, 4, 1)
        
        tab_widget.addTab(performance_tab, "Thống kê")
        
        # Contact Info Tab
        contact_tab = QWidget()
        contact_layout = QGridLayout(contact_tab)
        
        contact_layout.addWidget(QLabel("Số điện thoại:"), 0, 0)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("VD: 0123456789")
        contact_layout.addWidget(self.phone_input, 0, 1)
        
        contact_layout.addWidget(QLabel("CCCD:"), 1, 0)
        self.cccd_input = QLineEdit()
        self.cccd_input.setPlaceholderText("Số căn cướ công dân")
        contact_layout.addWidget(self.cccd_input, 1, 1)
        
        contact_layout.addWidget(QLabel("Địa chỉ:"), 2, 0)
        self.address_input = QTextEdit()
        self.address_input.setMaximumHeight(80)
        self.address_input.setPlaceholderText("Địa chỉ đầy đủ...")
        contact_layout.addWidget(self.address_input, 2, 1)
        
        tab_widget.addTab(contact_tab, "Liên hệ")
        
        form_layout.addWidget(tab_widget)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Thêm cầu thủ")
        self.add_btn.setStyleSheet("QPushButton { background-color: #27ae60; color: white; padding: 8px; font-weight: bold; }")
        
        self.update_btn = QPushButton("✏️ Cập nhật")
        self.update_btn.setStyleSheet("QPushButton { background-color: #3498db; color: white; padding: 8px; font-weight: bold; }")
        
        self.delete_btn = QPushButton("🗑️ Xóa")
        self.delete_btn.setStyleSheet("QPushButton { background-color: #e74c3c; color: white; padding: 8px; font-weight: bold; }")
        
        self.clear_btn = QPushButton("🔄 Làm mới")
        self.clear_btn.setStyleSheet("QPushButton { background-color: #95a5a6; color: white; padding: 8px; font-weight: bold; }")
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.clear_btn)
        
        form_layout.addLayout(button_layout)
        
        return form_widget

    def create_table_widget(self):
        """Create the table widget for displaying players"""
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        
        # Search and filter controls
        search_group = QGroupBox("🔍 Tìm kiếm & Lọc")
        search_layout = QHBoxLayout(search_group)
        
        search_layout.addWidget(QLabel("Tên:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm theo tên...")
        search_layout.addWidget(self.search_input)
        
        search_layout.addWidget(QLabel("Vị trí:"))
        self.position_filter = QComboBox()
        self.position_filter.addItem("Tất cả vị trí")
        positions = ["GK", "CB", "LB", "RB", "LWB", "RWB", "SW", "CDM", "CM", "CAM", "LM", "RM", "LW", "RW", "CF", "ST", "LF", "RF"]
        self.position_filter.addItems(positions)
        search_layout.addWidget(self.position_filter)
        
        search_layout.addWidget(QLabel("Quốc tịch:"))
        self.nationality_filter = QComboBox()
        self.nationality_filter.addItem("Tất cả quốc gia")
        search_layout.addWidget(self.nationality_filter)
        
        self.refresh_btn = QPushButton("🔄 Làm mới danh sách")
        self.refresh_btn.setStyleSheet("QPushButton { background-color: #34495e; color: white; padding: 5px; }")
        search_layout.addWidget(self.refresh_btn)
        
        table_layout.addWidget(search_group)
        
        # Players table
        self.table = QTableWidget()
        self.table.setColumnCount(15)
        headers = [
            "ID", "Tên", "Tuổi", "Vị trí", "Số áo", "Quốc tịch", 
            "Chiều cao", "Cân nặng", "Trận", "Bàn thắng", "Kiến tạo", 
            "Thẻ vàng", "Thẻ đỏ", "Lương", "Giá trị TN"
        ]
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Name
        for i in range(2, 15):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        # Hide ID column
        self.table.setColumnHidden(0, True)
        
        table_layout.addWidget(self.table)
        
        # Statistics panel
        stats_group = QGroupBox("📊 Thống kê")
        stats_layout = QHBoxLayout(stats_group)
        
        self.total_players_label = QLabel("Tổng cầu thủ: 0")
        self.avg_age_label = QLabel("Tuổi TB: 0")
        self.total_goals_label = QLabel("Tổng bàn thắng: 0")
        self.total_matches_label = QLabel("Tổng trận: 0")
        
        stats_layout.addWidget(self.total_players_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.avg_age_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.total_goals_label)
        stats_layout.addWidget(QLabel("|"))
        stats_layout.addWidget(self.total_matches_label)
        stats_layout.addStretch()
        
        table_layout.addWidget(stats_group)
        
        return table_widget

    def connect_signals(self):
        """Connect signals to slots"""
        self.add_btn.clicked.connect(self.add_player)
        self.update_btn.clicked.connect(self.update_player)
        self.delete_btn.clicked.connect(self.delete_player)
        self.clear_btn.clicked.connect(self.clear_form)
        self.refresh_btn.clicked.connect(self.load_players)
        
        self.search_input.textChanged.connect(self.filter_players)
        self.position_filter.currentTextChanged.connect(self.filter_players)
        self.nationality_filter.currentTextChanged.connect(self.filter_players)
        
        self.table.cellClicked.connect(self.load_to_form)
        self.table.cellDoubleClicked.connect(self.show_player_details)

    def load_players(self):
        """Load all players from database"""
        try:
            players_data = list(self.players_col.find())
            self.all_players = [Player.from_dict(p) for p in players_data]
            self.update_nationality_filter()
            self.display_players(self.all_players)
            self.update_statistics()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def update_nationality_filter(self):
        """Update nationality filter options"""
        nationalities = set()
        for player in self.all_players:
            if player.nationality:
                nationalities.add(player.nationality)
        
        current_text = self.nationality_filter.currentText()
        self.nationality_filter.clear()
        self.nationality_filter.addItem("Tất cả quốc gia")
        self.nationality_filter.addItems(sorted(nationalities))
        
        # Restore previous selection if possible
        index = self.nationality_filter.findText(current_text)
        if index >= 0:
            self.nationality_filter.setCurrentIndex(index)

    def filter_players(self):
        """Filter players based on search criteria"""
        if not hasattr(self, 'all_players'):
            return
            
        filtered_players = []
        search_text = self.search_input.text().lower()
        position_filter = self.position_filter.currentText()
        nationality_filter = self.nationality_filter.currentText()
        
        for player in self.all_players:
            # Name filter
            if search_text and search_text not in player.name.lower():
                continue
                
            # Position filter
            if position_filter != "Tất cả vị trí" and player.position != position_filter:
                continue
                
            # Nationality filter
            if nationality_filter != "Tất cả quốc gia" and player.nationality != nationality_filter:
                continue
                
            filtered_players.append(player)
        
        self.display_players(filtered_players)

    def display_players(self, players):
        """Display players in the table"""
        self.table.setRowCount(len(players))
        
        for row, player in enumerate(players):
            self.table.setItem(row, 0, QTableWidgetItem(str(player.id or "")))
            self.table.setItem(row, 1, QTableWidgetItem(player.name))
            self.table.setItem(row, 2, QTableWidgetItem(str(player.age)))
            self.table.setItem(row, 3, QTableWidgetItem(player.position))
            self.table.setItem(row, 4, QTableWidgetItem(str(player.jersey_number)))
            self.table.setItem(row, 5, QTableWidgetItem(player.nationality))
            self.table.setItem(row, 6, QTableWidgetItem(f"{player.height:.1f} cm" if player.height > 0 else "N/A"))
            self.table.setItem(row, 7, QTableWidgetItem(f"{player.weight:.1f} kg" if player.weight > 0 else "N/A"))
            self.table.setItem(row, 8, QTableWidgetItem(str(player.matches_played)))
            self.table.setItem(row, 9, QTableWidgetItem(str(player.goals)))
            self.table.setItem(row, 10, QTableWidgetItem(str(player.assists)))
            self.table.setItem(row, 11, QTableWidgetItem(str(player.yellow_cards)))
            self.table.setItem(row, 12, QTableWidgetItem(str(player.red_cards)))
            self.table.setItem(row, 13, QTableWidgetItem(f"${player.salary:,.0f}" if player.salary > 0 else "N/A"))
            self.table.setItem(row, 14, QTableWidgetItem(player.get_market_value_formatted()))

    def update_statistics(self):
        """Update statistics panel"""
        if not hasattr(self, 'all_players'):
            return
            
        total_players = len(self.all_players)
        avg_age = sum(p.age for p in self.all_players) / total_players if total_players > 0 else 0
        total_goals = sum(p.goals for p in self.all_players)
        total_matches = sum(p.matches_played for p in self.all_players)
        
        self.total_players_label.setText(f"Tổng cầu thủ: {total_players}")
        self.avg_age_label.setText(f"Tuổi TB: {avg_age:.1f}")
        self.total_goals_label.setText(f"Tổng bàn thắng: {total_goals}")
        self.total_matches_label.setText(f"Tổng trận: {total_matches}")

    def load_to_form(self, row, column):
        """Load selected player data to form"""
        if row < 0:
            return
            
        self.selected_id = self.table.item(row, 0).text()
        
        # Find the player object
        player = None
        for p in self.all_players:
            if str(p.id) == self.selected_id:
                player = p
                break
        
        if not player:
            return
        
        # Load basic info
        self.name_input.setText(player.name)
        self.age_input.setValue(player.age)
        
        # Set position
        pos_index = self.position_input.findText(player.position)
        if pos_index >= 0:
            self.position_input.setCurrentIndex(pos_index)
            
        self.jersey_number_input.setValue(player.jersey_number)
        self.nationality_input.setText(player.nationality)
        
        # Physical info
        self.height_input.setValue(player.height)
        self.weight_input.setValue(player.weight)
        
        # Contract info
        if player.contract_start:
            self.contract_start_input.setDate(QDate(player.contract_start))
        if player.contract_end:
            self.contract_end_input.setDate(QDate(player.contract_end))
            
        self.salary_input.setValue(player.salary)
        self.market_value_input.setValue(player.market_value)
        self.previous_clubs_input.setPlainText(player.previous_clubs)
        
        # Performance info
        self.matches_played_input.setValue(player.matches_played)
        self.goals_input.setValue(player.goals)
        self.assists_input.setValue(player.assists)
        self.yellow_cards_input.setValue(player.yellow_cards)
        self.red_cards_input.setValue(player.red_cards)
        
        # Contact info
        self.phone_input.setText(player.phone)
        self.cccd_input.setText(player.cccd)
        self.address_input.setPlainText(player.address)

    def create_player_from_form(self):
        """Create Player object from form data"""
        return Player(
            name=self.name_input.text().strip(),
            age=self.age_input.value(),
            position=self.position_input.currentText(),
            jersey_number=self.jersey_number_input.value(),
            height=self.height_input.value(),
            weight=self.weight_input.value(),
            nationality=self.nationality_input.text().strip(),
            contract_start=self.contract_start_input.date().toPyDate(),
            contract_end=self.contract_end_input.date().toPyDate(),
            salary=self.salary_input.value(),
            market_value=self.market_value_input.value(),
            previous_clubs=self.previous_clubs_input.toPlainText().strip(),
            goals=self.goals_input.value(),
            assists=self.assists_input.value(),
            yellow_cards=self.yellow_cards_input.value(),
            red_cards=self.red_cards_input.value(),
            matches_played=self.matches_played_input.value(),
            phone=self.phone_input.text().strip(),
            cccd=self.cccd_input.text().strip(),
            address=self.address_input.toPlainText().strip()
        )

    def validate_player_data(self, player):
        """Validate player data before saving"""
        if not player.name:
            QMessageBox.warning(self, "Lỗi", "Tên cầu thủ không được để trống!")
            return False
        
        if not player.nationality:
            QMessageBox.warning(self, "Lỗi", "Quốc tịch cầu thủ không được để trống!")
            return False
        
        if not player.weight:
            QMessageBox.warning(self, "Lỗi", "Cân nặng cầu thủ không được để trống!")
            return False
        
        if not player.height:
            QMessageBox.warning(self, "Lỗi", "Chiều cao cầu thủ không được để trống!")
            return False
            
        if not player.phone:
            QMessageBox.warning(self, "Lỗi", "Số điện thoại cầu thủ không được để trống!")
            return False
        
        if not player.cccd:
            QMessageBox.warning(self, "Lỗi", "Số CCCD cầu thủ không được để trống!")
            return False
        
        if not player.address:
            QMessageBox.warning(self, "Lỗi", "Địa chỉ cầu thủ không được để trống!")
            return False
        
        # Check for duplicate jersey number
        query = {"jersey_number": player.jersey_number}
        if self.selected_id:
            query["_id"] = {"$ne": ObjectId(self.selected_id)}
            
        if self.players_col.find_one(query):
            QMessageBox.warning(self, "Lỗi", f"Số áo {player.jersey_number} đã được sử dụng!")
            return False
            
        return True

    def add_player(self):
        """Add new player"""
        try:
            player = self.create_player_from_form()
            
            if not self.validate_player_data(player):
                return
                
            result = self.players_col.insert_one(player.to_dict())
            
            if result.inserted_id:
                QMessageBox.information(self, "Thành công", "Thêm cầu thủ thành công!")
                self.clear_form()
                self.load_players()
            else:
                QMessageBox.warning(self, "Lỗi", "Không thể thêm cầu thủ!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi thêm cầu thủ: {str(e)}")

    def update_player(self):
        """Update selected player"""
        if not self.selected_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cầu thủ cần cập nhật!")
            return
            
        try:
            player = self.create_player_from_form()
            
            if not self.validate_player_data(player):
                return
                
            result = self.players_col.update_one(
                {"_id": ObjectId(self.selected_id)},
                {"$set": player.to_dict()}
            )
            
            if result.modified_count > 0:
                QMessageBox.information(self, "Thành công", "Cập nhật cầu thủ thành công!")
                self.clear_form()
                self.load_players()
            else:
                QMessageBox.warning(self, "Lỗi", "Không có thay đổi nào được thực hiện!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi cập nhật cầu thủ: {str(e)}")

    def delete_player(self):
        """Delete selected player"""
        if not self.selected_id:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn cầu thủ cần xóa!")
            return
            
        # Confirm deletion
        player_name = self.name_input.text()
        reply = QMessageBox.question(
            self, "Xác nhận xóa", 
            f"Bạn có chắc chắn muốn xóa cầu thủ '{player_name}'?\n\nHành động này không thể hoàn tác!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                result = self.players_col.delete_one({"_id": ObjectId(self.selected_id)})
                
                if result.deleted_count > 0:
                    QMessageBox.information(self, "Thành công", "Xóa cầu thủ thành công!")
                    self.clear_form()
                    self.load_players()
                else:
                    QMessageBox.warning(self, "Lỗi", "Không thể xóa cầu thủ!")
                    
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi khi xóa cầu thủ: {str(e)}")

    # Các function bị thiếu trong PlayerManagerWidget class

    def clear_form(self):
        """Clear all form inputs"""
        # Basic info
        self.name_input.clear()
        self.age_input.setValue(20)
        self.position_input.setCurrentIndex(0)
        self.jersey_number_input.setValue(1)
        self.nationality_input.clear()
        
        # Physical info
        self.height_input.setValue(175.0)
        self.weight_input.setValue(70.0)
        
        # Contract info
        self.contract_start_input.setDate(QDate.currentDate())
        self.contract_end_input.setDate(QDate.currentDate().addYears(2))
        self.salary_input.setValue(50000)
        self.market_value_input.setValue(100000)
        self.previous_clubs_input.clear()
        
        # Performance info
        self.matches_played_input.setValue(0)
        self.goals_input.setValue(0)
        self.assists_input.setValue(0)
        self.yellow_cards_input.setValue(0)
        self.red_cards_input.setValue(0)
        
        # Contact info
        self.phone_input.clear()
        self.cccd_input.clear()
        self.address_input.clear()
        
        # Reset selected ID
        self.selected_id = None
        
        # Clear table selection
        self.table.clearSelection()

    def show_player_details(self, row, column):
        """Show detailed player information in a popup dialog"""
        if row < 0:
            return
            
        player_id = self.table.item(row, 0).text()
        
        # Find the player object
        player = None
        for p in self.all_players:
            if str(p.id) == player_id:
                player = p
                break
        
        if not player:
            return
        
        # Create detail dialog
        from PyQt5.QtWidgets import QDialog, QScrollArea
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Chi tiết cầu thủ - {player.name}")
        dialog.setMinimumSize(500, 600)
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Create scroll area for content
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Player header
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #3498db;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        name_label = QLabel(f"🏃‍♂️ {player.name}")
        name_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        name_label.setAlignment(Qt.AlignCenter)
        
        jersey_label = QLabel(f"#{player.jersey_number} - {player.position}")
        jersey_label.setStyleSheet("color: white; font-size: 14px;")
        jersey_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(name_label)
        header_layout.addWidget(jersey_label)
        scroll_layout.addWidget(header_frame)
        
        # Basic information group
        basic_group = QGroupBox("📋 Thông tin cơ bản")
        basic_layout = QGridLayout(basic_group)
        
        basic_layout.addWidget(QLabel("Tên:"), 0, 0)
        basic_layout.addWidget(QLabel(player.name), 0, 1)
        basic_layout.addWidget(QLabel("Tuổi:"), 1, 0)
        basic_layout.addWidget(QLabel(str(player.age)), 1, 1)
        basic_layout.addWidget(QLabel("Vị trí:"), 2, 0)
        basic_layout.addWidget(QLabel(player.position), 2, 1)
        basic_layout.addWidget(QLabel("Quốc tịch:"), 3, 0)
        basic_layout.addWidget(QLabel(player.nationality), 3, 1)
        basic_layout.addWidget(QLabel("Chiều cao:"), 4, 0)
        basic_layout.addWidget(QLabel(f"{player.height:.1f} cm"), 4, 1)
        basic_layout.addWidget(QLabel("Cân nặng:"), 5, 0)
        basic_layout.addWidget(QLabel(f"{player.weight:.1f} kg"), 5, 1)
        
        scroll_layout.addWidget(basic_group)
        
        # Contract information group
        contract_group = QGroupBox("💼 Thông tin hợp đồng")
        contract_layout = QGridLayout(contract_group)
        
        contract_layout.addWidget(QLabel("Bắt đầu HĐ:"), 0, 0)
        contract_layout.addWidget(QLabel(player.contract_start.strftime('%d/%m/%Y') if player.contract_start else 'N/A'), 0, 1)
        contract_layout.addWidget(QLabel("Kết thúc HĐ:"), 1, 0)
        contract_layout.addWidget(QLabel(player.contract_end.strftime('%d/%m/%Y') if player.contract_end else 'N/A'), 1, 1)
        contract_layout.addWidget(QLabel("Lương:"), 2, 0)
        contract_layout.addWidget(QLabel(f"${player.salary:,.0f}"), 2, 1)
        contract_layout.addWidget(QLabel("Giá trị TN:"), 3, 0)
        contract_layout.addWidget(QLabel(player.get_market_value_formatted()), 3, 1)
        
        if player.previous_clubs:
            contract_layout.addWidget(QLabel("CLB trước:"), 4, 0)
            clubs_label = QLabel(player.previous_clubs)
            clubs_label.setWordWrap(True)
            contract_layout.addWidget(clubs_label, 4, 1)
        
        scroll_layout.addWidget(contract_group)
        
        # Performance statistics group
        performance_group = QGroupBox("📊 Thống kê thi đấu")
        performance_layout = QGridLayout(performance_group)
        
        performance_layout.addWidget(QLabel("Số trận:"), 0, 0)
        performance_layout.addWidget(QLabel(str(player.matches_played)), 0, 1)
        performance_layout.addWidget(QLabel("Bàn thắng:"), 1, 0)
        performance_layout.addWidget(QLabel(str(player.goals)), 1, 1)
        performance_layout.addWidget(QLabel("Kiến tạo:"), 2, 0)
        performance_layout.addWidget(QLabel(str(player.assists)), 2, 1)
        performance_layout.addWidget(QLabel("Thẻ vàng:"), 3, 0)
        performance_layout.addWidget(QLabel(str(player.yellow_cards)), 3, 1)
        performance_layout.addWidget(QLabel("Thẻ đỏ:"), 4, 0)
        performance_layout.addWidget(QLabel(str(player.red_cards)), 4, 1)
        
        # Calculate averages
        if player.matches_played > 0:
            goals_per_match = player.goals / player.matches_played
            assists_per_match = player.assists / player.matches_played
            performance_layout.addWidget(QLabel("BT/trận:"), 5, 0)
            performance_layout.addWidget(QLabel(f"{goals_per_match:.2f}"), 5, 1)
            performance_layout.addWidget(QLabel("KT/trận:"), 6, 0)
            performance_layout.addWidget(QLabel(f"{assists_per_match:.2f}"), 6, 1)
        
        scroll_layout.addWidget(performance_group)
        
        # Contact information group
        contact_group = QGroupBox("📞 Thông tin liên hệ")
        contact_layout = QGridLayout(contact_group)
        
        if player.phone:
            contact_layout.addWidget(QLabel("Điện thoại:"), 0, 0)
            contact_layout.addWidget(QLabel(player.phone), 0, 1)
        
        if player.cccd:
            contact_layout.addWidget(QLabel("CCCD:"), 1, 0)
            contact_layout.addWidget(QLabel(player.cccd), 1, 1)
        
        if player.address:
            contact_layout.addWidget(QLabel("Địa chỉ:"), 2, 0)
            address_label = QLabel(player.address)
            address_label.setWordWrap(True)
            contact_layout.addWidget(address_label, 2, 1)
        
        scroll_layout.addWidget(contact_group)
        
        # Set up scroll area
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Close button
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet("QPushButton { background-color: #95a5a6; color: white; padding: 8px; font-weight: bold; }")
        layout.addWidget(close_btn)
        
        dialog.exec_()

    def export_to_json(self):
        """Export player data to JSON file"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getSaveFileName(
                self, "Xuất dữ liệu", "players_data.json", "JSON Files (*.json)"
            )
            
            if filename:
                players_data = []
                for player in self.all_players:
                    player_dict = player.to_dict()
                    # Convert ObjectId and datetime to string for JSON serialization
                    if '_id' in player_dict:
                        player_dict['_id'] = str(player_dict['_id'])
                    if 'contract_start' in player_dict and player_dict['contract_start']:
                        player_dict['contract_start'] = player_dict['contract_start'].isoformat()
                    if 'contract_end' in player_dict and player_dict['contract_end']:
                        player_dict['contract_end'] = player_dict['contract_end'].isoformat()
                    players_data.append(player_dict)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(players_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "Thành công", f"Đã xuất {len(players_data)} cầu thủ ra file JSON!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi xuất dữ liệu: {str(e)}")

    def import_from_json(self):
        """Import player data from JSON file"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            
            filename, _ = QFileDialog.getOpenFileName(
                self, "Nhập dữ liệu", "", "JSON Files (*.json)"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    players_data = json.load(f)
                
                imported_count = 0
                skipped_count = 0
                
                for player_dict in players_data:
                    try:
                        # Remove _id if exists to avoid conflicts
                        if '_id' in player_dict:
                            del player_dict['_id']
                        
                        # Convert date strings back to date objects
                        if 'contract_start' in player_dict and player_dict['contract_start']:
                            player_dict['contract_start'] = datetime.fromisoformat(player_dict['contract_start']).date()
                        if 'contract_end' in player_dict and player_dict['contract_end']:
                            player_dict['contract_end'] = datetime.fromisoformat(player_dict['contract_end']).date()
                        
                        # Check if jersey number already exists
                        if self.players_col.find_one({"jersey_number": player_dict.get("jersey_number")}):
                            skipped_count += 1
                            continue
                        
                        # Insert player
                        self.players_col.insert_one(player_dict)
                        imported_count += 1
                        
                    except Exception as e:
                        print(f"Error importing player: {e}")
                        skipped_count += 1
                        continue
                
                message = f"Đã nhập {imported_count} cầu thủ thành công!"
                if skipped_count > 0:
                    message += f"\nBỏ qua {skipped_count} cầu thủ (trùng số áo hoặc lỗi dữ liệu)"
                
                QMessageBox.information(self, "Kết quả nhập", message)
                self.load_players()
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi khi nhập dữ liệu: {str(e)}")

    def show_statistics_dialog(self):
        """Show detailed statistics in a dialog"""
        from PyQt5.QtWidgets import QDialog
        
        dialog = QDialog(self)
        dialog.setWindowTitle("📊 Thống kê chi tiết")
        dialog.setMinimumSize(600, 500)
        dialog.setModal(True)
        
        layout = QVBoxLayout(dialog)
        
        # Title
        title = QLabel("📊 THỐNG KÊ CHI TIẾT")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Create tabs for different statistics
        tab_widget = QTabWidget()
        
        # General statistics tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)
        
        if hasattr(self, 'all_players') and self.all_players:
            total_players = len(self.all_players)
            avg_age = sum(p.age for p in self.all_players) / total_players
            total_goals = sum(p.goals for p in self.all_players)
            total_matches = sum(p.matches_played for p in self.all_players)
            total_assists = sum(p.assists for p in self.all_players)
            total_yellow = sum(p.yellow_cards for p in self.all_players)
            total_red = sum(p.red_cards for p in self.all_players)
            
            general_stats = QGroupBox("Thống kê chung")
            general_stats_layout = QGridLayout(general_stats)
            
            general_stats_layout.addWidget(QLabel("Tổng số cầu thủ:"), 0, 0)
            general_stats_layout.addWidget(QLabel(str(total_players)), 0, 1)
            general_stats_layout.addWidget(QLabel("Tuổi trung bình:"), 1, 0)
            general_stats_layout.addWidget(QLabel(f"{avg_age:.1f}"), 1, 1)
            general_stats_layout.addWidget(QLabel("Tổng bàn thắng:"), 2, 0)
            general_stats_layout.addWidget(QLabel(str(total_goals)), 2, 1)
            general_stats_layout.addWidget(QLabel("Tổng trận đấu:"), 3, 0)
            general_stats_layout.addWidget(QLabel(str(total_matches)), 3, 1)
            general_stats_layout.addWidget(QLabel("Tổng kiến tạo:"), 4, 0)
            general_stats_layout.addWidget(QLabel(str(total_assists)), 4, 1)
            general_stats_layout.addWidget(QLabel("Tổng thẻ vàng:"), 5, 0)
            general_stats_layout.addWidget(QLabel(str(total_yellow)), 5, 1)
            general_stats_layout.addWidget(QLabel("Tổng thẻ đỏ:"), 6, 0)
            general_stats_layout.addWidget(QLabel(str(total_red)), 6, 1)
            
            general_layout.addWidget(general_stats)
        
        tab_widget.addTab(general_tab, "Tổng quan")
        
        # Position distribution tab
        position_tab = QWidget()
        position_layout = QVBoxLayout(position_tab)
        
        position_group = QGroupBox("Phân bố theo vị trí")
        position_table = QTableWidget()
        position_table.setColumnCount(3)
        position_table.setHorizontalHeaderLabels(["Vị trí", "Số lượng", "Tỷ lệ (%)"])
        
        if hasattr(self, 'all_players') and self.all_players:
            position_count = {}
            for player in self.all_players:
                position_count[player.position] = position_count.get(player.position, 0) + 1
            
            position_table.setRowCount(len(position_count))
            row = 0
            for position, count in sorted(position_count.items()):
                percentage = (count / total_players) * 100
                position_table.setItem(row, 0, QTableWidgetItem(position))
                position_table.setItem(row, 1, QTableWidgetItem(str(count)))
                position_table.setItem(row, 2, QTableWidgetItem(f"{percentage:.1f}%"))
                row += 1
        
        position_table.resizeColumnsToContents()
        position_layout.addWidget(position_table)
        tab_widget.addTab(position_tab, "Vị trí")
        
        # Top performers tab
        performers_tab = QWidget()
        performers_layout = QVBoxLayout(performers_tab)
        
        if hasattr(self, 'all_players') and self.all_players:
            # Top scorers
            top_scorers_group = QGroupBox("Top 5 Vua phá lưới")
            top_scorers_table = QTableWidget()
            top_scorers_table.setColumnCount(4)
            top_scorers_table.setHorizontalHeaderLabels(["Tên", "Vị trí", "Bàn thắng", "Tỷ lệ/trận"])
            
            top_scorers = sorted(self.all_players, key=lambda x: x.goals, reverse=True)[:5]
            top_scorers_table.setRowCount(len(top_scorers))
            
            for i, player in enumerate(top_scorers):
                ratio = player.goals / player.matches_played if player.matches_played > 0 else 0
                top_scorers_table.setItem(i, 0, QTableWidgetItem(player.name))
                top_scorers_table.setItem(i, 1, QTableWidgetItem(player.position))
                top_scorers_table.setItem(i, 2, QTableWidgetItem(str(player.goals)))
                top_scorers_table.setItem(i, 3, QTableWidgetItem(f"{ratio:.2f}"))
            
            top_scorers_table.resizeColumnsToContents()
            
            scorers_layout = QVBoxLayout(top_scorers_group)
            scorers_layout.addWidget(top_scorers_table)
            performers_layout.addWidget(top_scorers_group)
            
            # Top assisters
            top_assisters_group = QGroupBox("Top 5 Kiến tạo")
            top_assisters_table = QTableWidget()
            top_assisters_table.setColumnCount(4)
            top_assisters_table.setHorizontalHeaderLabels(["Tên", "Vị trí", "Kiến tạo", "Tỷ lệ/trận"])
            
            top_assisters = sorted(self.all_players, key=lambda x: x.assists, reverse=True)[:5]
            top_assisters_table.setRowCount(len(top_assisters))
            
            for i, player in enumerate(top_assisters):
                ratio = player.assists / player.matches_played if player.matches_played > 0 else 0
                top_assisters_table.setItem(i, 0, QTableWidgetItem(player.name))
                top_assisters_table.setItem(i, 1, QTableWidgetItem(player.position))
                top_assisters_table.setItem(i, 2, QTableWidgetItem(str(player.assists)))
                top_assisters_table.setItem(i, 3, QTableWidgetItem(f"{ratio:.2f}"))
            
            top_assisters_table.resizeColumnsToContents()
            
            assisters_layout = QVBoxLayout(top_assisters_group)
            assisters_layout.addWidget(top_assisters_table)
            performers_layout.addWidget(top_assisters_group)
        
        tab_widget.addTab(performers_tab, "Xuất sắc")
        
        layout.addWidget(tab_widget)
        
        # Close button
        close_btn = QPushButton("Đóng")
        close_btn.clicked.connect(dialog.close)
        close_btn.setStyleSheet("QPushButton { background-color: #95a5a6; color: white; padding: 8px; font-weight: bold; }")
        layout.addWidget(close_btn)
        
        dialog.exec_()

    def add_toolbar_buttons(self):
        """Add toolbar with quick action buttons"""
        from PyQt5.QtWidgets import QToolBar
        
        toolbar = QToolBar("Công cụ", self)
        
        # Statistics button
        stats_btn = QPushButton("📊 Thống kê")
        stats_btn.clicked.connect(self.show_statistics_dialog)
        stats_btn.setStyleSheet("QPushButton { background-color: #9b59b6; color: white; padding: 5px; margin: 2px; }")
        toolbar.addWidget(stats_btn)
        
        # Export button
        export_btn = QPushButton("📤 Xuất JSON")
        export_btn.clicked.connect(self.export_to_json)
        export_btn.setStyleSheet("QPushButton { background-color: #f39c12; color: white; padding: 5px; margin: 2px; }")
        toolbar.addWidget(export_btn)
        
        # Import button
        import_btn = QPushButton("📥 Nhập JSON")
        import_btn.clicked.connect(self.import_from_json)
        import_btn.setStyleSheet("QPushButton { background-color: #e67e22; color: white; padding: 5px; margin: 2px; }")
        toolbar.addWidget(import_btn)
        
        return toolbar

    def backup_database(self):
        """Create backup of current database"""
        try:
            from PyQt5.QtWidgets import QFileDialog
            import os
            
            # Default filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_filename = f"backup_players_{timestamp}.json"
            
            filename, _ = QFileDialog.getSaveFileName(
                self, "Sao lưu dữ liệu", default_filename, "JSON Files (*.json)"
            )
            
            if filename:
                # Get all data from database
                all_data = list(self.players_col.find())
                
                # Convert ObjectId and datetime for JSON serialization
                for item in all_data:
                    if '_id' in item:
                        item['_id'] = str(item['_id'])
                    if 'contract_start' in item and item['contract_start']:
                        if isinstance(item['contract_start'], date):
                            item['contract_start'] = item['contract_start'].isoformat()
                    if 'contract_end' in item and item['contract_end']:
                        if isinstance(item['contract_end'], date):
                            item['contract_end'] = item['contract_end'].isoformat()
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(all_data, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "Thành công", f"Đã sao lưu {len(all_data)} bản ghi vào file backup!")
                
        except Exception as e:
            QMessageBox.critical(self, "Lỗı̂", f"Lỗi khi sao lưu: {str(e)}")

    # Thêm vào hàm setup_ui() trong class chính:
    def setup_ui_additions(self):
        """Additional UI setup - call this at the end of setup_ui()"""
        
        # Add toolbar to main layout (insert after title)
        toolbar = self.add_toolbar_buttons()
        # Cần thêm toolbar vào layout chính
        
        # Connect additional signals
        self.connect_additional_signals()

    def connect_additional_signals(self):
        """Connect additional signals for new features"""
        # These would be connected to keyboard shortcuts or additional buttons
        pass