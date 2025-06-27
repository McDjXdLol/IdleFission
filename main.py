import datetime
import json
import sys
import time
from functools import partial

import customtkinter as ctk
from customtkinter import CTkLabel, CTkButton, CTkFrame, CTkSlider


class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, master, message="Are you sure?"):
        super().__init__(master)

        self.result = None  # Tutaj będzie True/False
        self.title("Confirmation")

        self.geometry("400x150")
        self.grab_set()  # Zablokuj inne okna, dopóki to nie zostanie zamknięte
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

        self.protocol("WM_DELETE_WINDOW", self.no)  # Zamknięcie = No

    def yes(self):
        self.result = True
        self.destroy()

    def no(self):
        self.result = False
        self.destroy()


class Popup(ctk.CTkToplevel):
    def __init__(self, master, message):
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
        self.destroy()


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


class SavegameManager:

    def __init__(self, points_manager, shop, achievements, rebirth, time_played):
        """
        :type points_manager: PointManager
        :type shop: Shop
        :type achievements: Achievements
        :type rebirth: Rebirth
        :param points_manager: Object with PointsManager Class
        :param shop: Object with Shop Class
        :param achievements: Object with Achievements Class
        :param rebirth: Object with Rebirth Class
        """
        self.time_played = time_played
        self.points_manager = points_manager
        self.shop = shop
        self.achievements = achievements
        self.rebirth = rebirth
        self.save_filename = "save.json"

    def save_game(self, master):
        current_time = datetime.datetime.now()
        data = {
            # PointManager
            "rebirth_click_multiplier": self.points_manager.rebirth_click_multiplier,
            "rebirth_idle": self.points_manager.rebirth_idle,
            "total_clicks": self.points_manager.total_clicks,
            "total_points": self.points_manager.total_points,
            "points": self.points_manager.points,
            "idle": self.points_manager.idle,
            "click_multiplier": self.points_manager.click_multiplier,
            "time_played": self.time_played,

            # Shop
            "upgrades": self.shop.upgrades,
            "rebirth_discount": self.shop.rebirth_discount,
            "bought_upgrades": self.shop.bought_upgrades,

            # Achievements
            "conditions": self.achievements.conditions,

            # Rebirth
            "points_record": self.rebirth.points_record,
            "rebirth_starting_points": self.rebirth.rebirth_starting_points,
            "rebirths": self.rebirth.rebirths,
            "rebirths_points": self.rebirth.rebirths_points,
            "rebirth_condition": self.rebirth.rebirth_condition,

            "save_datetime": current_time.strftime("%G/%m/%d %H:%M:%S")
        }
        with open(self.save_filename, "w") as f:
            json.dump(data, f, indent=4)
        Popup(master, "Game saved!")

    def load_game(self, master):
        save_data = {}
        with open(self.save_filename, "r") as f:
            save_data = json.load(f)

        # PointManager
        self.points_manager.rebirth_click_multiplier = save_data["rebirth_click_multiplier"]
        self.points_manager.rebirth_idle = save_data["rebirth_idle"]
        self.points_manager.total_clicks = save_data["total_clicks"]
        self.points_manager.total_points = save_data["total_points"]
        self.points_manager.points = save_data["points"]
        self.points_manager.idle = save_data["idle"]
        self.points_manager.click_multiplier = save_data["click_multiplier"]
        self.points_manager.time_played = save_data["time_played"]

        # Shop
        self.shop.upgrades = save_data["upgrades"]
        self.shop.rebirth_discount = save_data["rebirth_discount"]
        self.shop.bought_upgrades = save_data["bought_upgrades"]

        # Achievements
        self.achievements.conditions = save_data["conditions"]

        # Rebirth
        self.rebirth.points_record = save_data["points_record"]
        self.rebirth.rebirth_starting_points = save_data["rebirth_starting_points"]
        self.rebirth.rebirths = save_data["rebirths"]
        self.rebirth.rebirths_points = save_data["rebirths_points"]
        self.rebirth.rebirth_condition = save_data["rebirth_condition"]

        Popup(master, "Game loaded!")


