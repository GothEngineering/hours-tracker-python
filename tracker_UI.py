import customtkinter

class TrackerUI:
    def __init__(self):
        background_color = "#1E1E1E"
        button_color = "#3a1c42"
        label_color = "#1E1E1E"
        color_of_text = "#B0B0B0"
        text_font = customtkinter.CTkFont(family="Century Gothic", size=12, weight="bold")

        self.root.config(bg=background_color)

        # The tracker label
        self.ui_label = customtkinter.CTkLabel(self.root, 
                                               text=f"Time invested: {hours_in_the_float} hours, {minutes} minutes, {seconds_modulo} seconds.", 
                                               bg_color=background_color, fg_color=label_color, text_color=color_of_text, font=text_font)
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

