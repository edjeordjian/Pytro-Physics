"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel,
        QFileDialog, QHBoxLayout, QVBoxLayout, QGridLayout,
        QRadioButton,QGroupBox,
        QPushButton, QComboBox, QCheckBox, QLineEdit)

from PyQt6.QtCore import Qt

import numpy as np

from constants.general_constants import FARENHEIT_UNIT_LBL, CELCIUS_UNIT_LBL, METERS_LBL

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS

from constants.pytrophysicsConstants import READ_MODE_WELL_NAME, SEE_WINDOW_LBL

from constants.sw_constants import CELCIUS_LBL, FARENHEIT_LBL

from constants.tab_constants import TEMPERATURE_TAB_NAME

from constants.messages_constants import (MISSING_CURVE_NAME, MISSING_CURVE_TO_SAVE,
                                          CURVE_ALREADY_EXISTS_QUESTION_LBL)

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.informationWindow import InformationWindow

from ui.popUps.YesOrNoQuestion import YesOrNoQuestion

from ui.style.StyleCombos import (color_combo_box, marker_combo_box, line_combo_box)

from services.temperature_service import (get_geothermal_gradient,
                                          get_temperature)

from services.tools.string_service import is_number
from ui.style.button_styles import SAVE_BUTTON_STYLE, QLE_DEPTH_STYLE, PREVIEW_BUTTON_STYLE


