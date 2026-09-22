print("Opening main")
import customtkinter
import tracker_UI

def main():
    root = customtkinter.CTk()
    root.title("Hours tracker v3.0")
    root.geometry("300x100")
    app = tracker_UI.TrackerUI(root)
    root.mainloop()
    root.after(500, tracking_hours)
    root.after(500, update_ui)
    root.after(60000, auto_save)
    # Initialize the after() functions somehow, i suppose each one should be on their
    # respective module but i don't exactly know how to do it... i'll take a lil break rn
if __name__ == __name__:
    main()