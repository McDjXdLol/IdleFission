from popup import Popup


class Shop:
    def __init__(self, point_manager):
        """
        Manage shop upgrades, buying, and upgrade costs.

        Parameters
        ----------
        point_manager : PointManager
            Instance managing player points and multipliers.
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
        """
        Attempt to add an upgrade to the player's inventory.

        Parameters
        ----------
        name : str
            Name of the upgrade to add.
        master : tkinter widget
            Parent widget to display popup messages.

        Returns
        -------
        bool
            True if upgrade was successfully added, False otherwise.
        """
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
        """
        Count how many times a specific upgrade was bought.

        Parameters
        ----------
        name : str
            Name of the upgrade to count.

        Returns
        -------
        int
            Number of times the upgrade was purchased.
        """
        for bought_upgrade in self.bought_upgrades:
            if name in bought_upgrade:
                return bought_upgrade[1]
        return 0

    def shop_menu(self, name, master):
        """
        Handle the buying process of an upgrade if the player can afford it.

        Parameters
        ----------
        name : str
            Name of the upgrade to purchase.
        master : tkinter widget
            Parent widget to display popup messages.
        """
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
