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
from PyQt6.QtCore import Qt, QTimer
import numpy as np

from constants.general_constants import loading_pop_up_timeout_ms

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.messages_constants import MISSING_WELL
from constants.pytrophysicsConstants import (COLOR_CONSTANTS, LINE_TYPE_CONSTANTS, 
                                             LINE_MARKER_CONSTANTS, CUTOFF_LBL, SEE_WINDOW_LBL)
from constants.messages_constants import MISSING_CURVE_NAME, MISSING_CURVE_TO_SAVE, MISSING_WELL, \
    CURVE_ALREADY_EXISTS_QUESTION_LBL
from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow
from ui.popUps.YesOrNoQuestion import YesOrNoQuestion
from ui.style.StyleCombos import (color_combo_box, line_combo_box)
from ui.style.button_styles import SAVE_BUTTON_STYLE, PREVIEW_BUTTON_STYLE
from ui.popUps.LoadingWindow import LoadingWindow

from services.cutoff_service import (get_cutoff_general,
                                     get_thickness_rectangles,
                                     get_cutoff_rectangles)

from services.tools.string_service import is_number

from ui.visual_components.constant_curves_handler import (add_rectangle_to,
                                                          add_bottom_half_bucket_to, 
                                                          add_upper_half_bucket_to)


class ThicknessesTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("Espesores")

        self.initUI()

        self.numeric_inputs.extend([self.c1CutoffQle, self.c2CutoffQle, self.c3CutoffQle ,self.c4CutoffQle,
                                    self.customMaxDepthQle, self.customMinDepthQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.c1ThicknessQle, self.c1CurveLineCbo,
             self.c1CutoffQle, self.c1CurveColorCbo, self.c1AboveCutoffTypeRb,  self.c1BelowCutoffTypeRb,
             self.c2CutoffCb,  self.c2ThicknessQle, self.c2CurveLineCbo,
             self.c2CutoffQle, self.c2CurveColorCbo, self.c2AboveCutoffTypeRb,  self.c2BelowCutoffTypeRb,
             self.c3CutoffCb, self.c3ThicknessQle, self.c3CurveLineCbo,
             self.c3CutoffQle, self.c3CurveColorCbo, self.c3AboveCutoffTypeRb, self.c3BelowCutoffTypeRb,
             self.c4CutoffCb, self.c4ThicknessQle, self.c4CurveLineCbo,
             self.c4CutoffQle, self.c4CurveColorCbo, self.c4AboveCutoffTypeRb, self.c4BelowCutoffTypeRb])

    def initUI(self):
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

        self.c1CutoffGrpBox = QGroupBox("C1")
        self.c1CutoffGrpLayout = QVBoxLayout()

        self.c1Lbl = QLabel("Variable de entrada")
        self.c1Cbo = QComboBox(self)
        self.c1Cbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.c1Cbo)

        self.c1CurveLayout = QHBoxLayout()
        self.c1CurveLayout.addWidget(self.c1Lbl)
        self.c1CurveLayout.addWidget(self.c1Cbo)

        self.c1CutoffLbl = QLabel(CUTOFF_LBL)
        self.c1CutoffQle = QLineEdit()
        self.c1CutoffQle.setPlaceholderText("Valor positivo")

        self.c1CutoffLayout = QHBoxLayout()
        self.c1CutoffLayout.addWidget(self.c1CutoffLbl)
        self.c1CutoffLayout.addWidget(self.c1CutoffQle)

        self.c1ValueRangeGrpBox = QGroupBox("Rango de valores")

        self.c1BelowCutoffTypeRb = QRadioButton("Valores por debajo del Cutoff")
        self.c1BelowCutoffTypeRb.setChecked(True)
        self.c1AboveCutoffTypeRb = QRadioButton("Valores por encima del Cutoff")

        self.c1ValueRangeLayout = QHBoxLayout()
        self.c1ValueRangeLayout.addWidget(self.c1BelowCutoffTypeRb)
        self.c1ValueRangeLayout.addWidget(self.c1AboveCutoffTypeRb)
        
        self.c1ValueRangeGrpBox.setLayout(self.c1ValueRangeLayout)

        self.c1CurveColorCbo = color_combo_box()
        self.c1CurveColorCbo.removeItem(0)
        self.c1CurveColorCbo.removeItem(0)
        self.c1CurveColorCbo.setCurrentIndex(0)    
        self.c1CurveLineCbo = line_combo_box()

        self.c1CurveStyleLayout = QHBoxLayout()
        self.c1CurveStyleLayout.addWidget(self.c1CurveColorCbo)
        self.c1CurveStyleLayout.addWidget(self.c1CurveLineCbo)

        self.c1ThicknessLbl = QLabel("Nombre Espesor:")
        self.c1ThicknessQle = QLineEdit()
        self.c1ThicknessQle.setPlaceholderText("Ingrese nombre espesor")

        self.c1ThicknessLayout = QHBoxLayout()
        self.c1ThicknessLayout.addWidget(self.c1ThicknessLbl)
        self.c1ThicknessLayout.addWidget(self.c1ThicknessQle)

        self.c1CutoffGrpLayout.addLayout(self.c1CurveLayout)
        self.c1CutoffGrpLayout.addLayout(self.c1CutoffLayout)
        self.c1CutoffGrpLayout.addWidget(self.c1ValueRangeGrpBox)
        self.c1CutoffGrpLayout.addLayout(self.c1CurveStyleLayout)
        self.c1CutoffGrpLayout.addLayout(self.c1ThicknessLayout)

        self.c1CutoffGrpBox.setLayout(self.c1CutoffGrpLayout)
        self.gridLayout.addWidget(self.c1CutoffGrpBox, row, 0, 1, 1)
        
        ########################################################################

        row += 1

        self.c2CutoffCb = QCheckBox("Tomar Cutoff C2")
        self.c2CutoffCb.setChecked(False)
            
        self.c2CutoffCb.stateChanged.connect(self.updateC2CutoffGrpBox)

        self.gridLayout.addWidget(self.c2CutoffCb, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.c2CutoffGrpBox = QGroupBox("C2")
        self.c2CutoffGrpLayout = QVBoxLayout()

        self.c2Lbl = QLabel("Variable de Entrada")
        self.c2Cbo = QComboBox(self)
        self.c2Cbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.c2Cbo)

        self.c2CurveLayout = QHBoxLayout()
        self.c2CurveLayout.addWidget(self.c2Lbl)
        self.c2CurveLayout.addWidget(self.c2Cbo)

        self.c2CutoffLbl = QLabel(CUTOFF_LBL)
        self.c2CutoffQle = QLineEdit()
        self.c2CutoffQle.setPlaceholderText("Valor positivo")

        self.c2CutoffLayout = QHBoxLayout()
        self.c2CutoffLayout.addWidget(self.c2CutoffLbl)
        self.c2CutoffLayout.addWidget(self.c2CutoffQle)

        self.c2ValueRangeGrpBox = QGroupBox("Rango de valores")

        self.c2BelowCutoffTypeRb = QRadioButton("Valores por debajo del Cutoff")
        self.c2BelowCutoffTypeRb.setChecked(True)
        self.c2AboveCutoffTypeRb = QRadioButton("Valores por encima del Cutoff")

        self.c2ValueRangeLayout = QHBoxLayout()
        self.c2ValueRangeLayout.addWidget(self.c2BelowCutoffTypeRb)
        self.c2ValueRangeLayout.addWidget(self.c2AboveCutoffTypeRb)
        
        self.c2ValueRangeGrpBox.setLayout(self.c2ValueRangeLayout)

        self.c2CurveColorCbo = color_combo_box()
        self.c2CurveColorCbo.removeItem(0)
        self.c2CurveColorCbo.removeItem(0)
        self.c2CurveColorCbo.setCurrentIndex(0)
        self.c2CurveLineCbo = line_combo_box()

        self.c2CurveStyleLayout = QHBoxLayout()
        self.c2CurveStyleLayout.addWidget(self.c2CurveColorCbo)
        self.c2CurveStyleLayout.addWidget(self.c2CurveLineCbo)

        self.c2ThicknessLbl = QLabel("Nombre Espesor:")
        self.c2ThicknessQle = QLineEdit()
        self.c2ThicknessQle.setPlaceholderText("Ingrese nombre espesor")

        self.c2ThicknessLayout = QHBoxLayout()
        self.c2ThicknessLayout.addWidget(self.c2ThicknessLbl)
        self.c2ThicknessLayout.addWidget(self.c2ThicknessQle)

        self.c2CutoffGrpLayout.addLayout(self.c2CurveLayout)
        self.c2CutoffGrpLayout.addLayout(self.c2CutoffLayout)
        self.c2CutoffGrpLayout.addWidget(self.c2ValueRangeGrpBox)
        self.c2CutoffGrpLayout.addLayout(self.c2CurveStyleLayout)
        self.c2CutoffGrpLayout.addLayout(self.c2ThicknessLayout)

        self.c2CutoffGrpBox.setEnabled(False)

        self.c2CutoffGrpBox.setLayout(self.c2CutoffGrpLayout)
        self.gridLayout.addWidget(self.c2CutoffGrpBox, row, 0, 1, 1)
        
        ########################################################################

        row += 1

        self.c3CutoffCb = QCheckBox("Tomar Cutoff C3")
        self.c3CutoffCb.setChecked(False)
            
        self.c3CutoffCb.stateChanged.connect(self.updateC3CutoffGrpBox)

        self.gridLayout.addWidget(self.c3CutoffCb, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.c3CutoffGrpBox = QGroupBox("C3")
        self.c3CutoffGrpLayout = QVBoxLayout()

        self.c3Lbl = QLabel("Variable de Entrada")
        self.c3Cbo = QComboBox(self)
        self.c3Cbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.c3Cbo)

        self.c3CurveLayout = QHBoxLayout()
        self.c3CurveLayout.addWidget(self.c3Lbl)
        self.c3CurveLayout.addWidget(self.c3Cbo)

        self.c3CutoffLbl = QLabel(CUTOFF_LBL)
        self.c3CutoffQle = QLineEdit()
        self.c3CutoffQle.setPlaceholderText("Valor positivo")

        self.c3CutoffLayout = QHBoxLayout()
        self.c3CutoffLayout.addWidget(self.c3CutoffLbl)
        self.c3CutoffLayout.addWidget(self.c3CutoffQle)

        self.c3ValueRangeGrpBox = QGroupBox("Rango de valores")

        self.c3BelowCutoffTypeRb = QRadioButton("Valores por debajo del Cutoff")
        self.c3BelowCutoffTypeRb.setChecked(True)
        self.c3AboveCutoffTypeRb = QRadioButton("Valores por encima del Cutoff")

        self.c3ValueRangeLayout = QHBoxLayout()
        self.c3ValueRangeLayout.addWidget(self.c3BelowCutoffTypeRb)
        self.c3ValueRangeLayout.addWidget(self.c3AboveCutoffTypeRb)
        
        self.c3ValueRangeGrpBox.setLayout(self.c3ValueRangeLayout)

        self.c3CurveColorCbo = color_combo_box()
        self.c3CurveColorCbo.removeItem(0)
        self.c3CurveColorCbo.removeItem(0)
        self.c3CurveColorCbo.setCurrentIndex(0)
        self.c3CurveLineCbo = line_combo_box()

        self.c3CurveStyleLayout = QHBoxLayout()
        self.c3CurveStyleLayout.addWidget(self.c3CurveColorCbo)
        self.c3CurveStyleLayout.addWidget(self.c3CurveLineCbo)

        self.c3ThicknessLbl = QLabel("Nombre Espesor:")
        self.c3ThicknessQle = QLineEdit()
        self.c3ThicknessQle.setPlaceholderText("Ingrese nombre espesor")

        self.c3ThicknessLayout = QHBoxLayout()
        self.c3ThicknessLayout.addWidget(self.c3ThicknessLbl)
        self.c3ThicknessLayout.addWidget(self.c3ThicknessQle)

        self.c3CutoffGrpLayout.addLayout(self.c3CurveLayout)
        self.c3CutoffGrpLayout.addLayout(self.c3CutoffLayout)
        self.c3CutoffGrpLayout.addWidget(self.c3ValueRangeGrpBox)
        self.c3CutoffGrpLayout.addLayout(self.c3CurveStyleLayout)
        self.c3CutoffGrpLayout.addLayout(self.c3ThicknessLayout)

        self.c3CutoffGrpBox.setEnabled(False)

        self.c3CutoffGrpBox.setLayout(self.c3CutoffGrpLayout)
        self.gridLayout.addWidget(self.c3CutoffGrpBox, row, 0, 1, 1)
        
        ########################################################################

        row += 1

        self.c4CutoffCb = QCheckBox("Tomar Cutoff C4")
        self.c4CutoffCb.setChecked(False)
            
        self.c4CutoffCb.stateChanged.connect(self.updateC4CutoffGrpBox)

        self.gridLayout.addWidget(self.c4CutoffCb, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.c4CutoffGrpBox = QGroupBox("C4")
        self.c4CutoffGrpLayout = QVBoxLayout()

        self.c4Lbl = QLabel("Variable de Entrada")
        self.c4Cbo = QComboBox(self)
        self.c4Cbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.c4Cbo)

        self.c4CurveLayout = QHBoxLayout()
        self.c4CurveLayout.addWidget(self.c4Lbl)
        self.c4CurveLayout.addWidget(self.c4Cbo)

        self.c4CutoffLbl = QLabel(CUTOFF_LBL)
        self.c4CutoffQle = QLineEdit()
        self.c4CutoffQle.setPlaceholderText("Valor positivo")

        self.c4CutoffLayout = QHBoxLayout()
        self.c4CutoffLayout.addWidget(self.c4CutoffLbl)
        self.c4CutoffLayout.addWidget(self.c4CutoffQle)

        self.c4ValueRangeGrpBox = QGroupBox("Rango de valores")

        self.c4BelowCutoffTypeRb = QRadioButton("Valores por debajo del Cutoff")
        self.c4BelowCutoffTypeRb.setChecked(True)
        self.c4AboveCutoffTypeRb = QRadioButton("Valores por encima del Cutoff")

        self.c4ValueRangeLayout = QHBoxLayout()
        self.c4ValueRangeLayout.addWidget(self.c4BelowCutoffTypeRb)
        self.c4ValueRangeLayout.addWidget(self.c4AboveCutoffTypeRb)
        
        self.c4ValueRangeGrpBox.setLayout(self.c4ValueRangeLayout)

        self.c4CurveColorCbo = color_combo_box()
        self.c4CurveColorCbo.removeItem(0)
        self.c4CurveColorCbo.removeItem(0)
        self.c4CurveColorCbo.setCurrentIndex(0)
        self.c4CurveLineCbo = line_combo_box()

        self.c4CurveStyleLayout = QHBoxLayout()
        self.c4CurveStyleLayout.addWidget(self.c4CurveColorCbo)
        self.c4CurveStyleLayout.addWidget(self.c4CurveLineCbo)

        self.c4ThicknessLbl = QLabel("Nombre Espesor:")
        self.c4ThicknessQle = QLineEdit()
        self.c4ThicknessQle.setPlaceholderText("Ingrese nombre espesor")

        self.c4ThicknessLayout = QHBoxLayout()
        self.c4ThicknessLayout.addWidget(self.c4ThicknessLbl)
        self.c4ThicknessLayout.addWidget(self.c4ThicknessQle)

        self.c4CutoffGrpLayout.addLayout(self.c4CurveLayout)
        self.c4CutoffGrpLayout.addLayout(self.c4CutoffLayout)
        self.c4CutoffGrpLayout.addWidget(self.c4ValueRangeGrpBox)
        self.c4CutoffGrpLayout.addLayout(self.c4CurveStyleLayout)
        self.c4CutoffGrpLayout.addLayout(self.c4ThicknessLayout)

        self.c4CutoffGrpBox.setEnabled(False)

        self.c4CutoffGrpBox.setLayout(self.c4CutoffGrpLayout)
        self.gridLayout.addWidget(self.c4CutoffGrpBox, row, 0, 1, 1)

        ########################################################################
        
        row += 1
        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2)

        ########################################################################
        
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
        self.cutoffToSaveCbo = QComboBox()
        self.cutoffToSaveCbo.addItem("Cutoff C1")
        self.nameLayout = QHBoxLayout()
        self.nameLayout.addWidget(self.nameLbl)
        self.nameLayout.addWidget(self.nameQle)
        
        self.cutoffToSaveLayout = QHBoxLayout()
        self.cutoffToSaveLayout.addWidget(self.cutoffToSaveCbo)
        self.cutoffToSaveLayout.addWidget(QLabel(""))

        self.gridLayout.addLayout(self.nameLayout, row, 0, 1, 1)
        self.gridLayout.addLayout(self.cutoffToSaveLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

        self.saveCurveBtn = QPushButton("Guardar curva Pay Flag")
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


    def updateC2CutoffGrpBox(self, state):
        self.c2CutoffGrpBox.setEnabled(state != 0)
        if state != 0:
            self.cutoffToSaveCbo.addItem("Cutoff C2")
        else:
            self.cutoffToSaveCbo.setCurrentText("Cutoff C2")
            index = self.cutoffToSaveCbo.currentIndex()
            self.cutoffToSaveCbo.removeItem(index)


    def updateC3CutoffGrpBox(self, state):
        self.c3CutoffGrpBox.setEnabled(state != 0)
        if state != 0:
            self.cutoffToSaveCbo.addItem("Cutoff C3")
        else:
            self.cutoffToSaveCbo.setCurrentText("Cutoff C3")
            index = self.cutoffToSaveCbo.currentIndex()
            self.cutoffToSaveCbo.removeItem(index)


    def updateC4CutoffGrpBox(self, state):
        self.c4CutoffGrpBox.setEnabled(state != 0)
        if state != 0:
            self.cutoffToSaveCbo.addItem("Cutoff C4")
        else:
            self.cutoffToSaveCbo.setCurrentText("Cutoff C4")
            index = self.cutoffToSaveCbo.currentIndex()
            self.cutoffToSaveCbo.removeItem(index)


    def getCutoff(self):

        
        if (self.c3CutoffGrpBox.isEnabled() and (not self.c2CutoffGrpBox.isEnabled())) \
                or (self.c4CutoffGrpBox.isEnabled() and ((not self.c2CutoffGrpBox.isEnabled()) or (not self.c3CutoffGrpBox.isEnabled()))):
            AlertWindow("Por favor, habilite los cutoff en orden correcto (C2 o C3 están deshabilitados y deben estar habilitados para la configuracion actual)")
            return None

        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        curves_list = []
        cutoff_list = []
        values_below_cutoff_list = []
        result_list = []

        if (not is_number(self.c1CutoffQle.text())) or float(self.c1CutoffQle.text()) < 0:
            AlertWindow("El valor de cutoff para C1 ingresado es invalido, ingrese un numero positivo (Se usa punto '.' como separador decimal)")
            return None
        curves_list.append(self.well.wellModel.get_partial_ranged_df_curve(self.c1Cbo.currentText(), minDepth, maxDepth, "", ""))
        cutoff_list.append(float(self.c1CutoffQle.text()))
        values_below_cutoff_list.append(self.c1BelowCutoffTypeRb.isChecked())
        curve = get_cutoff_general(
                    curves_list,
                    cutoff_list,
                    values_below_cutoff_list,
                    self.well.wellModel.get_partial_ranged_df_curve(self.c1Cbo.currentText(), minDepth, maxDepth, "", ""),
                    depth_curve
                )
        
        curve[np.isnan(curve)] = 0
        curve = np.array(list(map(lambda x: 1 if x > 0 else 0, curve)))

        result_list.append({    
            "rectangle": get_thickness_rectangles(curve, depth_curve),
            "pay_flag_curve": curve,
            "cutoff": "Cutoff C1"
        })

        if self.c2CutoffGrpBox.isEnabled():
            if (not is_number(self.c2CutoffQle.text())) or float(self.c2CutoffQle.text()) < 0:
                AlertWindow("El valor de cutoff para C2 ingresado es invalido, ingrese un numero positivo (Se usa punto '.' como separador decimal)")
                return None
            curves_list.append(self.well.wellModel.get_partial_ranged_df_curve(self.c2Cbo.currentText(), minDepth, maxDepth, "", ""))
            cutoff_list.append(float(self.c2CutoffQle.text()))
            values_below_cutoff_list.append(self.c2BelowCutoffTypeRb.isChecked())
            curve = get_cutoff_general(
                        curves_list,
                        cutoff_list,
                        values_below_cutoff_list,
                        self.well.wellModel.get_partial_ranged_df_curve(self.c2Cbo.currentText(), minDepth, maxDepth, "", ""),
                        depth_curve
                    )
                    
            curve[np.isnan(curve)] = 0
            curve = np.array(list(map(lambda x: 1 if x > 0 else 0, curve)))

            result_list.append({
                "rectangle": get_thickness_rectangles(curve, depth_curve),
                "pay_flag_curve": curve,
                "cutoff": "Cutoff C2"
            })

        if self.c3CutoffGrpBox.isEnabled():
            if (not is_number(self.c3CutoffQle.text())) or float(self.c3CutoffQle.text()) < 0:
                AlertWindow("El valor de cutoff para C3 ingresado es invalido, ingrese un numero positivo (Se usa punto '.' como separador decimal)")
                return None
            curves_list.append(self.well.wellModel.get_partial_ranged_df_curve(self.c3Cbo.currentText(), minDepth, maxDepth, "", ""))
            cutoff_list.append(float(self.c3CutoffQle.text()))
            values_below_cutoff_list.append(self.c3BelowCutoffTypeRb.isChecked())
            curve = get_cutoff_general(
                        curves_list,
                        cutoff_list,
                        values_below_cutoff_list,
                        self.well.wellModel.get_partial_ranged_df_curve(self.c3Cbo.currentText(), minDepth, maxDepth, "", ""),
                        depth_curve
                    )            
    
            curve[np.isnan(curve)] = 0
            curve = np.array(list(map(lambda x: 1 if x > 0 else 0, curve)))

            result_list.append({
                "rectangle": get_thickness_rectangles(curve, depth_curve),
                "pay_flag_curve": curve,
                "cutoff": "Cutoff C3"
            })
        
        if self.c4CutoffGrpBox.isEnabled():
            if (not is_number(self.c4CutoffQle.text())) or float(self.c4CutoffQle.text()) < 0:
                AlertWindow("El valor de cutoff para C4 ingresado es invalido, ingrese un numero positivo (Se usa punto '.' como separador decimal)")
                return None
            curves_list.append(self.well.wellModel.get_partial_ranged_df_curve(self.c4Cbo.currentText(), minDepth, maxDepth, "", ""))
            cutoff_list.append(float(self.c4CutoffQle.text()))
            values_below_cutoff_list.append(self.c4BelowCutoffTypeRb.isChecked())
            curve = get_cutoff_general(
                        curves_list,
                        cutoff_list,
                        values_below_cutoff_list,
                        self.well.wellModel.get_partial_ranged_df_curve(self.c4Cbo.currentText(), minDepth, maxDepth, "", ""),
                        depth_curve
                    )

            curve[np.isnan(curve)] = 0
            curve = np.array(list(map(lambda x: 1 if x > 0 else 0, curve)))

            result_list.append({
                "rectangle": get_thickness_rectangles(curve, depth_curve),
                "pay_flag_curve": curve,
                "cutoff": "Cutoff C4"
            })

        return result_list


    def get_preview_config_curve(self, depth_curve, pay_flag_curve, curve_name, track_name, color, line_type, cutoff_value, values_below_cutoff):
        config = {
            "curve":{
                'tab_name': self.tab_name,
                'track_name': track_name,
                'curve_name': curve_name,

                'x_axis': self.well.wellModel.get_df_curve(curve_name),
                'y_axis': depth_curve,

                'color': color,
                'line_style': line_type,
                'line_marker': LINE_MARKER_CONSTANTS["NONE"],

                'cummulative': True,
                'ephimeral': True,
                'add_axis': False
            },
            "cutoff_rectangle":{
                    "y0": str(min(depth_curve)),
                    "y1": str(max(depth_curve)),
                    "x0": cutoff_value,
                    "x1": cutoff_value,
            
                    "color": COLOR_CONSTANTS["RED"],
                    "line": LINE_TYPE_CONSTANTS["SOLID_LINE"],
            
                    'tab_name': self.tab_name,
                    'track_name': track_name
            },
            "aux_rectangles": [],
            "values_below_cutoff": values_below_cutoff
        }
        rectangles = get_cutoff_rectangles(self.well.wellModel.get_df_curve(curve_name), pay_flag_curve, depth_curve)

        for i in range(len(rectangles)):
            if rectangles[i]["value"] == 0:
                #print("Rectangle " + str(i + 1) + " xi: " + str(rectangles[i]["x"][0]) + " xf: " + str(rectangles[i]["x"][1]) + " yi: " + str(rectangles[i]["y"][0]) + " yf: " + str(rectangles[i]["y"][1]))
                aux_curve_name = curve_name + " " + track_name + " " + str(i)
                config["aux_rectangles"].append({
                    'x_min': rectangles[i]["x"][0],
                    'x_max': rectangles[i]["x"][1],
                    'y_min': rectangles[i]["y"][0],
                    'y_max': rectangles[i]["y"][1],
                    'curve_name': aux_curve_name,
                    'add_axis': False,
                    'tab_name': self.tab_name,
                    'track_name': track_name,
                    'color': COLOR_CONSTANTS["GREEN"],
                    'no_grid': True,
                    'ephimeral': True,
                    'invisible': True,
                    'cummulative': True
                })
        return config


    def get_preview_config_thickness_curve(self, cutoff_rectangles, curve_name, track_name, color):
        config = {
            "aux_rectangles": []
        }
        for i in range(len(cutoff_rectangles)):
            if cutoff_rectangles[i]["value"]:
                color_aux = color
            else:
                color_aux = COLOR_CONSTANTS["BLACK"]
            aux_curve_name = curve_name + " " + track_name + " " + str(i + 1)
            config["aux_rectangles"].append({
                'x_min': cutoff_rectangles[i]["x"][0],
                'x_max': cutoff_rectangles[i]["x"][1],
                'y_min': cutoff_rectangles[i]["y"][0],
                'y_max': cutoff_rectangles[i]["y"][1],
                'curve_name': aux_curve_name,
                'add_axis': False,
                'tab_name': self.tab_name,
                'track_name': track_name,
                'color': color_aux,
                'no_grid': True,
                'ephimeral': True,
                'invisible': True,
                'cummulative': False
            })

        return config


    def _preview(self, rectangles):
        depth_curve = self.well.wellModel.get_depth_curve()

        curve_list = []
        thickness_list = []

        curve_list.append(self.get_preview_config_curve(depth_curve,
                                                        rectangles[0]["pay_flag_curve"],
                                                        self.c1Cbo.currentText(),
                                                        "Cutoff C1",
                                                        self.c1CurveColorCbo.currentText(),
                                                        self.c1CurveLineCbo.currentText(),
                                                        float(self.c1CutoffQle.text()),
                                                        self.c1BelowCutoffTypeRb.isChecked()))
        
        thickness_list.append(self.get_preview_config_thickness_curve(rectangles[0]["rectangle"], 
                                                            self.c1Cbo.currentText(), 
                                                            self.c1ThicknessQle.text(),
                                                            self.c1CurveColorCbo.currentText()))
        
        if self.c2CutoffGrpBox.isEnabled():
            curve_list.append(self.get_preview_config_curve(depth_curve,
                                                        rectangles[1]["pay_flag_curve"],
                                                        self.c2Cbo.currentText(),
                                                        "Cutoff C2",
                                                        self.c2CurveColorCbo.currentText(),
                                                        self.c2CurveLineCbo.currentText(),
                                                        float(self.c2CutoffQle.text()),
                                                        self.c2BelowCutoffTypeRb.isChecked()))
            thickness_list.append(self.get_preview_config_thickness_curve(rectangles[1]["rectangle"], 
                                                            self.c2Cbo.currentText(), 
                                                            self.c2ThicknessQle.text(),
                                                            self.c2CurveColorCbo.currentText()))

        if self.c3CutoffGrpBox.isEnabled():
            curve_list.append(self.get_preview_config_curve(depth_curve,
                                                        rectangles[2]["pay_flag_curve"],
                                                        self.c3Cbo.currentText(),
                                                        "Cutoff C3",
                                                        self.c3CurveColorCbo.currentText(),
                                                        self.c3CurveLineCbo.currentText(),
                                                        float(self.c3CutoffQle.text()),
                                                        self.c3BelowCutoffTypeRb.isChecked()))
            thickness_list.append(self.get_preview_config_thickness_curve(rectangles[2]["rectangle"], 
                                                            self.c3Cbo.currentText(), 
                                                            self.c3ThicknessQle.text(),
                                                            self.c3CurveColorCbo.currentText()))


        if self.c4CutoffGrpBox.isEnabled():
            curve_list.append(self.get_preview_config_curve(depth_curve,
                                                        rectangles[3]["pay_flag_curve"],
                                                        self.c4Cbo.currentText(),
                                                        "Cutoff C4",
                                                        self.c4CurveColorCbo.currentText(),
                                                        self.c4CurveLineCbo.currentText(),
                                                        float(self.c4CutoffQle.text()),
                                                        self.c4BelowCutoffTypeRb.isChecked()))
            thickness_list.append(self.get_preview_config_thickness_curve(rectangles[3]["rectangle"], 
                                                            self.c4Cbo.currentText(), 
                                                            self.c4ThicknessQle.text(),
                                                            self.c4CurveColorCbo.currentText()))
        ##         self.well.graphicWindow.remove_ephimeral_tracks(self.tab_name)

        track_names = ["Cutoff C1", "Cutoff C2", "Cutoff C3", "Cutoff C4",
                       self.c1ThicknessQle.text(), self.c2ThicknessQle.text(),
                       self.c3ThicknessQle.text(), self.c4ThicknessQle.text()]

        self.well \
            .graphicWindow \
            .remove_track_if_exists(track_names)

        self.well.graphicWindow.remove_ephimeral_tracks(self.tab_name)

        for curve in curve_list:
            x_label = self.well \
                .wellModel \
                .get_label_for(curve["curve"]["curve_name"])

            self.add_curve_with_y_label({
                ** curve["curve"],
                ** {
                    "x_label": x_label,
                    "cummulative": False,
                    "ephimeral": False
                }
            })

            self.well.graphicWindow.set_ephimeral_track(curve["curve"]["track_name"], self.tab_name)

            add_rectangle_to(self.well.graphicWindow, curve["cutoff_rectangle"], curve["cutoff_rectangle"]["track_name"])

            """if curve["values_below_cutoff"]:
                for aux_rectangle in curve["aux_rectangles"]:
                    add_bottom_half_bucket_to(self.well.graphicWindow, aux_rectangle)
                    self.well.graphicWindow.add_fill_between_curves({
                        'track_name': curve["curve"]["track_name"],
                        'curve_name_1': aux_rectangle["curve_name"],
                        'curve_name_2': curve["curve"]["curve_name"],
                        'color': COLOR_CONSTANTS["BLACK"],
                        'ephimeral': True,
                        'semi_fill': True,
                        'fill': "Sólido"
                    })
            else:
                for aux_rectangle in curve["aux_rectangles"]:
                    add_upper_half_bucket_to(self.well.graphicWindow, aux_rectangle)
                    self.well.graphicWindow.add_fill_between_curves({
                        'track_name': curve["curve"]["track_name"],
                        'curve_name_1': aux_rectangle["curve_name"],
                        'curve_name_2': curve["curve"]["curve_name"],
                        'color': COLOR_CONSTANTS["BLACK"],
                        'ephimeral': True,
                        'semi_fill': True,
                        'fill': "Sólido"
                    })"""

        
        for thickness in thickness_list:
            self.add_curve_with_y_label({
                'x_axis': [thickness["aux_rectangles"][0]["x_min"], thickness["aux_rectangles"][0]["x_max"]],
                'y_axis': [min(depth_curve), max(depth_curve)],

                'curve_name': thickness["aux_rectangles"][0]["curve_name"] + "_aux",
                'tab_name': self.tab_name,
                'track_name': thickness["aux_rectangles"][0]["track_name"],
                'color': COLOR_CONSTANTS["WHITE"],
                'line_style': LINE_TYPE_CONSTANTS["SOLID_LINE"],
                'line_marker': LINE_MARKER_CONSTANTS["NONE"],
                "x_label": thickness["aux_rectangles"][0]["track_name"],

                'no_grid': True,
                'ephimeral': True,
                'invisible': True,
                'add_axis': False
            })
            self.well.graphicWindow.set_ephimeral_track(thickness["aux_rectangles"][0]["track_name"],
                                                        self.tab_name)
            #self.well.graphicWindow.create_blank_track(thickness["aux_rectangles"][0][0]["tab_name"],
            #                                            thickness["aux_rectangles"][0]["track_name"])
            for thickness_rect in thickness["aux_rectangles"]:
                #add_bottom_half_bucket_to(self.well.graphicWindow, thickness_rect[0])
                #add_upper_half_bucket_to(self.well.graphicWindow, thickness_rect[1])
                self.well.graphicWindow.add_colored_rectangle(thickness_rect)
        
        self.well.graphicWindow.draw_tracks(self.tab_name)


    def preview(self):
        if not super().preview():
            return

        if (self.c1ThicknessQle.text() == "" or 
            (self.c2CutoffGrpBox.isEnabled() and self.c2ThicknessQle.text() == "") or
            (self.c3CutoffGrpBox.isEnabled() and self.c3ThicknessQle.text() == "") or
            (self.c4CutoffGrpBox.isEnabled() and self.c4ThicknessQle.text() == "")):
            AlertWindow("El nombre del espesor no puede estar vacío.")
            return

        if ((self.c2CutoffGrpBox.isEnabled() and self.c2ThicknessQle.text() == self.c1ThicknessQle.text()) or
            (self.c3CutoffGrpBox.isEnabled() and ((self.c3ThicknessQle.text() == self.c2ThicknessQle.text()) or 
                                                  (self.c3ThicknessQle.text() == self.c1ThicknessQle.text()))) or
            (self.c4CutoffGrpBox.isEnabled() and ((self.c4ThicknessQle.text() == self.c3ThicknessQle.text()) or 
                                                  (self.c4ThicknessQle.text() == self.c2ThicknessQle.text()) or 
                                                  (self.c4ThicknessQle.text() == self.c1ThicknessQle.text())))):
            AlertWindow("Dos espesores no pueden tener el mismo nombre")
            return

        rectangles = self.getCutoff()
        if rectangles is None:
            return

        pop_up = LoadingWindow("Por favor espere...")

        QTimer.singleShot(loading_pop_up_timeout_ms, lambda: (
            self._preview(rectangles),
            pop_up.close()
        ))


    def saveCurve(self):
        if not super().preview():
            return

        curve_name = self.nameQle.text()

        if len(curve_name) == 0:
            return AlertWindow(MISSING_CURVE_NAME)

        config_aux = self.getCutoff()
        if config_aux is None:
            return AlertWindow(MISSING_CURVE_TO_SAVE)
        
        currentCutoffToSave = self.cutoffToSaveCbo.currentText()
        self.curve_to_save = list(filter(lambda x: x["cutoff"] == currentCutoffToSave, config_aux))[0]["pay_flag_curve"]
        
        if self.curve_to_save is None:
            return AlertWindow(MISSING_CURVE_TO_SAVE)

        saved_ok = self.well \
                       .wellModel \
                       .append_curve(curve_name,
                                     self.curve_to_save)

        if not saved_ok:
            YesOrNoQuestion(CURVE_ALREADY_EXISTS_QUESTION_LBL,
                            lambda: (self.well
                                        .wellModel
                                        .append_curve(curve_name,
                                                      self.curve_to_save,
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
        
        if not super().update_tab(well, force_update):
            return

        self.window = self.well \
            .graphicWindow

        #self.c4Cbo.setCurrentIndex(0)
        #self.c3Cbo.setCurrentIndex(0)
        #self.c2Cbo.setCurrentIndex(0)
        #self.c1Cbo.setCurrentIndex(0)
