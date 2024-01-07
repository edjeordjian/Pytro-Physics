"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np
from PyQt6.QtWidgets import (QLabel,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox,
                             QPushButton, QComboBox, QCheckBox, QLineEdit)
from PyQt6.QtCore import Qt

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.LITHOLOGY_CONSTANTS import VSHALE_LABEL
from constants.MENU_CONSTANTS import CURVE_NAME_LABEL_2, SAVE_CURVE_BUTTON
from constants.buckles_constants import CUSTOM_BUCKLES_LBL, BUCKLES_BASE_X, BUCKLES_PREFIX_LBL, VALUE_LBL
from constants.general_constants import LOADING_LBL, SAVED_CURVE_LBL
from constants.messages_constants import MISSING_CURVE_NAME

from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS, LINE_TYPE_CONSTANTS, SEE_WINDOW_LBL
from constants.swirr_constants import SWIRR_TAB_NAME, SWIRR_BUCKLES_DISPLAY_NAME, SWIRR_BUCKLES_TAB_NAME
from services.swirr_service import get_swirr_buckles
from services.tools.string_service import is_positive_number
from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.alerts import get_positive_value_error_alert
from ui.popUps.informationWindow import InformationWindow
from ui.popUps.loading_handler import loading_pop_up
from ui.style.StyleCombos import (color_combo_box, marker_combo_box, colormap_combo_box)
from ui.style.button_styles import PREVIEW_BUTTON_STYLE

from services.crossplot_service import get_buckles
from services.tools.pandas_service import set_nan_in_array_if_another_is_nan
from ui.visual_components.combo_handler import disable_elements_with_component


class BucklesTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Buckles")

        self.initUI()

        self.numeric_inputs.extend([self.customMaxDepthQle, self.customMinDepthQle, self.custom_value_tb])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
              self.customMinDepthQle, self.customMaxDepthQle,  self.forceDepthZCb, self.forceZAxisCb,
              self.forceZAxisColormapCbo, self.bucklesColorCbo, self.bucklesMarkerStyleCbo, self.custom_value_tb,
              self.custom_value_color_cbo])


    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0

        self.swLbl = QLabel("Saturacion de Agua (Sw)")
        self.swCbo = QComboBox(self)
        self.swCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.swCbo)

        self.swLayout = QHBoxLayout()
        self.swLayout.addWidget(self.swLbl)
        self.swLayout.addWidget(self.swCbo)
        self.swLayout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.swLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.phieLbl = QLabel("Porosidad efectiva (\u03A6<sub>e</sub>)")
        self.phieCbo = QComboBox(self)
        self.phieCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.phieCbo)

        self.phieLayout = QHBoxLayout()
        self.phieLayout.addWidget(self.phieLbl)
        self.phieLayout.addWidget(self.phieCbo)
        self.phieLayout.addWidget(QLabel(""))
        self.gridLayout.addLayout(self.phieLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.bucklesStyleLbl = QLabel("Color y Tipo de Marcador: ")
        self.bucklesColorCbo = color_combo_box()
        self.bucklesColorCbo.setCurrentIndex(0)
        self.bucklesMarkerStyleCbo = marker_combo_box()
        self.bucklesMarkerStyleCbo.setCurrentIndex(1)
        self.bucklesMarkerStyleCbo.textActivated[str].connect(self.selectMarker)

        self.bucklesStyleLayout = QHBoxLayout()
        self.bucklesStyleLayout.addWidget(self.bucklesStyleLbl)
        self.bucklesStyleLayout.addWidget(self.bucklesColorCbo)
        self.bucklesStyleLayout.addWidget(self.bucklesMarkerStyleCbo)

        self.gridLayout.addLayout(self.bucklesStyleLayout, row, 0, 1, 2)

    
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

        self.custom_value_layout = QVBoxLayout()

        self.custom_value_label = QLabel(CUSTOM_BUCKLES_LBL)

        self.custom_value_cb = QCheckBox()

        self.custom_value_cb.toggled.connect(self.show_custom_values)

        self.custom_value_label_layout = QHBoxLayout()

        self.custom_value_label_layout.addWidget(self.custom_value_label)

        self.custom_value_label_layout.addWidget(self.custom_value_cb)

        self.custom_value_layout.addLayout(self.custom_value_label_layout)

        self.custom_value_label2 = QLabel(VALUE_LBL)

        self.custom_value_layout.addWidget(self.custom_value_label2)

        self.custom_value_input_layout = QHBoxLayout()

        self.custom_value_color_cbo = color_combo_box()

        self.custom_value_tb = QLineEdit()

        self.custom_value_input_layout.addWidget(self.custom_value_tb,
                                                 alignment=Qt.AlignmentFlag.AlignLeft)

        self.custom_value_input_layout.addWidget(self.custom_value_color_cbo)

        self.custom_value_layout.addLayout(self.custom_value_input_layout)

        self.gridLayout.addLayout(self.custom_value_layout, row, 0, 1, 1)

        row += 1

        self.custom_value_vshale_layout = QHBoxLayout()

        self.vshale_qlabel = QLabel(VSHALE_LABEL)

        self.custom_value_vshale_layout.addWidget(self.vshale_qlabel)

        self.vshale_cbo = QComboBox()

        self.curve_selectors.append(self.vshale_cbo)

        self.custom_value_vshale_layout.addWidget(self.vshale_cbo)

        self.gridLayout.addLayout(self.custom_value_vshale_layout, row, 0, 1, 1)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        self.curveNameLbl = QLabel(CURVE_NAME_LABEL_2)

        self.curveNameQle = QLineEdit(self)

        self.curveNameLayout = QHBoxLayout()

        self.curveNameLayout \
            .addWidget(self.curveNameLbl,
                       alignment=Qt.AlignmentFlag.AlignLeft)

        self.curveNameLayout \
            .addWidget(self.curveNameQle,
                       alignment=Qt.AlignmentFlag.AlignRight)

        self.gridLayout.addLayout(self.curveNameLayout, row, 0)

        row += 1

        self.save_button = QPushButton(SAVE_CURVE_BUTTON)

        self.save_button \
            .clicked \
            .connect(self.save_curve)

        self.gridLayout.addWidget(self.save_button, row, 0)

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

        self.show_custom_values()

    def save_curve(self):
        curve_name = self.curveNameQle \
            .text()

        if len(curve_name) == 0:
            return AlertWindow(MISSING_CURVE_NAME)

        self.well \
            .wellModel \
            .append_curve(curve_name,
                          self.curve_to_save)

        self.update_tab(self.well,
                        self.use_data_in_curve_selectors)

        InformationWindow(SAVED_CURVE_LBL)

    def show_custom_values(self):
        disable_elements_with_component(self.custom_value_cb, [
            self.custom_value_tb,
            self.custom_value_color_cbo,
            self.custom_value_label2,
            self.vshale_cbo,
            self.vshale_qlabel,
            self.curveNameLbl,
            self.curveNameQle,
            self.save_button
        ])

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
        self.bucklesColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.bucklesMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if self.forceZAxisCb.isChecked():
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.bucklesColorCbo.setEnabled(True)


    def forceZAxis(self, state):        
        self.bucklesColorCbo.setEnabled(False)
        self.forceZAxisCb.setEnabled(False)
        self.forceZAxisColormapCbo.setEnabled(False)
        self.zAxisLbl.setEnabled(False)
        self.zAxisCbo.setEnabled(False)
        self.forceDepthZCb.setEnabled(False)
        if self.bucklesMarkerStyleCbo.currentText() != LINE_MARKER_CONSTANTS["NONE"]:
            self.forceZAxisCb.setEnabled(True)
            if state != 0:
                self.forceZAxisColormapCbo.setEnabled(True)
                self.forceDepthZCb.setEnabled(True)
                self.zAxisLbl.setEnabled(not self.forceDepthZCb.isChecked())
                self.zAxisCbo.setEnabled(not self.forceDepthZCb.isChecked())
            else:
                self.bucklesColorCbo.setEnabled(True)

    def preview(self):
        if not super().preview():
            return

        return loading_pop_up(LOADING_LBL, self._preview)

    def _preview(self):
        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))

        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        config_aux = get_buckles()

        y_title = self.well.wellModel.get_label_for(self.swCbo.currentText(), "SW")

        x_title = self.well.wellModel.get_label_for(self.phieCbo.currentText(), "PHIe")

        x_axis = self.well.wellModel.get_partial_ranged_df_curve(self.phieCbo.currentText(), minDepth, maxDepth, "", "")
        y_axis = self.well.wellModel.get_partial_ranged_df_curve(self.swCbo.currentText(), minDepth, maxDepth, "", "")

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
            'title': 'Buckles',
            'x_axis_title': x_title,
            'y_axis_title': y_title,
            'flex_size': 6,
            'invert_x': False,
            'invert_y': False,
            'log_x': False,
            'log_y': False,
            'scatter_groups': [
                {       
                    'x_axis': x_axis,
                    'y_axis': y_axis,
                    'marker': self.bucklesMarkerStyleCbo.currentText(),
                    'scatter_name': "POZO: " + self.well.wellModel.get_name(),
                    'fixed_color': self.bucklesColorCbo.currentText(),
                    'has_z_axis': self.forceZAxisCb.isChecked(),
                    'z_axis': z_axis,
                    'z_axis_colormap': self.forceZAxisColormapCbo.currentText(),
                    'z_axis_title': "Profundidad" if self.forceDepthZCb.isChecked() else self.zAxisCbo.currentText(),
                }
            ],
            'line_groups': []
        }

        color_cbo = color_combo_box()
        
        for i in range(len(config_aux['buckles'])):
            config['line_groups'].append(
                {
                    'x_axis': config_aux['buckles'][i]['x'],
                    'y_axis': config_aux['buckles'][i]['y'],
                    'color': color_cbo.itemText(i),
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"],
                    'line_name': config_aux['buckles'][i]['name']
                }
            )

        if self.custom_value_cb.isChecked():
            if not is_positive_number(self.custom_value_tb.text()):
                return get_positive_value_error_alert(self.custom_value_tb.text())

            custom_value = float(self.custom_value_tb.text())

            config['line_groups'].append(
                {
                    'x_axis': BUCKLES_BASE_X,
                    'y_axis': custom_value / np.array(BUCKLES_BASE_X),
                    'color': self.custom_value_color_cbo.currentText(),
                    'line': LINE_TYPE_CONSTANTS["SOLID_LINE"],
                    'line_name': f"{BUCKLES_PREFIX_LBL} {custom_value}"
                }
            )

            kbuck = custom_value

            vshale = self.well.wellModel.get_partial_ranged_df_curve(self.vshale_cbo.currentText(), minDepth, maxDepth, "", "")

            sw = self.well.wellModel.get_partial_ranged_df_curve(self.swCbo.currentText(), minDepth, maxDepth, "", "")

            phie = self.well.wellModel.get_partial_ranged_df_curve(self.phieCbo.currentText(), minDepth, maxDepth, "", "")

            self.curve_to_save = get_swirr_buckles(sw, kbuck, phie, vshale)

            self.well.graphicWindow.add_curve({
                'tab_name': SWIRR_BUCKLES_DISPLAY_NAME,

                'track_name': SWIRR_BUCKLES_DISPLAY_NAME,

                'curve_name': SWIRR_BUCKLES_DISPLAY_NAME,

                'x_axis': self.curve_to_save,

                'y_axis': self.well.wellModel.get_depth_curve(),

                "x_label": SWIRR_BUCKLES_TAB_NAME,

                "y_label": self.get_y_label()
            })

            self.well.graphicWindow.draw_tracks(SWIRR_BUCKLES_DISPLAY_NAME)

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])

    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return

        self.swCbo.setCurrentIndex(0)

        self.phieCbo.setCurrentIndex(0)
