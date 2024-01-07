"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton,QGroupBox, QPushButton, QComboBox,
                             QCheckBox, QLineEdit)
from PyQt6.QtCore import Qt

import numpy as np

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS

from constants.messages_constants import MISSING_WELL

from constants.pytrophysicsConstants import (LINE_MARKER_CONSTANTS, LINE_TYPE_CONSTANTS, COLOR_CONSTANTS,
                                             SEE_WINDOW_LBL)

from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.informationWindow import InformationWindow

from ui.style.StyleCombos import (color_combo_box, marker_combo_box, colormap_combo_box)

from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE

from services.crossplot_service import get_rhoma_umaa

from services.tools.string_service import is_number

from services.tools.pandas_service import set_nan_in_array_if_another_is_nan

from constants.LETTERS import PHI


class RhomaUmaaTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Rhoma-Umaa")

        self.savedCurveName = ""

        self.initUI()

        self.numeric_inputs.extend([self.customMaxDepthQle, self.customMinDepthQle, self.rhofConstantQle,
                                    self.peffConstantQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
              self.customMinDepthQle, self.customMaxDepthQle,  self.forceDepthZCb, self.forceZAxisCb,
              self.forceZAxisColormapCbo, self.rhofConstantQle, self.saveAsUmaaRb, self.saveAsRhomaRb,
              self.rhomaUmaaMarkerStyleCbo, self.rhomaUmaaColorCbo, self.rhofConstantQle, self.peffConstantQle])

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0

        self.phiDNLbl = QLabel(f"Porosidad Densidad/Neutron ({PHI}<sub>D/N</sub>)")
        self.phiDNCbo = QComboBox(self)
        self.phiDNCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.phiDNCbo)

        self.phiDNLayout = QHBoxLayout()
        self.phiDNLayout.addWidget(self.phiDNLbl)
        self.phiDNLayout.addWidget(self.phiDNCbo)
        self.gridLayout.addLayout(self.phiDNLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.pefLbl = QLabel("Factor Fotoelectrico (Pe)")
        self.pefCbo = QComboBox(self)
        self.pefCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.pefCbo)

        self.pefLayout = QHBoxLayout()
        self.pefLayout.addWidget(self.pefLbl)
        self.pefLayout.addWidget(self.pefCbo)
        self.gridLayout.addLayout(self.pefLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.rhoLbl = QLabel("Densidad (\u03C1)")
        self.rhoCbo = QComboBox(self)
        self.rhoCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.rhoCbo)

        self.rhoLayout = QHBoxLayout()
        self.rhoLayout.addWidget(self.rhoLbl)
        self.rhoLayout.addWidget(self.rhoCbo)
        self.gridLayout.addLayout(self.rhoLayout, row, 0, 1, 2)


        ########################################################################

        row += 1

        self.constantsLayout = QHBoxLayout()
        self.peffConstantLbl = QLabel("Pe<sub>f</sub>:")
        self.peffConstantQle = QLineEdit(self)
        self.peffConstantQle.setPlaceholderText('0.36')
        self.rhofConstantLbl = QLabel("\u03C1<sub>f</sub>:")
        self.rhofConstantQle = QLineEdit(self)
        self.rhofConstantQle.setPlaceholderText('1')

        self.constantsLayout.addWidget(self.peffConstantLbl)
        self.constantsLayout.addWidget(self.peffConstantQle)
        self.constantsLayout.addWidget(self.rhofConstantLbl)
        self.constantsLayout.addWidget(self.rhofConstantQle)

        self.gridLayout.addLayout(self.constantsLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.rhomaUmaaStyleLbl = QLabel("Color y Tipo de Marcador: ")
        self.rhomaUmaaColorCbo = color_combo_box()
        self.rhomaUmaaColorCbo.setCurrentIndex(0)
        self.rhomaUmaaMarkerStyleCbo = marker_combo_box()
        self.rhomaUmaaMarkerStyleCbo.setCurrentIndex(1)
        self.rhomaUmaaMarkerStyleCbo.textActivated[str].connect(self.selectMarker)

        self.rhomaUmaaStyleLayout = QHBoxLayout()
        self.rhomaUmaaStyleLayout.addWidget(self.rhomaUmaaStyleLbl)
        self.rhomaUmaaStyleLayout.addWidget(self.rhomaUmaaColorCbo)
        self.rhomaUmaaStyleLayout.addWidget(self.rhomaUmaaMarkerStyleCbo)

        self.gridLayout.addLayout(self.rhomaUmaaStyleLayout, row, 0, 1, 2)

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

        self.saveAsLayout = QVBoxLayout()

        self.saveAsRhomaRb = QRadioButton(str("Guardar curva RHOMA"))
        self.saveAsRhomaRb.setChecked(True)
        #self.saveAsRhomaRb.setFont(QFont("Times New Roman", 14))
        self.saveAsLayout.addWidget(self.saveAsRhomaRb)

        self.saveAsUmaaRb = QRadioButton(str("Guardar curva UMAA"))
        self.saveAsUmaaRb.setChecked(False)
        #self.saveAsUmaaRb.setFont(QFont("Times New Roman", 14))
        self.saveAsLayout.addWidget(self.saveAsUmaaRb)

        self.saveAsGrpBox.setLayout(self.saveAsLayout)
        self.gridLayout.addWidget(self.saveAsGrpBox, row, 0, 1, 1)

        ########################################################################    

        row += 1

        self.nameLbl = QLabel("Nombre: ")
        self.nameQle = QLineEdit(self)
        self.nameQle.textChanged[str].connect(self.setSavedCurveName)
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


    def forceDepthZ(self, state):
        self.zAxisLbl.setEnabled(state == 0)
        self.zAxisCbo.setEnabled(state == 0)


    def selectMarker(self):
        self.rhomaUmaaColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.rhomaUmaaMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if self.forceZAxisCb.isChecked():
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.rhomaUmaaColorCbo.setEnabled(True)


    def forceZAxis(self, state):        
        self.rhomaUmaaColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.rhomaUmaaMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if state != 0:
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.rhomaUmaaColorCbo.setEnabled(True)


    def setSavedCurveName(self, text):
        self.savedCurveName = text


    def preview(self):
        if not super().preview():
            return

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(self.well.wellModel.get_depth_curve()))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(self.well.wellModel.get_depth_curve()))

        peff = 0.36
        if is_number(self.peffConstantQle.text()):
            peff = float(self.peffConstantQle.text())

        rhof = 1
        if is_number(self.rhofConstantQle.text()):
            rhof = float(self.rhofConstantQle.text())

        config_aux = get_rhoma_umaa(self.well.wellModel.get_partial_ranged_df_curve(self.phiDNCbo.currentText(), minDepth, maxDepth, "", ""),
                                    self.well.wellModel.get_partial_ranged_df_curve(self.pefCbo.currentText(), minDepth, maxDepth, "", ""),
                                    self.well.wellModel.get_partial_ranged_df_curve(self.rhoCbo.currentText(), minDepth, maxDepth, "", ""),
                                    peff,
                                    rhof
                                    )

        x_axis = config_aux["umaa"]
        y_axis = config_aux["rhoma"]

        x_axis, y_axis = set_nan_in_array_if_another_is_nan(x_axis, y_axis)
        z_axis = x_axis
        if self.forceZAxisCb.isChecked():
            if self.forceDepthZCb.isChecked():
                z_axis = self.well.wellModel.get_partial_depth_curve(minDepth, maxDepth)
            else:
                z_axis = self.well.wellModel.get_partial_ranged_df_curve(self.zAxisCbo.currentText(), minDepth, maxDepth, "", "")
        
            x_axis, z_axis = set_nan_in_array_if_another_is_nan(x_axis, z_axis)
            y_axis, z_axis = set_nan_in_array_if_another_is_nan(y_axis, z_axis)

        config = {
            'title': 'Crossplot RHOMA-UMAA',
            'x_axis_title': "UMAA",
            'y_axis_title': "RHOMA",
            'flex_size': 6,
            'invert_x': False,
            'invert_y': True,
            'scatter_groups': [
                {       
                    'x_axis': x_axis,
                    'y_axis': y_axis,
                    'marker': self.rhomaUmaaMarkerStyleCbo.currentText(),
                    'scatter_name': "POZO: " + self.well.wellModel.get_name(),
                    'fixed_color': self.rhomaUmaaColorCbo.currentText(),
                    'has_z_axis': self.forceZAxisCb.isChecked(),
                    'z_axis': z_axis,
                    'z_axis_colormap': self.forceZAxisColormapCbo.currentText(),
                    'z_axis_title': "Profundidad" if self.forceDepthZCb.isChecked() else self.zAxisCbo.currentText(),
                },
                {
                    'x_axis': np.array([config_aux["umaa_limestone"]]),
                    'y_axis': np.array([config_aux["rhoma_limestone"]]),
                    'scatter_name': "Caliza",
                    'marker': LINE_MARKER_CONSTANTS["PENTAGON"],
                    'fixed_color': COLOR_CONSTANTS["RED"],
                    'has_z_axis': False,
                },
                {
                    'x_axis': np.array([config_aux["umaa_dolomite"]]),
                    'y_axis': np.array([config_aux["rhoma_dolomite"]]),
                    'scatter_name': "Dolomita",
                    'marker': LINE_MARKER_CONSTANTS["HEXAGON"],
                    'fixed_color': COLOR_CONSTANTS["BLUE"],
                    'has_z_axis': False,
                },
                {
                    'x_axis': np.array([config_aux["umaa_sandstone"]]),
                    'y_axis': np.array([config_aux["rhoma_sandstone"]]),
                    'scatter_name': "Arenizca",
                    'marker': LINE_MARKER_CONSTANTS["STAR"],
                    'fixed_color': COLOR_CONSTANTS["YELLOW"],
                    'has_z_axis': False,
                }
            ],
            'line_groups': [
                {
                    'x_axis': np.array([config_aux["umaa_sandstone"], config_aux["umaa_dolomite"]]),
                    'y_axis': np.array([config_aux["rhoma_sandstone"], config_aux["rhoma_dolomite"]]),
                    'color': COLOR_CONSTANTS["BLACK"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"]
                },
                {
                    'x_axis': np.array([config_aux["umaa_sandstone"], config_aux["umaa_limestone"]]),
                    'y_axis': np.array([config_aux["rhoma_sandstone"], config_aux["rhoma_limestone"]]),
                    'color': COLOR_CONSTANTS["BLACK"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"]
                },
                {
                    'x_axis': np.array([config_aux["umaa_dolomite"], config_aux["umaa_limestone"]]),
                    'y_axis': np.array([config_aux["rhoma_dolomite"], config_aux["rhoma_limestone"]]),
                    'color': COLOR_CONSTANTS["BLACK"],
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"]
                }
            ],
        }

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])

    def saveCurve(self):
        if not super().preview():
            return

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(self.well.wellModel.get_depth_curve()))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(self.well.wellModel.get_depth_curve()))

        config_aux = get_rhoma_umaa(self.well.wellModel.get_partial_ranged_df_curve(self.phiDNCbo.currentText(), minDepth, maxDepth, "", ""),
                                    self.well.wellModel.get_partial_ranged_df_curve(self.pefCbo.currentText(), minDepth, maxDepth, "", ""),
                                    self.well.wellModel.get_partial_ranged_df_curve(self.rhoCbo.currentText(), minDepth, maxDepth, "", "")
                                    )

        if self.saveAsRhomaRb.isChecked():
            curve = config_aux["rhoma"]
        else:
            curve = config_aux["umaa"]
        self.well.wellModel.append_curve(self.savedCurveName, curve)

        InformationWindow("Curva guardada")

    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return

        self.phiDNCbo.setCurrentIndex(0)
        self.pefCbo.setCurrentIndex(0)
        self.rhoCbo.setCurrentIndex(0)