class TemperatureTab(QWidgetWithWell):
    def __init__(self):
        super().__init__(TEMPERATURE_TAB_NAME)
        self.graphWindow = None

        self.initUI()

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################

        row = 0

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

        self.gridLayout.addWidget(self.depthGrpBox, row, 0, 2, 1)

        self.customMinDepthLbl = QLabel("Profundidad mín.:  ")
        self.customMinDepthLbl.setStyleSheet(QLE_DEPTH_STYLE)
        self.customMinDepthQle = QLineEdit(self)
        self.customMinDepthLayout = QHBoxLayout()
        self.customMinDepthLayout.addWidget(self.customMinDepthLbl)
        self.customMinDepthLayout.addWidget(self.customMinDepthQle, alignment=Qt.AlignmentFlag.AlignLeft)
        self.customMinDepthQle.setEnabled(False)

        self.customMaxDepthLbl = QLabel("Profundidad máx.:")
        self.customMaxDepthLbl.setStyleSheet(QLE_DEPTH_STYLE)
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle, alignment=Qt.AlignmentFlag.AlignLeft)
        self.customMaxDepthQle.setEnabled(False)

        self.customMaxDepthQle.textChanged[str].connect(self.maxDepthChanged)

        self.gridLayout.addLayout(self.customMinDepthLayout, row, 1, 1, 1)

        row += 1

        self.gridLayout.addLayout(self.customMaxDepthLayout, row, 1, 1, 1)

        ########################################################################
        
        row += 1

        self.temperatureGrpBox = QGroupBox("Temperatura")
        self.temperatureGrpLayout = QVBoxLayout()

        #######################################################################

        self.temperatureCurveRb = QRadioButton("Registro")
        self.temperatureCurveCbo = QComboBox(self)
        self.temperatureCurveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.temperatureCurveCbo)

        self.temperatureCurveRb.setChecked(True)
        self.temperatureCurveRb.toggled.connect(self.temperatureSelection)

        self.temperatureCurveLayout = QHBoxLayout()
        self.temperatureCurveLayout.addWidget(self.temperatureCurveRb)
        self.temperatureCurveLayout.addWidget(self.temperatureCurveCbo)

        self.temperatureGrpLayout.addLayout(self.temperatureCurveLayout)

        ########################################################################

        self.temperatureCalcRb = QRadioButton("Calculo indirecto")

        self.temperatureCalcRb.toggled.connect(self.temperatureSelection)

        self.temperatureGrpLayout.addWidget(self.temperatureCalcRb)

        ########################################################################

        self.temperatureCalcGrpBox = QGroupBox("Calculo indirecto")
        self.temperatureCalcGrpLayout = QVBoxLayout()

        ########################################################################

        self.temperature_group_box = QGroupBox("Escala de temperatura")

        self.temperature_group_box_layout = QVBoxLayout()

        self.temperature_celcius_scale_rb = QRadioButton(CELCIUS_LBL)

        self.temperature_celcius_scale_rb.setChecked(True)

        self.temperature_group_box_layout.addWidget(self.temperature_celcius_scale_rb)

        self.temperature_farenehit_scale_rb = QRadioButton(FARENHEIT_LBL)

        self.temperature_group_box_layout.addWidget(self.temperature_farenehit_scale_rb)

        self.temperature_group_box.setLayout(self.temperature_group_box_layout)

        self.temperatureCalcGrpLayout.addWidget(self.temperature_group_box)

        #########################################################################

        self.gg_group_box = QGroupBox("Gradiente geotérmico")
        self.gg_group_layout = QVBoxLayout()

        self.ggRb = QRadioButton("Valor de GG:                                                ")
        self.ggQle = QLineEdit()
        self.ggQle.setStyleSheet(QLE_DEPTH_STYLE)
        self.ggUnitLbl = QLabel("[T]/Km")

        self.ggRb.setChecked(True)
        self.ggRb.toggled.connect(self.ggSelection)

        self.ggLayout = QHBoxLayout()
        self.ggLayout.addWidget(self.ggRb)
        self.ggLayout.addWidget(self.ggQle, alignment=Qt.AlignmentFlag.AlignLeft)
        self.ggLayout.addWidget(self.ggUnitLbl)

        self.envTempRb = QRadioButton("Calcular GG tomando temperatura ambiente: ")
        self.envTempQle = QLineEdit()
        self.envTempQle.setStyleSheet(QLE_DEPTH_STYLE)
        self.envTempUnitLbl = QLabel("[T]")

        self.envTempRb.toggled.connect(self.ggSelection)
        self.envTempQle.setEnabled(False)
        self.envTempUnitLbl.setEnabled(False)

        self.envTempLayout = QHBoxLayout()
        self.envTempLayout.addWidget(self.envTempRb)
        self.envTempLayout.addWidget(self.envTempQle, alignment=Qt.AlignmentFlag.AlignLeft)
        self.envTempLayout.addWidget(self.envTempUnitLbl)

        self.gg_group_layout.addLayout(self.ggLayout)
        self.gg_group_layout.addLayout(self.envTempLayout)
        self.gg_group_box.setLayout(self.gg_group_layout)

        self.temperatureCalcGrpLayout.addWidget(self.gg_group_box)

        ##########################################################################

        self.bhtGrpBox = QGroupBox("BHT")
        self.bhtGrpLayout = QVBoxLayout()

        self.bhtCurveRb = QRadioButton("Tomar del LAS: ")
        self.bhtCurveCbo = QComboBox()
        self.bhtCurveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.bhtCurveCbo)
        
        self.bhtCurveRb.setChecked(True)
        self.bhtCurveRb.toggled.connect(self.bhtSelection)

        self.bhtCurveLayout = QHBoxLayout()
        self.bhtCurveLayout.addWidget(self.bhtCurveRb)
        self.bhtCurveLayout.addWidget(self.bhtCurveCbo, alignment=Qt.AlignmentFlag.AlignLeft)

        self.bhtCustomRb = QRadioButton("Valor BHT Custom: ")
        self.bhtCustomQle = QLineEdit()

        self.bhtCustomRb.toggled.connect(self.bhtSelection)
        self.bhtCustomQle.setEnabled(False)

        self.bhtCustomLayout = QHBoxLayout()
        self.bhtCustomLayout.addWidget(self.bhtCustomRb)
        self.bhtCustomLayout.addWidget(self.bhtCustomQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.bhtGrpLayout.addLayout(self.bhtCurveLayout)
        self.bhtGrpLayout.addLayout(self.bhtCustomLayout)
        self.bhtGrpBox.setLayout(self.bhtGrpLayout)

        self.temperatureCalcGrpLayout.addWidget(self.bhtGrpBox)

        #########################################################################

        self.zBhtGrpBox = QGroupBox("Z_bht")
        self.zBhtGrpLayout = QVBoxLayout()

        self.zBhtCurveRb = QRadioButton("Tomar máximo de curva de profundidad")

        self.zBhtCurveRb.setChecked(True)
        self.zBhtCurveRb.toggled.connect(self.zBhtSelection)

        self.zBhtCustomRb = QRadioButton("Valor Z_bht Custom: ")
        self.zBhtCustomQle = QLineEdit()

        self.zBhtCustomRb.toggled.connect(self.zBhtSelection)
        self.zBhtCustomQle.setEnabled(False)

        self.zBhtCustomLayout = QHBoxLayout()
        self.zBhtCustomLayout.addWidget(self.zBhtCustomRb)
        self.zBhtCustomLayout.addWidget(self.zBhtCustomQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.zBhtGrpLayout.addWidget(self.zBhtCurveRb)
        self.zBhtGrpLayout.addLayout(self.zBhtCustomLayout)
        self.zBhtGrpBox.setLayout(self.zBhtGrpLayout)

        self.temperatureCalcGrpLayout.addWidget(self.zBhtGrpBox)

        #########################################################################

        self.nameLbl = QLabel("Nombre: ")
        self.nameQle = QLineEdit(self)
        self.nameLayout = QHBoxLayout()
        self.nameLayout.addWidget(self.nameLbl)
        self.nameLayout.addWidget(self.nameQle, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.temperatureCalcGrpLayout.addLayout(self.nameLayout)

        ########################################################################

        self.saveCurveBtn = QPushButton("Guardar curva de temperatura")
        self.saveCurveBtn.clicked.connect(
            lambda checked: self.saveCurve()
        )

        self.saveCurveBtn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.temperatureCalcGrpLayout.addWidget(QLabel(""))

        self.temperatureCalcGrpLayout.addWidget(self.saveCurveBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        ##########################################################################

        self.temperatureCalcGrpBox.setEnabled(False)
        self.temperatureCalcGrpBox.setLayout(self.temperatureCalcGrpLayout)
        self.temperatureGrpLayout.addWidget(self.temperatureCalcGrpBox)     

        ########################################################################

        self.temperatureGrpBox.setLayout(self.temperatureGrpLayout)
        self.gridLayout.addWidget(self.temperatureGrpBox, row, 0, 1, 2)

        ########################################################################

        row += 1
        self.curveStyleLbl = QLabel("Estilo de la curva:")
        self.gridLayout.addWidget(self.curveStyleLbl, row, 0, 1, 2)

        ########################################################################

        row += 1
        self.curveStyleLayout = QHBoxLayout()

        self.curveColorCbo = color_combo_box()
        self.curveLineCbo = line_combo_box()
        self.curveMarkerCbo = marker_combo_box()

        self.curveStyleLayout.addWidget(self.curveColorCbo)
        self.curveStyleLayout.addWidget(self.curveLineCbo)
        self.curveStyleLayout.addWidget(self.curveMarkerCbo)

        self.gridLayout.addLayout(self.curveStyleLayout, row, 0, 1, 2)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2)

        row += 1

        self.previewBtn = QPushButton(CROSSPLOTS_CONSTANTS.PREVIEW_BUTTON)

        self.previewBtn.clicked.connect(
            lambda checked: self.preview()
        )

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 1)

        row += 1

        self.previewBtn \
            .setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.previewLayout = QHBoxLayout()

        self.seeWindowBtn = QPushButton(SEE_WINDOW_LBL)

        self.seeWindowBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.seeWindowBtn \
            .clicked \
            .connect(lambda: self.see_window())

        self.previewLayout.addWidget(self.previewBtn)

        self.previewLayout.addWidget(self.seeWindowBtn)

        self.gridLayout.addLayout(self.previewLayout, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        #######################################################################

        self.numeric_inputs.extend([self.zBhtCustomQle, self.ggQle, self.bhtCustomQle])

        self.add_serializable_attributes(self.curve_selectors +
                                         [self.depthFullLasRb, self.depthCustomRb,
                                          self.curveMarkerCbo, self.curveLineCbo, self.curveColorCbo,
                                          self.temperatureCalcRb, self.temperatureCurveRb, self.envTempRb,
                                          self.ggRb, self.ggQle, self.envTempQle, self.bhtCurveRb,
                                          self.bhtCustomRb, self.bhtCustomQle, self.zBhtCustomRb, self.zBhtCurveRb,
                                          self.zBhtCustomQle, self.customMinDepthQle, self.customMaxDepthQle,
                                          self.temperature_farenehit_scale_rb, self.temperature_celcius_scale_rb])

    def get_max_depth_place_holder(self, given_max_depth=False):
        if len(self.well.wellModel.get_depth_curve()) != 0:
            max_depth = str(max(self.well.wellModel.get_depth_curve())) \
            if not given_max_depth \
            else self.customMaxDepthQle.text()

            self.zBhtCurveRb.setText(f"Tomar máximo de curva de profundidad ({max_depth})")

        else:
            self.zBhtCurveRb.setText(f"Tomar máximo de curva de profundidad")


    def maxDepthChanged(self):
        self.get_max_depth_place_holder(is_number(self.customMaxDepthQle.text()))

    def on_selected(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return

        self.customMinDepthQle \
            .setEnabled(self.depthCustomRb
                        .isChecked())

        self.customMaxDepthQle \
            .setEnabled(self.depthCustomRb
                        .isChecked())

        if self.depthCustomRb \
                        .isChecked():
            self.customMinDepthQle \
                .setPlaceholderText(str(
                min(self.well.wellModel.get_depth_curve())
            ))

            self.customMaxDepthQle \
                .setPlaceholderText(str(
                max(self.well.wellModel.get_depth_curve())
            ))

            self.maxDepthChanged()

        else:
            self.get_max_depth_place_holder()

    def temperatureSelection(self):
        self.temperatureCurveCbo.setEnabled(self.temperatureCurveRb.isChecked())
        self.temperatureCalcGrpBox.setEnabled(self.temperatureCalcRb.isChecked())


    def bhtSelection(self):
        self.bhtCurveCbo.setEnabled(self.bhtCurveRb.isChecked())
        self.bhtCustomQle.setEnabled(self.bhtCustomRb.isChecked())


    def zBhtSelection(self):
        self.zBhtCustomQle.setEnabled(self.zBhtCustomRb.isChecked())


    def ggSelection(self):
        self.ggQle.setEnabled(self.ggRb.isChecked())
        self.ggUnitLbl.setEnabled(self.ggRb.isChecked())
        self.envTempQle.setEnabled(not self.ggRb.isChecked())
        self.envTempUnitLbl.setEnabled(not self.ggRb.isChecked())


    def getTemperature(self):
        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        if self.temperatureCurveCbo.isEnabled():
            return self.well.wellModel.get_partial_curve(self.temperatureCurveCbo.currentText(),
                                                         minDepth,
                                                         maxDepth,
                                                         to_list=False)

        if self.bhtCustomQle.isEnabled():
            if not is_number(self.bhtCustomQle.text()):
                AlertWindow("El valor de BHT ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
                return None
        
        if self.ggQle.isEnabled():
            if not is_number(self.ggQle.text()):
                AlertWindow("El valor de Gradiente Geotermico ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
                return None

        if self.bhtCustomQle.isEnabled():
            bht_value = float(self.bhtCustomQle.text())
        else:
            bht_curve = self.well.wellModel.get_partial_ranged_df_curve(self.bhtCurveCbo.currentText(), minDepth, maxDepth, "", "")
            bht_curve = bht_curve[~np.isnan(bht_curve)]
            bht_value = float(bht_curve[0])
        
        if self.zBhtCustomQle.isEnabled():
            if not is_number(self.zBhtCustomQle.text()):
                AlertWindow("El valor de Z_bht ingresado es invalido, ingrese un numero (Se usa punto '.' como separador decimal)")
                return None
            else:
                maxDepth = self.zBhtCustomQle.text()

        if self.ggQle.isEnabled():
            # Km to m
            gg = float(self.ggQle.text()) / 1000

            # m to ft
            if METERS_LBL != self.well.wellModel.get_depth_unit():
                gg = gg / 3.28084

        else:
            gg = get_geothermal_gradient(bht_value, float(self.envTempQle.text()), float(maxDepth))

        return get_temperature(gg,
                               depth_curve,
                               float(maxDepth),
                               bht_value)

    def get_temperature_scale(self):
        # self.temperature_farenehit_scale_rb.isChecked()
        if self.temperature_celcius_scale_rb.isChecked():
            return CELCIUS_UNIT_LBL

        return FARENHEIT_UNIT_LBL

    def _preview(self, temperatureCurve):
        depthCurve = self.well.wellModel.get_depth_curve()

        if self.temperatureCurveCbo.isEnabled():
            unit = self.well.wellModel.get_unit_of(self.temperatureCurveCbo.currentText()),

        else:
            unit = self.get_temperature_scale()

        self.add_curve_with_y_label({
            'tab_name': self.tab_name,
            'track_name': TEMPERATURE_TAB_NAME,
            'curve_name': TEMPERATURE_TAB_NAME,
            'x_axis': temperatureCurve,
            'y_axis': depthCurve,
            "x_label": f"{TEMPERATURE_TAB_NAME} [{unit}]",
            "y_label": self.get_y_label(),
            'color': self.curveColorCbo.currentText(),
            'line_style': self.curveLineCbo.currentText(),
            'line_marker': self.curveMarkerCbo.currentText(),
            'add_axis': True
        })
        
        self.well.graphicWindow.draw_tracks(self.tab_name)

    def preview(self):
        if not super().preview():
            return
        
        temperatureCurve = self.getTemperature()

        if temperatureCurve is None:
            return

        self._preview(temperatureCurve)

    def saveCurve(self):
        if not super().preview():
            return

        curve_name = self.nameQle.text()

        if len(curve_name) == 0:
            return AlertWindow(MISSING_CURVE_NAME)

        self.curve_to_save = self.getTemperature()
        
        if self.curve_to_save is None:
            return AlertWindow(MISSING_CURVE_TO_SAVE)

        saved_ok = self.well \
                       .wellModel \
                       .append_curve(curve_name,
                                     self.curve_to_save,
                                     unit=self.get_temperature_scale())

        if not saved_ok:
            YesOrNoQuestion(CURVE_ALREADY_EXISTS_QUESTION_LBL,
                            lambda: (self.well
                                        .wellModel
                                        .append_curve(curve_name,
                                                      self.curve_to_save,
                                                      unit=self.get_temperature_scale(),
                                                      force_name=True),
                                    self.update_tab(self.well),
                                    InformationWindow("Curva guardada")),
                            lambda: (InformationWindow("No se guardo la curva"))
            )
        else:
            self.update_tab(self.well)
            InformationWindow("Curva guardada")

    def update_tab(self, well=None, force_update=False):
        if force_update:
            return

        if not super().update_tab(well):
            return

        depth_unit = self.well.wellModel.get_depth_unit() \
            if self.well is not None \
            else ""

        self.zBhtCustomRb.setText(f"Valor Z_bht Custom [{depth_unit}]: ")

        self.window = self.well \
            .graphicWindow

        self.on_selected()
