import customtkinter as ctk

class Popup(ctk.CTkToplevel):
    def __init__(self, master, message):
        """
        Initialize a popup window displaying a temporary message.

        The popup is positioned centered horizontally over the master window,
        slightly below its top edge, stays on top without window decorations,
        and automatically fades out after 3 seconds.

        Parameters
        ----------
        master : ctk.CTk
            The parent window over which the popup will appear.
        message : str
            The message to display inside the popup.
        """
        super().__init__(master)

        # Stick popup to window
        self.update_idletasks()
        master.update_idletasks()

        master_x = master.winfo_x()
        master_y = master.winfo_y()
        master_width = master.winfo_width()

        popup_width = 550
        popup_height = 100
        x = master_x + (master_width // 2) - (popup_width // 2)
        y = master_y + 50

        self.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        self.overrideredirect(True)
        self.lift()
        self.attributes("-topmost", True)

        label = ctk.CTkLabel(self, text=message, font=("Arial", 16))
        label.pack(padx=10, pady=10)

        self.after(3000, self.fade_out)

    def fade_out(self):
        """
        Destroy the popup window to remove it from the screen.

        Called automatically 3 seconds after initialization.
        """
        self.destroy()
