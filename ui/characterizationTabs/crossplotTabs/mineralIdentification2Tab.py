"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox, QPushButton, QComboBox,
                             QCheckBox, QLineEdit)

from PyQt6.QtCore import Qt

import numpy as np

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS

from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS, LINE_TYPE_CONSTANTS, SEE_WINDOW_LBL

from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone

from ui.popUps.alertWindow import AlertWindow

from ui.style.StyleCombos import (color_combo_box, marker_combo_box, colormap_combo_box)

from ui.style.button_styles import PREVIEW_BUTTON_STYLE

from services.crossplot_service import get_mineral_identification_2

from services.tools.pandas_service import set_nan_in_array_if_another_is_nan


class MineralIdentification2Tab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Identificacion Mineral\nGR Espectral 2")

        self.initUI()

        self.numeric_inputs.extend([self.customMaxDepthQle, self.customMinDepthQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
              self.customMinDepthQle, self.customMaxDepthQle,  self.forceDepthZCb, self.forceZAxisCb,
              self.forceZAxisColormapCbo, self.k_checkbox, self.hingleMarkerStyleCbo, self.hingleColorCbo])


    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0

        self.thLbl = QLabel("Torio (Th)")
        self.thCbo = QComboBox(self)
        self.thCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.thCbo)

        self.thLayout = QHBoxLayout()
        self.thLayout.addWidget(self.thLbl)
        self.thLayout.addWidget(self.thCbo)
        self.thLayout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.thLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.kLbl = QLabel("Potasio (K)")
        self.kCbo = QComboBox(self)
        self.kCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.kCbo)

        self.k_checkbox = QCheckBox("Pasar a porcentaje")

        self.kLayout = QHBoxLayout()
        self.kLayout.addWidget(self.kLbl)
        self.kLayout.addWidget(self.kCbo)
        self.kLayout.addWidget(self.k_checkbox)
        self.gridLayout.addLayout(self.kLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.pefLbl = QLabel("Factor Fotoelectrico (Pe)")
        self.pefCbo = QComboBox(self)
        self.pefCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.pefCbo)

        self.pefLayout = QHBoxLayout()
        self.pefLayout.addWidget(self.pefLbl)
        self.pefLayout.addWidget(self.pefCbo)
        self.pefLayout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.pefLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.hingleStyleLbl = QLabel("Color y Tipo de Marcador: ")
        self.hingleColorCbo = color_combo_box()
        self.hingleColorCbo.setCurrentIndex(0)
        self.hingleMarkerStyleCbo = marker_combo_box()
        self.hingleMarkerStyleCbo.setCurrentIndex(1)
        self.hingleMarkerStyleCbo.textActivated[str].connect(self.selectMarker)

        self.hingleStyleLayout = QHBoxLayout()
        self.hingleStyleLayout.addWidget(self.hingleStyleLbl)
        self.hingleStyleLayout.addWidget(self.hingleColorCbo)
        self.hingleStyleLayout.addWidget(self.hingleMarkerStyleCbo)

        self.gridLayout.addLayout(self.hingleStyleLayout, row, 0, 1, 2)

    
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
        self.forceZAxisLayout.addWidget(QLabel(""))

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
        self.customMinDepthLayout.addWidget(QLabel("                                                             "))
        self.customMinDepthQle.setEnabled(False)

        self.customMaxDepthLbl = QLabel("Profundidad máx.:")
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle)
        self.customMaxDepthLayout.addWidget(QLabel("                                                             "))
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
        self.hingleColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.hingleMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if self.forceZAxisCb.isChecked():
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.hingleColorCbo.setEnabled(True)


    def forceZAxis(self, state):        
        self.hingleColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.hingleMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if state != 0:
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.hingleColorCbo.setEnabled(True)


    def preview(self):
        if not super().preview():
            return

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(self.well.wellModel.get_depth_curve()))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(self.well.wellModel.get_depth_curve()))

        z_curve_name = self.zAxisCbo.currentText()

        k_curve_name = self.kCbo.currentText()

        th_curve_name = self.thCbo.currentText()

        if (not self.forceDepthZCb.isChecked() and len(z_curve_name) == 0) or len(k_curve_name) == 0 \
                or len(th_curve_name) == 0:
            AlertWindow("Falta indicar curvas")

        th_curve = self.well.wellModel.get_partial_ranged_df_curve(th_curve_name, minDepth, maxDepth, "", "")

        k_curve = self.well.wellModel.get_partial_ranged_df_curve(k_curve_name, minDepth, maxDepth, "", "")

        k_curve[k_curve == 0] = np.nan

        if (self.k_checkbox
                .isChecked()):
            k_curve = [x * 100 for x in k_curve]

            k_unit = "%"

        else:
            k_unit = f"{self.well.wellModel.get_unit_of(k_curve_name)}"

        if (not self.forceDepthZCb.isChecked() and len(z_curve_name) == 0) or len(k_curve_name) == 0 \
                or len(th_curve_name) == 0:
            AlertWindow("Falta indicar curvas")

        x_axis = th_curve / k_curve

        x_axis[x_axis == 0] = np.nan

        x_axis = np.log10(x_axis)

        config_aux = get_mineral_identification_2()

        th_unit = self.well.wellModel.get_unit_of(th_curve_name)

        y_title = self.well.wellModel.get_label_for(self.pefCbo.currentText(), "PEF")

        y_axis = self.well.wellModel.get_partial_ranged_df_curve(self.pefCbo.currentText(), minDepth, maxDepth, "", "")

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
            'title': 'Identificacion Mineral - GR Espectral ',
            'x_axis_title': f"Th/K [{th_unit}/{k_unit}]",
            'y_axis_title': y_title,
            'flex_size': 6,
            'invert_x': False,
            'invert_y': False,
            'log_x': True,
            'log_y': False,
            'scatter_groups': [
                {       
                    'x_axis': x_axis,
                    'y_axis': y_axis,
                    'marker': self.hingleMarkerStyleCbo.currentText(),
                    'scatter_name': "POZO: " + self.well.wellModel.get_name(),
                    'fixed_color': self.hingleColorCbo.currentText(),
                    'has_z_axis': self.forceZAxisCb.isChecked(),
                    'z_axis': z_axis,
                    'z_axis_colormap': self.forceZAxisColormapCbo.currentText(),
                    'z_axis_title': "Profundidad" if self.forceDepthZCb.isChecked() else z_curve_name,
                }
            ],
            'line_groups': [],
            'words': []
        }

        color_cbo = color_combo_box()
        
        for i in range(len(config_aux['rectangles'])):
            for j in range(len(config_aux['rectangles'][i]['x']) - 1):
                config['line_groups'].append(
                    {
                        'x_axis': [config_aux['rectangles'][i]['x'][j], config_aux['rectangles'][i]['x'][j + 1]],
                        'y_axis': [config_aux['rectangles'][i]['y'][j], config_aux['rectangles'][i]['y'][j + 1]],
                        'color': color_cbo.itemText(i),
                        'line': LINE_TYPE_CONSTANTS["SOLID_LINE"],
                        'line_name': (config_aux['rectangles'][i]['name'] if j == 0 else "")
                    }
            )

        
        for word in config_aux['words']:
            config['words'].append({
                'x': word['x'],
                'y': word['y'],
                'name': word['name']
            })

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])

    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return

        self.kCbo.setCurrentIndex(0)
        self.thCbo.setCurrentIndex(0)
