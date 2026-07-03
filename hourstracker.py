import time
import datetime
import tkinter

start_time = time.time()
current_time = 0
hours_label = 0

root = tkinter.Tk()
root.title("Hours tracker")

# Creating a file if there is not one
try:
    with open("horas", "x") as f:
        f.write("0")
except FileExistsError:
    print("Opening the file")


# Reading the file so it adds to the current_time variable
with open("horas", "r") as f:
    total_hours = f.read()
    current_time = total_hours
    float_time = float(current_time)
    
    hours = float_time
    #hours, remainder = divmod(float_time, 3600)
    #minutes, remainder = divmod(remainder, 60)
    hours_label = f"{hours}"
    
    print(current_time)    


def refresh_data():
    end_time = time.time()
    finished_time = end_time - start_time
    finished_time += float(current_time)
    
    hours_label.update()

def close_app():
    end_time = time.time()
    finished_time = end_time - start_time
    finished_time += float(current_time)

    with open("horas", "w") as f:
        f.write(str(finished_time))
    

    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_app)



hours_label = tkinter.Label(root, text=f"Time invested: {hours_label}", bg="gray", fg="white")
hours_label.pack(fill="both", expand=True)

timer_start = tkinter.Button(root, text="Start", width=10, bg="gray")
timer_start.pack(fill="both", expand=True)

refresh_button = tkinter.Button(root, text="Refresh", width=5, bg="gray", command=refresh_data)
refresh_button.pack(fill="both", expand=True)

root.mainloop()