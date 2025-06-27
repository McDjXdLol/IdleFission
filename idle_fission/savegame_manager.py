import datetime
import json

from popup import Popup


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
