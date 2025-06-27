import time
from functools import partial

import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkFrame, CTkSlider

import os
import sys

from confirm_dialog import ConfirmDialog
from savegame_manager import SavegameManager
from stats_manager import StatsManager


class GUIManager:
    def __init__(self, point_manager, shop, achievements, rebirth):
        """
        :type point_manager: PointManager
        :type shop: Shop
        :type achievements: Achievements
        :type rebirth: Rebirth
        :param point_manager: Object with PointManager Class
        :param shop: Object with Shop Class
        :param achievements: Object with Achievements Class
        :param rebirth: Object with Rebirth Class
        """
        # Objects/Classes
        self.point_manager = point_manager
        self.shop = shop
        self.achievements = achievements
        self.rebirth = rebirth

        # Window settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.WIDTH = 800
        self.HEIGHT = 600
        self.app = ctk.CTk()
        self.app.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.app.title("Clickyker")

        if hasattr(sys, '_MEIPASS'):
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            icon_path = "icon.ico"
        self.app.iconbitmap(icon_path)

        # Window variables
        self.running = True

        # Slider
        self.rebirth_progress_slider = None

        # String variables
        self.points_text_var = ctk.StringVar()
        self.idle_text_var = ctk.StringVar()
        self.statistics_text_var = ctk.StringVar()
        self.rebirth_points_var = ctk.StringVar()
        self.upgrades_text_variables = []
        self.achievements_text_variables = []
        self.rebirth_bonuses_variables = []

    @staticmethod
    def add_label_textvar(master, text_var, font_name="Arial", font_size=12):
        label = CTkLabel(master, textvariable=text_var, font=(font_name, font_size))
        return label

    @staticmethod
    def add_label(master, text, font_name="Arial", font_size=12):
        label = CTkLabel(master, text=text, font=(font_name, font_size))
        return label

    @staticmethod
    def add_button_textvar(master, text_var, func, width=50, height=20, fg="#ffffff"):
        button = CTkButton(master, textvariable=text_var, command=func, height=height, width=width, text_color=fg)
        return button

    @staticmethod
    def add_button(master, text, func, width=50, height=20, fg="#000000"):
        button = CTkButton(master, text=text, command=func, height=height, width=width, text_color=fg)
        return button

    @staticmethod
    def add_scrollableFrame(master, width, height, corner=0):
        scroll_frame = ctk.CTkScrollableFrame(master, width=width, height=height, corner_radius=corner)
        return scroll_frame

    @staticmethod
    def add_Frame(master, width, height, corner=0):
        frame = CTkFrame(master, width, height, corner_radius=corner)
        return frame

    @staticmethod
    def toggle_frame(frame, frame_to_hide, another_one):
        if frame.winfo_ismapped():
            frame.pack_forget()
            frame_to_hide.pack(fill="both", expand=True, side="right")
            another_one.pack(side="left", fill="y")
        else:
            frame_to_hide.pack_forget()
            another_one.pack_forget()
            frame.pack(fill="both", expand=True)
            frame.lift()

    def savenexit(self):
        SavegameManager(self.point_manager, self.shop, self.achievements, self.rebirth,
                        self.point_manager.time_played).save_game(self.app)
        time.sleep(1)
        sys.exit()

    def build(self):
        # Main window

        main_window = self.add_Frame(self.app, 0, 0)
        main_window.pack(fill="both", expand=True, side="right")

        # Elements

        points_label = self.add_label_textvar(main_window, self.points_text_var, font_size=25)
        points_label.pack()

        idle_label = self.add_label_textvar(main_window, self.idle_text_var, font_size=15)
        idle_label.pack()

        main_button = self.add_button(main_window, "", func=self.point_manager.click, width=100, height=100)
        main_button.place(relx=0.5, rely=0.5, anchor='center')

        # Buttons
        right_buttons_frame = self.add_Frame(main_window, 100, 0)
        right_buttons_frame.pack(side="right")

        stats_show_button = self.add_button(right_buttons_frame, "Stats",
                                            func=lambda: self.toggle_frame(stats_frame, main_window, upgrade_menu),
                                            width=100, height=50)

        achievements_show_button = self.add_button(right_buttons_frame, "Achievements",
                                                   func=lambda: self.toggle_frame(achievements_frame, main_window,
                                                                                  upgrade_menu), width=100, height=50)
        show_rebirth_button = self.add_button(right_buttons_frame, "Rebirth",
                                              func=lambda: self.toggle_frame(rebirth_frame, main_window, upgrade_menu),
                                              width=100, height=50)

        save_game_button = self.add_button(right_buttons_frame, "Save",
                                           func=lambda: SavegameManager(self.point_manager, self.shop,
                                                                        self.achievements, self.rebirth,
                                                                        self.point_manager.time_played).save_game(
                                               self.app),
                                           width=100, height=50)

        load_game_button = self.add_button(right_buttons_frame, "Load",
                                           func=lambda: SavegameManager(self.point_manager, self.shop,
                                                                        self.achievements, self.rebirth,
                                                                        self.point_manager.time_played).load_game(
                                               self.app),
                                           width=100, height=50)

        save_n_exit_button = self.add_button(right_buttons_frame, "Save & Exit", func=self.savenexit, width=100,
                                             height=50)

        exit_button = self.add_button(right_buttons_frame, "Exit", func=sys.exit, width=100, height=50)

        save_n_exit_button.pack(side="bottom", pady=(2, 0))
        exit_button.pack(side="bottom", pady=(10, 2))
        load_game_button.pack(side="bottom", pady=(2, 10))
        save_game_button.pack(side="bottom", pady=(10, 2))
        show_rebirth_button.pack(side="bottom", pady=(2, 10))
        achievements_show_button.pack(side="bottom", pady=2)
        stats_show_button.pack(side="bottom", pady=(0, 2))

        # Statistics
        stats_frame = self.add_Frame(self.app, 0, 0)
        stats_frame.pack(fill="both", expand=True, side="right")
        stats_frame.pack_forget()

        stats_label = self.add_label_textvar(stats_frame, self.statistics_text_var, font_size=15)
        stats_label.pack()

        exit_stats_button = self.add_button(stats_frame, "Exit",
                                            func=lambda: self.toggle_frame(stats_frame, main_window, upgrade_menu),
                                            width=100, height=50)
        exit_stats_button.pack()

        # Achievements

        achievements_frame = self.add_Frame(self.app, width=0, height=0)
        achievements_frame.pack(fill="both", expand=True)
        achievements_frame.pack_forget()

        achievements_scrollable_frame = self.add_scrollableFrame(achievements_frame, width=600, height=600)
        achievements_scrollable_frame.pack(fill="both", expand=True, pady=10)

        # Elements
        achv_label = self.add_label(achievements_scrollable_frame, "ACHIEVEMENTS:", font_size=20)
        achv_label.pack(side="top")

        for _ in self.achievements.achievements:
            self.achievements_text_variables.append(ctk.StringVar())

        for nr, i in enumerate(self.achievements.achievements):
            label = self.add_label_textvar(achievements_scrollable_frame,
                                           text_var=self.achievements_text_variables[nr],
                                           font_size=14)
            label.pack(pady=10)

        # Przycisk Exit na samym dole
        exit_achv_button = self.add_button(achievements_scrollable_frame, "Exit",
                                           func=lambda: self.toggle_frame(achievements_frame, main_window,
                                                                          upgrade_menu), width=100, height=50)
        exit_achv_button.pack(pady=20)

        # Rebirth

        rebirth_frame = self.add_Frame(self.app, 200, 200)
        rebirth_frame.pack(fill="both", expand=True)
        rebirth_frame.pack_forget()

        # Elements

        rebirth_points_label = self.add_label_textvar(rebirth_frame, text_var=self.rebirth_points_var, font_size=20)
        rebirth_points_label.pack(side="top")

        rebirth_exit_button = self.add_button(rebirth_frame, "Exit",
                                              func=lambda: self.toggle_frame(rebirth_frame, main_window,
                                                                             upgrade_menu), width=100, height=50)

        rebirth_exit_button.pack(side="bottom")

        rebirth_button = self.add_button(rebirth_frame, text="Rebirth", func=self.confirm_rebirth, width=200, height=50)
        rebirth_button.pack(side="bottom", pady=15)

        self.rebirth_progress_slider = CTkSlider(rebirth_frame, from_=0, to=100, state="disabled")
        self.rebirth_progress_slider.pack(side="bottom", pady=20)

        # Upgrade Menu

        upgrade_menu = self.add_scrollableFrame(self.app, 200, 600)
        upgrade_menu.pack(side="left", fill="y")

        # Elements
        upgrade_label = self.add_label(upgrade_menu, "UPGRADES", font_size=20)
        upgrade_label.pack()

        # Rebirths
        for _ in self.rebirth.rebirth_bonuses:
            self.rebirth_bonuses_variables.append(ctk.StringVar())

        for nr, i in enumerate(self.rebirth.rebirth_bonuses):
            button = self.add_button_textvar(rebirth_frame, text_var=self.rebirth_bonuses_variables[nr],
                                             func=partial(self.rebirth.buy_rebirth_bonus, i['name'], self.app),
                                             width=190, fg="#000000")
            button.pack(pady=5, ipady=5)

        # Upgrades

        for _ in self.shop.upgrades:
            self.upgrades_text_variables.append([ctk.StringVar(), None])

        for nr, i in enumerate(self.shop.upgrades):
            button = self.add_button_textvar(upgrade_menu,
                                             text_var=self.upgrades_text_variables[nr][0],
                                             func=partial(self.shop.shop_menu, i['name'], self.app),
                                             width=190, fg="#000000")

            button.pack(pady=5, ipady=5)

    def confirm_rebirth(self):
        if self.rebirth.can_rebirth():
            popup = ConfirmDialog(self.app, "Are you sure?")
            self.app.wait_window(popup)
            if popup.result:
                self.rebirth.rebirth(self.app)
        else:
            self.rebirth.rebirth(self.app)

    def run(self):
        self.update_text_var()
        self.idle_timer()
        self.app.mainloop()

    def idle_timer(self):
        self.point_manager.idle_point()
        self.achievements.check_ach(self.app)
        self.point_manager.time_played += 1
        self.app.after(1000, self.idle_timer)

    def update_text_var(self):
        self.points_text_var.set(f"Points: {self.point_manager.points}")
        self.idle_text_var.set(f"Idle: {self.point_manager.idle}")

        # Achievements
        for nr, i in enumerate(self.achievements.achievements):
            ach_data = self.achievements.get_ach_data(i['id'])
            if ach_data[3]:
                self.achievements_text_variables[nr].set(
                    f"{ach_data[0]}\n{ach_data[1]}\nReward: {ach_data[2]}\nUNLOCKED")
            else:
                self.achievements_text_variables[nr].set(f"???????\n?????????????\nReward: ?????\nHIDDEN")

        # Upgrades
        for nr, i in enumerate(self.shop.upgrades):
            if i['idle'] == 0:
                self.upgrades_text_variables[nr][0].set(
                    f"{i['name']}\nCost: {int(i["cost"] * self.shop.rebirth_discount)}\nClick Multiplier: {i['click_mult']}\nCount: {self.shop.count_upgrades(i['name'])}")
            else:
                self.upgrades_text_variables[nr][0].set(
                    f"{i['name']}\nCost: {i['cost']}\nIdle: {i['idle']}\nCount: {self.shop.count_upgrades(i['name'])}")

        # Rebirths
        self.rebirth_points_var.set(f"Rebirth points: {self.rebirth.rebirths_points}")
        for nr, i in enumerate(self.rebirth.rebirth_bonuses):
            self.rebirth_bonuses_variables[nr].set(i['name'])

        self.rebirth_progress_slider.set(self.rebirth.get_rebirth_done_perc())

        # Statistics
        self.statistics_text_var.set(
            StatsManager.show_stats(self.point_manager, self.shop, self.achievements, self.rebirth,
                                    self.point_manager.time_played))
        self.app.after(100, self.update_text_var)
