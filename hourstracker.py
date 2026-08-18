import time
import datetime
import tkinter
import customtkinter
import sqlite3

root = tkinter.Tk()
root.title("Hours tracker")
root.geometry("300x100")

# Purple palette test
#background_color = "#0e0b12"
#button_color = "#3a1c42"
#label_color = "#6a2c6b"
#color_of_text = "#f2d7f7"

# More professional purple
background_color = "#1E1E1E"
button_color = "#3a1c42"
label_color = "#1E1E1E"
color_of_text = "#B0B0B0"
text_font = customtkinter.CTkFont(family="Century Gothic", size=12, weight="bold")

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

        # Check to see if the tracker is paused or not
        self.time_ticking = None

        # Stores the total amount of time in a single session
        self.session_amount = 0

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

        # The tracker label
        self.ui_label = customtkinter.CTkLabel(root, 
        text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.", 
        bg_color=background_color, fg_color=label_color, text_color=color_of_text, font=text_font)
        self.ui_label.grid(row=0, column=0, sticky="nsew")

        # Pause button
        self.pause_button = customtkinter.CTkButton(root, 
        text="Pause", command=self.pause_timer, bg_color=background_color, fg_color=button_color, text_color=color_of_text,
        font=text_font)
        self.pause_button.grid(row=2, column=0, sticky="s")

        # Grabbing the database row to have the two weeks average
        two_weeks_average = "SELECT SUM(duration) FROM sessions WHERE date >= datetime('now', '-14 days')"
        cursor.execute(two_weeks_average)
        last_14_sessions = cursor.fetchone()[0]

        # Turning the sum of everything into a decimal number
        hours = round(last_14_sessions / 3600, 1)

        connection.commit()
        

        # Two weeks average label
        self.average_time_label = customtkinter.CTkLabel(root, 
        text=f"Last two weeks average: {hours} hours", bg_color=background_color, text_color=color_of_text, fg_color=label_color
        , font=text_font)
        self.average_time_label.grid(row=1, column=0, sticky="nsew")

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)


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

        self.time_ticking = root.after(1000, self.tracking_hours)

    def update_ui(self):

        # This part is JUST the data that goes into the label, it grabs the finished_time which is the latest value
        # and then it changes the float into hours and minutes
        self.hours_label = self.finished_time
        hours_in_the_float = round(self.hours_label) // 3600
        seconds_without_hours = round(self.hours_label) % 3600
        minutes = seconds_without_hours // 60
        seconds_modulo = seconds_without_hours % 60

        self.ui_label.configure(text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.")

        self.updating_label = root.after(1000, self.update_ui)

        

    def pause_timer(self):
        self.is_time_paused = not self.is_time_paused

        if self.is_time_paused:
            self.pause_button.configure(text="Unpause")
            root.after_cancel(self.updating_label)

            current_date = datetime.date.today()
            cursor.execute("INSERT INTO sessions (date, duration) VALUES (?, ?)", (str(current_date), self.session_amount))
            connection.commit()
            
        else:
            self.pause_button.configure(text="Pause")
            self.update_ui()
            

    
    def close_app(self):
        end_time = time.time()
        self.finished_time = end_time - self.start_time - self.time_spent_paused
        self.finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(self.finished_time))

        # Remember to use the parentheses to call the function, dummy
        current_date = datetime.date.today()
        
        
        cursor.execute("INSERT INTO sessions (date, duration) VALUES (?, ?)", (str(current_date), self.session_amount))
        connection.commit()
        connection.close()

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