class StatsManager:

    @staticmethod
    def show_stats(point_manager, shop, achievements, rebirth, time_played):
        """
        :type point_manager: PointManager
        :type shop: Shop
        :type achievements: Achievements
        :type rebirth: Rebirth
        :param point_manager: Object with PointManager Class
        :param shop: Object with Shop Class
        :param achievements: Object with Achievements Class
        :param rebirth: Object with Rebirth Class
        :return:
        """
        total_upgrades_bought = 0
        for x in shop.bought_upgrades:
            total_upgrades_bought += x[1]
        total_achievements_got = 0
        total_achievements_reward_granted = 0
        for y in achievements.conditions:
            if y["unlocked"]:
                total_achievements_got += 1
                for z in achievements.achievements:
                    if z["condition_id"] == y["title"]:
                        total_achievements_reward_granted += z["reward"]
        output_text = f"""
STATS:


CLICKER STATS:
Current Points: {point_manager.points}
Total Points: {point_manager.total_points}
Total Clicks: {point_manager.total_clicks}
Click Multiplier: {point_manager.click_multiplier}
Idle: {point_manager.idle}
Time played: {time.strftime("%H:%M:%S", time.gmtime(time_played))}
 
SHOP STATS:
Number of upgrades bought: {total_upgrades_bought}

ACHIEVEMENTS:
Total Achievements Unlocked: {total_achievements_got}
Total Achievements Rewards Granted: {total_achievements_reward_granted}

REBIRTH:
Rebirths Amount: {rebirth.rebirths}
Most points in rebirth: {rebirth.points_record}
Rebirth Points: {rebirth.rebirths_points}
Points needed for next rebirth: {rebirth.rebirth_condition}
Starting points: {rebirth.rebirth_starting_points}
Idle bonus: {point_manager.rebirth_idle * 100}%
Click Multiplier: {int(point_manager.rebirth_click_multiplier * 100)}%
"""
        return output_text


class PointManager:
    def __init__(self):
        self.rebirth_click_multiplier = 1
        self.rebirth_idle = 1
        self.total_clicks = 0
        self.total_points = 0
        self.points = 0
        self.idle = 0
        self.click_multiplier = 1
        self.time_played = 0

    def click(self):
        self.total_points += int(1 * self.click_multiplier * self.rebirth_click_multiplier)
        self.points += int(1 * self.click_multiplier * self.rebirth_click_multiplier)
        self.total_clicks += 1

    def idle_point(self):
        self.points += int(self.idle * self.rebirth_idle)

    def can_afford(self, cost):
        return cost <= self.points

    def spend_points(self, cost):
        self.points -= cost


