import customtkinter as ctk
class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, master, message="Are you sure?"):
        super().__init__(master)

        self.result = None
        self.title("Confirmation")

        self.geometry("400x150")
        self.grab_set()
        self.focus_force()
        self.resizable(False, False)

        # Wyśrodkowanie
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (400 // 2)
        y = (screen_height // 2) - (150 // 2)
        self.geometry(f"+{x}+{y}")

        # Label
        label = ctk.CTkLabel(self, text=message, font=("Arial", 16))
        label.pack(pady=20)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack()

        yes_btn = ctk.CTkButton(btn_frame, text="Yes", command=self.yes)
        no_btn = ctk.CTkButton(btn_frame, text="No", command=self.no)
        yes_btn.pack(side="left", padx=10)
        no_btn.pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", self.no)

    def yes(self):
        self.result = True
        self.destroy()

    def no(self):
        self.result = False
        self.destroy()

