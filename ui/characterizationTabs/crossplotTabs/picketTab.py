"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox,
                             QPushButton, QComboBox, QCheckBox, QLineEdit)
from PyQt6.QtCore import Qt

import numpy as np

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.messages_constants import MISSING_WELL
from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS, LINE_TYPE_CONSTANTS, SEE_WINDOW_LBL
from constants.sw_constants import RW_TAB_FULL_NAME
from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone
from ui.popUps.alertWindow import AlertWindow
from ui.style.StyleCombos import (color_combo_box, marker_combo_box,
                                  colormap_combo_box)
from ui.style.button_styles import PREVIEW_BUTTON_STYLE

from services.crossplot_service import get_picket
from services.tools.string_service import is_number
from services.tools.pandas_service import set_nan_in_array_if_another_is_nan


class PicketTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Pickett")

        self.initUI()

        self.numeric_inputs.extend([self.customMaxDepthQle, self.customMinDepthQle,
                                    self.aConstantQle, self.mConstantQle, self.nConstantQle, self.rwQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
              self.customMinDepthQle, self.customMaxDepthQle,  self.forceDepthZCb, self.forceZAxisCb,
              self.forceZAxisColormapCbo, self.picketColorCbo, self.picketMarkerStyleCbo,
              self.aConstantQle, self.mConstantQle, self.nConstantQle, self.rwQle])

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0

        self.rtLbl = QLabel("Resistividad Profunda (Rt)")
        self.rtCbo = QComboBox(self)
        self.rtCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.rtCbo)

        self.rtLayout = QHBoxLayout()
        self.rtLayout.addWidget(self.rtLbl)
        self.rtLayout.addWidget(self.rtCbo)
        self.gridLayout.addLayout(self.rtLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.phieLbl = QLabel("Porosidad Efectiva (\u03A6<sub>e</sub>)")
        self.phieCbo = QComboBox(self)
        self.phieCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.phieCbo)

        self.phieLayout = QHBoxLayout()
        self.phieLayout.addWidget(self.phieLbl)
        self.phieLayout.addWidget(self.phieCbo)
        self.gridLayout.addLayout(self.phieLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.rwLbl = QLabel(RW_TAB_FULL_NAME)
        self.rwCbo = QComboBox(self)
        self.rwCbo.setPlaceholderText('Elige Curva')
        self.rwCbo.textActivated[str].connect(self.updateRw)
        self.curve_selectors.append(self.rwCbo)

        self.rwLayout = QHBoxLayout()
        self.rwLayout.addWidget(self.rwLbl)
        self.rwLayout.addWidget(self.rwCbo)
        self.gridLayout.addLayout(self.rwLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.meanRwLbl = QLabel("Valor medio tomado de RW: ")
        self.rwQle = QLineEdit(self)

        self.meanRwLayout = QHBoxLayout()
        self.meanRwLayout.addWidget(self.meanRwLbl)
        self.meanRwLayout.addWidget(self.rwQle)
        self.gridLayout.addLayout(self.meanRwLayout, row, 0, 1, 1)

        ########################################################################

        row += 1

        self.constantsLayout = QHBoxLayout()
        self.aConstantLbl = QLabel("a:")
        self.aConstantQle = QLineEdit(self)
        self.aConstantQle.setPlaceholderText('1')
        self.mConstantLbl = QLabel("m:")
        self.mConstantQle = QLineEdit(self)
        self.mConstantQle.setPlaceholderText('2')
        self.nConstantLbl = QLabel("n:")
        self.nConstantQle = QLineEdit(self)
        self.nConstantQle.setPlaceholderText('2')

        self.constantsLayout.addWidget(self.aConstantLbl)
        self.constantsLayout.addWidget(self.aConstantQle)
        self.constantsLayout.addWidget(self.mConstantLbl)
        self.constantsLayout.addWidget(self.mConstantQle)
        self.constantsLayout.addWidget(self.nConstantLbl)
        self.constantsLayout.addWidget(self.nConstantQle)

        self.gridLayout.addLayout(self.constantsLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.picketStyleLbl = QLabel("Color y Tipo de Marcador: ")
        self.picketColorCbo = color_combo_box()
        self.picketColorCbo.setCurrentIndex(0)
        self.picketMarkerStyleCbo = marker_combo_box()
        self.picketMarkerStyleCbo.setCurrentIndex(1)
        self.picketMarkerStyleCbo.textActivated[str].connect(self.selectMarker)

        self.picketStyleLayout = QHBoxLayout()
        self.picketStyleLayout.addWidget(self.picketStyleLbl)
        self.picketStyleLayout.addWidget(self.picketColorCbo)
        self.picketStyleLayout.addWidget(self.picketMarkerStyleCbo)

        self.gridLayout.addLayout(self.picketStyleLayout, row, 0, 1, 2)

    
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
        self.customMinDepthQle.textChanged[str].connect(self.updateRwDepth)

        self.customMaxDepthLbl = QLabel("Profundidad máx.:")
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle)
        self.customMaxDepthQle.setEnabled(False)
        self.customMaxDepthQle.textChanged[str].connect(self.updateRwDepth)

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
        self.picketColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.picketMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if self.forceZAxisCb.isChecked():
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.picketColorCbo.setEnabled(True)


    def forceZAxis(self, state):        
        self.picketColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.picketMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if state != 0:
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.picketColorCbo.setEnabled(True)

    def updateRw(self):
        depth_curve = self.well\
            .wellModel\
            .get_depth_curve()

        if not any(depth_curve):
            return

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))

        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        rw_values = self.well \
            .wellModel \
            .get_partial_ranged_df_curve(self.rwCbo.currentText(), minDepth, maxDepth, "", "")

        rw_values = rw_values[~np.isnan(rw_values)]

        self.rwQle.setPlaceholderText(str(round(np.mean(rw_values), 4)))

    def updateRwDepth(self, text):
        self.updateRw()

    def preview(self):
        if not super().preview():
            return

        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        rw_values = self.well.wellModel.get_partial_ranged_df_curve(self.rwCbo.currentText(), minDepth, maxDepth, "", "")

        rw = round(np.mean(rw_values[~np.isnan(rw_values)]), 4)
        if is_number(self.rwQle.text()):
            rw = float(self.rwQle.text())

        a = 1
        if is_number(self.aConstantQle.text()):
            a = float(self.aConstantQle.text())

        m = 2
        if is_number(self.mConstantQle.text()):
            m = float(self.mConstantQle.text())

        n = 2
        if is_number(self.nConstantQle.text()):
            n = float(self.nConstantQle.text())

        config_aux = get_picket(self.well
                                    .wellModel
                                    .get_partial_ranged_df_curve(self.rtCbo.currentText(),
                                                                 minDepth,
                                                                 maxDepth,
                                                                 "",
                                                                 ""),
                                rw,
                                a,
                                m,
                                n
                                )

        log_phie = self.well.wellModel.get_partial_ranged_df_curve(self.phieCbo.currentText(), minDepth, maxDepth, "", "")
        log_phie[log_phie == 0] = np.nan
        log_phie = np.log10(log_phie)

        x_title = self.well.wellModel.get_label_for(self.rtCbo.currentText(), "Resistividad")

        y_title = self.well.wellModel.get_label_for(self.phieCbo.currentText(), "Porosidad")

        x_axis = np.log10(self.well.wellModel.get_partial_ranged_df_curve(self.rtCbo.currentText(), minDepth, maxDepth, "", ""))
        y_axis = log_phie

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
            'title': 'Crossplot Pickett',
            'x_axis_title': x_title,
            'y_axis_title': y_title,
            'flex_size': 6,
            'invert_x': False,
            'invert_y': False,
            'log_x': True,
            'log_y': True,
            'scatter_groups': [
                {       
                    'x_axis': x_axis,
                    'y_axis': y_axis,
                    'marker': self.picketMarkerStyleCbo.currentText(),
                    'scatter_name': "POZO: " + self.well.wellModel.get_name(),
                    'fixed_color': self.picketColorCbo.currentText(),
                    'has_z_axis': self.forceZAxisCb.isChecked(),
                    'z_axis': z_axis,
                    'z_axis_colormap': self.forceZAxisColormapCbo.currentText(),
                    'z_axis_title': "Profundidad" if self.forceDepthZCb.isChecked() else self.zAxisCbo.currentText(),
                }
            ],
            'line_groups': [],
        }

        color_cbo = color_combo_box()
        
        for i in range(len(config_aux['log_rt'])):
            config['line_groups'].append(
                {
                    'x_axis': config_aux['log_rt'][i],
                    'y_axis': config_aux['log_phie'][i],
                    'color': color_cbo.itemText(i),
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"],
                    'line_name': "SW: " + str(config_aux['sw'][i])
                }
            )

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])


    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return

        self.rtCbo.setCurrentIndex(0)
        self.phieCbo.setCurrentIndex(0)
        self.rwCbo.setCurrentIndex(0)
        self.updateRw()
