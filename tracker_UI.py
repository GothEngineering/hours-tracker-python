import customtkinter
import tracker_logic

class TrackerUI:
    # don't forget the root, dummy
    def __init__(self, root):
        self.root = root

        self.logic = tracker_logic.trackerLogic()


        # The pause variable
        self.is_time_paused = False
        

        # Colours
        background_color = "#1E1E1E"
        button_color = "#3a1c42"
        label_color = "#1E1E1E"
        color_of_text = "#B0B0B0"
        text_font = customtkinter.CTkFont(family="Century Gothic", size=12, weight="bold")

        self.root.config(bg=background_color)

        # Grabs the database and converts it to the two weeks average
        start_db = self.logic.start_db()
        
        # Initializes the tracker 
        self.logic.tracking_hours(self.is_time_paused)
        
        # Shoves the time instantly to the label upon starting the app
        # It has a weird delay on the beginning, fix later oomfie
        self.hours1, self.minutes1, self.seconds_modulo1 = self.logic.get_finished_time()

        
        # The tracker label
        self.ui_label = customtkinter.CTkLabel(self.root, 
                                               text=f"Time invested: {self.hours1} hours, {self.minutes1} minutes, {self.seconds_modulo1} seconds.", 
                                               bg_color=background_color, 
                                               fg_color=label_color, 
                                               text_color=color_of_text, 
                                               font=text_font)
        self.ui_label.grid(row=0, column=0, sticky="nsew")

        # Pause button
        self.pause_button = customtkinter.CTkButton(self.root, 
                                                    text="Pause", 
                                                    command=self.pause_timer, 
                                                    bg_color=background_color, 
                                                    fg_color=button_color, 
                                                    text_color=color_of_text,
                                                    font=text_font
                                                    )
        self.pause_button.grid(row=2, column=0, sticky="s")

        # Two weeks average label 
        self.average_time_label = customtkinter.CTkLabel(self.root, 
                                                         text=f"Last two weeks average: {start_db} hours", 
                                                         bg_color=background_color, text_color=color_of_text, 
                                                         fg_color=label_color,
                                                         font=text_font
                                                         )
        self.average_time_label.grid(row=1, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.root.after(1000, self.update_ui)
        self.root.after(60000, self.autosave_UI)
        self.repeat_every_sec()
    
    
    # The function that updates the UI every second (duuh)
    def update_ui(self):
        self.hours1, self.minutes1, self.seconds_modulo1 = self.logic.get_finished_time()

        self.ui_label.configure(text=f"Time invested: {self.hours1} hours, {self.minutes1} minutes, {self.seconds_modulo1} seconds.")

        self.updating_label = self.root.after(1000, self.update_ui)

    
    # The function that loops to have the tracker working
    def repeat_every_sec(self):
        self.logic.tracking_hours(self.is_time_paused)
        self.time_ticking = self.root.after(1000, self.repeat_every_sec)
    
    
    # The autosave function
    def autosave_UI(self):
        self.logic.autosave_logic()
        self.root.after(120000, self.autosave_UI)
    
    
    # Self explanatory
    def close_app(self):
        self.logic.close_app(self.is_time_paused)
        self.root.destroy()
    

    # The pause button, it's purpose is to simply change the variable and calling the actual pause function in the logic
    def pause_timer(self):
        self.is_time_paused = not self.is_time_paused

        
        if self.is_time_paused:
            self.pause_button.configure(text="Unpause")
            self.root.after_cancel(self.updating_label)
            
            two_weeks_avg = self.logic.pause_n_save()
            self.average_time_label.configure(text=f"Last two weeks average: {two_weeks_avg} hours")
            
        else:
            self.pause_button.configure(text="Pause")
            self.update_ui()