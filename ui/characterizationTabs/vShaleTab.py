"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell

from constants.general_constants import FONT_SIZE

from ui.characterizationTabs.vShaleTabs.grTab import GRTab

from ui.characterizationTabs.vShaleTabs.neutronDensityTab import NeutronDensityTab

from ui.characterizationTabs.vShaleTabs.resistivityTab import ResistivityTab

from ui.characterizationTabs.vShaleTabs.spTab import SPTab


class VShaleTab(QTabWidgetWithWell):
    def __init__(self):
        super().__init__("V shale")

        self.tabs = [SPTab(),
                     GRTab(),
                     ResistivityTab(),
                     NeutronDensityTab()]

        self.initUI()

    def initUI(self):
        #self.gridLayout = QGridLayout()

        #self.setLayout(self.gridLayout)

        ########################################################################
        self.add_tabs()
        #for tab in self.tabs:
        #    self.addTab(tab, tab.get_name())

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
