import time
import datetime
import tkinter

start_time = time.time()
current_time = 0

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
    print(current_time)
    

def close_app():
    end_time = time.time()
    finished_time = end_time - start_time
    finished_time += float(current_time)

    with open("horas", "w") as f:
        f.write(str(finished_time))
    
    hours, remainder = divmod(finished_time, 3600)
    minutes, remainder = divmod(remainder, 60)
    root.destroy()

# The part where it does the writing to the file every 1 second
#while True:
    #try:
        #time.sleep(1)


    #except KeyboardInterrupt:
        #end_time = time.time()

        
        #finished_time = end_time - start_time
        #finished_time += float(current_time)


        # Writes the final time to the notepad
        #with open("horas", "w") as f:
            #f.write(str(finished_time))

        # Study more about divmod i still don't understand this
        #hours, remainder = divmod(finished_time, 3600)
        #minutes, remainder = divmod(remainder, 60)
        #print(f"{int(hours)} hours {int(minutes)} minutes")

        #break


root.protocol("WM_DELETE_WINDOW", close_app)
root.mainloop()