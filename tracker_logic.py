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
        self.start_time = time()

        # This variable gets filled with the content of the notepad
        self.current_time = 0

        # Variable that stores the total amount paused so the tracker doesn't skip to the present after unpausing it
        self.time_spent_paused = 0

        # Check to see if the tracker is paused or not
        self.time_ticking = None

        # Stores the total amount of time in a single session
        self.session_amount = 0

        # Empty variable so the average time can be stored
        # maybe i have to move this to the UI, let me think
        self.rounded_hours = 0.0

        self.hours_in_the_float = 0
        self.minutes = 0
        self.seconds_modulo = 0


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


    
    def start_db(self):
        # Grabbing the database row to have the two weeks average

        self.two_weeks_average = "SELECT SUM(duration) FROM sessions WHERE date >= datetime('now', '-14 days')"
        cursor.execute(self.two_weeks_average)
        last_14_sessions = cursor.fetchone()[0]


        if last_14_sessions == None:
            pass
        else:
            # Grabbing the average by dividing it with the total
            avg_seconds = last_14_sessions / 14
            self.rounded_hours = round(avg_seconds / 3600, 1)
            return self.rounded_hours
    
    def start_logic(self):
        # Reading the notepad so it adds to the current_time variable on start up
        with open("hours", "r") as f:
            self.total_hours = f.read()
            self.current_time = self.total_hours
    
    def tracking_hours(self, is_paused):
        
        if is_paused == True:
            self.time_spent_paused += 1    
        
        else:
            self.session_amount += 1
            
        # This part here simply updates the time because it does this operation whenever I refresh
        # The finished_time value grows bigger because it adds the latest end_time and it simply adds it up to the current_time variable
        # It substracts the time paused so it doesn't wake up and skips to the boring present
        end_time = time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)



    # Returns the finished_time to the UI
    def get_finished_time(self):
        return self.finished_time
    
    
    # Triggers the auto save
    def autosave_logic(self):
        end_time = time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))
    

    def pause_n_save(self):
            
            current_date = date.today()
            cursor.execute("INSERT INTO sessions (date, duration) VALUES (?, ?)", (str(current_date), self.session_amount))
            connection.commit()

            cursor.execute(self.two_weeks_average)
            last_14_sessions = cursor.fetchone()[0]
            avg_seconds = last_14_sessions / 14
            self.rounded_hours = round(avg_seconds / 3600, 1)

            connection.commit()
            return self.rounded_hours
    
    
    # Check later if this variable is being properly used, I dont think it is
    def close_app(self, is_paused):
        end_time = time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))

        if is_paused == True:
            pass
        else:
            # Remember to use the parentheses to call the function, dummy
            current_date = date.today()
        
        
            cursor.execute("INSERT INTO sessions (date, duration) VALUES (?, ?)", (str(current_date), self.session_amount))
            connection.commit()
            connection.close()
