"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell

from ui.filesTabs.editFileTab import EditFileTab

from ui.filesTabs.editCurvesTab import EditCurvesTab

from ui.filesTabs.seeFileTab import SeeFileTab

from constants.general_constants import FONT_SIZE


class FilesWindow(QTabWidgetWithWell):
    def __init__(self):
        super().__init__("Files window")
        
        self.tabs = [
            EditFileTab(),
            EditCurvesTab(),
            SeeFileTab()
        ]

        self.initUI()

    
    def initUI(self):
        self.add_tabs()
        #for tab in self.tabs:
        #    self.addTab(tab, tab.get_name())

        # Ej Stylesheet: https://gist.github.com/espdev/4f1565b18497a42d317cdf2531b7ef05

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

    def update_tab(self, well):
        if not super().update_tab(well):
            return
