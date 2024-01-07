"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QComboBox, QLabel, QHBoxLayout, QLineEdit,
                             QCheckBox)

from constants import permeability_constants

from constants.LITHOLOGY_CONSTANTS import VSHALE_LABEL

from constants.permeability_constants import (RESISTIVITY_HYDROCARBON_LBL, RESISTIVITY_SWIRR_LBL,
                                              CONSTANT_1_C_COATES_DUM, CONSTANT_2_C_COATES_DUM,
                                              CONSTANT_3_C_COATES_DUM, CONSTANT_1_W_COATES_DUM,
                                              CONSTANT_2_W_COATES_DUM, CONSTANT_3_W_COATES_DUM,
                                              ERROR_MSG_COATES_DUM_CONSTANTS, CONSTANT_1_C_DEFAULT,
                                              CONSTANT_2_C_DEFAULT, CONSTANT_3_C_DEFAULT, CONSTANT_1_W_DEFAULT,
                                              CONSTANT_2_W_DEFAULT, CONSTANT_3_W_DEFAULT, LOG_LABEL, K_LBL,
                                              A_CONSTANT_LBL, RSHALE_LBL, A_DEFAULT_VALUE, SW_LBL, MD_LBL)

from constants.porosity_constants import EFFECTIVE_POROSITY_CURVE

from services.permeability_service import get_coates_and_dumanoir

from services.tools.string_service import is_number

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections

from ui.popUps.alertWindow import AlertWindow

from ui.style.StyleCombos import color_combo_box, line_combo_box, marker_combo_box


