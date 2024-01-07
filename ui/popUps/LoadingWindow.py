"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import pyautogui

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from PyQt6.QtGui import QMovie, QIcon

from PyQt6.QtCore import Qt

from constants.media_constants import APP_ICON_ROUTE


class LoadingWindow(QWidget):
    def __init__(self,
                 message):
        super().__init__()

        width, height = pyautogui.size()

        self.setGeometry(int(width / 2 - 300 / 2),
                         int(height / 2 - 100 / 2),
                         300,
                         100)

        self.setWindowTitle('Cargando')
        self.setWindowIcon(QIcon(APP_ICON_ROUTE))

        self.vLayout = QVBoxLayout()

        self.label = QLabel(message)
        self.loading_gif_label = QLabel('')
        self.loading_gif = QMovie('media/loading.gif')
        self.loading_gif_label.setMovie(self.loading_gif)
        self.loading_gif.start()

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.loading_gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.vLayout\
            .addWidget(self.label)

        self.vLayout\
            .addWidget(self.loading_gif_label)

        self.setLayout(self.vLayout)

        self.show()
