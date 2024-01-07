"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QGridLayout, QSlider,
                             QPushButton, QLineEdit)
from PyQt6.QtCore import Qt


import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.messages_constants import MISSING_WELL
from constants.ipr_constants import PRECISION
from constants.LETTERS import COMBINING_OVERLINE
from constants.pytrophysicsConstants import SEE_WINDOW_LBL
from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow
from ui.style.StyleCombos import (color_combo_box, line_combo_box)
from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE

from services.ipr_service import get_klins_clark
from services.tools.string_service import is_number


class KlinsClarkTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Klins-Clark")

        self.initUI()

        self.numeric_inputs.extend([self.reservoirPressureQle, self.reservoirPressureQle, self.bubblePressureQle])

        self.add_serializable_attributes(self.curve_selectors + [self.iprCurveSizeSlider, self.iprLineStyleCbo,
              self.iprColorCbo, self.customMaxFlowQle, self.reservoirPressureQle, self.reservoirPressureQle,
              self.bubblePressureQle])


    def initUI(self):
        self.setLayout(self.gridLayout)

        row = 0

        self.reservoirPressureLbl = QLabel("Presion media del reservorio [psia] ( p" + COMBINING_OVERLINE + "<sub>r</sub> ):")
        self.reservoirPressureQle = QLineEdit()
        self.reservoirPressureQle.setStyleSheet(QLE_NAME_STYLE)
        self.reservoirPressureQle.setPlaceholderText("pr")

        self.reservoirPressureLayout = QHBoxLayout()
        self.reservoirPressureLayout.addWidget(self.reservoirPressureLbl)
        self.reservoirPressureLayout.addWidget(self.reservoirPressureQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.reservoirPressureLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.bubblePressureLbl = QLabel("Presion de burbuja [psia] ( p<sub>b</sub> ):")
        self.bubblePressureQle = QLineEdit()
        self.bubblePressureQle.setStyleSheet(QLE_NAME_STYLE)
        self.bubblePressureQle.setPlaceholderText("pb")

        self.bubblePressureLayout = QHBoxLayout()
        self.bubblePressureLayout.addWidget(self.bubblePressureLbl)
        self.bubblePressureLayout.addWidget(self.bubblePressureQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.bubblePressureLayout, row, 0, 1, 2)

        #######################################################################

        row += 1

        self.customMaxFlowLbl = QLabel("Caudal máximo [bbl/d] ( Q0Max ):")
        self.customMaxFlowQle = QLineEdit()
        self.customMaxFlowQle.setStyleSheet(QLE_NAME_STYLE)
        self.customMaxFlowQle.setPlaceholderText("Q0Max")

        self.customMaxFlowLayout = QHBoxLayout()
        self.customMaxFlowLayout.addWidget(self.customMaxFlowLbl)
        self.customMaxFlowLayout.addWidget(self.customMaxFlowQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.customMaxFlowLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.iprStyleLbl = QLabel("Color y Tipo de Linea: ")
        self.iprColorCbo = color_combo_box()
        self.iprColorCbo.setCurrentIndex(0)
        self.iprLineStyleCbo = line_combo_box()
        self.iprLineStyleCbo.setCurrentIndex(0)

        self.iprStyleLayout = QHBoxLayout()
        self.iprStyleLayout.addWidget(self.iprStyleLbl)
        self.iprStyleLayout.addWidget(self.iprColorCbo)
        self.iprStyleLayout.addWidget(self.iprLineStyleCbo)

        self.gridLayout.addLayout(self.iprStyleLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.iprCurveSizeLbl = QLabel("Precision (cantidad de valores en la curva IPR):")
        self.iprCurveSizeSlider = QSlider(Qt.Orientation.Horizontal, self)
        self.iprCurveSizeSlider.setMinimum(1)
        self.iprCurveSizeSlider.setMaximum(40)
        self.iprCurveSizeSlider.setValue(2)
        self.iprCurveSizeSliderValueLbl = QLabel(str(self.iprCurveSizeSlider.value() * PRECISION))
        self.iprCurveSizeSlider.valueChanged.connect(self.ipr_size_value_changed)

        self.iprCurveSizeLayout = QHBoxLayout()
        self.iprCurveSizeLayout.addWidget(self.iprCurveSizeLbl)
        self.iprCurveSizeLayout.addWidget(self.iprCurveSizeSlider)
        self.iprCurveSizeLayout.addWidget(self.iprCurveSizeSliderValueLbl)

        self.gridLayout.addLayout(self.iprCurveSizeLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2)

        row += 1

        self.previewBtn = QPushButton(CROSSPLOTS_CONSTANTS.PREVIEW_BUTTON)

        self.previewBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.previewBtn.clicked.connect(
            lambda checked: self.preview()
        )

        self.previewLayout = QHBoxLayout()

        self.seeWindowBtn = QPushButton(SEE_WINDOW_LBL)

        self.seeWindowBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.seeWindowBtn \
            .clicked \
            .connect(lambda: self.see_window())

        self.previewLayout.addWidget(self.previewBtn)

        self.previewLayout.addWidget(self.seeWindowBtn)

        self.gridLayout.addLayout(self.previewLayout, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        ########################################################################

        row += 1
        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2)

        ########################################################################

        row += 1

        self.nameLbl = QLabel("Nombre: ")
        self.nameQle = QLineEdit(self)
        self.nameQle.setStyleSheet(QLE_NAME_STYLE)
        self.nameLayout = QHBoxLayout()
        self.nameLayout.addWidget(self.nameLbl)
        self.nameLayout.addWidget(self.nameQle, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.gridLayout.addLayout(self.nameLayout, row, 0, 1, 1)

        ########################################################################

        row += 1

        self.saveCurveBtn = QPushButton(CROSSPLOTS_CONSTANTS.SAVE_CURVE_BUTTON)
        self.saveCurveBtn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.saveCurveBtn.clicked.connect(
            lambda checked: self.saveCurve()
        )
        
        self.gridLayout.addWidget(self.saveCurveBtn, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

    def ipr_size_value_changed(self, value):
        self.iprCurveSizeSliderValueLbl.setText(str(value * PRECISION))


    def checkErrorNumberInputs(self):
        if not is_number(self.reservoirPressureQle.text()):
            AlertWindow("El valor de presion del reservorio ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        if not is_number(self.bubblePressureQle.text()):
            AlertWindow("El valor de presion de burbuja ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True
        
        if float(self.reservoirPressureQle.text()) < float(self.bubblePressureQle.text()):
            AlertWindow("El valor de presion de reservorio ingresado es invalido, debe ser mayor o igual al valor de presion de burbuja")
            return True

        if not is_number(self.customMaxFlowQle.text()):
            AlertWindow("El valor de Q0Max ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        return False


    def getIpr(self):
        config_aux = get_klins_clark(
            pr = float(self.reservoirPressureQle.text()),
            pb = float(self.bubblePressureQle.text()),
            q0_max = float(self.customMaxFlowQle.text()),
            precision = self.iprCurveSizeSlider.value() * PRECISION
        )
        
        return config_aux


    def preview(self):
        if not super().preview():
            return

        if self.checkErrorNumberInputs():
            return

        config_aux = self.getIpr()

        if config_aux is None:
            AlertWindow("Error numerico al calcular IPR, por favor verifique los valores ingresados")
            return

        config = {
            'title': 'IPR - Klins - Clark',
            'x_axis_title': "Q0 [bbl/d]",
            'y_axis_title': "Pwf [psia]",
            'flex_size': 6,
            'invert_x': False,
            'invert_y': False,
            'log_x': False,
            'log_y': False,
            'scatter_groups': [],
            'line_groups': [{
                    'x_axis': config_aux['x_axis'],
                    'y_axis': config_aux['y_axis'],
                    'color': self.iprColorCbo.currentText(),
                    'line': self.iprLineStyleCbo.currentText()
                }
            ]
        }

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])


    def saveCurve(self):
        if not super().preview():
            return

        if str(self.nameQle.text()) == "":
            AlertWindow("El nombre de la curva no puede ser vacio")
            return

        ipr_curves = self.well.wellModel.get_ipr_curves()

        ipr_curve_names = list(map(lambda x: x["name"], ipr_curves))

        if str(self.nameQle.text()).upper() in set(ipr_curve_names):
            AlertWindow("Ya existe una curva de IPR con ese nombre")
            return

        if self.checkErrorNumberInputs():
            return

        config_aux = self.getIpr()

        if config_aux is None:
            AlertWindow("Error numerico al calcular IPR, por favor verifique los valores ingresados")
            return

        ipr_curves.append({
            "name": str(self.nameQle.text()).upper(),
            "x_axis": config_aux["x_axis"],
            "y_axis": config_aux["y_axis"]
        })
        
        self.well.wellModel.set_ipr_curves(ipr_curves)

        self.well.wellModel.save_ipr_curves()

        InformationWindow("Curva guardada")

    def update_tab(self, well=None, force_update=False):
        super().update_tab(well, force_update=force_update)
