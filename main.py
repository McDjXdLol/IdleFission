import datetime
import json

import customtkinter as ctk


class GUIManager:
    def __init__(self):
        ctk.set_appearance_mode("dark")

        self.app = ctk.CTk()
        self.app.geometry("1280x720")
        self.app.title("Clickyer")


class OutputManager:
    @staticmethod
    def print_out(text):
        print(text)

    @staticmethod
    def print_in():
        return input()


class SavegameManager:
    def __init__(self, points_manager, shop, achievements, rebirth):
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
        self.points_manager = points_manager
        self.shop = shop
        self.achievements = achievements
        self.rebirth = rebirth
        self.save_filename = "save.json"

    def save_game(self):
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

    def load_game(self):
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


class StatsManager:
    @staticmethod
    def show_stats(point_manager, shop, achievements, rebirth):
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
                    if z["id"] == y["name"]:
                        total_achievements_reward_granted += z["reward"]
        output_text = f"""
            STATS:
CLICKER STATS:
Current Points: {point_manager.points}
Most Points: {point_manager.total_points}
Total Clicks: {point_manager.total_clicks}
Click Multiplier: {point_manager.click_multiplier}
Idle: {point_manager.idle}
 
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
Click Multiplier: {point_manager.click_multiplier * 100}%
"""
        OutputManager.print_out(output_text)


class PointManager:
    def __init__(self):
        self.rebirth_click_multiplier = 1
        self.rebirth_idle = 1
        self.total_clicks = 0
        self.total_points = 0
        self.points = 0
        self.idle = 0
        self.click_multiplier = 1

    def click(self):
        self.total_points = 1 * self.click_multiplier * self.rebirth_click_multiplier
        self.points += 1 * self.click_multiplier * self.rebirth_click_multiplier
        self.total_clicks += 1

    def idle_point(self):
        self.points += self.idle * self.rebirth_idle

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
            {"name": "Tiny Reactor Boost", "cost": 5, "click_mult": 1, "idle": 0},
            {"name": "Small Capacitor", "cost": 15, "click_mult": 2, "idle": 0},
            {"name": "Heat Sink", "cost": 30, "click_mult": 0, "idle": 1},
            {"name": "Power Amplifier", "cost": 50, "click_mult": 3, "idle": 0},
            {"name": "Quantum Flux", "cost": 80, "click_mult": 0, "idle": 3},
            {"name": "Nano Circuit", "cost": 120, "click_mult": 4, "idle": 0},
            {"name": "Superconductor", "cost": 170, "click_mult": 0, "idle": 5},
            {"name": "Particle Accelerator", "cost": 230, "click_mult": 5, "idle": 0},
            {"name": "Dark Matter Collector", "cost": 300, "click_mult": 0, "idle": 10},
            {"name": "Plasma Converter", "cost": 380, "click_mult": 6, "idle": 0},
            {"name": "Fusion Core", "cost": 470, "click_mult": 0, "idle": 15},
            {"name": "Antimatter Storage", "cost": 570, "click_mult": 8, "idle": 0},
            {"name": "Graviton Emitter", "cost": 680, "click_mult": 0, "idle": 20},
            {"name": "Chrono Stabilizer", "cost": 800, "click_mult": 10, "idle": 0},
            {"name": "Dimensional Rift", "cost": 930, "click_mult": 0, "idle": 30},
            {"name": "Energy Matrix", "cost": 1070, "click_mult": 12, "idle": 0},
            {"name": "Singularity Reactor", "cost": 1220, "click_mult": 0, "idle": 40},
            {"name": "Neutrino Collector", "cost": 1380, "click_mult": 15, "idle": 0},
            {"name": "Omega Core", "cost": 1550, "click_mult": 0, "idle": 50},
            {"name": "Eternity Engine", "cost": 1730, "click_mult": 20, "idle": 0},
        ]
        self.rebirth_discount = 1
        self.point_manager = point_manager
        self.bought_upgrades = []
        self.MAX_UPGRADES = 100

    def add_upgrade(self, name):
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
                        OutputManager.print_out("You already got the maximum amount of upgrades!")
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

    def upgrades_list(self):
        output = ""
        for nr, upgrade in enumerate(self.upgrades):
            if upgrade['idle'] == 0:
                output += f"""
{nr}. {upgrade['name']} Cost: {upgrade['cost']} Click Multiplier: {upgrade['click_mult']} Already bought: {self.count_upgrades(upgrade['name'])}
"""
            else:
                output += f"""
{nr}. {upgrade['name']} Cost: {upgrade['cost']} Idle: {upgrade['idle']} Already bought: {self.count_upgrades(upgrade['name'])}
"""
        return output

    def shop_menu(self):
        OutputManager.print_out("Which one do you want to buy?")
        OutputManager.print_out(self.upgrades_list())
        OutputManager.print_out("Exit. Back")
        while True:
            user_input = OutputManager.print_in()
            if user_input.lower() in ['q', 'exit']:
                return
            try:
                upgrade_nr = int(user_input)
                if 0 <= upgrade_nr < len(self.upgrades):
                    break
                else:
                    OutputManager.print_out("Invalid upgrade number!")
            except ValueError:
                OutputManager.print_out("It has to be a number!")
        cost = self.upgrades[upgrade_nr]["cost"] * self.rebirth_discount
        if self.point_manager.can_afford(cost=cost):
            if self.add_upgrade(self.upgrades[upgrade_nr]["name"]):
                self.upgrades[upgrade_nr]['cost'] = int(self.upgrades[upgrade_nr]['cost'] * 1.20)
                self.point_manager.spend_points(cost=cost)
                OutputManager.print_out(
                    f"{self.upgrades[upgrade_nr]['name']} bought! You have now: {self.count_upgrades(self.upgrades[upgrade_nr]['name'])} of them.")
        else:
            OutputManager.print_out("Not enough point to buy upgrade!")


