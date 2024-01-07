"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox, QPushButton, QComboBox,
                             QCheckBox, QLineEdit)
from PyQt6.QtCore import Qt

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS

from constants.messages_constants import MISSING_WELL

from constants.pytrophysicsConstants import (LINE_MARKER_CONSTANTS, LINE_TYPE_CONSTANTS,
                                             COLOR_CONSTANTS, SEE_WINDOW_LBL)
from constants.tab_constants import MATRIX_PROPERTIES_CUTOFF_TAB
from services.tools.pandas_service import set_nan_in_array_if_another_is_nan

from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone

from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow

from ui.style.StyleCombos import (color_combo_box, marker_combo_box, 
                                  line_combo_box, colormap_combo_box)

from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE

from services.crossplot_service import (get_pef_density, get_neutron_density, 
                                        get_sonic_neutron, get_sonic_density)


class RHOShaleTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__(MATRIX_PROPERTIES_CUTOFF_TAB)

        self.methods = {
            'Densidad-PEF': {
                'method': get_pef_density,
                'x_label': 'Factor Fotoelectrico (Pe)',
                'y_label': 'Densidad (\u03C1)',
                'z_label': 'Eje Z',
                'x_union': ['x_sand', 'x_dolomite', 'x_limestone'],
                'y_union': ['y_sand', 'y_dolomite', 'y_limestone'],
                },
            'Densidad-Neutron': {
                'method':  get_neutron_density,
                'x_label': 'Porosidad Neutron (\u03A6<sub>N</sub>)',
                'y_label': 'Densidad (\u03C1)',
                'z_label': 'Eje Z',
                'x_union': ['x_sand', 'x_limestone', 'x_dolomite'],
                'y_union': ['y_sand', 'y_limestone', 'y_dolomite'],
                },
            'Sonico-Neutron': {
                'method':  get_sonic_neutron,
                'x_label': 'Porosidad Neutron (\u03A6<sub>N</sub>)',
                'y_label': 'Sonico Compresional (\u0394T)',
                'z_label': 'Eje Z',
                'x_union': ['x_dolomite', 'x_limestone', 'x_sand'],
                'y_union': ['y_dolomite', 'y_limestone', 'y_sand'],
                },
            'Densidad-Sonico': {
                'method':  get_sonic_density,
                'x_label': 'Sonico Compresional (\u0394T)',
                'y_label': 'Densidad (\u03C1)',
                'z_label': 'Eje Z',
                'x_union': ['x_limestone', 'x_sand', 'x_dolomite'],
                'y_union': ['y_limestone', 'y_sand', 'y_dolomite'],
            }
        }

        self.initUI()

        self.numeric_inputs.extend([self.customMaxDepthQle, self.customMinDepthQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
              self.customMinDepthQle, self.customMaxDepthQle, self.adjustCurveLineStyleCbo,
              self.adjustCurveColorCbo, self.adjustCurveCb, self.forceDepthZCb, self.forceZAxisCb,
              self.rhoShaleColorCbo, self.rhoShaleMarkerStyleCbo, self.forceZAxisColormapCbo,
              self.crossplotTypeCbo, self.lithologiesUnionCurveCb, self.saveAsRHOMatrixRb,  self.saveAsDTMatrixRb])

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        row = 0

        self.crossplotTypeLbl = QLabel(CROSSPLOTS_CONSTANTS.CROSSPLOT_TYPE_LABEL)
        self.crossplotTypeCbo = QComboBox(self)
        self.crossplotTypeCbo.setPlaceholderText(CROSSPLOTS_CONSTANTS.CROSSPLOT_TYPE_CBO_PLACEHOLDER)
        self.crossplotTypeCbo.textActivated[str].connect(self.selectMethod)
        for key in self.methods.keys():
            self.crossplotTypeCbo.addItem(key)
        self.crossplotTypeCbo.setCurrentIndex(0)

        self.crossplotTypeLayout = QHBoxLayout()
        self.crossplotTypeLayout.addWidget(self.crossplotTypeLbl)
        self.crossplotTypeLayout.addWidget(self.crossplotTypeCbo)
        self.crossplotTypeLayout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.crossplotTypeLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.yAxisLbl = QLabel(self.methods[self.crossplotTypeCbo.currentText()]['y_label'])
        self.yAxisCbo = QComboBox(self)
        self.yAxisCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.yAxisCbo)

        self.yAxisLayout = QHBoxLayout()
        self.yAxisLayout.addWidget(self.yAxisLbl)
        self.yAxisLayout.addWidget(self.yAxisCbo)
        self.yAxisLayout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.yAxisLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.xAxisLbl = QLabel(self.methods[self.crossplotTypeCbo.currentText()]['x_label'])
        self.xAxisCbo = QComboBox(self)
        self.xAxisCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.xAxisCbo)

        self.xAxisLayout = QHBoxLayout()
        self.xAxisLayout.addWidget(self.xAxisLbl)
        self.xAxisLayout.addWidget(self.xAxisCbo)
        self.xAxisLayout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.xAxisLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.rhoShaleStyleLbl = QLabel("Color y Tipo de Marcador: ")
        self.rhoShaleColorCbo = color_combo_box()
        self.rhoShaleColorCbo.setCurrentIndex(0)
        self.rhoShaleMarkerStyleCbo = marker_combo_box()
        self.rhoShaleMarkerStyleCbo.setCurrentIndex(1)
        self.rhoShaleMarkerStyleCbo.textActivated[str].connect(self.selectMarker)

        self.rhoShaleStyleLayout = QHBoxLayout()
        self.rhoShaleStyleLayout.addWidget(self.rhoShaleStyleLbl)
        self.rhoShaleStyleLayout.addWidget(self.rhoShaleColorCbo)
        self.rhoShaleStyleLayout.addWidget(self.rhoShaleMarkerStyleCbo)

        self.gridLayout.addLayout(self.rhoShaleStyleLayout, row, 0, 1, 2)

    
        ########################################################################

        row += 1

        self.forceZAxisCb = QCheckBox("Usar escala de color según el eje Z")
        self.forceZAxisCb.stateChanged.connect(self.forceZAxis)

        self.forceZAxisColormapCbo = colormap_combo_box()
        self.forceZAxisColormapCbo.setCurrentIndex(0)
        self.forceZAxisColormapCbo.setEnabled(False)

        self.forceZAxisLayout = QHBoxLayout()
        self.forceZAxisLayout.addWidget(self.forceZAxisCb)
        self.forceZAxisLayout.addWidget(self.forceZAxisColormapCbo)

        self.gridLayout.addLayout(self.forceZAxisLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.zAxisLbl = QLabel("Eje Z")
        self.zAxisCbo = QComboBox(self)
        self.zAxisCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.zAxisCbo)
        
        self.forceDepthZCb = QCheckBox("Usar eje Z = Profundidad")
        self.forceDepthZCb.stateChanged.connect(self.forceDepthZ)

        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)

        self.zAxisLayout = QHBoxLayout()
        self.zAxisLayout.addWidget(self.zAxisLbl)
        self.zAxisLayout.addWidget(self.zAxisCbo)
        self.zAxisLayout.addWidget(self.forceDepthZCb)
        self.gridLayout.addLayout(self.zAxisLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.adjustCurveCb = QCheckBox("Mostrar Mejor Ajuste")
        self.adjustCurveColorCbo = color_combo_box()
        self.adjustCurveColorCbo.setCurrentIndex(0)
        self.adjustCurveLineStyleCbo = line_combo_box()
        self.adjustCurveLineStyleCbo.setCurrentIndex(0)

        self.adjustCurveCb.stateChanged.connect(self.adjustCurve)
        self.adjustCurveCb.setChecked(False)
        self.adjustCurveColorCbo.setEnabled(False)
        self.adjustCurveLineStyleCbo.setEnabled(False)

        self.adjustCurveLayout = QHBoxLayout()
        self.adjustCurveLayout.addWidget(self.adjustCurveCb)
        self.adjustCurveLayout.addWidget(self.adjustCurveColorCbo)
        self.adjustCurveLayout.addWidget(self.adjustCurveLineStyleCbo)

        self.gridLayout.addLayout(self.adjustCurveLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.lithologiesUnionCurveCb = QCheckBox("Mostrar Linea Union entre Litologias")
        self.lithologiesUnionCurveCb.setChecked(True)

        self.gridLayout.addWidget(self.lithologiesUnionCurveCb, row, 0, 1, 2)

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

        self.saveAsGrpBox = QGroupBox()
        #self.colorBarGrpBox.setFont(QFont("Times New Roman", 15))

        # this is hbox layout
        self.saveAsLayout = QVBoxLayout()

        # these are the radiobuttons
        self.saveAsRHOMatrixRb = QRadioButton(str("Guardar como RHO (\u03C1)"))
        self.saveAsRHOMatrixRb.setChecked(True)
        #self.saveAsRHOMatrixRb.setFont(QFont("Times New Roman", 14))
        self.saveAsRHOMatrixRb.toggled.connect(self.on_selected2)
        self.saveAsLayout.addWidget(self.saveAsRHOMatrixRb)

        # these are the radiobuttons
        self.saveAsDTMatrixRb = QRadioButton(str("Guardar como DT (\u0394T)"))
        self.saveAsDTMatrixRb.setChecked(False)
        #self.saveAsDTMatrixRb.setFont(QFont("Times New Roman", 14))
        self.saveAsDTMatrixRb.toggled.connect(self.on_selected2)
        self.saveAsLayout.addWidget(self.saveAsDTMatrixRb)

        self.saveAsGrpBox.setLayout(self.saveAsLayout)
        self.gridLayout.addWidget(self.saveAsGrpBox, row, 0, 1, 1)

        ########################################################################

        row += 1

        self.nameLbl = QLabel("Nombre: Matrix_")
        self.nameQle = QLineEdit(self)
        self.nameQle.setStyleSheet(QLE_NAME_STYLE)
        self.nameQle.textChanged[str].connect(self.setMatrixCurveName)
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


    def selectMethod(self, method):
        self.xAxisLbl.setText(self.methods[self.crossplotTypeCbo.currentText()]['x_label'])
        self.yAxisLbl.setText(self.methods[self.crossplotTypeCbo.currentText()]['y_label'])
        self.saveAsRHOMatrixRb.setEnabled(True)
        self.saveAsDTMatrixRb.setEnabled(True)
        if self.crossplotTypeCbo.currentText() == list(self.methods.keys())[1]:
            self.saveAsRHOMatrixRb.setChecked(True)
            self.saveAsDTMatrixRb.setEnabled(False) 
        elif self.crossplotTypeCbo.currentText() == list(self.methods.keys())[2]:
            self.saveAsDTMatrixRb.setChecked(True)
            self.saveAsRHOMatrixRb.setEnabled(False)


    def forceDepthZ(self, state):
        self.zAxisLbl.setEnabled(state == 0)
        self.zAxisCbo.setEnabled(state == 0)


    def selectMarker(self):
        self.rhoShaleColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.rhoShaleMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if self.forceZAxisCb.isChecked():
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.rhoShaleColorCbo.setEnabled(True)


    def forceZAxis(self, state):
        self.rhoShaleColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.rhoShaleMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if state != 0:
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.rhoShaleColorCbo.setEnabled(True)


    def adjustCurve(self, state):
        self.adjustCurveColorCbo.setEnabled(state != 0)
        self.adjustCurveLineStyleCbo.setEnabled(state != 0)


    # method or slot for the toggled signal
    def on_selected(self):
        radio_button = self.sender()
        
        if radio_button.isChecked():
            print("You have selected : " + radio_button.text())
        #    self.label.setText("You have selected : " + radio_button.text())

        self.customMinDepthQle.setEnabled(self.depthCustomRb.isChecked())
        self.customMaxDepthQle.setEnabled(self.depthCustomRb.isChecked())

        #self.groupsQle.setEnabled(self.depthCustomRb.isChecked())
        #self.enableGroupAmount("")

    def on_selected2(self):
        radio_button = self.sender()
        
        if radio_button.isChecked():
            print("You have selected : " + radio_button.text())

    def setMatrixCurveName(self, text):
        self.matrix_curve_name = "Matrix_" + text


    def preview(self):
        if not super().preview():
            return

        self.init_window()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(self.well.wellModel.get_depth_curve()))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(self.well.wellModel.get_depth_curve()))

        x_axis = self.well.wellModel.get_partial_ranged_df_curve(self.xAxisCbo.currentText(), minDepth, maxDepth, "", "")
        y_axis = self.well.wellModel.get_partial_ranged_df_curve(self.yAxisCbo.currentText(), minDepth, maxDepth, "", "" )

        x_axis, y_axis = set_nan_in_array_if_another_is_nan(x_axis, y_axis)
        
        z_axis = x_axis
        if self.forceZAxisCb.isChecked():
            if self.forceDepthZCb.isChecked():
                z_axis = self.well.wellModel.get_partial_depth_curve(minDepth, maxDepth)
            else:
                z_axis = self.well.wellModel.get_partial_ranged_df_curve(self.zAxisCbo.currentText(), minDepth, maxDepth, "", "")
        
            x_axis, z_axis = set_nan_in_array_if_another_is_nan(x_axis, z_axis)
            y_axis, z_axis = set_nan_in_array_if_another_is_nan(y_axis, z_axis)

        config_aux = self.methods[self.crossplotTypeCbo.currentText()]['method'](x_axis, y_axis)

        x_union = self.methods[self.crossplotTypeCbo.currentText()]['x_union']
        y_union = self.methods[self.crossplotTypeCbo.currentText()]['y_union']
        lithologies_aux = {
            "x_axis": [config_aux[x_union[0]][0], config_aux[x_union[1]][0], config_aux[x_union[2]][0]],
            "y_axis": [config_aux[y_union[0]][0], config_aux[y_union[1]][0], config_aux[y_union[2]][0]]
        }

        x_axis_title = self.well.wellModel.get_label_for(self.xAxisCbo.currentText())

        y_axis_title = self.well.wellModel.get_label_for(self.yAxisCbo.currentText())

        config = {
            'title': str('Crossplot ' + self.crossplotTypeCbo.currentText()),
            'x_axis_title': x_axis_title,
            'y_axis_title': y_axis_title,
            'flex_size': 6,
            'invert_y': False if self.crossplotTypeCbo.currentText() == 'Sonico-Neutron' else True,
            'scatter_groups': [
                {       
                    'x_axis': x_axis,
                    'y_axis': y_axis,
                    'scatter_name': "POZO: " + self.well.wellModel.get_name(),
                    'marker': self.rhoShaleMarkerStyleCbo.currentText(),
                    'fixed_color': self.rhoShaleColorCbo.currentText(),
                    'has_z_axis': self.forceZAxisCb.isChecked(),
                    'z_axis': z_axis,
                    'z_axis_colormap': self.forceZAxisColormapCbo.currentText(),
                    'z_axis_title': "Profundidad" if self.forceDepthZCb.isChecked() else self.zAxisCbo.currentText(),
                }
            ],
            'line_groups': [
                {
                    'x_axis': config_aux['x_sand'],
                    'y_axis': config_aux['y_sand'],
                    'line_name': "Arena",
                    'color': COLOR_CONSTANTS["RED"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"]
                },
                {
                    'x_axis': config_aux['x_limestone'],
                    'y_axis': config_aux['y_limestone'],
                    'line_name': "Caliza",
                    'color': COLOR_CONSTANTS["YELLOW"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"]
                },
                {  
                    'x_axis': config_aux['x_dolomite'],
                    'y_axis': config_aux['y_dolomite'],
                    'line_name': "Dolomita",
                    'color': COLOR_CONSTANTS["MAGENTA"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"]
                }
            ],
        }

        if self.lithologiesUnionCurveCb.isChecked():
            config['line_groups'].append(
                {
                    'x_axis': lithologies_aux['x_axis'],
                    'y_axis': lithologies_aux['y_axis'],
                    #'line_name': None,
                    'color': COLOR_CONSTANTS["LIGHT_BLUE"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"]
                })

        if self.adjustCurveCb.isChecked():
            config['line_groups'].append(
                {
                    'x_axis': config_aux['x_minimized'],
                    'y_axis': config_aux['y_minimized'],
                    'line_name': "Mejor Ajuste",
                    'color': self.adjustCurveColorCbo.currentText(),
                    'line': self.adjustCurveLineStyleCbo.currentText()
                })

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])

    def saveCurve(self):
        if not super().preview():
            return

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(self.well.wellModel.get_depth_curve()))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(self.well.wellModel.get_depth_curve()))

        config_aux = self.methods[self.crossplotTypeCbo.currentText()]['method'](
                                    self.well.wellModel.get_partial_ranged_df_curve(self.xAxisCbo.currentText(), minDepth, maxDepth, "", ""),
                                    self.well.wellModel.get_partial_ranged_df_curve(self.yAxisCbo.currentText(), minDepth, maxDepth, "", "" )
                                    )
        if self.saveAsRHOMatrixRb.isChecked():
            curve = config_aux["rho_matrix"]
        else:
            curve = config_aux["dt_matrix"]

        self.well.wellModel.append_curve(self.matrix_curve_name, curve)

        InformationWindow("Curva guardada")

    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return

        self.yAxisCbo.setCurrentIndex(0)
        self.xAxisCbo.setCurrentIndex(0)
        self.zAxisCbo.setCurrentIndex(0)
