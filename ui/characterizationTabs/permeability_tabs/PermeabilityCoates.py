"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QComboBox, QLabel, QLineEdit

from constants import permeability_constants

from constants.permeability_constants import INVALID_CONSTANT, CONSTANT_LBL, DEFAULT_COATES_CONSTANT, K_LBL, MD_LBL

from constants.porosity_constants import EFFECTIVE_POROSITY_CURVE

from constants.swirr_constants import SWIRR_TAB_NAME

from services.permeability_service import get_coates_permeability

from services.tools.string_service import is_number

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections

from ui.popUps.alertWindow import AlertWindow


class PermeabilityCoates(QWidgetWithSections):
    def __init__(self):
        super().__init__(permeability_constants.PERMEABILITY_COATES)

        self.init_ui(permeability_constants.PERMEABILITY_COATES)

    def init_ui(self,
                name):
        self.curves_section()

        super().init_ui(name)

        self.numeric_inputs.append(self.constant_textbox)

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.curve_to_save_marker, self.curve_to_save_line,
             self.curve_to_save_color, self.log_checkbox, self.constant_textbox])

    def curves_section(self):
        self.porosity_lbl = QLabel(EFFECTIVE_POROSITY_CURVE)

        self.add_widget_to_layout(self.porosity_lbl)

        self.porosity_cbo = QComboBox()

        self.add_widget_to_layout(self.porosity_cbo)

        self.add_blank_line()

        self.swirr_lbl = QLabel(SWIRR_TAB_NAME)

        self.add_widget_to_layout(self.swirr_lbl)

        self.swirr_cbo = QComboBox()

        self.curve_selectors \
            .extend([self.porosity_cbo,
                     self.swirr_cbo])

        self.add_widget_to_layout(self.swirr_cbo)

        self.add_blank_line()

        self.constant_lbl = QLabel(CONSTANT_LBL)

        self.add_widget_to_layout(self.constant_lbl)

        self.constant_textbox = QLineEdit(DEFAULT_COATES_CONSTANT)

        self.add_widget_to_layout(self.constant_textbox,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_blank_line()

    def preview(self):
        if not super().preview():
            return

        constant = self.constant_textbox \
            .text()

        if not is_number(constant):
            AlertWindow(INVALID_CONSTANT)

        graphic_window = self.well.graphicWindow

        porosity = self.well \
            .wellModel \
            .get_partial_curve(self.porosity_cbo
                               .currentText(),
                               self.depth_curve_min,
                               self.depth_curve_max,
                               to_list=False)

        swirr = self.well \
            .wellModel \
            .get_partial_curve(self.swirr_cbo
                               .currentText(),
                               self.depth_curve_min,
                               self.depth_curve_max,
                               to_list=False)

        self.curve_to_save = get_coates_permeability(porosity,
                                                     swirr,
                                                     float(constant))

        self.unit_to_save = MD_LBL

        x_label = K_LBL

        self.add_curve_with_y_label({
            'tab_name': permeability_constants.PERMEABILITY_COATES,

            'track_name': permeability_constants.COATES_TRACK_NAME,

            'curve_name': permeability_constants.COATES_TRACK_NAME,

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

        graphic_window.draw_tracks(permeability_constants.PERMEABILITY_COATES)
