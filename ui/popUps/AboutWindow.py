"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from constants.general_constants import ABOUT_TEXT

from constants.media_constants import APP_ICON_ROUTE


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()

        self.setWindowIcon(QIcon(APP_ICON_ROUTE))

        self.setWindowTitle("Acerca de")

        self.label = QLabel()

        self.label.setText(ABOUT_TEXT)

        self.label.setOpenExternalLinks(True)

        self.layout.addWidget(self.label)

        self.setLayout(self.layout)
