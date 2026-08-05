import time
import datetime
import tkinter
import customtkinter


root = tkinter.Tk()
root.title("Hours tracker")
root.geometry("300x200")


class HoursTracker():

    def __init__(self):
        # This part grabs the time as soon as it opens the app
        self.start_time = time.time()

        # This variable gets filled with the content of the notepad
        self.current_time = 0

        # This variable manages the label that shows the hours, it is used to turn the float into time
        self.hours_label = 0


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

        self.ui_label = tkinter.Label(root, text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.", 
                                      bg="gray", fg="white")
        self.ui_label.pack()



    def update_ui(self):
        # Please change this global variable for later, it can cause issues (I think)
        global hours_label

        # This part here simply updates the time because it does this operation whenever I refresh
        # The finished_time value grows bigger because it adds the latest end_time and it simply adds it up to the current_time variable
        end_time = time.time()
        finished_time = end_time - self.start_time
        finished_time += float(self.current_time)

        # This part is JUST the data that goes into the label, it grabs the finished_time which is the latest value
        # and then it changes the float into hours and minutes
        hours_label = finished_time
        hours_in_the_float = round(hours_label) // 3600
        seconds_without_hours = round(hours_label) % 3600
        minutes = seconds_without_hours // 60
        seconds_modulo = seconds_without_hours % 60

        self.ui_label.config(text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.")

        test_lmao = root.after(1000, self.update_ui)
        

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


tracker = HoursTracker()


root.protocol("WM_DELETE_WINDOW", tracker.close_app)

root.after(1000, tracker.update_ui)
root.after(60000, tracker.auto_save)
root.mainloop()