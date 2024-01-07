"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import QTabWidget, QScrollArea


class ScrollableWellWrapper(QTabWidget):
    def __init__(self, tab):
        super().__init__()

        scrollArea = QScrollArea()

        scrollArea.setWidgetResizable(True)

        scrollArea.setWidget(tab)

        self.tab = tab

        self.addTab(scrollArea, tab.get_name())

    def update_tab(self, well):
        return self.tab.update_tab(well)
