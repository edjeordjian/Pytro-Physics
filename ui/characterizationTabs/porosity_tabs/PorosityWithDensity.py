"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QLabel, QComboBox, QHBoxLayout, QLineEdit, QVBoxLayout, QCheckBox

from constants import MENU_CONSTANTS

from constants.MENU_CONSTANTS import USE_CONSTANT_VALUE

from constants.messages_constants import MISSING_CURVES, INVALID_NUMERIC_INPUT

from constants.porosity_constants import (RHO_MATRIX_CURVE, POROSITY_STYLE_LBL, POROSITY_DENSITY_CURVE,
                                          POROSITY_LOG_DENSITY_CURVE, TOTAL_POROSITY_BY_DENSITY_NAME, POROSITY_CURVE,
                                          ADJUST_RANGE_LBL, ADJUSTED_MIN_LBL, DEFAULT_ADJUSTED_MIN_LBL,
                                          ADJUSTED_MAX_LBL, DEFAULT_ADJUSTED_MAX_LBL)

from constants.tab_constants import TOTAL_POROSITY_TAB_NAME

from services.porosity_service import get_porosity_with_density

from services.tools.string_service import are_numbers

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections

from ui.popUps.alertWindow import AlertWindow

from ui.style.StyleCombos import color_combo_box, line_combo_box, marker_combo_box

from constants.LETTERS import RHO

from ui.visual_components.combo_handler import disable_elements_with_component


