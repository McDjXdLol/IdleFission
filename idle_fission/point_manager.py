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
