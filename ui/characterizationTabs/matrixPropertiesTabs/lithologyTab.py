"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import QTimer, Qt

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QRadioButton,
                             QGroupBox, QPushButton, QComboBox, QLineEdit,
                             QCheckBox)

import constants.VSHALE_MENU_CONSTANTS as VSHALE_MENU_CONSTANTS

from constants.LITHOLOGY_CONSTANTS import (RHO_B_LABEL, SONIC_LABEL, PROFILE_LABEL, VSHALE_LABEL,
                                           PEF_LABEL, NEUTRON_LABEL, LITOLOGIES_LABEL, POROSITY_NAME,
                                           SAVE_POROSITY_CURVE, SAVE_LITHOLOGY_CURVE, RHO_DSH_LBL, RHO_CARBON_LBL,
                                           RHO_COAL_DEFAULT_VALUE, RHO_ANHY_LBL, RHO_ANHY_DEFAULT_VALUE,
                                           RHO_DSH_DEFAULT_VALUE, DT_MATRIX_LBL, RHO_MATRIX_LBL, CURVE_NAME_LBL,
                                           SAVE_RHO_CURVE, SAVE_DT_CURVE)

from constants.general_constants import loading_pop_up_timeout_ms, PLEASE_WAIT_LBL, SAVED_CURVE_LBL

from constants.messages_constants import (MISSING_CURVE_NAME, MISSING_CURVE, CURVE_ALREADY_EXISTS_LBL,
                                          MISSING_CURVE_TO_SAVE)

from constants.pytrophysicsConstants import DEFAULT_LITHOLOGY_CONFIG, SEE_WINDOW_LBL

from constants.tab_constants import (MIN_DEPTH_LBL, MAX_DEPTH_LBL, DEPTH_LBL, ALL_FILE_LBL,
                                     CUSTOM_FILE_LBL)

from services.DTCO_service import get_DTCO_variables

from services.tools.json_service import are_similarl_json_lists

from services.tools.string_service import is_number

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell

from ui.popUps.LoadingWindow import LoadingWindow

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.informationWindow import InformationWindow

from ui.popUps.alerts import get_alert_from_label

from ui.style.LineColors import getColor

from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE

from ui.visual_components.combo_handler import update_cbos, add_none_option, disable_elements_with_component

from ui.visual_components.constant_curves_handler import add_bottom_half_bucket_to, add_upper_half_bucket_to

from services.tools.list_service import last_element

import copy


class LithologyTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("Litologias")

        self.lithologies = None

        self.lithologies_cbos = []

        self.setLayout(self.gridLayout)

        self.profile_section()

        self.litology_section()

        self.flags_section()

        self.depth_section()

        self.save_and_draw_section()

        self.lithologies_cbos \
            .extend([self.litology1_cbo, self.litology2_cbo, self.litology3_cbo, self.litology4_cbo,
                     self.litology5_cbo, self.litology6_cbo, self.litology7_cbo, self.litology8_cbo,
                     self.vshale_lithology_cbo, self.carbon_curve_cb, self.anhydrit_curve_cb])

        self.add_serializable_attributes([self.delta_t_cbo, self.rho_b_cbo, self.pef_cbo, self.neutron_cbo,
                                          self.vhsale_cbo, self.vshale_lithology_cbo, self.depthFullLasRb,
                                          self.depthCustomRb, self.customMaxDepthQle, self.customMinDepthQle,
                                          self.rhodsh_tb, self.carbon_cb, self.carbon_tb, self.anhydrit_tb,
                                          self.anhydrit_cb, self.carbon_curve_cb, self.anhydrit_curve_cb] +
                                          self.lithologies_cbos)

        self.numeric_inputs.extend([self.rhodsh_tb, self.carbon_tb, self.anhydrit_tb])

    def append_curve(self,
                     lit_config,
                     first=False):
        if len(lit_config['curve_name']) == 0:
            return

        base_config = {
            'tab_name': self.tab_name,
            'track_name': self.tab_name,
            'y_axis': self.depth_curve,
            'line_width': 1,
            'invisible': True,
            'cummulative': True,
            'add_axis': False,
            'no_grid': True
        }

        lit_config.update(base_config)

        if first:
            lit_config['cummulative'] = False

            self.add_curve_with_y_label(lit_config)

        else:
            self.well \
                .graphicWindow \
                .append_curve(lit_config)

    def profile_section(self):
        self.profile_label = QLabel(PROFILE_LABEL)

        self.profile_layout = QHBoxLayout()

        self.profile_layout \
            .addWidget(self.profile_label)

        self.add_layout_to_layout(self.profile_layout)

        self.rho_b_label = QLabel(RHO_B_LABEL)

        self.rho_b_cbo = QComboBox(self)

        self.rho_b_layout = QHBoxLayout()

        self.rho_b_cbo \
            .setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.rho_b_layout \
            .addWidget(self.rho_b_label)

        self.rho_b_layout \
            .addWidget(self.rho_b_cbo)

        self.add_layout_to_layout(self.rho_b_layout)

        self.delta_t_label = QLabel(SONIC_LABEL)

        self.delta_t_cbo = QComboBox(self)

        self.delta_t_layout = QHBoxLayout()

        self.delta_t_cbo \
            .setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.delta_t_layout \
            .addWidget(self.delta_t_label)

        self.delta_t_layout \
            .addWidget(self.delta_t_cbo)

        self.add_layout_to_layout(self.delta_t_layout)

        self.pef_label = QLabel(PEF_LABEL)

        self.pef_cbo = QComboBox(self)

        self.pef_layout = QHBoxLayout()

        self.pef_cbo \
            .setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.pef_layout \
            .addWidget(self.pef_label)

        self.pef_layout \
            .addWidget(self.pef_cbo)

        self.add_layout_to_layout(self.pef_layout)

        self.neutron_label = QLabel(NEUTRON_LABEL)

        self.neutron_layout = QHBoxLayout()

        self.neutron_cbo = QComboBox(self)

        self.neutron_cbo \
            .setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.neutron_layout \
            .addWidget(self.neutron_label)

        self.neutron_layout \
            .addWidget(self.neutron_cbo)

        self.add_layout_to_layout(self.neutron_layout)

        self.vhsale_label = QLabel(VSHALE_LABEL)

        self.vhsale_cbo = QComboBox(self)

        self.vhsale_layout = QHBoxLayout()

        self.vhsale_cbo \
            .setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)

        self.vhsale_layout \
            .addWidget(self.vhsale_label)

        self.vhsale_layout \
            .addWidget(self.vhsale_cbo)

        self.vhsale_lit_layout = QHBoxLayout()

        self.vshale_lithology_cbo = QComboBox()

        self.vshale_lit_label = QLabel("Litología")

        self.vhsale_lit_layout \
            .addWidget(self.vshale_lit_label)

        self.vhsale_lit_layout \
            .addWidget(self.vshale_lithology_cbo)

        self.add_layout_to_layout(self.vhsale_layout,
                                  next_line=False)

        self.add_layout_to_layout(self.vhsale_lit_layout,
                                  column=1,
                                  next_line=False)

        self.add_widget_to_layout(QLabel("                            "),
                                  column=2)

        self.add_blank_line()

        self.curve_selectors \
            .extend([self.rho_b_cbo, self.delta_t_cbo, self.pef_cbo, self.neutron_cbo,
                     self.vhsale_cbo])

    def flags_section(self):
        self.rhodsh_label = QLabel(RHO_DSH_LBL)

        self.rhodsh_tb = QLineEdit(RHO_DSH_DEFAULT_VALUE)

        self.rhodsh_layout = QHBoxLayout()

        self.rhodsh_layout.addWidget(QLabel())

        self.rhodsh_layout.addWidget(self.rhodsh_label)

        self.rhodsh_layout.addWidget(self.rhodsh_tb, alignment=Qt.AlignmentFlag.AlignRight)

        self.add_layout_to_layout(self.rhodsh_layout)

        self.carbon_cb = QCheckBox()

        self.carbon_label = QLabel(RHO_CARBON_LBL)

        self.carbon_tb = QLineEdit(RHO_COAL_DEFAULT_VALUE)

        self.carbon_curve_cb = QComboBox()

        self.carbon_layout = QHBoxLayout()

        self.carbon_layout.addWidget(self.carbon_cb)

        self.carbon_layout.addWidget(self.carbon_label)

        self.carbon_layout.addWidget(self.carbon_tb, alignment=Qt.AlignmentFlag.AlignRight)

        carbon_fn = lambda: disable_elements_with_component(self.carbon_cb,
                            [self.carbon_tb, self.carbon_label, self.carbon_curve_cb])

        carbon_fn()

        self.carbon_cb.toggled.connect(carbon_fn)

        self.add_layout_to_layout(self.carbon_layout,
                                  next_line=False)

        self.add_widget_to_layout(self.carbon_curve_cb,
                                  column=1,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.anhydrit_cb = QCheckBox()

        self.anhydrit_label = QLabel(RHO_ANHY_LBL)

        self.anhydrit_tb = QLineEdit(RHO_ANHY_DEFAULT_VALUE)

        self.anhydrit_curve_cb = QComboBox()

        self.anhydrit_layout = QHBoxLayout()

        self.anhydrit_layout.addWidget(self.anhydrit_cb)

        self.anhydrit_layout.addWidget(self.anhydrit_label)

        self.anhydrit_layout.addWidget(self.anhydrit_tb, alignment=Qt.AlignmentFlag.AlignRight)

        anhydrit_fn = lambda: disable_elements_with_component(self.anhydrit_cb,
                              [self.anhydrit_tb, self.anhydrit_label, self.anhydrit_curve_cb])

        anhydrit_fn()

        self.anhydrit_cb.toggled.connect(anhydrit_fn)

        self.add_layout_to_layout(self.anhydrit_layout,
                                  next_line=False)

        self.add_widget_to_layout(self.anhydrit_curve_cb,
                                  column=1,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_layout_to_layout(self.anhydrit_layout)

    def litology_section(self):
        self.litologies_label = QLabel(LITOLOGIES_LABEL)

        self.add_widget_to_layout(self.litologies_label)

        self.litology1_cbo = QComboBox()

        self.litology2_cbo = QComboBox()

        self.litology3_cbo = QComboBox()

        self.litology4_cbo = QComboBox()

        self.litology5_cbo = QComboBox()

        self.litology6_cbo = QComboBox()

        self.litology7_cbo = QComboBox()

        self.litology8_cbo = QComboBox()

        self.litology_1st_layout = QHBoxLayout()

        self.litology_1st_layout \
            .addWidget(self.litology1_cbo)

        self.litology_1st_layout \
            .addWidget(self.litology2_cbo)

        self.add_layout_to_layout(self.litology_1st_layout)

        self.litology_2nd_layout = QHBoxLayout()

        self.litology_2nd_layout \
            .addWidget(self.litology3_cbo)

        self.litology_2nd_layout \
            .addWidget(self.litology4_cbo)

        self.add_layout_to_layout(self.litology_2nd_layout)

        self.litology_3rd_layout = QHBoxLayout()

        self.litology_3rd_layout \
            .addWidget(self.litology5_cbo)

        self.litology_3rd_layout \
            .addWidget(self.litology6_cbo)

        self.add_layout_to_layout(self.litology_3rd_layout)

        self.litology_4rd_layout = QHBoxLayout()

        self.litology_4rd_layout \
            .addWidget(self.litology7_cbo)

        self.litology_4rd_layout \
            .addWidget(self.litology8_cbo)

        self.add_layout_to_layout(self.litology_4rd_layout)

        self.add_blank_line()

    def depth_section(self):
        self.depthGrpBox = QGroupBox(DEPTH_LBL)

        self.depthLayout = QVBoxLayout()

        self.depthFullLasRb = QRadioButton(ALL_FILE_LBL)
        self.depthFullLasRb.setChecked(True)
        self.depthFullLasRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthFullLasRb)

        self.depthCustomRb = QRadioButton(CUSTOM_FILE_LBL)
        self.depthCustomRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthCustomRb)

        self.depthGrpBox.setLayout(self.depthLayout)

        self.gridLayout.addWidget(self.depthGrpBox, self.lines, 0, 1, 1)

        self.customMinDepthLbl = QLabel(f"{MIN_DEPTH_LBL} ")
        self.customMinDepthQle = QLineEdit(self)
        self.customMinDepthLayout = QHBoxLayout()
        self.customMinDepthLayout.addWidget(self.customMinDepthLbl)
        self.customMinDepthLayout.addWidget(self.customMinDepthQle)
        self.customMinDepthQle.setEnabled(False)

        self.customMaxDepthLbl = QLabel(MAX_DEPTH_LBL)
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle)
        self.customMaxDepthQle.setEnabled(False)

        self.customDepthLayout = QVBoxLayout()
        self.customDepthLayout.addLayout(self.customMinDepthLayout)
        self.customDepthLayout.addLayout(self.customMaxDepthLayout)
        self.gridLayout.addLayout(self.customDepthLayout, self.lines, 1, 1, 1)

        self.add_layout_to_layout(self.depthLayout)

        self.add_blank_line()

    def save_and_draw_section(self):
        self.previewBtn = QPushButton(VSHALE_MENU_CONSTANTS.PREVIEW_BUTTON)

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

        self.add_layout_to_layout(self.previewLayout)

        self.add_blank_line()

        self.curveNameLbl = QLabel("Nombre de curva")

        self.curveNameQle = QLineEdit(self)

        self.curveNameLayout = QHBoxLayout()

        self.curveNameLayout \
            .addWidget(self.curveNameLbl)

        self.curveNameLayout \
            .addWidget(self.curveNameQle)

        self.add_layout_to_layout(self.curveNameLayout)

        self.save_button = QPushButton(SAVE_POROSITY_CURVE)
        self.save_button.setStyleSheet(SAVE_BUTTON_STYLE)

        self.save_button.clicked.connect(
            lambda checked: self.save_porosity_curve()
        )

        self.add_widget_to_layout(self.save_button)

        self.add_blank_line()

        self.lithology_name_lbl = QLabel(CURVE_NAME_LBL)

        self.lithology_text_input = QLineEdit()

        self.lithology_layout = QHBoxLayout()

        self.lithology_layout \
            .addWidget(self.lithology_name_lbl)

        self.lithology_layout \
            .addWidget(self.lithology_text_input)

        self.lithology_cbo = QComboBox()

        self.lithology_save_btn = QPushButton(SAVE_LITHOLOGY_CURVE)
        self.lithology_save_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.lithology_save_btn \
            .clicked \
            .connect(self.save_lithology_curve)

        self.add_layout_to_layout(self.lithology_layout)

        self.add_widget_to_layout(self.lithology_cbo)

        self.add_widget_to_layout(self.lithology_save_btn)

        self.add_blank_line()

        self.rho = None

        self.rho_v_layout = QVBoxLayout()

        self.rho_lbl = QLabel(CURVE_NAME_LBL)

        self.rho_name_tb = QLineEdit(self)

        self.rho_h_layout = QHBoxLayout()

        self.rho_h_layout.addWidget(self.rho_lbl)

        self.rho_h_layout.addWidget(self.rho_name_tb)

        self.rho_v_layout.addLayout(self.rho_h_layout)

        self.rho_btn = QPushButton(SAVE_RHO_CURVE)
        self.rho_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.rho_btn \
            .clicked \
            .connect(lambda: self.save_curve(self.rho_name_tb.text(), self.rho))

        self.rho_v_layout.addWidget(self.rho_btn)

        self.add_layout_to_layout(self.rho_v_layout)

        self.add_blank_line()

        self.dt = None

        self.dt_v_layout = QVBoxLayout()

        self.dt_lbl = QLabel(CURVE_NAME_LBL)

        self.dt_name_tb = QLineEdit(self)

        self.dt_h_layout = QHBoxLayout()

        self.dt_h_layout.addWidget(self.dt_lbl)

        self.dt_h_layout.addWidget(self.dt_name_tb)

        self.dt_v_layout.addLayout(self.dt_h_layout)

        self.dt_btn = QPushButton(SAVE_DT_CURVE)

        self.dt_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.dt_btn \
            .clicked \
            .connect(lambda: self.save_curve(self.dt_name_tb.text(), self.dt))

        self.dt_v_layout.addWidget(self.dt_btn)

        self.add_layout_to_layout(self.dt_v_layout)

    def on_selected(self):
        self.customMinDepthQle \
            .setEnabled(self.depthCustomRb
                        .isChecked())

        self.customMaxDepthQle \
            .setEnabled(self.depthCustomRb
                        .isChecked())

        if self.depthCustomRb \
                        .isChecked():
            self.customMinDepthQle \
                .setPlaceholderText(str(
                min(self.well.wellModel.get_depth_curve())
            ))

            self.customMaxDepthQle \
                .setPlaceholderText(str(
                max(self.well.wellModel.get_depth_curve())
            ))

    def get_dtco_information(self):
        depth_curve = self.well \
            .wellModel \
            .get_depth_curve()

        min_depth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() \
            else str(min(depth_curve))

        max_depth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() \
            else str(max(depth_curve))

        self.depth_curve = self.well.wellModel \
            .get_depth_curve()

        rho_b_partial = self.well \
            .wellModel \
            .get_partial_curve(self.rho_b_cbo \
                               .currentText(),
                               min_depth,
                               max_depth)

        dt_partial = self.well \
            .wellModel \
            .get_partial_curve(self.delta_t_cbo \
                               .currentText(),
                               min_depth,
                               max_depth)

        pef_partial = self.well \
            .wellModel \
            .get_partial_curve(self.pef_cbo \
                               .currentText(),
                               min_depth,
                               max_depth)

        neutron_partial = self.well \
            .wellModel \
            .get_partial_curve(self.neutron_cbo \
                               .currentText(),
                               min_depth,
                               max_depth)

        vshale_partial = self.well \
            .wellModel \
            .get_partial_curve(self.vhsale_cbo \
                               .currentText(),
                               min_depth,
                               max_depth)

        not_none_lithologies = list(
            filter(lambda lithology: lithology is not None,
                   [self.used_lithology_1, self.used_lithology_2,
                    self.used_lithology_3, self.used_lithology_4,
                    self.used_lithology_5, self.used_lithology_6,
                    self.used_lithology_7, self.used_lithology_8]))

        carbon_idx = self.get_lithology_index(self.carbon_curve_cb.currentData(),
                                              not_none_lithologies)

        anhidrit_idx = self.get_lithology_index(self.anhydrit_curve_cb.currentData(),
                                                not_none_lithologies)

        result_dict = get_DTCO_variables({
            "rho_b": rho_b_partial,

            "dt": dt_partial,

            "pef": pef_partial,

            "neutron": neutron_partial,

            "vshale": vshale_partial,

            "lithology1": self.used_lithology_1,

            "lithology2": self.used_lithology_2,

            "lithology3": self.used_lithology_3,

            "lithology4": self.used_lithology_4,

            "lithology5": self.used_lithology_5,

            "lithology6": self.used_lithology_6,

            "lithology7": self.used_lithology_7,

            "lithology8": self.used_lithology_8,

            "carbon": self.carbon,

            "rhodsh": self.rhodsh,

            "anhydrit": self.anhydrit,

            "carbon_idx": carbon_idx,

            "anhidrit_idx": anhidrit_idx
        },
            self.lithologies_data)

        self.vshale = result_dict["vshale"]

        self.porosity = result_dict["phie"]

        self.lean_lit1 = result_dict["lean_lit1"]

        self.lean_lit2 = result_dict["lean_lit2"]

        self.lean_lit3 = result_dict["lean_lit3"]

        self.lean_lit4 = result_dict["lean_lit4"]

        self.lean_lit5 = result_dict["lean_lit5"]

        self.lean_lit6 = result_dict["lean_lit6"]

        self.lean_lit7 = result_dict["lean_lit7"]

        self.lean_lit8 = result_dict["lean_lit8"]

        self.lit1 = result_dict["lit1"]

        self.lit2 = result_dict["lit2"]

        self.lit3 = result_dict["lit3"]

        self.lit4 = result_dict["lit4"]

        self.lit5 = result_dict["lit5"]

        self.lit6 = result_dict["lit6"]

        self.lit7 = result_dict["lit7"]

        self.lit8 = result_dict["lit8"]

        self.cummulative_porosity = result_dict["cummulative_porosity"]

        self.rho = result_dict["rho"]

        self.dt = result_dict["dt"]

        self.porosity = self.well \
            .wellModel \
            .get_partial_curve_in_range(self.porosity,
                                        min_depth,
                                        max_depth)

        graphic_window = self.well \
            .graphicWindow

        depth_curve = self.well \
            .wellModel \
            .get_depth_curve()

        # An area must be enclosed to fill with colors
        aux_line_name = 'Línea auxiliar litologías (abajo)'

        graphic_window.clear_track_curves(self.tab_name,
                                          self.tab_name)

        self.append_curve({
            'x_axis': self.vshale,
            'curve_name': self.vshale_lithology["name"],
            "x_label":  LITOLOGIES_LABEL,
            'legend': True,
            'color': self.vshale_lithology["color"],
            'x_adjusted': True,
            'x_adjusted_min': 0 - 0.001,
            'x_adjusted_max': 1 + 0.001
        },
            True)

        add_bottom_half_bucket_to(graphic_window, {
                            'x_min': 0,
                            'x_max': max(self.vshale),
                            'y_min': int(min(depth_curve)),
                            'y_max': int(max(depth_curve)),
                            'curve_name': aux_line_name,
                            'add_axis': False,
                            'tab_name': self.tab_name,
                            'track_name': self.tab_name,
                            'color': 'Negro',
                            'no_grid': True,
                            'invisible': True
                           })

        self.add_fill_between_curves(graphic_window,
                                     aux_line_name,
                                     self.vshale_lithology["name"],
                                     self.vshale_lithology)

        self.append_curve({
            'x_axis': self.lit1,
            'curve_name': self.lithologies_data[1]["name"],
            'legend': self.lit_1_selected,
            'color': self.lithologies_data[1]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.vshale_lithology["name"],
                                     self.lithologies_data[1]["name"],
                                     self.lithologies_data[1])

        self.append_curve({
            'x_axis': self.lit2,
            'curve_name': self.lithologies_data[2]["name"],
            'legend': self.lit_2_selected,
            'color': self.lithologies_data[2]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.lithologies_data[1]["name"],
                                     self.lithologies_data[2]["name"],
                                     self.lithologies_data[2])

        self.append_curve({
            'x_axis': self.lit3,
            'curve_name': self.lithologies_data[3]["name"],
            'legend': self.lit_3_selected,
            'color': self.lithologies_data[3]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.lithologies_data[2]["name"],
                                     self.lithologies_data[3]["name"],
                                     self.lithologies_data[3])

        self.append_curve({
            'x_axis': self.lit4,
            'curve_name': self.lithologies_data[4]["name"],
            'legend': self.lit_4_selected,
            'color': self.lithologies_data[4]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.lithologies_data[3]["name"],
                                     self.lithologies_data[4]["name"],
                                     self.lithologies_data[4])

        self.append_curve({
            'x_axis': self.lit5,
            'curve_name': self.lithologies_data[5]["name"],
            'legend': self.lit_5_selected,
            'color': self.lithologies_data[5]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.lithologies_data[4]["name"],
                                     self.lithologies_data[5]["name"],
                                     self.lithologies_data[5])

        self.append_curve({
            'x_axis': self.lit6,
            'curve_name': self.lithologies_data[6]["name"],
            'legend': self.lit_6_selected,
            'color': self.lithologies_data[6]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.lithologies_data[5]["name"],
                                     self.lithologies_data[6]["name"],
                                     self.lithologies_data[6])

        self.append_curve({
            'x_axis': self.lit7,
            'curve_name': self.lithologies_data[7]["name"],
            'legend': self.lit_7_selected,
            'color': self.lithologies_data[7]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.lithologies_data[6]["name"],
                                     self.lithologies_data[7]["name"],
                                     self.lithologies_data[7])

        self.append_curve({
            'x_axis': self.lit8,
            'curve_name': self.lithologies_data[8]["name"],
            'legend': self.lit_8_selected,
            'color': self.lithologies_data[8]["color"]
        })

        self.add_fill_between_curves(graphic_window,
                                     self.lithologies_data[7]["name"],
                                     self.lithologies_data[8]["name"],
                                     self.lithologies_data[8])

        self.append_curve({
            'x_axis': self.cummulative_porosity,
            'curve_name': POROSITY_NAME,
            'color': "Blanco",
            'legend': True
        })

        last_used_lithology = last_element(
            list(
                filter(lambda data: len(data["name"]) != 0,
                       self.lithologies_data)))

        if last_used_lithology is None:
            last_curve_name = self.vshale_lithology["name"]

        else:
            last_curve_name = last_used_lithology["name"]

        self.add_fill_between_curves(graphic_window,
                                     last_curve_name,
                                     POROSITY_NAME,
                                     DEFAULT_LITHOLOGY_CONFIG)

        aux_line_name_2 = 'Línea auxiliar litologías (arriba)'

        add_upper_half_bucket_to(graphic_window, {
            'x_min': 1,
            'x_max': 1,
            'y_min': int(min(depth_curve)),
            'y_max': int(max(depth_curve)),
            'curve_name': aux_line_name_2,
            'add_axis': False,
            'tab_name': self.tab_name,
            'track_name': self.tab_name,
            'color': 'Negro',
            'no_grid': True,
            'invisible': True
        })

        self.add_fill_between_curves(graphic_window,
                                     POROSITY_NAME,
                                     aux_line_name_2,
                                     DEFAULT_LITHOLOGY_CONFIG)

        legend_config = {
            'x_offset': 40,
            'y_offset': 0,
            'legend_text_size': '10pt',
            'legend_text_color': getColor("Negro"),
            'columns': 1,
            'tab_name': self.tab_name,
            'track_name': self.tab_name,
            'no_grid': True
        }

        self.well \
            .graphicWindow \
            .add_legend(legend_config)

        depth_curve = self.well \
                          .wellModel \
                          .get_depth_curve()

        self.add_curve_with_y_label({
            'tab_name': self.tab_name,
            'track_name': POROSITY_NAME,
            'x_axis': self.porosity,
            'y_axis': depth_curve,
            "x_label": POROSITY_NAME,
            "y_label": self.get_y_label(),
            'curve_name': POROSITY_NAME
        })

        self.add_curve_with_y_label({
            'tab_name': self.tab_name,
            'track_name': DT_MATRIX_LBL,
            'x_axis': self.dt,
            'y_axis': depth_curve,
            "x_label": DT_MATRIX_LBL,
            "y_label": self.get_y_label(),
            'curve_name': DT_MATRIX_LBL
        })

        self.add_curve_with_y_label({
            'tab_name': self.tab_name,
            'track_name': RHO_MATRIX_LBL,
            'x_axis': self.rho,
            'y_axis': depth_curve,
            "x_label": RHO_MATRIX_LBL,
            "y_label": self.get_y_label(),
            'curve_name': RHO_MATRIX_LBL
        })

        graphic_window.draw_tracks(self.tab_name)

        self.lithology_cbo \
            .clear()

        lithologies_curves = [self.lean_lit1, self.lean_lit2, self.lean_lit3, self.lean_lit4,
                              self.lean_lit5, self.lean_lit6, self.lean_lit7, self.lean_lit8,
                              self.vshale]

        for i in range(len(self.lithologies_data)):
            if self.lithologies_data[i]["name"] != "":
                self.lithology_cbo \
                    .addItem(self.lithologies_data[i]["name"],
                             lithologies_curves[i])

    def get_lithology_index(self, carbon_curve, not_none_lithologies):
        if carbon_curve is None:
            return -1

        for i in range(
                    len(not_none_lithologies
                )):
            if not_none_lithologies[i]["name"] == carbon_curve["name"]:
                return i

        return -1

    def preview(self):
        if not super().preview():
            return

        self.used_lithology_1 = self.litology1_cbo \
                .currentData()

        self.used_lithology_2 = self.litology2_cbo \
                .currentData()

        self.used_lithology_3 = self.litology3_cbo \
                .currentData()

        self.used_lithology_4 = self.litology4_cbo \
                .currentData()

        self.used_lithology_5 = self.litology5_cbo \
            .currentData()

        self.used_lithology_6 = self.litology6_cbo \
            .currentData()

        self.used_lithology_7 = self.litology7_cbo \
            .currentData()

        self.used_lithology_8 = self.litology8_cbo \
            .currentData()

        self.v_shale_data = self.vhsale_cbo \
                .currentData()

        self.vshale_lithology = self.vshale_lithology_cbo \
            .currentData()

        if not is_number(self.rhodsh_tb.text()):
            return get_alert_from_label(self.rhodsh_tb.text())

        self.rhodsh = float(self.rhodsh_tb.text())

        if self.v_shale_data is None or self.vshale_lithology is None:
            AlertWindow("Se debe elegir un perfil de VShale con su litología.")

            return

        self.lit_1_selected = self.used_lithology_1 is not None

        self.lit_2_selected = self.used_lithology_2 is not None

        self.lit_3_selected = self.used_lithology_3 is not None

        self.lit_4_selected = self.used_lithology_4 is not None

        self.lit_5_selected = self.used_lithology_5 is not None

        self.lit_6_selected = self.used_lithology_6 is not None

        self.lit_7_selected = self.used_lithology_7 is not None

        self.lit_8_selected = self.used_lithology_8 is not None

        self.lithologies_data = [
            self.vshale_lithology,

            self.used_lithology_1 if self.lit_1_selected else DEFAULT_LITHOLOGY_CONFIG,

            self.used_lithology_2 if self.lit_2_selected else DEFAULT_LITHOLOGY_CONFIG,

            self.used_lithology_3 if self.lit_3_selected else DEFAULT_LITHOLOGY_CONFIG,

            self.used_lithology_4 if self.lit_4_selected else DEFAULT_LITHOLOGY_CONFIG,

            self.used_lithology_5 if self.lit_5_selected else DEFAULT_LITHOLOGY_CONFIG,

            self.used_lithology_6 if self.lit_6_selected else DEFAULT_LITHOLOGY_CONFIG,

            self.used_lithology_7 if self.lit_7_selected else DEFAULT_LITHOLOGY_CONFIG,

            self.used_lithology_8 if self.lit_8_selected else DEFAULT_LITHOLOGY_CONFIG,
        ]

        if self.carbon_cb.isChecked():
            if not is_number(self.carbon_tb.text()):
                return get_alert_from_label(self.carbon_label.text())

            self.carbon = float(self.carbon_tb.text())

        else:
            self.carbon = None

        if self.anhydrit_cb.isChecked():
            if not is_number(self.anhydrit_tb.text()):
                return get_alert_from_label(self.anhydrit_label.text())

            self.anhydrit = float(self.anhydrit_tb.text())

        else:
            self.anhydrit = None

        pop_up = LoadingWindow(PLEASE_WAIT_LBL)

        QTimer.singleShot(loading_pop_up_timeout_ms, lambda: (
            self.get_dtco_information(),
            pop_up.close()
        ))

    def add_fill_between_curves(self,
                                graphic_window,
                                curve_1,
                                curve_2,
                                config):
        graphic_window.add_fill_between_curves({
            'track_name': self.tab_name,
            'curve_name_1': curve_1,
            'curve_name_2': curve_2,
            'color': config["color"],
            'cummulative': True,
            'fill': config["fill"]
        })

    def update_tab(self, well=None, force_update=False, keep_index=True):
        if force_update:
            return

        if not super().update_tab(well) and are_similarl_json_lists(self.lithologies,
                                                                    self.well
                                                                        .wellModel
                                                                        .lithologies):
            return

        self.window = self.well \
                          .graphicWindow

        self.lithologies = copy.deepcopy(self.well
                                         .wellModel
                                         .lithologies)

        update_cbos(self.lithologies_cbos,
                    self.lithologies,
                    lambda lithology: lithology["name"])

        add_none_option(self.lithologies_cbos, keep_index, True)

        add_none_option(self.curve_selectors, keep_index)

    def save_porosity_curve(self):
        curve_name = self.curveNameQle \
                          .text()

        self.save_curve(curve_name,
                        self.porosity)

    def save_lithology_curve(self):
        lithology_data = self.lithology_cbo \
            .currentData()

        curve_name = self.lithology_text_input \
            .text()

        self.save_curve(curve_name,
                        lithology_data)

    def save_curve(self,
                   curve_name,
                   lithology_data):
        if lithology_data is None:
            return AlertWindow(MISSING_CURVE_TO_SAVE)

        if curve_name is None or len(curve_name) == 0:
            return AlertWindow(MISSING_CURVE_NAME)

        success = self.well \
            .wellModel\
            .append_curve(curve_name,
                          lithology_data)

        if success:
            InformationWindow(SAVED_CURVE_LBL)

        else:
            AlertWindow(CURVE_ALREADY_EXISTS_LBL)

        self.update_tab(self.well,
                        False)
