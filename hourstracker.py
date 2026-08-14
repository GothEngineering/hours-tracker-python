import time
import datetime
import tkinter
import customtkinter
import sqlite3

root = tkinter.Tk()
root.title("Hours tracker")
root.geometry("300x200")

background_color = "#2a2a41"
button_color = "#5c0603"

root.config(bg=background_color)

connection = sqlite3.connect("time_invested.db")

cursor = connection.cursor()

tables_creation = """CREATE TABLE IF NOT EXISTS
sessions(
id INTEGER PRIMARY KEY, 
date TEXT, 
duration INTEGER
)"""

cursor.execute(tables_creation)

# TO DO:
# Add a way to track the time invested in a session and then add it to a date 
# and somehow calculate the time spent in the last two weeks (i know u can do it pal), modernize it into customtkinter

class HoursTracker():

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

        # Just a check so Python doesn't throw an error 
        self.time_ticking = None

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

        # Remember to organize these buttons, sorry for the mess
        self.ui_label = tkinter.Label(root, text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.", 
                                      bg=button_color, fg="white")
        self.ui_label.pack()

        self.pause_button = tkinter.Button(root, text="Pause", command=self.pause_timer, bg=button_color)
        self.pause_button.pack()


    def tracking_hours(self):  

        if self.is_time_paused:
            self.time_spent_paused += 1
            print(self.time_spent_paused)      
        
        # This part here simply updates the time because it does this operation whenever I refresh
        # The finished_time value grows bigger because it adds the latest end_time and it simply adds it up to the current_time variable
        # It substracts the time paused so it doesn't wake up and skips to the boring present
        end_time = time.time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        self.time_ticking = root.after(1000, self.tracking_hours)

    def update_ui(self):

        # This part is JUST the data that goes into the label, it grabs the finished_time which is the latest value
        # and then it changes the float into hours and minutes
        self.hours_label = self.finished_time
        hours_in_the_float = round(self.hours_label) // 3600
        seconds_without_hours = round(self.hours_label) % 3600
        minutes = seconds_without_hours // 60
        seconds_modulo = seconds_without_hours % 60

        self.ui_label.config(text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.")

        self.updating_label = root.after(1000, self.update_ui)

        

    def pause_timer(self):
        self.is_time_paused = not self.is_time_paused

        if self.is_time_paused:
            self.pause_button.configure(text="Unpause")
            root.after_cancel(self.updating_label)
            
            print(f"Tengo ahora mismo un {self.time_spent_paused}")

        else:
            self.pause_button.configure(text="Pause")
            self.update_ui()
            print(f"mreow ahora tengo {self.time_spent_paused}")


    def close_app(self):
        end_time = time.time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))
    

        root.destroy()


    def auto_save(self):
        end_time = time.time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))
    
        root.after(120000, self.auto_save)




tracker = HoursTracker()


root.protocol("WM_DELETE_WINDOW", tracker.close_app)

root.after(500, tracker.tracking_hours)
root.after(500, tracker.update_ui)
root.after(60000, tracker.auto_save)
root.mainloop()