class Shop:
    def __init__(self, point_manager):
        """
        :param point_manager: PointManager
        :type point_manager: PointManager
        """
        self.upgrades = [
            {"name": "Tiny Reactor Boost", "cost": 10, "click_mult": 1, "idle": 0},
            {"name": "Small Capacitor", "cost": 25, "click_mult": 2, "idle": 0},
            {"name": "Heat Sink", "cost": 50, "click_mult": 0, "idle": 3},
            {"name": "Power Amplifier", "cost": 85, "click_mult": 3, "idle": 0},
            {"name": "Quantum Flux", "cost": 140, "click_mult": 0, "idle": 5},
            {"name": "Nano Circuit", "cost": 220, "click_mult": 4, "idle": 0},
            {"name": "Superconductor", "cost": 350, "click_mult": 0, "idle": 10},

            {"name": "Particle Accelerator", "cost": 600, "click_mult": 5, "idle": 0},
            {"name": "Dark Matter Collector", "cost": 1000, "click_mult": 0, "idle": 20},
            {"name": "Plasma Converter", "cost": 1700, "click_mult": 6, "idle": 0},
            {"name": "Fusion Core", "cost": 3000, "click_mult": 0, "idle": 25},
            {"name": "Antimatter Storage", "cost": 5000, "click_mult": 8, "idle": 0},
            {"name": "Graviton Emitter", "cost": 8500, "click_mult": 0, "idle": 40},
            {"name": "Chrono Stabilizer", "cost": 14000, "click_mult": 10, "idle": 0},

            {"name": "Dimensional Rift", "cost": 25000, "click_mult": 0, "idle": 60},
            {"name": "Energy Matrix", "cost": 50000, "click_mult": 12, "idle": 0},
            {"name": "Singularity Reactor", "cost": 100000, "click_mult": 0, "idle": 80},
            {"name": "Neutrino Collector", "cost": 250000, "click_mult": 15, "idle": 0},
            {"name": "Omega Core", "cost": 600000, "click_mult": 0, "idle": 100},
            {"name": "Eternity Engine", "cost": 1250000, "click_mult": 20, "idle": 0},
        ]

        for nr, upgrade in enumerate(self.upgrades):
            if nr >= int(len(self.upgrades) / 2):
                upgrade['cost'] = int(upgrade['cost'] * 7)
                upgrade['idle'] = int(upgrade['idle'] * 9)
            elif nr >= int(len(self.upgrades) / 3):
                upgrade['cost'] = int(upgrade['cost'] * 5)
                upgrade['idle'] = int(upgrade['idle'] * 7)
            else:
                upgrade['cost'] = int(upgrade['cost'] * 3)
                upgrade['idle'] = int(upgrade['idle'] * 5)

        self.rebirth_discount = 1
        self.point_manager = point_manager
        self.bought_upgrades = []
        self.MAX_UPGRADES = 100

    def add_upgrade(self, name, master):
        for upgrade in self.upgrades:
            if upgrade["name"] != name:
                continue
            for bought_upgrade in self.bought_upgrades:
                if upgrade["name"] in bought_upgrade:
                    if bought_upgrade[1] < self.MAX_UPGRADES:
                        bought_upgrade[1] += 1
                        self.point_manager.idle += upgrade["idle"]
                        self.point_manager.click_multiplier += upgrade["click_mult"]
                        return True
                    else:
                        Popup(master, "You already got the maximum amount of upgrades!")
                        return False
            self.bought_upgrades.append([upgrade["name"], 1])
            self.point_manager.idle += upgrade["idle"]
            self.point_manager.click_multiplier += upgrade["click_mult"]
            return True
        return False

    def count_upgrades(self, name):
        for bought_upgrade in self.bought_upgrades:
            if name in bought_upgrade:
                return bought_upgrade[1]
        return 0

    def shop_menu(self, name, master):
        upgrade_nr = 0
        for nr, upgrade in enumerate(self.upgrades):
            if upgrade['name'] == name:
                upgrade_nr = nr
        cost = int(self.upgrades[upgrade_nr]["cost"] * self.rebirth_discount)
        if self.point_manager.can_afford(cost=cost):
            if self.add_upgrade(self.upgrades[upgrade_nr]["name"], master):
                self.upgrades[upgrade_nr]['cost'] = int(self.upgrades[upgrade_nr]['cost'] * 1.3)
                self.point_manager.spend_points(cost=cost)
        else:
            Popup(master, "Not enough points to buy upgrade!")


