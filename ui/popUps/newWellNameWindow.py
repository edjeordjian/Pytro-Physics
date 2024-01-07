"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QWidget, QLabel, QFileDialog, QHBoxLayout,
                             QVBoxLayout, QPushButton, QLineEdit)
from constants.general_constants import las_extention

import traceback

from pathlib import Path

from constants.media_constants import APP_ICON_ROUTE
from services.tools.logger_service import log_error
from ui.popUps.alertWindow import AlertWindow


class NewWellNameWindow(QWidget):
    def __init__(self, wellName, saveWellFunction, wellExists):
        super().__init__()
        
        self.hLayout = QHBoxLayout()
        self.vLayout = QVBoxLayout()

        self.wellExists = wellExists
        self.wellName = wellName
        self.saveWellFunction = saveWellFunction

        self.setWindowTitle("Pozo")

        self.label = QLabel("Nombre del Pozo: ")

        self.setWindowIcon(QIcon(APP_ICON_ROUTE))

        self.wellNameQle = QLineEdit(self)
        self.wellNameQle.textChanged[str].connect(self.updateWellName)
        self.wellNameQle.setPlaceholderText("Ingrese el nombre del pozo")
        self.hLayout.addWidget(self.label)
        self.hLayout.addWidget(self.wellNameQle)

        self.saveNameButton = QPushButton("Guardar Pozo", self)
        
        self.saveNameButton.clicked.connect(
            lambda checked: self.saveButtonPressed()
        )
        
        self.wellNameQle.returnPressed.connect(self.saveNameButton.click)

        self.vLayout.addLayout(self.hLayout)
        self.vLayout.addWidget(self.saveNameButton)
        self.setLayout(self.vLayout)

    def saveButtonPressed(self):
        try:
            if self.wellExists(self.wellName):
                raise Exception("Ya existe un pozo con ese nombre, elige otro")

            file_uri = self.open_file_saving_prompt()

            self.saveWellFunction(file_uri,
                                  self.wellName,
                                  True)

            self.close()

        except Exception as ex:
            log_error(traceback.format_exc())

            AlertWindow(str(ex))

    def open_file_saving_prompt(self):
        file_url = QFileDialog.getSaveFileName(self,
                                               'Guardar archivo',
                                               self.wellName,
                                               "Archivo LAS (*.las)")[0]

        if len(file_url) == 0:
            raise Exception("Se debe especificar un nombre y una ruta para guardar el pozo")

        plain_url = file_url.split("/")

        file_name = plain_url.pop()

        plain_url = f"{'/'.join(plain_url)}/{self.wellName}"

        if las_extention not in file_name:
            raise Exception("Formato inválido: debe ser '.las'")

        if self.well_exists(file_name):
            raise Exception("Ya existe un pozo con ese nombre, elige otro")

        try:
            Path(plain_url).mkdir(parents=True,
                                  exist_ok=True)

        except OSError:
            raise Exception("Ocurrió un error al guardar el pozo")

        return f"{plain_url}/{file_name}"

    def updateWellName(self):
        self.wellName = self.wellNameQle.text()

    def well_exists(self,
                    file_name):
        return self.wellExists(file_name.replace(las_extention, ""))
