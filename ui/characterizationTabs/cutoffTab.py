"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell
from ui.characterizationTabs.cutoffTabs.c1CutoffTab import C1CutoffTab
from ui.characterizationTabs.cutoffTabs.c2CutoffTab import C2CutoffTab
from ui.characterizationTabs.cutoffTabs.c3CutoffTab import C3CutoffTab
from ui.characterizationTabs.cutoffTabs.c4CutoffTab import C4CutoffTab
from ui.characterizationTabs.cutoffTabs.thicknessesTab import ThicknessesTab

from constants.general_constants import FONT_SIZE


class CutoffTab(QTabWidgetWithWell):
    def __init__(self):
        super().__init__("Parametros de corte")

        self.tabs = [
            C1CutoffTab(),
            C2CutoffTab(),
            C3CutoffTab(),
            C4CutoffTab(),
            ThicknessesTab()
        ]

        self.initUI()
    
    def initUI(self):
        self.add_tabs()

        self.setStyleSheet('''QTabBar::tab{width: ''' + str((100/9) * FONT_SIZE) + '''; \
            height: ''' + str((16/9) * FONT_SIZE) + '''; margin: 0; padding: 5; \
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
