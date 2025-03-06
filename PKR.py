import sqlite3

# Here is where I would like to start creating some functions for the program. These will utilize
# SQLite3 databases.

conn = sqlite3.connect("poker_tracker.db")
cursor = conn.cursor()

# Function to create a fresh database entry for the poker session
def create_db_session():
  cursor.execute("""
  CREATE TABLE IF NOT EXISTS sessions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      date TEXT,
      location TEXT,
      buy_in REAL,
      cash_out REAL,
      hours_played REAL,
      net_profit REAL
  )
  """)

# Now that we created the table, we can commit it and close the connection to the database
conn.commit()
conn.close()


# Helper function to add sessions to the database
def add_session(date, location, buy_in, cash_out, hours_played):
  try:
    net_profit = (cash_out - buy_in)
    conn = sqlite3.connect("poker_tracker.db")
    cursor = conn.cursor()

    cursor.execute("""
      INSERT INTO sessions (date, location, buy_in, cash_out, hours_played, net_profit)
      VALUES (?, ?, ?, ?, ?, ?)       
    """, (date, location, buy_in, cash_out, hours_played, net_profit))

    conn.commit()
    conn.close()
    return True
  except Exception as e:
     print("Database error: ", e)
     return False



# Function to create a session
def create_session():
  date = input("Date: ")
  location = input("Location: ")
  hours_played = float(input("Time played: "))
  buy_in = float(input("Buy-in: "))
  cash_out = float(input("Cash-out: "))

  add_session(date, location, buy_in, cash_out, hours_played)


# Function to delete a session
def delete_session(session_id: int):
    # Connect to the database
    conn = sqlite3.connect("poker_tracker.db")
    cursor = conn.cursor()

    # Debugging: Check if the session exists before deleting
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    session = cursor.fetchone()
    if session is None:
        print(f"Session ID {session_id} not found.")
        conn.close()
        return

    # Enable foreign keys in case constraints are blocking deletion
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Execute the delete statement
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    conn.commit()

    # Debugging: Verify if the session is still present
    cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
    remaining_session = cursor.fetchone()

    conn.close()

    if remaining_session:
        print(f"Session ID {session_id} was NOT deleted. Check constraints.")
    else:
        print(f"Session ID {session_id} deleted successfully.")


# Function to display a session
def display_session(session_id: int):
  # Connect to database
  conn = sqlite3.connect("poker_tracker.db")
  cursor = conn.cursor()
  
  # Get session
  cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
  session = cursor.fetchone()

  # Close connection
  conn.close

  # Display session after checking if it exists
  if session:
    print("\n--- Poker Session Summary ---")
    print(f"Date: {session[1]}")
    print(f"Location: {session[2]}")
    print(f"Buy-in: ${session[3]:.2f}")
    print(f"Cash-out: ${session[4]:.2f}")
    print(f"Duration: {session[5]} hours")
    print(f"Profit/Loss: ${session[4] - session[3]:.2f}")
    print("============================\n")
  else:
    print(f"Session with ID {session_id} not found.")


# Calculate net profit
def calculate_net_profit():
  # Connect to database
  conn = sqlite3.connect("poker_tracker.db")
  cursor = conn.cursor()

  # Grab total of both buy-in and cash-out
  cursor.execute("SELECT SUM(net_profit) FROM sessions")
  net_profit = cursor.fetchone()[0]

  # Close connection
  conn.close()

  # Check that total_buy_in exists
  if net_profit:
     return net_profit
  else:
     print("No win/loss to display.")


# Get total buyins
def get_total_buyins():
  conn = sqlite3.connect("poker_tracker.db")
  cursor = conn.cursor()

  try:
    cursor.execute("SELECT SUM(buy_in) FROM sessions")
    result = cursor.fetchone()
    print("Raw SQL Query Result:", result)

    total_buy_in = result[0] if result and result[0] is not None else 0
  
  except sqlite3.Error as e:
     print("SQLite Error:", e)
     total_buy_in = 0
  
  finally:
     conn.close()
  
  return total_buy_in


# Display poker history
def display_poker_history():
  # Connect to database
  conn = sqlite3.connect("poker_tracker.db")
  cursor = conn.cursor()

  # Get all sessions and order by date
  cursor.execute("SELECT * FROM sessions ORDER BY date DESC")
  sessions = cursor.fetchall()

  # Close connection to database
  conn.close()

  # Check to make sure there are sessions
  if not sessions:
    print("\nNo session history found.")
    return

  # Print session history
  print("\n--- Poker Session History ---")
  print("{:<5} {:<12} {:<15} {:<5} {:<10} {:<10} {:<10}".format("ID", "Date", "Location", "Duration", "Buy-in", "Cash-out", "Profit/Loss"))
  print("-" * 80)

  for session in sessions:
    session_id, date, location, buy_in, cash_out, duration, profit_loss = session
    profit_loss = cash_out - buy_in
    print("{:<5} {:<12} {:<15} {:<9.1f} ${:<9.2f} ${:<9.2f} ${:<+9.2f}".format(
            session_id, date, location, duration, buy_in, cash_out, profit_loss
    ))
  
  print("-" * 80)


# Calculate hourly winrate
def calculate_winrate():
  # Connect to database
  conn = sqlite3.connect("poker_tracker.db")
  cursor = conn.cursor()

  # Collect total profit/loss
  cursor.execute("SELECT SUM(net_profit) FROM sessions")
  profit_loss = cursor.fetchone()[0]
  
  # Collect total duration
  cursor.execute("SELECT SUM(hours_played) FROM sessions")
  duration = cursor.fetchone()[0]

  # Close database
  conn.close()


  winrate = profit_loss / duration
  return winrate