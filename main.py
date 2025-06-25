class OutputManager:
    @staticmethod
    def print_out(data):
        print(data)

    @staticmethod
    def print_in():
        return input()


class PointManager:
    def __init__(self):
        self.points = 0
        self.idle = 0
        self.click_multiplier = 1

    def click(self):
        self.points += 1 * self.click_multiplier

    def idle_point(self):
        self.points += self.idle

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
        self.point_manager = point_manager
        self.bought_upgrades = []

    def add_upgrade(self, name):
        for upgrade in self.upgrades:
            if upgrade["name"] == name:
                was_upgrade = False
                self.point_manager.idle += upgrade["idle"]
                self.point_manager.click_multiplier += upgrade["click_mult"]
                for bought_upgrade in self.bought_upgrades:
                    if upgrade["name"] in bought_upgrade:
                        was_upgrade = True
                        bought_upgrade[1] += 1
                        break
                    else:
                        was_upgrade = False
                if not was_upgrade:
                    self.bought_upgrades.append([upgrade["name"], 1])

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
{nr}. {upgrade['name']} Cost: {upgrade['cost']} Idle: {upgrade['click_mult']} Already bought: {self.count_upgrades(upgrade['name'])}
"""
            else:
                output += f"""
{nr}. {upgrade['name']} Cost: {upgrade['cost']} Click Multiplier: {upgrade['idle']} Already bought: {self.count_upgrades(upgrade['name'])}
"""
        return output

    def shop_menu(self):
        OutputManager.print_out("Which one do you want to buy?")
        OutputManager.print_out(self.upgrades_list())
        upgrade_nr = 0
        while True:
            try:
                upgrade_nr = int(OutputManager.print_in())
                break
            except ValueError:
                OutputManager.print_out("It has to be a number!")
        cost = self.upgrades[upgrade_nr]["cost"]
        if self.point_manager.can_afford(cost=cost):
            self.add_upgrade(self.upgrades[upgrade_nr]["name"])
            self.upgrades[upgrade_nr]['cost'] = int(self.upgrades[upgrade_nr]['cost'] * 1.20)
            self.point_manager.spend_points(cost=cost)


class Achievements:
    def __init__(self):
        self.achievements = [
            {"id": "first_click", "name": "First Click", "reward": 10, "unlocked": False, "condition_id": "clicks_1"},
            {"id": "hundred_clicks", "name": "Hundred Clicks", "reward": 50, "unlocked": False,
             "condition_id": "clicks_100"},
            {"id": "idle_master", "name": "Idle Master", "reward": 5000, "unlocked": False, "condition_id": "idle_1000"},
            {"id": "upgrade_collector", "name": "Upgrade Collector", "reward": 75, "unlocked": False,
             "condition_id": "upgrades_10"},
        ]
        self.conditions = {
            "clicks_1": {"description": "Make your first click", "condition_name": "click", "condition_value": 1},
            "clicks_100": {"description": "Make 100 clicks", "condition_name": "click", "condition_value": 100},
            "idle_1000": {"description": "Accumulate 1000 idle points", "condition_name": "idle", "condition_value": 1000},
            "upgrades_10": {"description": "Buy 10 upgrades", "condition_name": "upgrades", "condition_value": 10},
        }

    def check_achv(self):
        pass