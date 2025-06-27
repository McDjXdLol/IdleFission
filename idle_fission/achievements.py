from popup import Popup


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
