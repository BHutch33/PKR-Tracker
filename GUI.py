import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem

class PKRApp(QWidget):
  # Initialization
  def __init__(self):
    super().__init__()
    self.init_ui()

  # Initialize UI
  def init_ui(self):
    self.setWindowTitle("PKR Tracker")
    self.setGeometry(100, 100, 600, 400)

    layout = QVBoxLayout()

    self.table = QTableWidget()
    self.load_data()
    layout.addWidget(self.table)

    # Refresh button
    refresh_button = QPushButton("Refresh Data")
    refresh_button.clicked.connect(self.load_data)
    layout.addWidget(refresh_button)

    self.setLayout(layout)
  
  def load_data(self):
    # Connect to database
    conn = sqlite3.connect("Poker_tracker.db")
    cursor = conn.cursor()

    # Grab all sessions
    cursor.execute("SELECT * FROM sessions ORDER BY date DESC")
    sessions = cursor.fetchall()

    # Disconnect from database
    conn.close()

    self.table.setRowCount(len(sessions))
    self.table.setColumnCount(5)
    self.table.setHorizontalHeaderLabels(["ID", "Date", "Location", "Buy-in", "Cash-out"])

    for row_idx, session in enumerate(sessions):
      for col_idx, value in enumerate(session[:5]):
        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

app = QApplication(sys.argv)
window = PKRApp()
window.show()
sys.exit(app.exec())
