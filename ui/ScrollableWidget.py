"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QWidget, QScrollArea

from constants.media_constants import VIEW_ICON_ROUTE


class ScrollableWidget(QWidget):
    def __init__(self, layout):
        super().__init__()

        self.layout = layout

        self.setLayout(self.layout)

    def _init_scroll_area(self, x, y, w,
                          h, title):
        self.scrollArea = QScrollArea()

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.scrollArea.setWidgetResizable(True)

        self.scrollArea.setWindowTitle(title)

        self.scrollArea.setWindowIcon(QIcon(VIEW_ICON_ROUTE))

        self.scrollArea.setGeometry(x, y, w, h)

        self.scrollArea.setWidget(self)

    def show(self):
        self.scrollArea.show()

    def closeEvent(self, event):
        self.scrollArea.close()

        super().closeEvent(event)
