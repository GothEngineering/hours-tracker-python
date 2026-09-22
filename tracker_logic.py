import sqlite3
from time import time
from datetime import date

connection = sqlite3.connect("time_invested.db")

cursor = connection.cursor()

tables_creation = """CREATE TABLE IF NOT EXISTS
sessions(
id INTEGER PRIMARY KEY, 
date TEXT, 
duration INTEGER
)"""

cursor.execute(tables_creation)

class trackerLogic:

    def __init__(self):
        # This part grabs the time as soon as it opens the app
        self.start_time = time.time()

        # This variable gets filled with the content of the notepad
        self.current_time = 0

        # This variable manages the label that shows the hours, it is used to turn the float into time
        self.hours_label = 0

        # The variable that changes if the pause button is pressed
        self.is_time_paused = False

        # Variable that stores the total amount paused so the tracker doesn't skip to the present after unpausing it
        self.time_spent_paused = 0

        # Check to see if the tracker is paused or not
        self.time_ticking = None

        # Stores the total amount of time in a single session
        self.session_amount = 0

        # Empty variable so the average time can be stored
        self.rounded_hours = 0.0

        # Creating a text file if there is not one
        try:
            with open("hours", "x") as f:
                f.write("0")
        except FileExistsError:
            print("Opening the file")



        # Reading the notepad so it adds to the current_time variable on start up
        with open("hours", "r") as f:
            self.total_hours = f.read()
            self.current_time = self.total_hours
    
            # This part right here simply turns the text from an string to a float so i can use it for the labels
            float_time = float(self.current_time)
            self.hours_label = float_time
    
            # Float into hours and minutes respectively
            hours_in_the_float = round(self.hours_label) // 3600
            seconds_without_hours = round(self.hours_label) % 3600
            minutes = seconds_without_hours // 60
            seconds_modulo = seconds_without_hours % 60

        # Grabbing the database row to have the two weeks average

        self.two_weeks_average = "SELECT SUM(duration) FROM sessions WHERE date >= datetime('now', '-14 days')"
        cursor.execute(self.two_weeks_average)
        last_14_sessions = cursor.fetchone()[0]

        # Turning the sum of everything into a decimal number
        # This prevents a crash when opening the app for the first time
        if last_14_sessions == None:
            pass
        else:
            # Grabbing the average by dividing it with the total
            avg_seconds = last_14_sessions / 14
            self.rounded_hours = round(avg_seconds / 3600, 1)

        connection.commit()


    def tracking_hours(self):
        
        if self.is_time_paused:
            self.time_spent_paused += 1    
        
        else:
            self.session_amount += 1
            
        # This part here simply updates the time because it does this operation whenever I refresh
        # The finished_time value grows bigger because it adds the latest end_time and it simply adds it up to the current_time variable
        # It substracts the time paused so it doesn't wake up and skips to the boring present
        end_time = time.time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        self.time_ticking = self.root.after(1000, self.tracking_hours)

# move the functions for the butttons into UI, and also maybe i should add the database
# and the label there too.. 

    def auto_save(self):
        end_time = time.time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))
    
        self.root.after(120000, self.auto_save)
        