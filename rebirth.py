from popup import Popup


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
                    Popup(master, f"Upgrades are discounted to: {int(self.shop.rebirth_discount * 100)}%")
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
