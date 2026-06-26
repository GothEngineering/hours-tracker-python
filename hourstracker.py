import time
import datetime

start_time = time.time()
current_time = 0


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
    

# The part where it does the writing
while True:
    try:
        time.sleep(1)


    except KeyboardInterrupt:
        end_time = time.time()

        
        finished_time = end_time - start_time
        finished_time += float(current_time)


        # Writes the final time to the notepad
        with open("horas", "w") as f:
            f.write(str(finished_time))

        # Study more about divmod i still don't understand this
        hours, remainder = divmod(finished_time, 3600)
        minutes, remainder = divmod(remainder, 60)
        print(f"{int(hours)} hours {int(minutes)} minutes")

        break