class Achievements:
    def __init__(self, point_manager, shop):
        """
        :type point_manager PointManager
        :param point_manager: Object with PointManager Class
        :type shop: Shop
        :param shop: Object with Shop Class
        """
        self.point_manager = point_manager
        self.shop = shop
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
                "reward": 50000,
                "condition_id": "idle_1000"
            },
            {
                "id": "upgrade_collector",
                "name": "Upgrade Collector",
                "reward": 75,
                "condition_id": "upgrades_10"
            },
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
        ]

    def unlock_ach(self, title):
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
                if ach["id"] == title:
                    self.point_manager.points += ach["reward"]
                    OutputManager.print_out(f"Achievement unlocked: {ach['name']}\nYou got: {ach['reward']} points!")
                    break

    def get_ach_data(self, title):
        """
        Function that returns [Achievement name, Achievement reward]
        :param title: title/id of the achievement
        :return:
        """
        for ach in self.achievements:
            if ach["id"] == title:
                return [ach["name"], ach["reward"]]
        return None, None

    def check_ach(self):
        """
        Returns [Achievement unlocked, Achievement title/id]
        :return:
        """
        for condition in self.conditions:
            if not condition["unlocked"]:
                match condition["condition_name"]:
                    case "click":
                        if condition["condition_value"] <= self.point_manager.points:
                            return [True, condition["title"]]
                    case "idle":
                        if condition["condition_value"] <= self.point_manager.idle:
                            return [True, condition["title"]]
                    case "upgrades":
                        if condition["condition_value"] <= len(self.shop.bought_upgrades):
                            return [True, condition["title"]]
        return [False, None]


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
                "name": "+10% Click Multiplier",
                "type": "click",
                "amount": 0.1
            },
            {
                "name": "+10% Idle",
                "type": "idle",
                "amount": 0.1,
            },
            {
                "name": "-5% Upgrade discount",
                "type": "cost",
                "amount": 0.05
            },
            {
                "name": "+100 points after rebirth",
                "type": "starting_points",
                "amount": 100
            }
        ]

    def get_bonuses_list(self):
        output = ""
        for nr, upgrade in enumerate(self.rebirth_bonuses):
            output += f"{nr}. {upgrade['name']}"
        return output

    def rebirth_shop(self):
        OutputManager.print_out("Which one do you want to buy?")
        OutputManager.print_out(self.get_bonuses_list())
        OutputManager.print_out("Exit. Back")
        while True:
            user_input = OutputManager.print_in()
            bonus_nr = 0
            if user_input.lower() in ['q', 'exit']:
                return
            try:
                bonus_nr = int(user_input)
                if 0 <= bonus_nr < len(self.rebirth_bonuses):
                    break
                else:
                    OutputManager.print_out("Invalid upgrade number!")
                    return
            except ValueError:
                OutputManager.print_out("It has to be a number!")
            if self.rebirths_points > 0:
                match self.rebirth_bonuses[bonus_nr]["type"]:
                    case "click":
                        self.point_manager.rebirth_click_multiplier += self.rebirth_bonuses[bonus_nr]["amount"]
                        OutputManager.print_out(
                            f"Click multiplier increased to: {self.point_manager.rebirth_click_multiplier}")
                    case "idle":
                        self.point_manager.rebirth_idle += self.rebirth_bonuses[bonus_nr]['amount']
                        OutputManager.print_out(f"Idle multiplier increased to: {self.point_manager.rebirth_idle}")
                    case "cost":
                        self.shop.rebirth_discount += self.rebirth_bonuses[bonus_nr]['amount']
                        OutputManager.print_out(f"Upgrades are discounted to: {self.shop.rebirth_discount}%")
                    case "starting_points":
                        self.rebirth_starting_points += self.rebirth_bonuses[bonus_nr]['amount']
                        OutputManager.print_out(f"Starting points increased to: {self.rebirth_starting_points}")
                self.rebirths_points -= 1
            else:
                OutputManager.print_out("Not enough rebirth points to buy!")

    def can_rebirth(self):
        return self.point_manager.points >= self.rebirth_condition

    def rebirth(self):
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
                {"name": "Tiny Reactor Boost", "cost": 5, "click_mult": 1, "idle": 0},
                {"name": "Small Capacitor", "cost": 15, "click_mult": 2, "idle": 0},
                {"name": "Heat Sink", "cost": 30, "click_mult": 0, "idle": 1},
                {"name": "Power Amplifier", "cost": 50, "click_mult": 3, "idle": 0},
                {"name": "Quantum Flux", "cost": 80, "click_mult": 0, "idle": 3},
                {"name": "Nano Circuit", "cost": 120, "click_mult": 4, "idle": 0},
                {"name": "Superconductor", "cost": 170, "click_mult": 0, "idle": 5},
                {"name": "Particle Accelerator", "cost": 230, "click_mult": 5, "idle": 0},
                {"name": "Dark Matter Collector", "cost": 300, "click_mult": 0, "idle": 10},
                {"name": "Plasma Converter", "cost": 380, "click_mult": 6, "idle": 0},
                {"name": "Fusion Core", "cost": 470, "click_mult": 0, "idle": 15},
                {"name": "Antimatter Storage", "cost": 570, "click_mult": 8, "idle": 0},
                {"name": "Graviton Emitter", "cost": 680, "click_mult": 0, "idle": 20},
                {"name": "Chrono Stabilizer", "cost": 800, "click_mult": 10, "idle": 0},
                {"name": "Dimensional Rift", "cost": 930, "click_mult": 0, "idle": 30},
                {"name": "Energy Matrix", "cost": 1070, "click_mult": 12, "idle": 0},
                {"name": "Singularity Reactor", "cost": 1220, "click_mult": 0, "idle": 40},
                {"name": "Neutrino Collector", "cost": 1380, "click_mult": 15, "idle": 0},
                {"name": "Omega Core", "cost": 1550, "click_mult": 0, "idle": 50},
                {"name": "Eternity Engine", "cost": 1730, "click_mult": 20, "idle": 0},
            ]

    def amount_to_next_rebirth(self):
        OutputManager.print_out(
            f"{self.point_manager.points}/{self.rebirth_condition} - {int(self.point_manager.points / self.rebirth_condition) * 100}")


