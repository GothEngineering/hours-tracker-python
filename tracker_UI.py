import customtkinter
import tracker_logic

class TrackerUI:
    # don't forget the root, dummy
    def __init__(self, root):
        self.root = root

        self.logic = tracker_logic.trackerLogic()

        # This variable manages the label that shows the hours, it is used to turn the float into time
        self.hours_label = 0

        # Colours
        background_color = "#1E1E1E"
        button_color = "#3a1c42"
        label_color = "#1E1E1E"
        color_of_text = "#B0B0B0"
        text_font = customtkinter.CTkFont(family="Century Gothic", size=12, weight="bold")

        self.root.config(bg=background_color)

        # The tracker label
        self.ui_label = customtkinter.CTkLabel(self.root, 
                                               text=f"Time invested: {self.hours_in_the_float} hours, {self.minutes} minutes, {self.seconds_modulo} seconds.", 
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
                                                         text=f"Last two weeks average: {self.rounded_hours} hours", 
                                                         bg_color=background_color, text_color=color_of_text, 
                                                         fg_color=label_color,
                                                         font=text_font
                                                         )
        self.average_time_label.grid(row=1, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.after(1000, self.update_ui)
        self.root.after(1000, self.logic.tracking_hours)
        self.root.after(60000, self.logic.auto_save)

    def update_ui(self):

        # This part is JUST the data that goes into the label, it grabs the finished_time which is the latest value
        # and then it changes the float into hours and minutes
        self.hours_label = self.finished_time
        self.hours_in_the_float = round(self.hours_label) // 3600
        self.seconds_without_hours = round(self.hours_label) % 3600
        self.minutes = self.seconds_without_hours // 60
        self.seconds_modulo = self.seconds_without_hours % 60

        self.ui_label.configure(text=f"Time invested: {self.hours_in_the_float} hours, {self.minutes} minutes, {self.seconds_modulo} seconds.")

        self.updating_label = self.root.after(1000, self.update_ui)

