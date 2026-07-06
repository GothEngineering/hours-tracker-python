import time
import datetime
import tkinter

# This part grabs the time as soon as it opens the app
start_time = time.time()

# This variable gets filled with the content of the notepad
current_time = 0


hours_label = 0

root = tkinter.Tk()
root.title("Hours tracker")

# Creating a text file if there is not one
try:
    with open("horas", "x") as f:
        f.write("0")
except FileExistsError:
    print("Opening the file")


# Reading the notepad so it adds to the current_time variable on start up
with open("horas", "r") as f:
    total_hours = f.read()
    current_time = total_hours
    
    float_time = float(current_time)
    
    hours = float_time
    #
    hours_label = f"{hours}"
    

def refresh_data():
    # Please change this global variable for later, it can cause issues (supposedly)
    global hours_label

    # This part here simply updates the time because it does this operation whenever i refresh.
    # The finished_time value grows bigger because it adds the latest end_time and it simply adds it up to the current_time variable
    # SO that's where the number goes up!!
    end_time = time.time()
    finished_time = end_time - start_time
    finished_time += float(current_time)

    # This part is JUST the data that goes into the label, it grabs the finished_time which is the latest value
    # and then it rounds it to get hours and minutes respectively. 
    hours_label = finished_time
    hours_in_the_float = round(hours_label) // 3600
    seconds_without_hours = round(hours_label) % 3600
    minutes = seconds_without_hours // 60

    ui_label.config(text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes")


#def start_tracking():
    #pass

def close_app():
    end_time = time.time()
    finished_time = end_time - start_time
    finished_time += float(current_time)

    with open("horas", "w") as f:
        f.write(str(finished_time))
    

    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)



ui_label = tkinter.Label(root, text=f"Time invested: {hours_label}", bg="gray", fg="white")
ui_label.pack(fill="both", expand=True)

# Didn't found a practical purpose to this button but maybe i'll add use to it someday
#timer_start = tkinter.Button(root, text="Start", width=10, bg="gray")
#timer_start.pack(fill="both", expand=True)

refresh_button = tkinter.Button(root, text="Refresh", width=5, bg="gray", command=refresh_data)
refresh_button.pack(fill="both", expand=True)




root.mainloop()