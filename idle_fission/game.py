from GUI_manager import GUIManager
from achievements import Achievements
from point_manager import PointManager
from rebirth import Rebirth
from shop import Shop

def main():
    """
    Main entry point for the game application.

    Initializes the core game components including:
    - PointManager for handling points and clicks,
    - Shop for upgrades,
    - Rebirth system,
    - Achievements tracking,
    - GUI management.

    Builds and runs the GUI application.

    Returns
    -------
    None
    """
    pt_manager = PointManager()
    shop = Shop(pt_manager)
    rebir = Rebirth(pt_manager, shop)
    achv = Achievements(pt_manager, shop, rebir)
    GUI = GUIManager(pt_manager, shop, achv, rebir)
    app = GUI.app
    GUI.build()
    GUI.run()

if __name__ == "__main__":
    main()
