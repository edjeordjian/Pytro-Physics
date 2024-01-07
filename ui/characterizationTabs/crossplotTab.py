"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell
from ui.characterizationTabs.crossplotTabs.genericCrossplotTab import GenericCrossplotTab
from ui.characterizationTabs.crossplotTabs.rhoShaleTab import RHOShaleTab
from ui.characterizationTabs.crossplotTabs.mNTab import MNTab
from ui.characterizationTabs.crossplotTabs.rhomaUmaaTab import RhomaUmaaTab
from ui.characterizationTabs.crossplotTabs.mineralIdentification1Tab import MineralIdentification1Tab
from ui.characterizationTabs.crossplotTabs.mineralIdentification2Tab import MineralIdentification2Tab
from ui.characterizationTabs.crossplotTabs.bucklesTab import BucklesTab
from ui.characterizationTabs.crossplotTabs.picketTab import PicketTab
from ui.characterizationTabs.crossplotTabs.hingleTab import HingleTab
from constants.general_constants import FONT_SIZE


class Crossplot(QTabWidgetWithWell):
    def __init__(self):
        super().__init__("Crossplot")
        
        self.tabs = [
            GenericCrossplotTab(),
            RHOShaleTab(),
            MNTab(),
            RhomaUmaaTab(),
            MineralIdentification1Tab(),
            MineralIdentification2Tab(),
            BucklesTab(),
            PicketTab(),
            HingleTab()
        ]

        self.initUI()

    def initUI(self):
        self.add_tabs()

        self.setStyleSheet('''QTabBar::tab{width: ''' + str((125/9) * FONT_SIZE) + '''; \
            height: ''' + str((28/9) * FONT_SIZE) + '''; margin: 0; padding: 4; \
            border: 1px solid black; font-size: ''' + str(FONT_SIZE) + '''pt}\
            QTabBar::tab:selected { \
                background: white;  \
            }                       \

            QTabBar::tab:!selected { \
                background: silver; \
            }
            
            QTabBar::tab:!selected:hover { \
                background: #999; \
            } \

            QTabBar::tab:top:selected { \
                border-bottom-color: none; \
            } \

            QTabBar::tab:bottom:selected { \
                border-top-color: none; \
            } \

            QTabBar::tab:left:selected { \
                border-left-color: none; \
            } \

            QTabBar::tab:right:selected { \
                border-right-color: none; \
            }''')

    def get_tab_name(self):
        return self.tab_name
