"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QMessageBox

from constants.media_constants import APP_ICON_ROUTE

from ui.popUps.alertWindow import icon_mapper


class YesOrNoQuestion(QMessageBox):
    def __init__(self, message, yes_fn, no_fn,
                 title="Confirmación"):
        super().__init__()

        self.setIcon(icon_mapper["info"])

        self.setWindowIcon(QIcon(APP_ICON_ROUTE))

        self.setWindowTitle(title)

        self.setText(message)

        yes_button = self.addButton('Sí', QMessageBox.ButtonRole.YesRole)

        yes_button.clicked.connect(yes_fn)

        no_button = self.addButton('No', QMessageBox.ButtonRole.NoRole)

        no_button.clicked.connect(no_fn)

        self.exec()
