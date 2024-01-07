"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import QTabWidget, QScrollArea

from constants.general_constants import FONT_SIZE


class QTabWidgetWithWell(QTabWidget):
    def __init__(self, screen_name):
        super().__init__()

        self.well = None

        self.screen_name = screen_name

        self.tabs = []

        self.currentChanged.connect(self._updateTab)

    def update_tab(self,
                   well):
        print("Update: " + self.screen_name)

        self.well = well

        for tab in self.tabs:
            tab.update_tab(well)
    
    def _updateTab(self, tabIndex):
        if self.well is not None:
            self.tabs[tabIndex].update_tab(self.well)

    def add_tabs(self):
        for tab in self.tabs:
            scrollArea = QScrollArea()
            scrollArea.setWidgetResizable(True)
            scrollArea.setWidget(tab)
            self.addTab(scrollArea, tab.get_name())

    def get_name(self):
        return self.screen_name

    def initUI(self, tab_width=14):
        self.add_tabs()

        self.setStyleSheet('''QTabBar::tab{width: ''' + str(tab_width * FONT_SIZE) + '''; \
            height: ''' + str((16 / 9) * FONT_SIZE) + '''; margin: 0; padding: 5; \
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

    def get_tabs(self):
        return self.tabs
