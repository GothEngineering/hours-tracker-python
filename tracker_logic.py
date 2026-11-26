import sqlite3
from time import time, monotonic
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
        # Why monotonic? to not get confused with start_time, duuh
        #self.active_time = monotonic()
        
        # This variable gets filled with the content of the notepad
        self.current_time = 0

        # Variable that stores the total time paused, this comes from the UI
        self.time_spent_paused = 0
        
        # Empty variable so the average time can be stored
        # maybe i have to move this to the UI, let me think
        self.rounded_hours = 0.0

        # test
        #self.duration = 0

        # Creating a text file if there is not one
        try:
            with open("hours", "x") as f:
                f.write("0")
        except FileExistsError:
            print("File exists, opening it now")



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
    

    def tracking_hours(self, total_paused_time):
        
        self.time_spent_paused = total_paused_time
        # Grabs the current time, substracts the beginning and the time paused, and adds the current time
        end_time = time()
        self.finished_time = end_time - self.start_time
        self.finished_time -= self.time_spent_paused
        self.finished_time += float(self.current_time)



    # Returns the finished_time to the UI
    def get_finished_time(self):
        # This part is JUST the data that goes into the label, it grabs the finished_time which is the latest value
        self.hours_label = self.finished_time
        self.hours_in_the_float = round(self.hours_label) // 3600
        self.seconds_without_hours = round(self.hours_label) % 3600
        self.minutes = self.seconds_without_hours // 60
        self.seconds_modulo = self.seconds_without_hours % 60

        
        return self.hours_in_the_float, self.minutes, self.seconds_modulo
    
    
    # Triggers the auto save
    def autosave_logic(self):
        end_time = time()
        self.finished_time = end_time - self.start_time
        self.finished_time -= self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))
    

    # This function purpose is that it saves to the database when pausing. It's different from the UI pause function
    # The reason I made it separate was to not use the auto save on the db saving
    def pause_n_save(self, total_duration):
            self.duration = total_duration
            
            current_date = date.today()
            cursor.execute("INSERT INTO sessions (date, duration) VALUES (?, ?)", (str(current_date), round(self.duration)))
            connection.commit()

            cursor.execute(self.two_weeks_average)
            last_14_sessions = cursor.fetchone()[0]
            avg_seconds = last_14_sessions / 14
            self.rounded_hours = round(avg_seconds / 3600, 1)

            return self.rounded_hours
    
    
    # Keep an eye on this function, I feel it's wrong somehow
    def close_app(self, is_paused, total_duration):
        self.duration = total_duration
        end_time = time()
        self.finished_time = end_time - self.start_time
        self.finished_time -= self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))

        if is_paused:
            pass
        else:
            # Remember to use the parentheses to call the function, dummy
            current_date = date.today()
        
        
            cursor.execute("INSERT INTO sessions (date, duration) VALUES (?, ?)", (str(current_date), round(self.duration)))
            connection.commit()
            connection.close()


# TO DO: Fix the weird delay on the UI when unpausing and it'll be finished...