class PorosityWithDensity(QWidgetWithSections):
    def __init__(self):
        self.use_data_in_curve_selectors = False

        super().__init__(TOTAL_POROSITY_BY_DENSITY_NAME)

        self.initUI()

    def initUI(self):
        self.density_curve_section()

        self.density_log_curve_section()

        self.rho_matrix_section()

        self.porosity_style_config_section(f"{POROSITY_STYLE_LBL} {TOTAL_POROSITY_TAB_NAME}")

        self.add_blank_line()

        self.choose_range_section()

        self.add_blank_line()

        self.depth_section()

        self.save_and_draw_section()

        self.numeric_inputs.extend([self.rho_matrix_constant_textbox, self.rho_log_constant_textbox,
                                   self.x_adjusted_min_textbox, self.x_adjusted_max_textbox])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
                                         self.density_cbo, self.density_log_cbo, self.rho_matrix_cbo,
                                         self.rho_matrix_constant_textbox, self.porosity_color, self.porosity_line,
                                         self.porosity_marker, self.customMinDepthQle, self.customMaxDepthQle,
                                         self.rho_log_constant_textbox, self.x_adjusted_min_textbox,
                                         self.x_adjusted_max_textbox, self.x_adjusted_cb])

    def density_curve_section(self):
        self.density_lbl = QLabel(POROSITY_DENSITY_CURVE)

        self.density_cbo = QComboBox(self)

        self.density_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.curve_selectors.append(self.density_cbo)

        self.curveLayout = QHBoxLayout()

        self.curveLayout \
            .addWidget(self.density_lbl)

        self.curveLayout \
            .addWidget(self.density_cbo)

        self.add_layout_to_layout(self.curveLayout,
                                  column=0)

    def density_log_curve_section(self):
        self.density_log_lbl = QLabel(POROSITY_LOG_DENSITY_CURVE)

        self.density_log_cbo = QComboBox(self)

        self.density_log_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.curve_selectors.append(self.density_log_cbo)

        self.curve_log_layout = QHBoxLayout()

        self.curve_log_layout \
            .addWidget(self.density_log_lbl)

        self.curve_log_layout \
            .addWidget(self.density_log_cbo)

        self.add_layout_to_layout(self.curve_log_layout,
                                  column=0,
                                  next_line=False)

        self.rho_log_constant_lbl = QLabel(f"{USE_CONSTANT_VALUE}")

        self.rho_log_constant_textbox = QLineEdit()

        self.add_widget_to_layout(self.rho_log_constant_lbl,
                                  column=1,
                                  next_line=False)

        self.add_widget_to_layout(self.rho_log_constant_textbox,
                                  column=2)

    def rho_matrix_section(self):
        self.rho_matrix_lbl = QLabel(RHO_MATRIX_CURVE)

        self.rho_matrix_cbo = QComboBox(self)

        self.rho_matrix_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.curve_selectors \
            .append(self.rho_matrix_cbo)

        self.rho_matrix_layout = QHBoxLayout()

        self.rho_matrix_layout \
            .addWidget(self.rho_matrix_lbl)

        self.rho_matrix_layout \
            .addWidget(self.rho_matrix_cbo)

        self.rho_matrix_constant_lbl = QLabel(f"{USE_CONSTANT_VALUE}")

        self.rho_matrix_constant_textbox = QLineEdit()

        self.add_layout_to_layout(self.rho_matrix_layout,
                                  column=0,
                                  next_line=False)

        self.add_widget_to_layout(self.rho_matrix_constant_lbl,
                                  column=1,
                                  next_line=False)

        self.add_widget_to_layout(self.rho_matrix_constant_textbox,
                                  column=2)

    def choose_range_section(self):
        self.adjusted_layout = QVBoxLayout()

        self.adjust_range_layout = QHBoxLayout()

        self.x_adjusted_label = QLabel(ADJUST_RANGE_LBL)

        self.x_adjusted_cb = QCheckBox()

        self.x_adjusted_cb.toggled.connect(self.show_adjusted_values)

        self.x_adjusted_cb.setChecked(False)

        self.adjust_range_layout.addWidget(self.x_adjusted_label)

        self.adjust_range_layout.addWidget(self.x_adjusted_cb)

        self.adjusted_layout.addLayout(self.adjust_range_layout)

        self.x_min_layout = QHBoxLayout()

        self.x_adjusted_min_label = QLabel(ADJUSTED_MIN_LBL)

        self.x_adjusted_min_textbox = QLineEdit(DEFAULT_ADJUSTED_MIN_LBL)

        self.x_min_layout.addWidget(self.x_adjusted_min_label)

        self.x_min_layout.addWidget(self.x_adjusted_min_textbox,
                                    alignment=Qt.AlignmentFlag.AlignLeft)

        self.adjusted_layout.addLayout(self.x_min_layout)

        self.x_max_layout = QHBoxLayout()

        self.x_adjusted_max_label = QLabel(ADJUSTED_MAX_LBL)

        self.x_adjusted_max_textbox = QLineEdit(DEFAULT_ADJUSTED_MAX_LBL)

        self.x_max_layout.addWidget(self.x_adjusted_max_label)

        self.x_max_layout.addWidget(self.x_adjusted_max_textbox,
                                    alignment=Qt.AlignmentFlag.AlignLeft)

        self.adjusted_layout.addLayout(self.x_max_layout)

        self.add_layout_to_layout(self.adjusted_layout)

        self.show_adjusted_values()

    def show_adjusted_values(self):
        disable_elements_with_component(self.x_adjusted_cb, [
            self.x_adjusted_min_textbox,
            self.x_adjusted_max_textbox,
            self.x_adjusted_min_label,
            self.x_adjusted_max_label
        ])

    def porosity_style_config_section(self,
                                      section_header):
        self.porosity_style_lbl = QLabel(section_header)

        self.porosity_color = color_combo_box()

        self.porosity_line = line_combo_box()

        self.porosity_marker = marker_combo_box()

        self.add_blank_line()

        self.add_widget_to_layout(self.porosity_style_lbl)

        self.add_widget_to_layout(self.porosity_color,
                                  column=0,
                                  next_line=False)

        self.add_widget_to_layout(self.porosity_line,
                                  column=1,
                                  next_line=False)

        self.add_widget_to_layout(self.porosity_marker,
                                  column=2)

    def preview(self):
        if not super().preview():
            return

        density = self.density_cbo \
            .currentText()

        density_log = self.get_constant_curve_data(self.density_log_cbo,
                                                   self.rho_log_constant_textbox,
                                                   "densidad de fluído")

        rho_matrix = self.get_constant_curve_data(self.rho_matrix_cbo,
                                                  self.rho_matrix_constant_textbox,
                                                  "densidad de matriz")

        if density is None or density_log is None:
            return AlertWindow(f"{MISSING_CURVES} {TOTAL_POROSITY_TAB_NAME}")

        density_curve_data = self.well \
            .wellModel \
            .get_partial_curve(density,
                               self.depth_curve_min,
                               self.depth_curve_max,
                               to_list=False)

        x_adjusted_min = self.x_adjusted_min_textbox.text()

        x_adjusted_max = self.x_adjusted_max_textbox.text()

        if not are_numbers([x_adjusted_min, x_adjusted_max]):
            return AlertWindow(INVALID_NUMERIC_INPUT)

        forced_min = float(x_adjusted_min) if len(x_adjusted_min) != 0 else 0

        forced_max = float(x_adjusted_max) if len(x_adjusted_max) != 0 else 0

        if self.x_adjusted_cb.isChecked():
            self.curve_to_save = get_porosity_with_density(density_curve_data,
                                                           density_log,
                                                           rho_matrix,
                                                           forced_min,
                                                           forced_max)
        else:
            self.curve_to_save = get_porosity_with_density(density_curve_data,
                                                           density_log,
                                                           rho_matrix)



        if self.curve_to_save is None:
            return

        total_porosity_config = {
            'tab_name': TOTAL_POROSITY_BY_DENSITY_NAME,

            'track_name': TOTAL_POROSITY_BY_DENSITY_NAME,

            'curve_name': TOTAL_POROSITY_TAB_NAME,

            'x_axis': self.curve_to_save,

            'y_axis': self.depth_curve,

            "x_label": POROSITY_CURVE,

            "y_label": self.get_y_label(),

            'color': self.porosity_color.currentText(),

            'line_style': self.porosity_line.currentText(),

            'line_marker': self.porosity_marker.currentText(),

            'line_width': 1,

            'add_axis': True
        }

        self.add_curve_with_y_label(total_porosity_config)

        self.well \
            .graphicWindow \
            .draw_tracks(TOTAL_POROSITY_BY_DENSITY_NAME)
