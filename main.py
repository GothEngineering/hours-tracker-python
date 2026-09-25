print("Opening main")
import customtkinter
import tracker_UI

def main():
    root = customtkinter.CTk()
    root.title("Hours tracker v3.0")
    root.geometry("300x100")
    app = tracker_UI.TrackerUI(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()


if __name__ == __name__:
    main()