"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox, QSlider,
                             QPushButton, QComboBox, QCheckBox, QLineEdit)
from PyQt6.QtCore import Qt

import numpy as np

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.messages_constants import MISSING_WELL
from constants.ipr_constants import PRECISION
from constants.LETTERS import (CAPITAL_B, MU, COMBINING_OVERLINE)
from constants.pytrophysicsConstants import SEE_WINDOW_LBL
from constants.general_constants import METERS_LBL, FEETS_LBL
from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow
from ui.style.StyleCombos import (color_combo_box, line_combo_box)
from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE

from services.ipr_service import (get_darcy, get_h_from_curve, get_k_from_curve)
from services.tools.string_service import is_number


class DarcyTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Darcy")

        self.initUI()

        self.numeric_inputs.extend([self.customMinDepthQle, self.customMaxDepthQle, self.customMaxFlowQle,
         self.netPayQle, self.permeabilityQle, self.reservoirPressureQle,
         self.damageFactorQle, self.wellRadiusQle, self.reservoirRadiusQle,
         self.volumeFactorQle, self.viscosityQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
              self.customMinDepthQle, self.customMaxDepthQle, self.iprCurveSizeSlider, self.iprLineStyleCbo,
              self.iprColorCbo, self.customMaxFlowQle, self.customMaxFlowRb, self.defaultMaxFlowRb,
              self.netPayQle, self.permeabilityQle, self.reservoirPressureQle,
              self.damageFactorQle, self.wellRadiusQle, self.reservoirRadiusQle,
              self.volumeFactorQle, self.viscosityQle, self.netPayCurveCb, self.permeabilityCurveCb,
              self.distanceUnitMetersRb, self.distanceUnitFeetRb])

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0

        self.distanceUnitGrpBox = QGroupBox("Unidad de distancia")
        self.distanceUnitLayout = QHBoxLayout()
        self.distanceUnitMetersRb = QRadioButton("Distancia en metros [m]")
        self.distanceUnitFeetRb = QRadioButton("Distancia en pies [Ft]")
        self.distanceUnitMetersRb.setChecked(True)
        self.distanceUnitMetersRb.toggled.connect(self.change_distance_unit)
        self.distanceUnitFeetRb.toggled.connect(self.change_distance_unit)

        self.distanceUnitLayout.addWidget(self.distanceUnitMetersRb)
        self.distanceUnitLayout.addWidget(self.distanceUnitFeetRb)
        self.distanceUnitGrpBox.setLayout(self.distanceUnitLayout)
        self.gridLayout.addWidget(self.distanceUnitGrpBox, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.viscosityLbl = QLabel("Viscosidad del petroleo [cP] (" + MU + "<sub>0</sub>):")
        self.viscosityQle = QLineEdit()
        self.viscosityQle.setStyleSheet(QLE_NAME_STYLE)
        self.viscosityQle.setPlaceholderText(MU + "0")

        self.viscosityLayout = QHBoxLayout()
        self.viscosityLayout.addWidget(self.viscosityLbl)
        self.viscosityLayout.addWidget(self.viscosityQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.viscosityLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.volumeFactorLbl = QLabel("Factor de volumen del petroleo [RB/STB] (" + CAPITAL_B + "<sub>0</sub>):")
        self.volumeFactorQle = QLineEdit()
        self.volumeFactorQle.setStyleSheet(QLE_NAME_STYLE)
        self.volumeFactorQle.setPlaceholderText(CAPITAL_B + "0")

        self.volumeFactorLayout = QHBoxLayout()
        self.volumeFactorLayout.addWidget(self.volumeFactorLbl)
        self.volumeFactorLayout.addWidget(self.volumeFactorQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.volumeFactorLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.reservoirRadiusLbl = QLabel("Radio del reservorio [m] (r<sub>e</sub>):")
        self.reservoirRadiusQle = QLineEdit()
        self.reservoirRadiusQle.setStyleSheet(QLE_NAME_STYLE)
        self.reservoirRadiusQle.setPlaceholderText("re")

        self.reservoirRadiusLayout = QHBoxLayout()
        self.reservoirRadiusLayout.addWidget(self.reservoirRadiusLbl)
        self.reservoirRadiusLayout.addWidget(self.reservoirRadiusQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.reservoirRadiusLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.wellRadiusLbl = QLabel("Radio del pozo [m] (r<sub>w</sub>):")
        self.wellRadiusQle = QLineEdit()
        self.wellRadiusQle.setStyleSheet(QLE_NAME_STYLE)
        self.wellRadiusQle.setPlaceholderText("rw")

        self.wellRadiusLayout = QHBoxLayout()
        self.wellRadiusLayout.addWidget(self.wellRadiusLbl)
        self.wellRadiusLayout.addWidget(self.wellRadiusQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.wellRadiusLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.damageFactorLbl = QLabel("Factor de daño (S):")
        self.damageFactorQle = QLineEdit()
        self.damageFactorQle.setStyleSheet(QLE_NAME_STYLE)
        self.damageFactorQle.setPlaceholderText("S")

        self.damageFactorLayout = QHBoxLayout()
        self.damageFactorLayout.addWidget(self.damageFactorLbl)
        self.damageFactorLayout.addWidget(self.damageFactorQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.damageFactorLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

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

        self.permeabilityLbl = QLabel("Permeabilidad [mD] (k):")
        self.permeabilityQle = QLineEdit()
        self.permeabilityQle.setStyleSheet(QLE_NAME_STYLE)
        self.permeabilityQle.setPlaceholderText("k")

        self.permeabilityLayout = QHBoxLayout()
        self.permeabilityLayout.addWidget(self.permeabilityLbl)
        self.permeabilityLayout.addWidget(self.permeabilityQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.permeabilityLayout, row, 0, 1, 2)

        ########################################################################

        row += 1
        self.permeabilityCurveCb = QCheckBox("Tomar (valor medio de) curva de Permeabilidad")
        self.permeabilityCurveCbo = QComboBox(self)
        self.permeabilityCurveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.permeabilityCurveCbo)
        self.permeabilityCurveCbo.setEnabled(False)

        self.permeabilityCurveCb.stateChanged.connect(self.usePermeabilityCurve)

        self.permeabilityCurveLayout = QHBoxLayout()
        self.permeabilityCurveLayout.addWidget(self.permeabilityCurveCbo)
        self.permeabilityCurveLayout.addWidget(QLabel(""))
        
        self.gridLayout.addWidget(self.permeabilityCurveCb, row, 0, 1, 1)
        self.gridLayout.addLayout(self.permeabilityCurveLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

        self.netPayLbl = QLabel("Net Pay [m] (h):")
        self.netPayQle = QLineEdit()
        self.netPayQle.setStyleSheet(QLE_NAME_STYLE)
        self.netPayQle.setPlaceholderText("h")

        self.netPayLayout = QHBoxLayout()
        self.netPayLayout.addWidget(self.netPayLbl)
        self.netPayLayout.addWidget(self.netPayQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.netPayLayout, row, 0, 1, 2)

        ########################################################################

        row += 1
        self.netPayCurveCb = QCheckBox("Tomar (valor medio de) curva de Net Pay")
        self.netPayCurveCbo = QComboBox(self)
        self.netPayCurveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.netPayCurveCbo)
        self.netPayCurveCbo.setEnabled(False)

        self.netPayCurveCb.stateChanged.connect(self.useNetPayCurve)

        self.netPayCurveLayout = QHBoxLayout()
        self.netPayCurveLayout.addWidget(self.netPayCurveCbo)
        self.netPayCurveLayout.addWidget(QLabel(""))

        self.gridLayout.addWidget(self.netPayCurveCb, row, 0, 1, 1)
        self.gridLayout.addLayout(self.netPayCurveLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

        #https://geekscoders.com/courses/pyqt6-tutorials/lessons/how-to-create-qradiobutton-in-pyqt6/

        self.depthGrpBox = QGroupBox("Profundidad")
        #self.grpbox.setFont(QFont("Times New Roman", 15))

        # this is vbox layout
        self.depthLayout = QVBoxLayout()

        # these are the radiobuttons
        self.depthFullLasRb = QRadioButton("Todo el LAS")
        self.depthFullLasRb.setChecked(True)
        #self.depthFullLasRb.setFont(QFont("Times New Roman", 14))
        self.depthFullLasRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthFullLasRb)

        self.depthCustomRb = QRadioButton("personalizado")
        #self.depthCustomRb.setFont(QFont("Times New Roman", 14))
        self.depthCustomRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthCustomRb)

        self.depthGrpBox.setLayout(self.depthLayout)

        self.depthGrpBox.setEnabled(False)

        self.gridLayout.addWidget(self.depthGrpBox, row, 0, 1, 1)

        ########################################################################

        self.customMinDepthLbl = QLabel("Profundidad mín.: ")
        self.customMinDepthQle = QLineEdit(self)
        self.customMinDepthLayout = QHBoxLayout()
        self.customMinDepthLayout.addWidget(self.customMinDepthLbl)
        self.customMinDepthLayout.addWidget(self.customMinDepthQle)
        self.customMinDepthQle.setEnabled(False)

        self.customMaxDepthLbl = QLabel("Profundidad máx.:")
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle)
        self.customMaxDepthQle.setEnabled(False)

        self.customDepthLayout = QVBoxLayout()
        self.customDepthLayout.addLayout(self.customMinDepthLayout)
        self.customDepthLayout.addLayout(self.customMaxDepthLayout)
        self.gridLayout.addLayout(self.customDepthLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

        self.maxFlowGrp = QGroupBox("Q0 Max")
        
        self.maxFlowLayout = QVBoxLayout()

        self.defaultMaxFlowRb = QRadioButton("Calcular Q0Max como Q0(Pwf=0)")
        self.defaultMaxFlowRb.setChecked(True)
        self.defaultMaxFlowRb.toggled.connect(self.setMaxFlow)
        self.maxFlowLayout.addWidget(self.defaultMaxFlowRb)
        
        self.customMaxFlowRb = QRadioButton("Introducir valor de Q0Max: ")
        self.customMaxFlowRb.toggled.connect(self.setMaxFlow)
        self.customMaxFlowQle = QLineEdit(self)
        self.customMaxFlowQle.setPlaceholderText("Q0Max")
        self.customMaxFlowQle.setEnabled(False)

        self.customMaxFlowLayout = QHBoxLayout()
        self.customMaxFlowLayout.addWidget(self.customMaxFlowRb)
        self.customMaxFlowLayout.addWidget(self.customMaxFlowQle)
        self.maxFlowLayout.addLayout(self.customMaxFlowLayout)

        self.maxFlowGrp.setLayout(self.maxFlowLayout)

        # Q0 Custom can be set if the line below is uncommented (delete the '#' symbol)
        #self.gridLayout.addWidget(self.maxFlowGrp, row, 0, 1, 2)

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


    # method or slot for the toggled signal
    def on_selected(self):
        radio_button = self.sender()
        
        if radio_button.isChecked():
            print("You have selected : " + radio_button.text())
        #    self.label.setText("You have selected : " + radio_button.text())

        self.customMinDepthQle.setEnabled(self.depthCustomRb.isChecked())
        self.customMaxDepthQle.setEnabled(self.depthCustomRb.isChecked())


    def change_distance_unit(self):
        if self.distanceUnitMetersRb.isChecked():
            self.reservoirRadiusLbl.setText("Radio del reservorio [m] (r<sub>e</sub>):")
            self.wellRadiusLbl.setText("Radio del pozo [m] (r<sub>w</sub>):")
            self.netPayLbl.setText("Net Pay [m] (h):")
        else:
            self.reservoirRadiusLbl.setText("Radio del reservorio [ft] (r<sub>e</sub>):")
            self.wellRadiusLbl.setText("Radio del pozo [ft] (r<sub>w</sub>):")
            self.netPayLbl.setText("Net Pay [ft] (h):")


    def setMaxFlow(self):
        self.customMaxFlowQle.setEnabled(self.customMaxFlowRb.isChecked())


    def usePermeabilityCurve(self, state):
        self.permeabilityLbl.setEnabled(state == 0)
        self.permeabilityQle.setEnabled(state == 0)
        self.permeabilityCurveCbo.setEnabled(state != 0)
        self.depthGrpBox.setEnabled(state != 0 or self.netPayCurveCb.isChecked())


    def useNetPayCurve(self, state):
        self.netPayLbl.setEnabled(state == 0)
        self.netPayQle.setEnabled(state == 0)
        self.netPayCurveCbo.setEnabled(state != 0)
        self.depthGrpBox.setEnabled(state != 0 or self.permeabilityCurveCb.isChecked())


    def ipr_size_value_changed(self, value):
        self.iprCurveSizeSliderValueLbl.setText(str(value * PRECISION))


    def checkErrorNumberInputs(self):
        if not is_number(self.viscosityQle.text()):
            AlertWindow("El valor de viscosidad ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        if not is_number(self.volumeFactorQle.text()):
            AlertWindow("El valor de factor de volumen ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True
            
        if not is_number(self.reservoirRadiusQle.text()):
            AlertWindow("El valor de radio del reservorio ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        if not is_number(self.wellRadiusQle.text()):
            AlertWindow("El valor de radio del pozo ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        if not is_number(self.damageFactorQle.text()):
            AlertWindow("El valor de factor de daño ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True
            
        if not is_number(self.reservoirPressureQle.text()):
            AlertWindow("El valor de presion del reservorio ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        if not self.permeabilityCurveCb.isChecked() and (not is_number(self.permeabilityQle.text())):
            AlertWindow("El valor de permeabilidad ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        if not self.netPayCurveCb.isChecked() and (not is_number(self.netPayQle.text())):
            AlertWindow("El valor de net pay ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        if self.customMaxFlowRb.isChecked() and (not is_number(self.customMaxFlowQle.text())):
            AlertWindow("El valor de Q0Max ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
            return True

        return False


    def checkErrorCurveInputs(self):
        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))
        
        if self.permeabilityCurveCb.isChecked():
            permeability = self.well.wellModel.get_partial_ranged_df_curve(self.permeabilityCurveCbo.currentText(), minDepth, maxDepth, "", "")
            permeability[permeability == 0] = np.nan
            permeability = permeability[~np.isnan(permeability)]
            if len(permeability) < 1:
                AlertWindow("La curva de permeabilidad (k) elegida solo contiene valores nulos o 0s en el rango de profundidad elegido")
                return True

        if self.netPayCurveCb.isChecked():
            netPay = self.well.wellModel.get_partial_ranged_df_curve(self.netPayCurveCbo.currentText(), minDepth, maxDepth, "", "")
            netPay = netPay[~np.isnan(netPay)]
            if len(netPay) < 1:
                AlertWindow("La curva de Net Pay (h) elegida solo contiene valores nulos en el rango de profundidad elegido")
                return True
        
        return False


    def getIpr(self):
        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        if self.permeabilityCurveCb.isChecked():
            permeability = self.well.wellModel.get_partial_ranged_df_curve(self.permeabilityCurveCbo.currentText(), minDepth, maxDepth, "", "")
            permeability = str(get_k_from_curve(permeability))
        else:
            permeability = str(self.permeabilityQle.text())

        if self.netPayCurveCb.isChecked():
            netPay = self.well.wellModel.get_partial_ranged_df_curve(self.netPayCurveCbo.currentText(), minDepth, maxDepth, "", "")
            minDepthNetPay = minDepth
            maxDepthNetPay = maxDepth
            if self.well.wellModel.get_depth_unit() == METERS_LBL:
                minDepthNetPay = str((1/0.304800609601) * float(minDepth))
                maxDepthNetPay = str((1/0.304800609601) * float(maxDepth))
            netPay = str(get_h_from_curve(netPay, minDepthNetPay, maxDepthNetPay))
        else:
            netPay = self.netPayQle.text()
            if self.distanceUnitMetersRb.isChecked():
                netPay = str((1/0.304800609601) * float(netPay))

        config_aux = get_darcy(
            mu_0 = float(self.viscosityQle.text()),
            b_0 = float(self.volumeFactorQle.text()),
            re = float(self.reservoirRadiusQle.text()),
            rw = float(self.wellRadiusQle.text()),
            s = float(self.damageFactorQle.text()),
            pr = float(self.reservoirPressureQle.text()),
            k = float(permeability),
            h = float(netPay),
            q0_max = None if self.defaultMaxFlowRb.isChecked() else float(self.customMaxFlowQle.text()),
            precision = self.iprCurveSizeSlider.value() * PRECISION
        )
        
        return config_aux

    def preview(self):
        if not super().preview():
            return

        if self.checkErrorCurveInputs():
            return

        config_aux = self.getIpr()

        config = {
            'title': 'IPR - Darcy',
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

        if self.checkErrorCurveInputs():
            return

        config_aux = self.getIpr()

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
        self.permeabilityCurveCbo.setCurrentIndex(0)
        self.netPayCurveCbo.setCurrentIndex(0)
