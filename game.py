from GUI_manager import GUIManager
from achievements import Achievements
from point_manager import PointManager
from rebirth import Rebirth
from shop import Shop

if __name__ == "__main__":
    pt_manager = PointManager()
    shop = Shop(pt_manager)
    rebir = Rebirth(pt_manager, shop)
    achv = Achievements(pt_manager, shop, rebir)
    GUI = GUIManager(pt_manager, shop, achv, rebir)
    app = GUI.app
    GUI.build()
    GUI.run()