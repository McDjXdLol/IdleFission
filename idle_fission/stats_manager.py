import time


class StatsManager:

    @staticmethod
    def show_stats(point_manager, shop, achievements, rebirth, time_played):
        """
        Generate a formatted string summary of game stats.

        Parameters
        ----------
        point_manager : PointManager
            Instance managing points and multipliers.
        shop : Shop
            Instance managing upgrades and shop state.
        achievements : Achievements
            Instance managing achievements and their status.
        rebirth : Rebirth
            Instance managing rebirth mechanics and bonuses.
        time_played : float
            Total time played in seconds.

        Returns
        -------
        str
            Formatted multi-line string containing stats summary.
        """
        total_upgrades_bought = 0
        for x in shop.bought_upgrades:
            total_upgrades_bought += x[1]

        total_achievements_got = 0
        total_achievements_reward_granted = 0
        for cond in achievements.conditions:
            if cond["unlocked"]:
                total_achievements_got += 1
                for ach in achievements.achievements:
                    if ach["condition_id"] == cond["title"]:
                        total_achievements_reward_granted += ach["reward"]

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
