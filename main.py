import PKR
import os

# This is going to be the start of my project to make a Poker Tracker (PKR Tracker) for myself

# Check that database is being loaded properly
db_path = "poker_tracker.db" 

if os.path.exists(db_path):
  print(f"\nDatabase {db_path} exists.")
else:
  print(f"\nDatabase {db_path} not found")

# Print win/loss
winloss = PKR.calculate_net_profit()
print("\nTotal net win/loss: ${:+.2f}".format(winloss))

# Print winrate
winrate = PKR.calculate_winrate()
print("\nWinrate: ${:+.2f}/hr".format(winrate))

PKR.display_poker_history()

PKR.create_session()
