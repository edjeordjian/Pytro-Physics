"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox,
                             QPushButton, QComboBox, QLineEdit)
from PyQt6.QtCore import Qt

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.messages_constants import MISSING_WELL
from constants.pytrophysicsConstants import COLOR_CONSTANTS, LINE_TYPE_CONSTANTS, SEE_WINDOW_LBL
from constants.tab_constants import CUTOFF_C1_TITLE
from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow

from ui.style.StyleCombos import (color_combo_box, line_combo_box)
from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE

from services.cutoff_service import get_cutoff_general_using_cutoff, get_cutoff_general_using_thc
from services.tools.string_service import is_number


class C1CutoffTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("C1")

        self.initUI()

        self.numeric_inputs.extend([self.cutoffValueQle, self.thcValueQle,
                                    self.customMaxDepthQle, self.customMinDepthQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
                                                                 self.customMinDepthQle, self.customMaxDepthQle,
                                                                 self.c1CutoffLineStyleCbo, self.c1CutoffColorCbo,
                                                                 self.incAccumTypeRb, self.decAccumTypeRb,
                                                                 self.belowCutoffTypeRb, self.aboveCutoffTypeRb,
                                                                 self.cutoffValueQle, self.cutoffValueRb,
                                                                 self.thcValueQle, self.thcValueRb])

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0

        self.c1Lbl = QLabel("Variable de entrada (VShale)")
        self.c1Cbo = QComboBox(self)
        self.c1Cbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.c1Cbo)

        self.c1Layout = QHBoxLayout()
        self.c1Layout.addWidget(self.c1Lbl)
        self.c1Layout.addWidget(self.c1Cbo)
        self.c1Layout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.c1Layout, row, 0, 1, 2)

        ########################################################################

        row += 1

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

        self.c1CutoffStyleLbl = QLabel("Color y Tipo de Linea: ")
        self.c1CutoffColorCbo = color_combo_box()
        self.c1CutoffColorCbo.setCurrentIndex(0)
        self.c1CutoffLineStyleCbo = line_combo_box()
        self.c1CutoffLineStyleCbo.setCurrentIndex(0)

        self.c1CutoffStyleLayout = QHBoxLayout()
        self.c1CutoffStyleLayout.addWidget(self.c1CutoffStyleLbl)
        self.c1CutoffStyleLayout.addWidget(self.c1CutoffColorCbo)
        self.c1CutoffStyleLayout.addWidget(self.c1CutoffLineStyleCbo)

        self.gridLayout.addLayout(self.c1CutoffStyleLayout, row, 0, 1, 2)

    
        ########################################################################

        row += 1

        self.accumTypeGrpBox = QGroupBox("Acumulado")

        self.incAccumTypeRb = QRadioButton("Creciente")
        self.incAccumTypeRb.setChecked(True)
        self.decAccumTypeRb = QRadioButton("Decreciente")

        self.accumTypeLayout = QHBoxLayout()
        self.accumTypeLayout.addWidget(self.incAccumTypeRb)
        self.accumTypeLayout.addWidget(self.decAccumTypeRb)
        
        self.accumTypeGrpBox.setLayout(self.accumTypeLayout)
        self.gridLayout.addWidget(self.accumTypeGrpBox, row, 0, 1, 1)

        ########################################################################

        row += 1

        self.valueRangeGrpBox = QGroupBox("Rango de valores")

        self.belowCutoffTypeRb = QRadioButton("Valores por debajo del Cutoff")
        self.belowCutoffTypeRb.setChecked(True)
        self.aboveCutoffTypeRb = QRadioButton("Valores por encima del Cutoff")

        self.valueRangeLayout = QHBoxLayout()
        self.valueRangeLayout.addWidget(self.belowCutoffTypeRb)
        self.valueRangeLayout.addWidget(self.aboveCutoffTypeRb)
        
        self.valueRangeGrpBox.setLayout(self.valueRangeLayout)
        self.gridLayout.addWidget(self.valueRangeGrpBox, row, 0, 1, 1)

        ########################################################################

        row += 1

        self.cutoffGrpBox = QGroupBox("Cutoff")

        self.cutoffValueRb = QRadioButton("Valor de Cutoff:")
        self.cutoffValueRb.setChecked(True)
        self.cutoffValueQle = QLineEdit()
        self.cutoffValueQle.setPlaceholderText("Valor positivo")

        self.cutoffValueLayout = QHBoxLayout()
        self.cutoffValueLayout.addWidget(self.cutoffValueRb)
        self.cutoffValueLayout.addWidget(self.cutoffValueQle)

        self.thcValueRb = QRadioButton("Relación neto a total:")
        self.thcValueQle = QLineEdit()
        self.thcValueQle.setPlaceholderText("%")
        
        self.thcValueLayout = QHBoxLayout()
        self.thcValueLayout.addWidget(self.thcValueRb)
        self.thcValueLayout.addWidget(self.thcValueQle)

        labelMsg = "Aclaracion: La palabra 'nan' es una palabra reservada para identificar\nun valor nulo en caso de no lograr una solucion con los parametros ingresados"

        self.cutoffInfoLbl = QLabel(labelMsg)

        self.cutoffGrpLayout = QVBoxLayout()
        self.cutoffGrpLayout.addLayout(self.cutoffValueLayout)
        self.cutoffGrpLayout.addLayout(self.thcValueLayout)
        self.cutoffGrpLayout.addWidget(self.cutoffInfoLbl)
        
        self.cutoffGrpBox.setLayout(self.cutoffGrpLayout)
        self.gridLayout.addWidget(self.cutoffGrpBox, row, 0, 1, 1)

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
        row += 1

        self.nameLbl = QLabel("Nombre: ")
        self.nameQle = QLineEdit(self)
        self.nameLayout = QHBoxLayout()
        self.nameLayout.addWidget(self.nameLbl)
        self.nameLayout.addWidget(self.nameQle)

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

    def getCutoff(self):
        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        curves_list = []
        cutoff_list = []
        values_below_cutoff_list = []

        if self.thcValueRb.isChecked():
            config_aux = get_cutoff_general_using_thc(
                curves_list,
                cutoff_list,
                values_below_cutoff_list,
                self.well.wellModel.get_partial_ranged_df_curve(self.c1Cbo.currentText(), minDepth, maxDepth, "", ""),
                self.well.wellModel.get_depth_curve(),
                float(self.thcValueQle.text()),
                self.incAccumTypeRb.isChecked(),
                self.belowCutoffTypeRb.isChecked())
            self.cutoffValueQle.setText(str(config_aux["cutoff_value"]))

        else:
            config_aux = get_cutoff_general_using_cutoff(
                curves_list,
                cutoff_list,
                values_below_cutoff_list,
                self.well.wellModel.get_partial_ranged_df_curve(self.c1Cbo.currentText(), minDepth, maxDepth, "", ""),
                self.well.wellModel.get_depth_curve(), float(self.cutoffValueQle.text()),
                self.incAccumTypeRb.isChecked(),
                self.belowCutoffTypeRb.isChecked())
            self.thcValueQle.setText(str(config_aux["thc_value"]))

        return config_aux

    def preview(self):
        if not super().preview():
            return

        if self.thcValueRb.isChecked() and ((not is_number(self.thcValueQle.text())) or (
                float(self.thcValueQle.text()) < 0 or float(self.thcValueQle.text()) > 100)):
            AlertWindow("El porcentaje total de hidrocarburos ingresado es invalido, ingrese un numero entre 0 y 100 (Se usa punto '.' como separador decimal)")
            return

        if self.cutoffValueRb.isChecked() and (
                (not is_number(self.cutoffValueQle.text())) or (float(self.cutoffValueQle.text()) < 0)):
            AlertWindow("El valor de cutoff ingresado es invalido, ingrese un numero positivo (Se usa punto '.' como separador decimal)")
            return

        config_aux = self.getCutoff()

        x_title = self.well \
            .wellModel \
            .get_label_for(self.c1Cbo.currentText())

        config = {
            'title': CUTOFF_C1_TITLE,
            'x_axis_title': x_title,
            'y_axis_title': "Porcentaje total de hidrocarburos [%]",
            'flex_size': 6,
            'invert_x': False,
            'invert_y': False,
            'log_x': False,
            'log_y': False,
            'scatter_groups': [],
            'line_groups': [{
                'x_axis': config_aux['x_axis'],
                'y_axis': config_aux['y_axis'],
                'color': self.c1CutoffColorCbo.currentText(),
                'line': self.c1CutoffLineStyleCbo.currentText()
            },
                {
                    'x_axis': [config_aux['cutoff_value'], config_aux['cutoff_value']],
                    'y_axis': [0, config_aux['thc_value']],
                    'color': COLOR_CONSTANTS["RED"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"],
                },
                {
                    'x_axis': [0, config_aux['cutoff_value']],
                    'y_axis': [config_aux['thc_value'], config_aux['thc_value']],
                    'color': COLOR_CONSTANTS["RED"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"],
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

        if str(self.nameQle.text()).upper() in set(self.well.wellModel.get_curve_names()):
            AlertWindow("Ya existe una curva con ese nombre")
            return

        config_aux = self.getCutoff()

        self.well.wellModel.append_curve(self.nameQle.text(), config_aux["main_curve"])

        InformationWindow("Curva guardada")

    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return