if __name__ == "__main__":
    GUI = GUIManager()
    app = GUI.app
    app.mainloop()

# TODO:
#  - [x] Add function that checks if achievement is able to unlock
#  - [x] Add function that gives reward for achievement
#  - [x] Add function that spits out information about unlocked achievement
#  - [x] Add maximum number of upgrades
#  - [x] Add rebirths that gives rebirths point
#  - [x] Add rebirth shop with massive bonuses
#  - [x] Add function/class that is used to show current statistics
#  - [x] Add class that is used to save n' load game
#  - [ ] Add main function / main game loop
#  - [ ] Add time in game stat
#  - [ ] Add "turbo" boosts that are expensive but useful
#  - [ ] Add challenge mode (e.g. only idle, or no shop)
#  - [ ] Add export/import save via encoded string

# TODO GUI:
#  - [x] `Add main game loop function (update GUI elements and game state)`
#  - [ ] `Add CTkLabel to display current points, total points, click multiplier, idle, rebirth points`
#  - [ ] `Add CTkButton for clicking action, calling PointManager.click()`
#  - [ ] `Add upgrade shop UI: list upgrades with costs and bought amounts, buttons to buy upgrades`
#  - [ ] `Add rebirth shop UI with bonus list and buttons to buy rebirth bonuses`
#  - [ ] `Implement achievements check and display unlocked achievements in GUI`
#  - [ ] `Add save and load buttons, call SavegameManager.save_game() and load_game()`
#  - [ ] `Create output log widget (e.g. CTkTextbox) to replace console print outputs`
#  - [ ] `Add CTkEntry input box with confirm button to replace input() for user choices`
#  - [ ] `Display stats in GUI using StatsManager.show_stats() output`
#  - [ ] `Add idle point timer updating PointManager.idle_point() periodically`
#  - [ ] `Implement rebirth reset logic and GUI refresh after rebirth()`
#  - [ ] `Show notifications and messages in GUI for events like achievements unlocked, errors, etc.`
#  - [ ] `Update upgrade costs dynamically in GUI after each purchase`
#  - [ ] `Add progress bar showing progress to next rebirth`
#  - [ ] `Design layout with frames/panels for points display, shop, rebirth, achievements, and logs`