class PermeabilityCoatesAndDumanoir(QWidgetWithSections):
    def __init__(self):
        super().__init__(permeability_constants.PERMEABILITY_COATES_DUMANOIR)

        self.init_ui(permeability_constants.PERMEABILITY_COATES_DUMANOIR)

    def init_ui(self,
                name):
        self.curves_section()

        self.constants_section()

        super().init_ui(name)

        self.numeric_inputs.extend([self.constant_1_w_textbox, self.constant_2_w_textbox, self.constant_3_w_textbox,
                                    self.constant_1_c_textbox, self.constant_2_c_textbox, self.constant_3_c_textbox,
                                    self.a_constant_tb])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.curve_to_save_marker, self.curve_to_save_line,
             self.curve_to_save_color, self.log_checkbox, self.constant_3_w_textbox, self.constant_2_w_textbox,
             self.constant_1_w_textbox, self.constant_3_c_textbox, self.constant_2_c_textbox,
             self.constant_1_c_textbox, self.a_constant_tb, self.rshale_cbo, self.vshale_cbo])

    def curve_to_save_style_section(self,
                                    section_header):
        self.curve_to_save_style_lbl = QLabel(section_header)

        self.curve_to_save_color = color_combo_box()

        self.curve_to_save_line = line_combo_box()

        self.curve_to_save_marker = marker_combo_box()

        self.add_widget_to_layout(self.curve_to_save_style_lbl)

        self.curve_to_save_layout = QHBoxLayout()

        self.curve_to_save_layout.addWidget(self.curve_to_save_color)

        self.curve_to_save_layout.addWidget(self.curve_to_save_line)

        self.curve_to_save_layout.addWidget(self.curve_to_save_marker)

        self.add_layout_to_layout(self.curve_to_save_layout)

        self.add_blank_line()

        self.log_label = QLabel(LOG_LABEL)

        self.log_checkbox = QCheckBox()

        self.log_layout = QHBoxLayout()

        self.log_layout.addWidget(self.log_label)

        self.log_layout.addWidget(self.log_checkbox)

        self.add_layout_to_layout(self.log_layout)

        self.add_blank_line()

    def curves_section(self):
        self.first_line_layout = QHBoxLayout()

        self.porosity_lbl = QLabel(EFFECTIVE_POROSITY_CURVE)

        self.resistivity_lbl = QLabel(RESISTIVITY_SWIRR_LBL)

        self.first_line_layout.addWidget(self.porosity_lbl)

        self.first_line_layout.addWidget(self.resistivity_lbl)

        self.add_layout_to_layout(self.first_line_layout)

        self.second_line_layout = QHBoxLayout()

        self.porosity_cbo = QComboBox()

        self.resistivity_cbo = QComboBox()

        self.second_line_layout.addWidget(self.porosity_cbo)

        self.second_line_layout.addWidget(self.resistivity_cbo)

        self.add_layout_to_layout(self.second_line_layout)

        self.add_blank_line()

        self.resistivity_h_lbl = QLabel(RESISTIVITY_HYDROCARBON_LBL)

        self.swirr_lbl = QLabel(SW_LBL)

        self.third_line_layout = QHBoxLayout()

        self.third_line_layout.addWidget(self.resistivity_h_lbl)

        self.third_line_layout.addWidget(self.swirr_lbl)

        self.add_layout_to_layout(self.third_line_layout)

        self.fourth_line_layout = QHBoxLayout()

        self.resistivity_h_cbo = QComboBox()

        self.swirr_cbo = QComboBox()

        self.fourth_line_layout.addWidget(self.resistivity_h_cbo)

        self.fourth_line_layout.addWidget(self.swirr_cbo)

        self.add_layout_to_layout(self.fourth_line_layout)

        self.add_blank_line()

        self.curve_selectors \
            .extend([self.porosity_cbo,
                     self.resistivity_h_cbo,
                     self.swirr_cbo,
                     self.resistivity_cbo])

    def constants_section(self):
        self.line_5_layout = QHBoxLayout()

        self.constant_1_c_lbl = QLabel(CONSTANT_1_C_COATES_DUM)

        self.constant_2_c_lbl = QLabel(CONSTANT_2_C_COATES_DUM)

        self.constant_3_c_lbl = QLabel(CONSTANT_3_C_COATES_DUM)

        self.line_5_layout.addWidget(self.constant_1_c_lbl)

        self.line_5_layout.addWidget(self.constant_2_c_lbl)

        self.line_5_layout.addWidget(self.constant_3_c_lbl)

        self.add_layout_to_layout(self.line_5_layout)

        self.line_6_layout = QHBoxLayout()

        self.constant_1_c_textbox = QLineEdit()

        self.constant_2_c_textbox = QLineEdit()

        self.constant_3_c_textbox = QLineEdit()

        self.constant_1_c_textbox.setText(CONSTANT_1_C_DEFAULT)

        self.constant_2_c_textbox.setText(CONSTANT_2_C_DEFAULT)

        self.constant_3_c_textbox.setText(CONSTANT_3_C_DEFAULT)

        self.line_6_layout.addWidget(self.constant_1_c_textbox)

        self.line_6_layout.addWidget(self.constant_2_c_textbox)

        self.line_6_layout.addWidget(self.constant_3_c_textbox)

        self.add_layout_to_layout(self.line_6_layout)

        self.add_blank_line()

        self.line_7_layout = QHBoxLayout()

        self.constant_1_w_lbl = QLabel(CONSTANT_1_W_COATES_DUM)

        self.constant_2_w_lbl = QLabel(CONSTANT_2_W_COATES_DUM)

        self.constant_3_w_lbl = QLabel(CONSTANT_3_W_COATES_DUM)

        self.line_7_layout.addWidget(self.constant_1_w_lbl)

        self.line_7_layout.addWidget(self.constant_2_w_lbl)

        self.line_7_layout.addWidget(self.constant_3_w_lbl)

        self.add_layout_to_layout(self.line_7_layout)

        self.line_8_layout = QHBoxLayout()

        self.constant_1_w_textbox = QLineEdit()

        self.constant_2_w_textbox = QLineEdit()

        self.constant_3_w_textbox = QLineEdit()

        self.constant_1_w_textbox.setText(CONSTANT_1_W_DEFAULT)

        self.constant_2_w_textbox.setText(CONSTANT_2_W_DEFAULT)

        self.constant_3_w_textbox.setText(CONSTANT_3_W_DEFAULT)

        self.line_8_layout.addWidget(self.constant_1_w_textbox)

        self.line_8_layout.addWidget(self.constant_2_w_textbox)

        self.line_8_layout.addWidget(self.constant_3_w_textbox)

        self.add_layout_to_layout(self.line_8_layout)

        self.line_9_layout = QHBoxLayout()

        self.a_constant_lbl = QLabel(A_CONSTANT_LBL)

        self.line_9_layout.addWidget(self.a_constant_lbl)

        self.add_layout_to_layout(self.line_9_layout)

        self.line_10_layout = QHBoxLayout()

        self.a_constant_tb = QLineEdit(A_DEFAULT_VALUE)

        self.line_10_layout.addWidget(self.a_constant_tb,
                                      alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_layout_to_layout(self.line_10_layout)

        self.line_11_layout = QHBoxLayout()

        self.vshale_lbl = QLabel(VSHALE_LABEL)

        self.rshale_lbl = QLabel(RSHALE_LBL)

        self.line_11_layout.addWidget(self.vshale_lbl)

        self.line_11_layout.addWidget(self.rshale_lbl)

        self.add_layout_to_layout(self.line_11_layout)

        self.line_12_layout = QHBoxLayout()

        self.vshale_cbo = QComboBox()

        self.rshale_cbo = QComboBox()

        self.line_12_layout.addWidget(self.vshale_cbo)

        self.line_12_layout.addWidget(self.rshale_cbo)

        self.add_layout_to_layout(self.line_12_layout)

        self.curve_selectors.extend([self.vshale_cbo, self.rshale_cbo])

        self.add_blank_line()

    def preview(self):
        if not super().preview():
            return

        graphic_window = self.well.graphicWindow

        well_model = self.well \
            .wellModel

        const_1_w = self.constant_1_w_textbox.text()

        const_2_w = self.constant_2_w_textbox.text()

        const_3_w = self.constant_3_w_textbox.text()

        const_1_c = self.constant_1_c_textbox.text()

        const_2_c = self.constant_2_c_textbox.text()

        const_3_c = self.constant_3_c_textbox.text()

        a = self.a_constant_tb.text()

        if not is_number(const_1_w) or not is_number(const_2_w) or not is_number(const_3_w) \
            or not is_number(const_1_c) or not is_number(const_2_c) or not is_number(const_3_c) \
            or not is_number(a):
            AlertWindow(ERROR_MSG_COATES_DUM_CONSTANTS)

            return

        porosity = well_model.get_partial_curve(self.porosity_cbo
                                                .currentText(),
                                                self.depth_curve_min,
                                                self.depth_curve_max,
                                                to_list=False)

        resistiviy = well_model.get_partial_curve(self.resistivity_cbo
                                                  .currentText(),
                                                  self.depth_curve_min,
                                                  self.depth_curve_max,
                                                  to_list=False)

        resistiviy_h = well_model.get_partial_curve(self.resistivity_h_cbo
                                                    .currentText(),
                                                    self.depth_curve_min,
                                                    self.depth_curve_max,
                                                    to_list=False)

        swirr = well_model.get_partial_curve(self.swirr_cbo
                                             .currentText(),
                                             self.depth_curve_min,
                                             self.depth_curve_max,
                                             to_list=False)

        vshale = self.get_partial_curve(self.vshale_cbo.currentText())

        rshale = self.get_partial_curve(self.rshale_cbo.currentText())

        data_config = {
            "porosity": porosity,
            "resistivity_hydrocarbon": resistiviy_h,
            "swirr": swirr,
            "a": float(a),
            "vshale": vshale,
            "rshale": rshale,
            "resistivity": resistiviy,
            "w_constants": [float(const_1_w), float(const_2_w), float(const_3_w)],
            "c_constants": [float(const_1_c), float(const_2_c), float(const_3_c)]
        }

        self.curve_to_save = get_coates_and_dumanoir(data_config)

        self.unit_to_save = MD_LBL

        x_label = K_LBL

        self.add_curve_with_y_label({
            'tab_name': permeability_constants.PERMEABILITY_COATES_DUMANOIR,

            'track_name': permeability_constants.COATES_AND_DUMANOIR_TRACK_NAME,

            'curve_name': permeability_constants.COATES_AND_DUMANOIR_TRACK_NAME,

            'add_axis': True,

            'x_axis': self.curve_to_save,

            'y_axis': self.depth_curve,

            'color': self.curve_to_save_color.currentText(),

            'line_style': self.curve_to_save_line.currentText(),

            'line_marker': self.curve_to_save_marker.currentText(),

            "x_label": x_label,

            "y_label": self.get_y_label(),

            'line_width': 1,

            "is_log": self.log_checkbox.isChecked()
        })

        graphic_window.draw_tracks(permeability_constants.PERMEABILITY_COATES_DUMANOIR)