class Achievements:
    def __init__(self, point_manager, shop, rebirth):
        """
        :type rebirth: Rebirth
        :param rebirth: Object with Rebirth Class
        :type point_manager PointManager
        :param point_manager: Object with PointManager Class
        :type shop: Shop
        :param shop: Object with Shop Class
        """
        self.point_manager = point_manager
        self.shop = shop
        self.rebirth = rebirth
        self.achievements = [
            {
                "id": "first_click",
                "name": "First Click",
                "reward": 10,
                "condition_id": "clicks_1"
            },
            {
                "id": "hundred_clicks",
                "name": "Hundred Clicks",
                "reward": 300,
                "condition_id": "clicks_100"
            },
            {
                "id": "idle_master",
                "name": "Idle Master",
                "reward": 2000,
                "condition_id": "idle_1000"
            },
            {
                "id": "upgrade_collector",
                "name": "Upgrade Collector",
                "reward": 75,
                "condition_id": "upgrades_10"
            },
            {
                "id": "upgrade_hoarder",
                "name": "Upgrade Hoarder",
                "reward": 1500,
                "condition_id": "upgrades_50"
            },
            {
                "id": "first_rebirth",
                "name": "First Rebirth",
                "reward": 5000,
                "condition_id": "rebirths_1"
            },
            {
                "id": "time_flies",
                "name": "Time Flies",
                "reward": 2000,
                "condition_id": "time_1"
            },
            {
                "id": "prestige_collector",
                "name": "Prestige Collector",
                "reward": 5000,
                "condition_id": "rebirths_5"
            },
            {
                "id": "quantum_break",
                "name": "Quantum Break",
                "reward": 2000,
                "condition_id": "upgrade_quantum"
            },
            {
                "id": "the_grind_begins",
                "name": "The Grind Begins",
                "reward": 10000,
                "condition_id": "points_1000000"
            }
        ]
        self.conditions = [
            {
                "title": "clicks_1",
                "description": "Make your first click",
                "condition_name": "click",
                "condition_value": 1,
                "unlocked": False
            },
            {
                "title": "clicks_100",
                "description": "Make 100 clicks",
                "condition_name": "click",
                "condition_value": 100,
                "unlocked": False
            },
            {
                "title": "idle_1000",
                "description": "Accumulate 1000 idle points",
                "condition_name": "idle",
                "condition_value": 1000,
                "unlocked": False
            },
            {
                "title": "upgrades_10",
                "description": "Buy 10 upgrades",
                "condition_name": "upgrades",
                "condition_value": 10,
                "unlocked": False
            },
            {
                "title": "upgrades_50",
                "description": "Buy 50 upgrades",
                "condition_name": "upgrades",
                "condition_value": 50,
                "unlocked": False
            },
            {
                "title": "rebirths_1",
                "description": "Get 1 Rebirth",
                "condition_name": "rebirth",
                "condition_value": 1,
                "unlocked": False
            },
            {
                "title": "time_1",
                "description": "Play for 1 hour",
                "condition_name": "time",
                "condition_value": 3600,
                "unlocked": False
            },
            {
                "title": "rebirths_5",
                "description": "Get 5 rebirths",
                "condition_name": "rebirth",
                "condition_value": 5,
                "unlocked": False
            },
            {
                "title": "upgrade_quantum",
                "description": "Get 'Dimensional Rift' Upgrade",
                "condition_name": "upgrade",
                "condition_value": "Dimensional Rift",
                "unlocked": False
            },
            {
                "title": "points_1000000",
                "description": "Have 1,000,000 points at once",
                "condition_name": "points",
                "condition_value": 1000000,
                "unlocked": False
            }
        ]

    def unlock_ach(self, master, title):
        """
        Function that sets achievement as unlocked and gives reward to player
        :param title:
        :return:
        """
        unlocked = False
        for condition in self.conditions:
            if not condition["unlocked"]:
                if condition["title"] == title:
                    condition["unlocked"] = True
                    unlocked = True
                    break
        if unlocked:
            for ach in self.achievements:
                if ach["condition_id"] == title:
                    self.point_manager.points += ach["reward"]
                    Popup(master=master,
                          message=f"Achievement unlocked: {ach['name']}\nYou got: {ach['reward']} points!")
                    break

    def get_ach_data(self, title):
        """
        Function that returns [Achievement name, description, reward, unlocked]
        :param title: title/id of the achievement
        :return:
        """
        for ach in self.achievements:  # ← poprawione
            if ach["id"] == title:
                for con in self.conditions:
                    if ach["condition_id"] == con["title"]:
                        return [ach["name"], con['description'], ach["reward"], con["unlocked"]]
        return None

    def check_ach(self, master):
        """
        Returns [Achievement unlocked, Achievement title/id]
        :return:
        """
        for condition in self.conditions:
            if not condition["unlocked"]:
                match condition["condition_name"]:
                    case "click":
                        if condition["condition_value"] <= self.point_manager.total_clicks:
                            self.unlock_ach(master, condition["title"])
                            return True
                    case "idle":
                        if condition["condition_value"] <= self.point_manager.idle:
                            self.unlock_ach(master, condition["title"])
                            return True
                    case "upgrades":
                        if condition["condition_value"] <= len(self.shop.bought_upgrades):
                            self.unlock_ach(master, condition["title"])
                            return True
                    case "rebirth":
                        if condition["condition_value"] <= self.rebirth.rebirths:
                            self.unlock_ach(master, condition["title"])
                    case "time":
                        if condition["condition_value"] <= self.point_manager.time_played:
                            self.unlock_ach(master, condition["title"])
                    case "rebirth_points":
                        if condition["condition_value"] <= self.rebirth.rebirths_points:
                            self.unlock_ach(master, condition["title"])
                    case "discount":
                        if condition["condition_value"] <= self.shop.rebirth_discount:
                            self.unlock_ach(master, condition["title"])
                    case "upgrade_bought":
                        for upgrade in self.shop.bought_upgrades:
                            if upgrade[0] == condition["title"]:
                                self.unlock_ach(master, condition["title"])
                            break
                    case "points":
                        if condition["condition_value"] <= self.point_manager.points:
                            self.unlock_ach(master, condition["title"])

        return None


