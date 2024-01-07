"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QLabel, QComboBox, QHBoxLayout, QLineEdit,
                             QGroupBox, QRadioButton)

from constants import MENU_CONSTANTS

from constants.messages_constants import MISSING_CONSTANTS

from constants.permeability_constants import INVALID_CONSTANT, INVALID_NUMERIC_CONSTANT

from constants.sw_constants import (RW_TAB_FULL_NAME, TEMPERATUE_LBL, TEMPERATURE_SCALAR_LBL, RESISTIVITY_SCALAR_LBL,
                                    FARENHEIT_LBL, RW_X_LBL, CELCIUS_LBL, OHM_M_LBL)

from services.sw_service import get_rw

from services.tools.string_service import is_number

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections

from ui.popUps.alertWindow import AlertWindow

from ui.style.StyleCombos import color_combo_box, line_combo_box, marker_combo_box


class RwTab(QWidgetWithSections):
    def __init__(self,
                 RW_TAB_NAME):
        self.use_data_in_curve_selectors = False

        super().__init__(RW_TAB_NAME)

        self.setLayout(self.gridLayout)

        self.initUI()

    def initUI(self):
        self.curves_section()

        self.rw_style_config_section(RW_TAB_FULL_NAME)

        self.add_blank_line()

        self.depth_section()

        self.save_and_draw_section()

        self.numeric_inputs.extend([
            self.temperature_scalar_textbox, self.rwc_scalar_textbox
        ])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
                                         self.rwc_scalar_textbox, self.celcius_rb, self.farenheit_rb,
                                         self.temperature_scalar_textbox, self.rw_line,
                                         self.rw_color, self.rw_marker,
                                         self.customMinDepthQle, self.customMaxDepthQle])

    def curves_section(self):
        self.curveLayout = QHBoxLayout()

        self.add_layout_to_layout(self.curveLayout,
                                  column=0)

        self.temperature_lbl = QLabel(TEMPERATUE_LBL)

        self.temperature_cbo = QComboBox(self)

        self.temperature_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.temperature_layout = QHBoxLayout()

        self.temperature_layout \
            .addWidget(self.temperature_lbl)

        self.temperature_layout \
            .addWidget(self.temperature_cbo)

        self.curve_selectors.extend([self.temperature_cbo])

        self.add_layout_to_layout(self.temperature_layout,
                                  next_line=False,
                                  column=0)

        self.temperature_unit_groupbox = QGroupBox()

        self.temperature_unit_layout = QHBoxLayout()

        self.farenheit_rb = QRadioButton(FARENHEIT_LBL)

        self.celcius_rb = QRadioButton(CELCIUS_LBL)

        self.celcius_rb.setChecked(True)

        self.temperature_unit_layout \
            .addWidget(self.celcius_rb,
                       alignment=Qt.AlignmentFlag.AlignLeft)

        self.temperature_unit_layout \
            .addWidget(self.farenheit_rb,
                       alignment=Qt.AlignmentFlag.AlignLeft)

        self.temperature_unit_groupbox.setLayout(self.temperature_unit_layout)

        self.add_widget_to_layout(self.temperature_unit_groupbox,
                                  column=1)

        self.rwc_scalar_layout = QHBoxLayout()

        self.rwc_scalar_lbl = QLabel(RESISTIVITY_SCALAR_LBL)

        self.rwc_scalar_layout.addWidget(self.rwc_scalar_lbl)

        self.rwc_scalar_textbox = QLineEdit()

        self.rwc_scalar_layout.addWidget(self.rwc_scalar_textbox)

        self.add_layout_to_layout(self.rwc_scalar_layout)

        self.temperature_scalar_layout = QHBoxLayout()

        self.temperature_scalar_lbl = QLabel(TEMPERATURE_SCALAR_LBL)

        self.temperature_scalar_textbox = QLineEdit()

        self.temperature_scalar_layout.addWidget(self.temperature_scalar_lbl)

        self.temperature_scalar_layout.addWidget(self.temperature_scalar_textbox)

        self.add_layout_to_layout(self.temperature_scalar_layout,
                                  next_line=False,
                                  column=0)

        self.temperature_scalar_unit_groupbox = QGroupBox()

        self.temperature_scalar_rb_layout = QHBoxLayout()

        self.farenheit_scalar_rb = QRadioButton(FARENHEIT_LBL)

        self.celcius_scalar_rb = QRadioButton(CELCIUS_LBL)

        self.celcius_scalar_rb.setChecked(True)

        self.temperature_scalar_rb_layout \
            .addWidget(self.celcius_scalar_rb,
                       alignment=Qt.AlignmentFlag.AlignLeft)

        self.temperature_scalar_rb_layout \
            .addWidget(self.farenheit_scalar_rb,
                       alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.temperature_scalar_unit_groupbox.setLayout(self.temperature_scalar_rb_layout)

        self.add_widget_to_layout(self.temperature_scalar_unit_groupbox,
                                  column=1)

        self.add_blank_line()

    def rw_style_config_section(self,
                                section_header):
        self.rw_style_lbl = QLabel(section_header)

        self.rw_color = color_combo_box()

        self.rw_line = line_combo_box()

        self.rw_marker = marker_combo_box()

        self.add_blank_line()

        self.add_widget_to_layout(self.rw_style_lbl)

        self.add_widget_to_layout(self.rw_color,
                                  column=0,
                                  next_line=False,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_widget_to_layout(self.rw_line,
                                  column=1,
                                  next_line=False,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_widget_to_layout(self.rw_marker,
                                  column=2,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

    def preview(self):
        if not super().preview():
            return

        temperature = self.temperature_cbo \
            .currentText()

        temperature_scalar = self.temperature_scalar_textbox.text()

        resistivity_scalar = self.rwc_scalar_textbox.text()

        if len(temperature_scalar) == 0 or len(resistivity_scalar) == 0:
            return AlertWindow(MISSING_CONSTANTS)

        if not is_number(temperature_scalar) or not is_number(resistivity_scalar):
            return AlertWindow(INVALID_NUMERIC_CONSTANT)

        temperature_curve_data = self.well \
            .wellModel \
            .get_partial_curve(temperature,
                               self.depth_curve_min,
                               self.depth_curve_max,
                               False)

        self.curve_to_save = get_rw(float(resistivity_scalar),
                                    float(temperature_scalar),
                                    temperature_curve_data,
                                    self.celcius_rb.isChecked(),
                                    self.celcius_scalar_rb.isChecked())

        self.unit_to_save = OHM_M_LBL

        rw_config = {
            'tab_name': RW_TAB_FULL_NAME,

            'track_name': RW_TAB_FULL_NAME,

            'curve_name': RW_TAB_FULL_NAME,

            'x_axis': self.curve_to_save,

            'y_axis': self.well.wellModel.get_depth_curve(),

            "x_label": RW_X_LBL,

            "y_label": self.get_y_label(),

            'color': self.rw_color.currentText(),

            'line_style': self.rw_line.currentText(),

            'line_marker': self.rw_marker.currentText(),

            'line_width': 1,

            'add_axis': True
        }

        self.add_curve_with_y_label(rw_config)

        self.well \
            .graphicWindow \
            .draw_tracks(RW_TAB_FULL_NAME)
