import time


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