class Rebirth:
    def __init__(self, point_manager, shop):
        """
        :type shop: Shop
        :param shop: Object wth Shop Class
        :type point_manager: PointManager
        :param point_manager: Object with PointManager Class
        """
        self.shop = shop
        self.point_manager = point_manager
        self.points_record = 0
        self.rebirth_starting_points = 0
        self.rebirths = 0
        self.rebirths_points = 0
        self.rebirth_condition = 30000
        self.rebirth_multiplier = 1.15
        self.rebirth_bonuses = [
            {
                "id": "10_click_multi",
                "name": "+10% Click Multiplier",
                "type": "click",
                "amount": 0.1
            },
            {
                "id": "10_idle",
                "name": "+10% Idle",
                "type": "idle",
                "amount": 0.1,
            },
            {
                "id": "5_discount",
                "name": "-5% Upgrade discount",
                "type": "cost",
                "amount": 0.05
            },
            {
                "id": "100_start_points",
                "name": "+100 points after rebirth",
                "type": "starting_points",
                "amount": 100
            }
        ]

    def get_bonuses_list(self):
        output = []
        for nr, upgrade in enumerate(self.rebirth_bonuses):
            output.append(upgrade['name'])
        return output

    def buy_rebirth_bonus(self, name, master):
        bonus_nr = 0
        for nr, x in enumerate(self.rebirth_bonuses):
            if x['name'] == name:
                bonus_nr = nr
                break
        if self.rebirths_points > 0:
            match self.rebirth_bonuses[bonus_nr]["type"]:
                case "click":
                    self.point_manager.rebirth_click_multiplier += int(self.rebirth_bonuses[bonus_nr]["amount"])
                    Popup(master,
                          f"Click multiplier increased to: {self.point_manager.rebirth_click_multiplier}")
                case "idle":
                    self.point_manager.rebirth_idle += int(self.rebirth_bonuses[bonus_nr]['amount'])
                    Popup(master, f"Idle multiplier increased to: {self.point_manager.rebirth_idle}")
                case "cost":
                    self.shop.rebirth_discount -= self.rebirth_bonuses[bonus_nr]['amount']
                    Popup(master, f"Upgrades are discounted to: {int(self.shop.rebirth_discount*100)}%")
                case "starting_points":
                    self.rebirth_starting_points += int(self.rebirth_bonuses[bonus_nr]['amount'])
                    Popup(master, f"Starting points increased to: {self.rebirth_starting_points}")
            self.rebirths_points -= 1
        else:
            Popup(master=master, message="Not enough rebirth points to buy!")

    def can_rebirth(self):
        return self.point_manager.points >= self.rebirth_condition

    def rebirth(self, master):
        if self.can_rebirth():
            self.points_record = max(self.points_record, self.point_manager.points)
            self.point_manager.points = self.rebirth_starting_points
            self.point_manager.idle = 0
            self.point_manager.click_multiplier = 1
            self.shop.bought_upgrades = []
            self.rebirths += 1
            self.rebirths_points += 1
            self.rebirth_condition = int(self.rebirth_condition * self.rebirth_multiplier)
            self.shop.upgrades = [
                {"name": "Tiny Reactor Boost", "cost": 10, "click_mult": 1, "idle": 0},
                {"name": "Small Capacitor", "cost": 25, "click_mult": 2, "idle": 0},
                {"name": "Heat Sink", "cost": 50, "click_mult": 0, "idle": 3},
                {"name": "Power Amplifier", "cost": 85, "click_mult": 3, "idle": 0},
                {"name": "Quantum Flux", "cost": 140, "click_mult": 0, "idle": 5},
                {"name": "Nano Circuit", "cost": 220, "click_mult": 4, "idle": 0},
                {"name": "Superconductor", "cost": 350, "click_mult": 0, "idle": 10},

                {"name": "Particle Accelerator", "cost": 600, "click_mult": 5, "idle": 0},
                {"name": "Dark Matter Collector", "cost": 1000, "click_mult": 0, "idle": 20},
                {"name": "Plasma Converter", "cost": 1700, "click_mult": 6, "idle": 0},
                {"name": "Fusion Core", "cost": 3000, "click_mult": 0, "idle": 25},
                {"name": "Antimatter Storage", "cost": 5000, "click_mult": 8, "idle": 0},
                {"name": "Graviton Emitter", "cost": 8500, "click_mult": 0, "idle": 40},
                {"name": "Chrono Stabilizer", "cost": 14000, "click_mult": 10, "idle": 0},

                {"name": "Dimensional Rift", "cost": 25000, "click_mult": 0, "idle": 60},
                {"name": "Energy Matrix", "cost": 50000, "click_mult": 12, "idle": 0},
                {"name": "Singularity Reactor", "cost": 100000, "click_mult": 0, "idle": 80},
                {"name": "Neutrino Collector", "cost": 250000, "click_mult": 15, "idle": 0},
                {"name": "Omega Core", "cost": 600000, "click_mult": 0, "idle": 100},
                {"name": "Eternity Engine", "cost": 1250000, "click_mult": 20, "idle": 0},
            ]
            for nr, upgrade in enumerate(self.shop.upgrades):
                if nr >= int(len(self.shop.upgrades) / 2):
                    upgrade['cost'] = int(upgrade['cost'] * 7)
                    upgrade['idle'] = int(upgrade['idle'] * 9)
                elif nr >= int(len(self.shop.upgrades) / 3):
                    upgrade['cost'] = int(upgrade['cost'] * 5)
                    upgrade['idle'] = int(upgrade['idle'] * 7)
                else:
                    upgrade['cost'] = int(upgrade['cost'] * 3)
                    upgrade['idle'] = int(upgrade['idle'] * 5)
        else:
            Popup(master, "You don't have enough points to rebirth!")

    def get_rebirth_done_perc(self):
        return int((self.point_manager.points / self.rebirth_condition) * 100)


if __name__ == "__main__":
    pt_manager = PointManager()
    shop = Shop(pt_manager)
    rebir = Rebirth(pt_manager, shop)
    achv = Achievements(pt_manager, shop, rebir)
    GUI = GUIManager(pt_manager, shop, achv, rebir)
    app = GUI.app
    GUI.build()
    GUI.run()
