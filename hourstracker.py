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


# TO DO:
# Lay the groundwork for sqlite3, find a way to pause the app, modernize it into customtkinter
# im just kinda eepy

class HoursTracker():

    def __init__(self):
        # This part grabs the time as soon as it opens the app
        self.start_time = time.time()

        # This variable gets filled with the content of the notepad
        self.current_time = 0

        # This variable manages the label that shows the hours, it is used to turn the float into time
        self.hours_label = 0

        #
        self.is_time_paused = False
        self.time_while_paused = 0


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


    def update_ui(self):  

        # This part here simply updates the time because it does this operation whenever I refresh
        # The finished_time value grows bigger because it adds the latest end_time and it simply adds it up to the current_time variable
        end_time = time.time()
        finished_time = end_time - self.start_time
        finished_time += float(self.current_time)

        # This part is JUST the data that goes into the label, it grabs the finished_time which is the latest value
        # and then it changes the float into hours and minutes
        self.hours_label = finished_time
        hours_in_the_float = round(self.hours_label) // 3600
        seconds_without_hours = round(self.hours_label) % 3600
        minutes = seconds_without_hours // 60
        seconds_modulo = seconds_without_hours % 60

        self.ui_label.config(text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.")

        time_ticking = root.after(1000, self.update_ui)

        if self.is_time_paused:
            root.after_cancel(time_ticking)

        

    def close_app(self):
        end_time = time.time()
        finished_time = end_time - self.start_time
        finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(finished_time))
    

        root.destroy()


    def auto_save(self):
        end_time = time.time()
        finished_time = end_time - self.start_time
        finished_time += float(self.current_time)

        with open("hours", "w") as f:
            f.write(str(finished_time))
    
        root.after(120000, self.auto_save)

    def pause_timer(self):
        self.is_time_paused = not self.is_time_paused
        if self.is_time_paused:
            self.pause_button.configure(text="Unpause")
        else:
            self.pause_button.configure(text="Pause")


tracker = HoursTracker()


root.protocol("WM_DELETE_WINDOW", tracker.close_app)

root.after(1000, tracker.update_ui)
root.after(60000, tracker.auto_save)
root.mainloop()