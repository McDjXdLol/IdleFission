class PointManager:
    def __init__(self):
        """
        Initialize the point manager responsible for handling points, clicks, and multipliers.

        Variables
        ----------
        rebirth_click_multiplier : int
            Multiplier applied to points gained per click after rebirths.
        rebirth_idle : int
            Multiplier applied to idle points gained after rebirths.
        total_clicks : int
            Total number of clicks made by the player.
        total_points : int
            Total points accumulated throughout the game.
        points : int
            Current available points.
        idle : int
            Points gained passively (idle points).
        click_multiplier : int
            Multiplier applied to points per click.
        time_played : int
            Total time played in seconds.
        """
        self.rebirth_click_multiplier = 1
        self.rebirth_idle = 1
        self.total_clicks = 0
        self.total_points = 0
        self.points = 0
        self.idle = 0
        self.click_multiplier = 1
        self.time_played = 0

    def click(self):
        """
        Handle a click action by the player, increasing points and total clicks.

        Increments points and total_points by 1 multiplied by click multipliers.
        Increments total_clicks by 1.
        """
        self.total_points += int(1 * self.click_multiplier * self.rebirth_click_multiplier)
        self.points += int(1 * self.click_multiplier * self.rebirth_click_multiplier)
        self.total_clicks += 1

    def idle_point(self):
        """
        Add idle points to the current points based on idle rate and rebirth multiplier.
        """
        self.points += int(self.idle * self.rebirth_idle)

    def can_afford(self, cost):
        """
        Check if the player has enough points to afford a cost.

        Parameters
        ----------
        cost : int
            The cost to check against the current points.

        Returns
        -------
        bool
            True if points are sufficient, False otherwise.
        """
        return cost <= self.points

    def spend_points(self, cost):
        """
        Deduct points after spending.

        Parameters
        ----------
        cost : int
            The amount of points to spend.

        Notes
        -----
        Assumes that can_afford has been checked before calling this method.
        """
        self.points -= cost
