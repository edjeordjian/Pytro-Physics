"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QMessageBox

from constants.media_constants import APP_ICON_ROUTE

icon_mapper = {
    "warn": QMessageBox.Icon.Warning,
    "info": QMessageBox.Icon.Information
}


class AlertWindow(QMessageBox):
    def __init__(self,
                 message,
                 title='Alerta',
                 kind='warn'):
        super().__init__()

        self.setIcon(icon_mapper[kind])

        self.setWindowIcon(QIcon(APP_ICON_ROUTE))

        self.setWindowTitle(title)

        self.setText(message)

        self.setStandardButtons(QMessageBox.StandardButton.Ok)

        self.exec()
