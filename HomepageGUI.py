from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from PKR import add_session
import sqlite3

class PKRTracker(QMainWindow):
  def __init__(self):
    super().__init__()

    self.setWindowTitle("PKR Tracker")
    self.setGeometry(100, 100, 800, 600)

    # Create a stacked widget (for switching pages)
    self.stacked_widget = QStackedWidget()
    self.setCentralWidget(self.stacked_widget)

    # Create pages
    self.home_page = self.create_home_page()
    self.history_page = self.create_history_page()
    self.add_session_page = self.create_add_session_page()

    # Add pages to stacked widget
    self.stacked_widget.addWidget(self.home_page)
    self.stacked_widget.addWidget(self.history_page)
    self.stacked_widget.addWidget(self.add_session_page)

    # Display homepage first
    self.stacked_widget.setCurrentWidget(self.home_page)

  
  # Create the homepage
  def create_home_page(self):
    page = QWidget()
    layout = QVBoxLayout()

    # Create label and buttons
    label = QLabel("Welcome to PKR Tracker!")
    btn_history = QPushButton("View Session History")
    btn_add_session = QPushButton("Add New Session")

    # Change history and add session button sizes
    button_font = QFont("Arial", 35)
    btn_history.setFont(button_font)
    btn_add_session.setFont(button_font)

    # Change label font and size
    font = QFont("Arial", 50)
    label.setFont(font)

    # Center label
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    # Connect buttons to pages
    btn_history.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.history_page))
    btn_add_session.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.add_session_page))

    # Set the layout of the page
    layout.addWidget(label)
    layout.addWidget(btn_history)
    layout.addWidget(btn_add_session)
    page.setLayout(layout)
    return page

  # Create session history page
  def create_history_page(self):
    page = QWidget()
    layout = QVBoxLayout()
    
    # Title label
    label = QLabel("Poker Session History")
    layout.addWidget(label)

    # Create a table
    self.table = QTableWidget()
    layout.addWidget(self.table)

    # Load session data into the table
    self.load_poker_history()

    # Create back button
    btn_back = QPushButton("Return to Home")
    btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
    layout.addWidget(btn_back)

    page.setLayout(layout)
    return page

  # Helper function to load poker history
  def load_poker_history(self):
    # Connect to database
    conn = sqlite3.connect("poker_tracker.db")
    cursor = conn.cursor()

    # Get all sessions and order by date
    cursor.execute("SELECT date, location, hours_played, buy_in, cash_out, net_profit FROM sessions ORDER BY date DESC")
    sessions = cursor.fetchall()

    # Close connection to database
    conn.close()

    # Create table  
    headers = ["Date", "Location", "Duration", "Buy-in", "Cash-out", "Profit/Loss"]
    self.table.setColumnCount(len(headers))
    self.table.setHorizontalHeaderLabels(headers)
    self.table.setRowCount(len(sessions))
    
    # Populate table
    for row_idx, session in enumerate(sessions):
      date, location, duration, buy_in, cash_out, profit_loss = session

      row_data = [date, location, duration, buy_in, cash_out, profit_loss]

      for col_idx, value in enumerate(row_data):
        self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
    


  # Create add session page
  def create_add_session_page(self):
    page = QWidget()
    layout = QVBoxLayout()
    label = QLabel("Add New Poker Session")

    # Create fields for user to fill out regarding session
    self.date_input = QLineEdit()
    self.date_input.setPlaceholderText("Enter date (YYYY-MM-DD)")

    self.location_input = QLineEdit()
    self.location_input.setPlaceholderText("Enter location")

    self.duration_input = QLineEdit()
    self.duration_input.setPlaceholderText("Enter session duration (hours)")

    self.buy_in_input = QLineEdit()
    self.buy_in_input.setPlaceholderText("Buy-in amount")

    self.cash_out_input = QLineEdit()
    self.cash_out_input.setPlaceholderText("Cash-out amount")

    # Create a save button
    btn_save = QPushButton("Save session")
    btn_save.clicked.connect(self.handle_save_session)
    
    # Create back button
    btn_back = QPushButton("Return to Home")
    btn_back.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))

    # Create page layout
    layout.addWidget(label)
    layout.addWidget(self.date_input)
    layout.addWidget(self.location_input)
    layout.addWidget(self.duration_input)
    layout.addWidget(self.buy_in_input)
    layout.addWidget(self.cash_out_input)
    layout.addWidget(btn_save)
    layout.addWidget(btn_back)

    page.setLayout(layout)
    return page


  # Create function to handle saving sessions using PKR.py file
  def handle_save_session(self):
    date = self.date_input.text()
    location = self.location_input.text()
    duration = self.duration_input.text()
    
    try:
      buy_in = float(self.buy_in_input.text())
      cash_out = float(self.cash_out_input.text())
      duration = float(self.duration_input.text())
    except:
      msg_box = QMessageBox()
      msg_box.setIcon(QMessageBox.Icon.Critical)
      msg_box.setWindowTitle("Input Error")
      msg_box.setText("Buy-in, Cash-out and Duration fields must be numbers.")
      msg_box.exec()
      return
    
    # Call the function from PKR.py
    success = add_session(date, location, buy_in, cash_out, duration)

    # Check for successful addition
    if success:
      self.date_input.clear()
      self.location_input.clear()
      self.duration_input.clear()
      self.buy_in_input.clear()
      self.cash_out_input.clear()
      
      # Display success message
      msg_box = QMessageBox()
      msg_box.setIcon(QMessageBox.Icon.Information)
      msg_box.setWindowTitle("Success")
      msg_box.setText("Session saved successfully!")
      msg_box.exec()


if __name__ == "__main__":
  app = QApplication([])
  window = PKRTracker()
  window.show()
  app.exec()