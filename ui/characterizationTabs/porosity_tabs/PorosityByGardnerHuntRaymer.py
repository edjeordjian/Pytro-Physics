"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QLabel, QComboBox, QHBoxLayout, QLineEdit, QVBoxLayout, QCheckBox

from constants import MENU_CONSTANTS

from constants.MENU_CONSTANTS import USE_CONSTANT_DT_MATRIX_VALUE

from constants.messages_constants import MISSING_CURVES_OR_VALUES, INVALID_NUMERIC_INPUT

from constants.porosity_constants import (DELTA_T_MATRIX_CURVE, POROSITY_STYLE_LBL, DT_LOG_CURVE_LBL,
                                          TOTAL_POROSITY_GARDNER_HUNT_RAYMER_NAME, POROSITY_CURVE, ADJUST_RANGE_LBL,
                                          ADJUSTED_MIN_LBL, DEFAULT_ADJUSTED_MIN_LBL, ADJUSTED_MAX_LBL,
                                          DEFAULT_ADJUSTED_MAX_LBL)

from constants.tab_constants import TOTAL_POROSITY_TAB_NAME

from services.porosity_service import get_porosity_by_gardner_hunt_raymer

from services.tools.string_service import are_numbers

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections

from ui.popUps.alertWindow import AlertWindow

from ui.style.StyleCombos import color_combo_box, line_combo_box, marker_combo_box

from ui.visual_components.combo_handler import disable_elements_with_component


class PorosityByGardnerHuntRaymer(QWidgetWithSections):
    def __init__(self):
        self.use_data_in_curve_selectors = False

        super().__init__(TOTAL_POROSITY_GARDNER_HUNT_RAYMER_NAME)

        self.initUI()

    def initUI(self):
        self.dt_log_section()

        self.dt_matrix_section()

        self.porosity_style_config_section(f"{POROSITY_STYLE_LBL} {TOTAL_POROSITY_TAB_NAME}")

        self.add_blank_line()

        self.choose_range_section()

        self.add_blank_line()

        self.depth_section()

        self.save_and_draw_section()

        self.numeric_inputs.extend([self.delta_t_matrix_constant_textbox,
                                    self.x_adjusted_min_textbox,
                                    self.x_adjusted_max_textbox])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
                                         self.dt_log_cbo, self.delta_t_matrix_cbo, self.delta_t_matrix_constant_textbox,
                                         self.porosity_color, self.porosity_line, self.porosity_marker,
                                         self.customMinDepthQle, self.customMaxDepthQle,
                                         self.x_adjusted_min_textbox, self.x_adjusted_max_textbox, self.x_adjusted_cb])

    def dt_log_section(self):
        self.dt_log_lbl = QLabel(DT_LOG_CURVE_LBL)

        self.dt_log_cbo = QComboBox(self)

        self.dt_log_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.curve_selectors.append(self.dt_log_cbo)

        self.curveLayout = QHBoxLayout()

        self.curveLayout \
            .addWidget(self.dt_log_lbl)

        self.curveLayout \
            .addWidget(self.dt_log_cbo)

        self.add_layout_to_layout(self.curveLayout,
                                  column=0)

    def dt_matrix_section(self):
        self.delta_t_matrix_lbl = QLabel(DELTA_T_MATRIX_CURVE)

        self.delta_t_matrix_cbo = QComboBox(self)

        self.delta_t_matrix_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.curve_selectors \
            .append(self.delta_t_matrix_cbo)

        self.delta_t_matrix_layout = QHBoxLayout()

        self.delta_t_matrix_constant_lbl = QLabel(USE_CONSTANT_DT_MATRIX_VALUE)

        self.delta_t_matrix_constant_textbox = QLineEdit()

        self.delta_t_matrix_layout \
            .addWidget(self.delta_t_matrix_lbl)

        self.delta_t_matrix_layout \
            .addWidget(self.delta_t_matrix_cbo)

        self.add_layout_to_layout(self.delta_t_matrix_layout,
                                  column=0,
                                  next_line=False)

        self.add_widget_to_layout(self.delta_t_matrix_constant_lbl,
                                  column=1,
                                  next_line=False)

        self.add_widget_to_layout(self.delta_t_matrix_constant_textbox,
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

        dt_log = self.dt_log_cbo \
            .currentText()

        dt_matrix = self.get_constant_curve_data(self.delta_t_matrix_cbo,
                                                 self.delta_t_matrix_constant_textbox,
                                                 DELTA_T_MATRIX_CURVE)

        if dt_log is None:
            return AlertWindow(f"{MISSING_CURVES_OR_VALUES} {TOTAL_POROSITY_TAB_NAME}")

        dt_log_data = self.well \
            .wellModel \
            .get_partial_curve(dt_log,
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
            self.curve_to_save = get_porosity_by_gardner_hunt_raymer(dt_log_data,
                                                                     dt_matrix,
                                                                     forced_min,
                                                                     forced_max)
        else:
            self.curve_to_save = get_porosity_by_gardner_hunt_raymer(dt_log_data,
                                                                     dt_matrix)

        if self.curve_to_save is None:
            return

        total_porosity_config = {
            'tab_name': TOTAL_POROSITY_GARDNER_HUNT_RAYMER_NAME,

            'track_name': TOTAL_POROSITY_GARDNER_HUNT_RAYMER_NAME,

            'curve_name': TOTAL_POROSITY_GARDNER_HUNT_RAYMER_NAME,

            'x_axis': self.curve_to_save,

            'y_axis': self.well.wellModel.get_depth_curve(),

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
            .draw_tracks(TOTAL_POROSITY_GARDNER_HUNT_RAYMER_NAME)
