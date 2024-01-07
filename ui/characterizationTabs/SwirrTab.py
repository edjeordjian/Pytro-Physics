"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from functools import reduce

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QLabel, QComboBox, QHBoxLayout

from constants import MENU_CONSTANTS

from constants.LITHOLOGY_CONSTANTS import POROSITY_NAME

from constants.messages_constants import MISSING_CURVES

from constants.permeability_constants import INVALID_CONSTANT, CONSTANT_LBL

from constants.porosity_constants import POROSITY_STYLE_LBL, EFFECTIVE_POROSITY_TAB_NAME

from constants.swirr_constants import SWIRR_DISPLAY_NAME, PERMEABILITY_NAME, SWIRR_DEFAULT_CONSTANT, SWIRR_TAB_NAME

from services.constant_service import get_qle_group_name

from services.swirr_service import get_swirr_timur

from services.tools.string_service import is_positive_number, is_number

from ui.characterizationTabs.QWidgetWithWellGroups import QWidgetWithWellGroups

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.alerts import get_positive_value_error_alert

from ui.style.StyleCombos import color_combo_box, line_combo_box, marker_combo_box

from ui.visual_components.combo_handler import get_combo_text


class SwirrTab(QWidgetWithWellGroups):
    def __init__(self):
        self.use_data_in_curve_selectors = False

        super().__init__(SWIRR_DISPLAY_NAME)

        self.setLayout(self.gridLayout)

        self.initUI()

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
            self.swirr_color, self.swirr_line, self.swirr_marker, self.groups, self.groupsQle])

    def initUI(self):
        self.curves_section()

        self.swirr_style_config_section(f"{POROSITY_STYLE_LBL} {SWIRR_DISPLAY_NAME}")

        self.add_blank_line()

        self.depth_section()

        self.groups_section({
            CONSTANT_LBL: SWIRR_DEFAULT_CONSTANT
        })

        self.save_and_draw_section()

    def curves_section(self):
        self.density_lbl = QLabel(POROSITY_NAME)

        self.density_cbo = QComboBox(self)

        self.density_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.density_cbo \
            .textActivated[str] \
            .connect(self.curve_selected)

        self.curve_selectors.append(self.density_cbo)

        self.curveLayout = QHBoxLayout()

        self.curveLayout \
            .addWidget(self.density_lbl,
                       alignment=Qt.AlignmentFlag.AlignLeft)

        self.curveLayout \
            .addWidget(self.density_cbo)

        self.add_layout_to_layout(self.curveLayout,
                                  column=0)

        self.vshale_lbl = QLabel(PERMEABILITY_NAME)

        self.vshale_cbo = QComboBox(self)

        self.vshale_cbo.setPlaceholderText(MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.vshale_cbo \
            .textActivated[str] \
            .connect(self.curve_selected)

        self.curve_selectors.append(self.vshale_cbo)

        self.vshale_layout = QHBoxLayout()

        self.vshale_layout \
            .addWidget(self.vshale_lbl,
                       alignment=Qt.AlignmentFlag.AlignLeft)

        self.vshale_layout \
            .addWidget(self.vshale_cbo)

        self.add_layout_to_layout(self.vshale_layout,
                                  column=0)

        self.add_blank_line()

    def swirr_style_config_section(self,
                                   section_header):
        self.swirr_style_lbl = QLabel(section_header)

        self.swirr_color = color_combo_box()

        self.swirr_line = line_combo_box()

        self.swirr_marker = marker_combo_box()

        self.add_blank_line()

        self.add_widget_to_layout(self.swirr_style_lbl)

        self.add_widget_to_layout(self.swirr_color,
                                  column=0,
                                  next_line=False,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_widget_to_layout(self.swirr_line,
                                  column=1,
                                  next_line=False,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_widget_to_layout(self.swirr_marker,
                                  column=2,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

    def curve_selected(self):
        depth_curve = self.well \
            .wellModel \
            .get_depth_curve()

        for group in self.groups:
            group["Min Depth QLE"].setPlaceholderText(str(min(depth_curve)))

            group["Max Depth QLE"].setPlaceholderText(str(max(depth_curve)))

    def get_swirr(self,
                  porosity,
                  permeability):
        groups = []

        for group in self.groups:
            if group["Min Depth QLE"].isEnabled():
                min_depth_qle = get_combo_text(group["Min Depth QLE"])

                max_depth_qle = get_combo_text(group["Max Depth QLE"])

                if not is_positive_number(min_depth_qle):
                    get_positive_value_error_alert(min_depth_qle)

                    return None

                if not is_positive_number(max_depth_qle):
                    get_positive_value_error_alert(max_depth_qle)

                    return None

                porosity_curve_data = self.well \
                    .wellModel \
                    .get_partial_curve(
                        porosity,
                        min_depth_qle,
                        max_depth_qle,
                        False)

                permeability_curve_data = self.well \
                    .wellModel \
                    .get_partial_curve(
                        permeability,
                        min_depth_qle,
                        max_depth_qle,
                        False)

                constant = group[get_qle_group_name(CONSTANT_LBL)].text()

                if not is_number(constant):
                    AlertWindow(INVALID_CONSTANT)

                groups.append(get_swirr_timur(porosity_curve_data,
                                              permeability_curve_data,
                                              float(constant)))

        return reduce(self.well
                      .wellModel
                      .combine_curves,
                       groups)

    def preview(self):
        if not super().preview():
            return

        porosity = self.density_cbo \
            .currentText()

        permeability = self.vshale_cbo \
            .currentText()

        if porosity is None or permeability is None:
            return AlertWindow(f"{MISSING_CURVES} {EFFECTIVE_POROSITY_TAB_NAME}")

        self.curve_to_save = self.get_swirr(porosity,
                                            permeability)

        if self.curve_to_save is None:
            return

        config = {
            'tab_name': SWIRR_DISPLAY_NAME,

            'track_name': SWIRR_DISPLAY_NAME,

            'curve_name': SWIRR_DISPLAY_NAME,

            'x_axis': self.curve_to_save,

            'y_axis': self.well.wellModel
                .get_depth_curve(),

            "x_label": SWIRR_TAB_NAME,

            "y_label": self.get_y_label(),

            'color': self.swirr_color
                .currentText(),

            'line_style': self.swirr_line
                .currentText(),

            'line_marker': self.swirr_marker
                .currentText(),

            'line_width': 1
        }

        self.add_curve_with_y_label(config)

        self.well \
            .graphicWindow \
            .draw_tracks(SWIRR_DISPLAY_NAME)

    def update_tab(self, well=None, force_update=False):
        if force_update:
            return

        if not super().update_tab(well):
            return

        depth_curve = self.well.wellModel.get_depth_curve()

        if len(depth_curve) == 0:
            return

        self.window = self.well \
            .graphicWindow

        for group in self.groups:
            group["Min Depth QLE"].setPlaceholderText(str(min(depth_curve)))

            group["Max Depth QLE"].setPlaceholderText(str(max(depth_curve)))
