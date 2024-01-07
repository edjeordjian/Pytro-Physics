"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QLabel, QComboBox, QHBoxLayout, QLineEdit,
                             QRadioButton, QGroupBox, QVBoxLayout, QCheckBox)

from constants.LETTERS import ALPHA

from constants.MENU_CONSTANTS import USE_CONSTANT_RW_LBL

from constants.messages_constants import ZERO_DIVISION_ERROR, TOO_LARGE_ERROR

from constants.porosity_constants import POROSITY_CURVE, EFFECTIVE_POROSITY_CURVE, SW_LBL, EFFECTIVE_POROSITY_TAB_NAME

import constants.sw_constants as constants

from constants.pytrophysicsConstants import CUTOFF_LBL

from constants.tab_constants import VSHALE_LBL

from services.sw_service import (get_sw_archie, get_sw_dual_water, get_sw_simandoux, get_sw_indonesia,
                                 get_sw_fertl, get_sw_modified_simandoux)

from services.tools.number_service import celcius_to_farenheit, filter_by_cutoff

from services.tools.string_service import is_number

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.alerts import get_curve_error_alert, missing_constants_or_curves_alert, missing_constants_alert

from ui.style.StyleCombos import color_combo_box, line_combo_box, marker_combo_box

from ui.visual_components.LayoutWithFrame import LayoutWithFrame


class SwCalculation(QWidgetWithSections):
    def __init__(self,
                 tab_name):
        self.use_data_in_curve_selectors = False

        super().__init__(tab_name)

        self.setLayout(self.gridLayout)

        self.archie_componentes = []

        self.calculations = {
            constants.SW_ARCHIE: {
                "calculation": self.get_sw_archie,
                "frame": LayoutWithFrame()
            },

            constants.SW_DUAL_WATER: {
                "calculation": self.get_sw_dual_water,
                "frame": LayoutWithFrame()
            },

            constants.SW_SIMANDOUX: {
                "calculation": self.get_sw_simandoux,
                "frame": LayoutWithFrame()
            },

            constants.SW_MODIFIED_SIMANDOUX: {
                "calculation": self.get_sw_modified_simandoux,
                "frame": LayoutWithFrame()
            },

            constants.SW_INDONESIA: {
                "calculation": self.get_sw_indonesia,
                "frame": LayoutWithFrame()
            },

            constants.SW_FERTL: {
                "calculation": self.get_sw_fertl,
                "frame": LayoutWithFrame()
            },
        }

        self.initUI()

    def initUI(self):
        self.calculation_components_section()

        self.limit_sw_curve_section()

        self.sw_style_config_section(self.tab_name)

        self.depth_section()

        self.save_and_draw_section(btn_column=0)

        self.numeric_inputs.extend([self.archie_a_constant_textbox, self.archie_m_constant_textbox,
            self.archie_n_constant_textbox, self.archie_rw_textbox, self.dual_water_rw_textbox,
            self.dual_water_a_constant_textbox, self.dual_water_m_constant_textbox, self.dual_water_n_constant_textbox,
            self.dual_water_rwb_constant_textbox, self.dual_water_seed_constant_textbox,
            self.simandoux_rt_textbox, self.simandoux_a_constant_textbox, self.simandoux_rw_textbox,
            self.simandoux_m_constant_textbox, self.simandoux_r_shale_constant_textbox,
            self.modified_simandoux_rt_textbox, self.modified_simandoux_a_constant_textbox,
            self.modified_simandoux_rw_textbox, self.modified_simandoux_m_constant_textbox,
            self.modified_simandoux_n_constant_textbox, self.modified_simandoux_r_shale_constant_textbox,
            self.modified_simandoux_seed_constant_textbox, self.indonesia_rt_textbox, self.indonesia_a_constant_textbox,
            self.indonesia_rw_textbox, self.indonesia_m_constant_textbox, self.indonesia_n_constant_textbox,
            self.indonesia_r_shale_constant_textbox, self.fertl_rt_textbox, self.fertl_a_constant_textbox,
            self.fertl_m_constant_textbox, self.fertl_alpha_constant_textbox, self.fertl_rw_textbox,
            self.dual_water_rwb_factor_textbox, self.dual_water_rwb_constant_textbox, self.cutoff_value_textbox])

        self.add_serializable_attributes(
            self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb, self.customMinDepthQle,
                                    self.customMaxDepthQle,
                                    self.archie_a_constant_textbox, self.archie_m_constant_textbox,
                                    self.archie_n_constant_textbox, self.archie_rw_textbox,

                                    self.dual_water_rw_textbox,
                                    self.dual_water_a_constant_textbox, self.dual_water_m_constant_textbox,
                                    self.dual_water_n_constant_textbox,
                                    self.dual_water_rwb_constant_textbox, self.dual_water_seed_constant_textbox,
                                    self.dual_water_seed_cb,

                                    self.simandoux_rt_textbox, self.simandoux_a_constant_textbox,
                                    self.simandoux_rw_textbox,
                                    self.simandoux_m_constant_textbox, self.simandoux_r_shale_constant_textbox,

                                    self.modified_simandoux_rt_textbox, self.modified_simandoux_a_constant_textbox,
                                    self.modified_simandoux_rw_textbox,
                                    self.modified_simandoux_m_constant_textbox,
                                    self.modified_simandoux_n_constant_textbox,
                                    self.modified_simandoux_r_shale_constant_textbox,
                                    self.modified_simandoux_seed_constant_textbox, self.modified_simandoux_seed_cb,

                                    self.indonesia_rt_textbox, self.indonesia_a_constant_textbox,
                                    self.indonesia_rw_textbox,
                                    self.indonesia_m_constant_textbox, self.indonesia_n_constant_textbox,
                                    self.indonesia_r_shale_constant_textbox,

                                    self.fertl_rt_textbox, self.fertl_a_constant_textbox, self.fertl_m_constant_textbox,
                                    self.fertl_alpha_constant_textbox, self.fertl_rw_textbox,

                                    self.sw_calculation_cbo, self.curve_to_save_line,
                                    self.curve_to_save_color, self.curve_to_save_marker,

                                    self.dual_water_rwb_factor_textbox, self.dual_water_rwb_constant_textbox,
                                    self.rwb_is_constant_rb,
                                    self.rwb_is_array_rb,
                                    self.dual_water_rwb_temperature_cbo, self.rwb_with_temperature_rb,
                                    self.rwb_farenheit_temperature_rb,
                                    self.rwb_celcius_temperature_rb, self.limit_curve_cb,
                                    self.cutoff_value_textbox, self.phie_curve])

    def hide_elements(self):
        for component in self.calculations.values():
            component["frame"].hide()

    def show_elements(self,
                      value):
        self.calculations[self.previous_component]["frame"].hide()

        self.calculations[value]["frame"].show()

        self.previous_component = self.sw_calculation_cbo.currentText()

    def calculation_components_section(self):
        self.sw_calculation_label = QLabel(constants.SW_CALCULATION_LBL)

        self.sw_calculation_cbo = QComboBox()

        self.sw_calculation_cbo.addItems(self.calculations.keys())

        self.calculation_layout = QHBoxLayout()

        self.calculation_layout.addWidget(self.sw_calculation_label)

        self.calculation_layout.addWidget(self.sw_calculation_cbo)

        self.add_layout_to_layout(self.calculation_layout)

        self.add_blank_line()

        self.archie_parameters_section()

        self.dual_water_parameters_section()

        self.simandoux_parameters_section()

        self.modified_simandoux_parameters_section()

        self.indonesia_parameters_section()

        self.fertl_parameters_section()

        self.hide_elements()

        self.previous_component = self.sw_calculation_cbo.currentText()

        self.show_elements(self.sw_calculation_cbo.currentText())

        self.sw_calculation_cbo.currentTextChanged.connect(self.show_elements)

    def archie_parameters_section(self):
        archie_layout = self.calculations[constants.SW_ARCHIE]["frame"]

        self.archie_rw_lbl = QLabel(constants.RW_TAB_FULL_NAME)

        self.archie_phi_lbl = QLabel(POROSITY_CURVE)

        self.archie_rw_cbo = QComboBox()

        self.archie_phi_cbo = QComboBox()

        self.archie_rw_constant_lbl = QLabel(USE_CONSTANT_RW_LBL)

        archie_layout.addWidget(self.archie_rw_lbl,
                                next_line=False,
                                column=0)

        archie_layout.addWidget(self.archie_rw_constant_lbl,
                                column=1)

        self.archie_rw_textbox = QLineEdit()

        archie_layout.addWidget(self.archie_rw_cbo,
                                next_line=False,
                                column=0)

        archie_layout.addWidget(self.archie_rw_textbox,
                                column=1)

        archie_layout.addWidget(self.archie_phi_lbl)

        archie_layout.addWidget(self.archie_phi_cbo)

        self.archie_rt_lbl = QLabel(constants.RT_LBL)

        archie_layout.addWidget(self.archie_rt_lbl)

        self.archie_rt_cbo = QComboBox()

        archie_layout.addWidget(self.archie_rt_cbo)

        self.archie_a_constant_lbl = QLabel(constants.A_CONSTANT_LBL)

        self.archie_m_constant_lbl = QLabel(constants.M_CONSTANT_LBL)

        self.archie_n_constant_lbl = QLabel(constants.N_CONSTANT_LBL)

        archie_layout.addWidget(self.archie_a_constant_lbl,
                                next_line=False,
                                column=0)

        archie_layout.addWidget(self.archie_m_constant_lbl,
                                next_line=False,
                                column=1)

        archie_layout.addWidget(self.archie_n_constant_lbl,
                                column=2)

        self.archie_a_constant_textbox = QLineEdit(constants.A_DEFAULT_VALUE)

        self.archie_m_constant_textbox = QLineEdit(constants.M_DEFAULT_VALUE)

        self.archie_n_constant_textbox = QLineEdit(constants.N_DEFAULT_VALUE)

        archie_layout.addWidget(self.archie_a_constant_textbox,
                                next_line=False,
                                column=0)

        archie_layout.addWidget(self.archie_m_constant_textbox,
                                next_line=False,
                                column=1)

        archie_layout.addWidget(self.archie_n_constant_textbox,
                                next_line=False,
                                column=2)

        self.add_widget_to_layout(archie_layout.getFrame())

        self.curve_selectors.extend([self.archie_rw_cbo, self.archie_phi_cbo, self.archie_rt_cbo])

    def dual_water_parameters_section(self):
        dual_water_layout = self.calculations[constants.SW_DUAL_WATER]["frame"]

        self.dual_water_rw_lbl = QLabel(constants.RW_TAB_FULL_NAME)

        self.dual_water_rw_cbo = QComboBox()

        self.dual_water_rw_constant_lbl = QLabel(USE_CONSTANT_RW_LBL)

        dual_water_layout.addWidget(self.dual_water_rw_lbl,
                                    next_line=False,
                                    column=0)

        dual_water_layout.addWidget(self.dual_water_rw_constant_lbl,
                                    column=1)

        self.dual_water_rw_textbox = QLineEdit()

        dual_water_layout.addWidget(self.dual_water_rw_cbo,
                                    next_line=False,
                                    column=0)

        dual_water_layout.addWidget(self.dual_water_rw_textbox,
                                    column=1)

        self.dual_water_phi_e_lbl = QLabel(constants.POROSITY_E)

        self.dual_water_phi_e_cbo = QComboBox()

        dual_water_layout.addWidget(self.dual_water_phi_e_lbl)

        dual_water_layout.addWidget(self.dual_water_phi_e_cbo)

        self.dual_water_phi_t_lbl = QLabel(constants.POROSITY_T)

        self.dual_water_phi_t_cbo = QComboBox()

        dual_water_layout.addWidget(self.dual_water_phi_t_lbl)

        dual_water_layout.addWidget(self.dual_water_phi_t_cbo)

        self.dual_water_rt_lbl = QLabel(constants.RT_LBL)

        dual_water_layout.addWidget(self.dual_water_rt_lbl)

        self.dual_water_rt_cbo = QComboBox()

        dual_water_layout.addWidget(self.dual_water_rt_cbo)

        self.dual_water_a_constant_lbl = QLabel(constants.A_CONSTANT_LBL)

        self.dual_water_m_constant_lbl = QLabel(constants.M_CONSTANT_LBL)

        self.dual_water_n_constant_lbl = QLabel(constants.N_CONSTANT_LBL)

        dual_water_layout.addWidget(self.dual_water_a_constant_lbl,
                                    next_line=False,
                                    column=0)

        dual_water_layout.addWidget(self.dual_water_m_constant_lbl,
                                    next_line=False,
                                    column=1)

        dual_water_layout.addWidget(self.dual_water_n_constant_lbl,
                                    column=2)

        self.dual_water_a_constant_textbox = QLineEdit(constants.A_DEFAULT_VALUE)

        self.dual_water_m_constant_textbox = QLineEdit(constants.M_DEFAULT_VALUE)

        self.dual_water_n_constant_textbox = QLineEdit(constants.N_DEFAULT_VALUE)

        dual_water_layout.addWidget(self.dual_water_a_constant_textbox,
                                    next_line=False,
                                    column=0)

        dual_water_layout.addWidget(self.dual_water_m_constant_textbox,
                                    next_line=False,
                                    column=1)

        dual_water_layout.addWidget(self.dual_water_n_constant_textbox,
                                    column=2)

        self.dual_water_rwb_section(dual_water_layout)

        dual_water_layout.addWidget(QLabel(""))

        self.dual_water_seed_cb = QCheckBox()

        self.dual_water_seed_cb.setChecked(True)

        self.dual_water_seed_cb.toggled.connect(self.use_default_seed_dw)

        self.dual_water_seed_label = QLabel(constants.USE_DEFAULT_SEED_LBL)

        self.dual_water_seed_constant_layout = QHBoxLayout()

        self.dual_water_seed_constant_layout.addWidget(self.dual_water_seed_cb)

        self.dual_water_seed_constant_layout.addWidget(self.dual_water_seed_label)

        dual_water_layout.addLayout(self.dual_water_seed_constant_layout)

        self.dual_water_seed_constant_lbl = QLabel(constants.SEED_CONSTANT_LBL)

        dual_water_layout.addWidget(self.dual_water_seed_constant_lbl)

        self.dual_water_seed_constant_textbox = QLineEdit(constants.SEED_DEFAULT_VALUE)

        dual_water_layout.addWidget(self.dual_water_seed_constant_textbox)

        self.add_widget_to_layout(dual_water_layout.getFrame())

        self.dw_seed_previous_value = constants.SEED_DEFAULT_VALUE

        self.use_default_seed_dw()

        self.curve_selectors.extend([self.dual_water_rw_cbo, self.dual_water_phi_t_cbo,
                                     self.dual_water_phi_e_cbo, self.dual_water_rt_cbo])

    def simandoux_parameters_section(self):
        simandoux_layout = self.calculations[constants.SW_SIMANDOUX]["frame"]

        self.simandoux_rw_lbl = QLabel(constants.RW_TAB_FULL_NAME)

        self.simandoux_phi_lbl = QLabel(POROSITY_CURVE)

        self.simandoux_rw_cbo = QComboBox()

        self.simandoux_phi_cbo = QComboBox()

        self.simandoux_rw_constant_lbl = QLabel(USE_CONSTANT_RW_LBL)

        simandoux_layout.addWidget(self.simandoux_rw_lbl,
                                   next_line=False,
                                   column=0)

        simandoux_layout.addWidget(self.simandoux_rw_constant_lbl,
                                   column=1)

        self.simandoux_rw_textbox = QLineEdit()

        simandoux_layout.addWidget(self.simandoux_rw_cbo,
                                   next_line=False,
                                   column=0)

        simandoux_layout.addWidget(self.simandoux_rw_textbox,
                                   column=1)

        simandoux_layout.addWidget(self.simandoux_phi_lbl)

        simandoux_layout.addWidget(self.simandoux_phi_cbo)

        self.simandoux_rt_lbl = QLabel(constants.RT_LBL)

        simandoux_layout.addWidget(self.simandoux_rt_lbl)

        self.simandoux_rt_cbo = QComboBox()

        self.simandoux_rt_textbox = QLineEdit()

        simandoux_layout.addWidget(self.simandoux_rt_cbo)

        self.simandoux_vshale_lbl = QLabel(VSHALE_LBL)

        self.simandoux_vshale_cbo = QComboBox()

        simandoux_layout.addWidget(self.simandoux_vshale_lbl)

        simandoux_layout.addWidget(self.simandoux_vshale_cbo)

        self.simandoux_a_constant_lbl = QLabel(constants.A_CONSTANT_LBL)

        self.simandoux_m_constant_lbl = QLabel(constants.M_CONSTANT_LBL)

        self.simandoux_r_shale_constant_lbl = QLabel(constants.R_SHALE_CONSTANT_LBL)

        simandoux_layout.addWidget(self.simandoux_a_constant_lbl,
                                next_line=False,
                                column=0)

        simandoux_layout.addWidget(self.simandoux_m_constant_lbl,
                                next_line=False,
                                column=1)

        simandoux_layout.addWidget(self.simandoux_r_shale_constant_lbl,
                                column=2)

        self.simandoux_a_constant_textbox = QLineEdit(constants.A_DEFAULT_VALUE)

        self.simandoux_m_constant_textbox = QLineEdit(constants.M_DEFAULT_VALUE)

        self.simandoux_r_shale_constant_textbox = QLineEdit()

        simandoux_layout.addWidget(self.simandoux_a_constant_textbox,
                                next_line=False,
                                column=0)

        simandoux_layout.addWidget(self.simandoux_m_constant_textbox,
                                next_line=False,
                                column=1)

        simandoux_layout.addWidget(self.simandoux_r_shale_constant_textbox,
                                next_line=False,
                                column=2)

        self.add_widget_to_layout(simandoux_layout.getFrame())

        self.curve_selectors.extend([self.simandoux_rw_cbo, self.simandoux_phi_cbo, self.simandoux_rt_cbo,
                                     self.simandoux_vshale_cbo])

    def modified_simandoux_parameters_section(self):
        modified_simandoux_layout = self.calculations[constants.SW_MODIFIED_SIMANDOUX]["frame"]

        self.modified_simandoux_rw_lbl = QLabel(constants.RW_TAB_FULL_NAME)

        self.modified_simandoux_rw_constant_lbl = QLabel(USE_CONSTANT_RW_LBL)

        modified_simandoux_layout.addWidget(self.modified_simandoux_rw_lbl,
                                next_line=False,
                                column=0)

        modified_simandoux_layout.addWidget(self.modified_simandoux_rw_constant_lbl,
                                column=1)

        self.modified_simandoux_rw_textbox = QLineEdit()

        self.modified_simandoux_rw_cbo = QComboBox()

        modified_simandoux_layout.addWidget(self.modified_simandoux_rw_cbo,
                                next_line=False,
                                column=0)

        modified_simandoux_layout.addWidget(self.modified_simandoux_rw_textbox,
                                column=1)

        self.modified_simandoux_phi_lbl = QLabel(POROSITY_CURVE)

        self.modified_simandoux_phi_cbo = QComboBox()

        modified_simandoux_layout.addWidget(self.modified_simandoux_phi_lbl)

        modified_simandoux_layout.addWidget(self.modified_simandoux_phi_cbo)

        self.modified_simandoux_vshale_lbl = QLabel(VSHALE_LBL)

        self.modified_simandoux_vshale_cbo = QComboBox()

        modified_simandoux_layout.addWidget(self.modified_simandoux_vshale_lbl)

        modified_simandoux_layout.addWidget(self.modified_simandoux_vshale_cbo)

        self.modified_simandoux_rt_lbl = QLabel(constants.RT_LBL)

        modified_simandoux_layout.addWidget(self.modified_simandoux_rt_lbl)

        self.modified_simandoux_rt_cbo = QComboBox()

        self.modified_simandoux_rt_textbox = QLineEdit()

        modified_simandoux_layout.addWidget(self.modified_simandoux_rt_cbo)

        self.modified_simandoux_a_constant_lbl = QLabel(constants.A_CONSTANT_LBL)

        self.modified_simandoux_m_constant_lbl = QLabel(constants.M_CONSTANT_LBL)

        self.modified_simandoux_n_constant_lbl = QLabel(constants.N_CONSTANT_LBL)

        self.modified_simandoux_r_shale_constant_lbl = QLabel(constants.R_SHALE_CONSTANT_LBL)

        modified_simandoux_layout.addWidget(self.modified_simandoux_a_constant_lbl,
                                    next_line=False,
                                    column=0)

        modified_simandoux_layout.addWidget(self.modified_simandoux_m_constant_lbl,
                                    next_line=False,
                                    column=1)

        modified_simandoux_layout.addWidget(self.modified_simandoux_n_constant_lbl,
                                    next_line=False,
                                    column=2)

        modified_simandoux_layout.addWidget(self.modified_simandoux_r_shale_constant_lbl,
                                    column=3)

        self.modified_simandoux_a_constant_textbox = QLineEdit(constants.A_DEFAULT_VALUE)

        self.modified_simandoux_m_constant_textbox = QLineEdit(constants.M_DEFAULT_VALUE)

        self.modified_simandoux_n_constant_textbox = QLineEdit(constants.N_DEFAULT_VALUE)

        self.modified_simandoux_r_shale_constant_textbox = QLineEdit()

        modified_simandoux_layout.addWidget(self.modified_simandoux_a_constant_textbox,
                                    next_line=False,
                                    column=0)

        modified_simandoux_layout.addWidget(self.modified_simandoux_m_constant_textbox,
                                    next_line=False,
                                    column=1)

        modified_simandoux_layout.addWidget(self.modified_simandoux_n_constant_textbox,
                                    next_line=False,
                                    column=2)

        modified_simandoux_layout.addWidget(self.modified_simandoux_r_shale_constant_textbox,
                                    column=3)

        modified_simandoux_layout.addWidget(QLabel(""))

        self.modified_simandoux_seed_cb = QCheckBox()

        self.modified_simandoux_seed_cb.setChecked(True)

        self.modified_simandoux_seed_cb.toggled.connect(self.use_default_seed_ms)

        self.modified_simandoux_seed_label = QLabel(constants.USE_DEFAULT_SEED_LBL)

        self.modified_simandoux_seed_constant_layout = QHBoxLayout()

        self.modified_simandoux_seed_constant_layout.addWidget(self.modified_simandoux_seed_cb)

        self.modified_simandoux_seed_constant_layout.addWidget(self.modified_simandoux_seed_label)

        modified_simandoux_layout.addLayout(self.modified_simandoux_seed_constant_layout)

        self.modified_simandoux_seed_constant_lbl = QLabel(constants.SEED_CONSTANT_LBL)

        modified_simandoux_layout.addWidget(self.modified_simandoux_seed_constant_lbl)

        self.modified_simandoux_seed_constant_textbox = QLineEdit(constants.SEED_DEFAULT_VALUE)

        modified_simandoux_layout.addWidget(self.modified_simandoux_seed_constant_textbox)

        self.use_default_seed_ms()

        self.ms_seed_previous_value = constants.SEED_DEFAULT_VALUE

        self.add_widget_to_layout(modified_simandoux_layout.getFrame())

        self.curve_selectors.extend([self.modified_simandoux_rw_cbo, self.modified_simandoux_vshale_cbo,
                                     self.modified_simandoux_phi_cbo, self.modified_simandoux_rt_cbo])

    def indonesia_parameters_section(self):
        indonesia_layout = self.calculations[constants.SW_INDONESIA]["frame"]

        self.indonesia_rw_lbl = QLabel(constants.RW_TAB_FULL_NAME)

        self.indonesia_rw_cbo = QComboBox()

        self.indonesia_rw_constant_lbl = QLabel(USE_CONSTANT_RW_LBL)

        indonesia_layout.addWidget(self.indonesia_rw_lbl,
                                next_line=False,
                                column=0)

        indonesia_layout.addWidget(self.indonesia_rw_constant_lbl,
                                column=1)

        self.indonesia_rw_textbox = QLineEdit()

        indonesia_layout.addWidget(self.indonesia_rw_cbo,
                                next_line=False,
                                column=0)

        indonesia_layout.addWidget(self.indonesia_rw_textbox,
                                column=1)

        self.indonesia_phi_lbl = QLabel(EFFECTIVE_POROSITY_CURVE)

        self.indonesia_phi_cbo = QComboBox()

        indonesia_layout.addWidget(self.indonesia_phi_lbl)

        indonesia_layout.addWidget(self.indonesia_phi_cbo)

        self.indonesia_rt_lbl = QLabel(constants.RT_LBL)

        indonesia_layout.addWidget(self.indonesia_rt_lbl)

        self.indonesia_rt_cbo = QComboBox()

        self.indonesia_rt_textbox = QLineEdit()

        indonesia_layout.addWidget(self.indonesia_rt_cbo)

        self.indonesia_vshale_lbl = QLabel(VSHALE_LBL)

        self.indonesia_vshale_cbo = QComboBox()

        indonesia_layout.addWidget(self.indonesia_vshale_lbl)

        indonesia_layout.addWidget(self.indonesia_vshale_cbo)

        self.indonesia_a_constant_lbl = QLabel(constants.A_CONSTANT_LBL)

        self.indonesia_m_constant_lbl = QLabel(constants.M_CONSTANT_LBL)

        self.indonesia_n_constant_lbl = QLabel(constants.N_CONSTANT_LBL)

        self.indonesia_r_shale_constant_lbl = QLabel(constants.R_SHALE_CONSTANT_LBL)

        indonesia_layout.addWidget(self.indonesia_a_constant_lbl,
                                next_line=False,
                                column=0)

        indonesia_layout.addWidget(self.indonesia_m_constant_lbl,
                                next_line=False,
                                column=1)

        indonesia_layout.addWidget(self.indonesia_n_constant_lbl,
                                next_line=False,
                                column=2)

        indonesia_layout.addWidget(self.indonesia_r_shale_constant_lbl,
                                column=3)

        self.indonesia_a_constant_textbox = QLineEdit(constants.A_DEFAULT_VALUE)

        self.indonesia_m_constant_textbox = QLineEdit(constants.M_DEFAULT_VALUE)

        self.indonesia_n_constant_textbox = QLineEdit(constants.N_DEFAULT_VALUE)

        self.indonesia_r_shale_constant_textbox = QLineEdit()

        indonesia_layout.addWidget(self.indonesia_a_constant_textbox,
                                next_line=False,
                                column=0)

        indonesia_layout.addWidget(self.indonesia_m_constant_textbox,
                                next_line=False,
                                column=1)

        indonesia_layout.addWidget(self.indonesia_n_constant_textbox,
                                next_line=False,
                                column=2)

        indonesia_layout.addWidget(self.indonesia_r_shale_constant_textbox,
                                column=3)

        self.add_widget_to_layout(indonesia_layout.getFrame())

        self.curve_selectors.extend([self.indonesia_rw_cbo, self.indonesia_phi_cbo, self.indonesia_rt_cbo,
                                     self.indonesia_vshale_cbo])

    def fertl_parameters_section(self):
        fertl_layout = self.calculations[constants.SW_FERTL]["frame"]

        self.fertl_rw_lbl = QLabel(constants.RW_TAB_FULL_NAME)

        self.fertl_rw_constant_lbl = QLabel(USE_CONSTANT_RW_LBL)

        self.fertl_rw_cbo = QComboBox()

        fertl_layout.addWidget(self.fertl_rw_lbl,
                               next_line=False,
                               column=0)

        fertl_layout.addWidget(self.fertl_rw_constant_lbl,
                               column=1)

        self.fertl_rw_textbox = QLineEdit()

        fertl_layout.addWidget(self.fertl_rw_cbo,
                               next_line=False,
                               column=0)

        fertl_layout.addWidget(self.fertl_rw_textbox,
                               column=1)

        self.fertl_phi_lbl = QLabel(EFFECTIVE_POROSITY_CURVE)

        self.fertl_phi_cbo = QComboBox()

        fertl_layout.addWidget(self.fertl_phi_lbl)

        fertl_layout.addWidget(self.fertl_phi_cbo)

        self.fertl_rt_lbl = QLabel(constants.RT_LBL)

        fertl_layout.addWidget(self.fertl_rt_lbl)

        self.fertl_rt_cbo = QComboBox()

        self.fertl_rt_textbox = QLineEdit()

        fertl_layout.addWidget(self.fertl_rt_cbo)

        self.fertl_vshale_lbl = QLabel(VSHALE_LBL)

        self.fertl_vshale_cbo = QComboBox()

        fertl_layout.addWidget(self.fertl_vshale_lbl)

        fertl_layout.addWidget(self.fertl_vshale_cbo)

        self.fertl_a_constant_lbl = QLabel(constants.A_CONSTANT_LBL)

        self.fertl_m_constant_lbl = QLabel(constants.M_CONSTANT_LBL)

        self.fertl_alpha_constant_lbl = QLabel(ALPHA)

        fertl_layout.addWidget(self.fertl_a_constant_lbl,
                               next_line=False,
                               column=0)

        fertl_layout.addWidget(self.fertl_m_constant_lbl,
                               next_line=False,
                               column=1)

        fertl_layout.addWidget(self.fertl_alpha_constant_lbl,
                               column=2)

        self.fertl_a_constant_textbox = QLineEdit(constants.A_DEFAULT_VALUE)

        self.fertl_m_constant_textbox = QLineEdit(constants.M_DEFAULT_VALUE)

        self.fertl_alpha_constant_textbox = QLineEdit()

        fertl_layout.addWidget(self.fertl_a_constant_textbox,
                               next_line=False,
                               column=0)

        fertl_layout.addWidget(self.fertl_m_constant_textbox,
                               next_line=False,
                               column=1)

        fertl_layout.addWidget(self.fertl_alpha_constant_textbox,
                               column=2)

        self.add_widget_to_layout(fertl_layout.getFrame())

        self.curve_selectors.extend([self.fertl_rw_cbo, self.fertl_phi_cbo, self.fertl_rt_cbo,
                                     self.fertl_vshale_cbo])

    def limit_sw_curve_section(self):
        self.limit_curve_layout = QHBoxLayout()

        self.limit_curve_cb = QCheckBox()

        self.limit_curve_cb.setChecked(True)

        self.limit_curve_lbl = QLabel(constants.LIMIT_FRACTION_VALUE_LBL)

        self.add_widget_to_layout(self.limit_curve_lbl,
                                  next_line=False)

        self.add_widget_to_layout(self.limit_curve_cb,
                                  next_line=True,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_blank_line()

        self.phie_curve_lbl = QLabel(EFFECTIVE_POROSITY_TAB_NAME)

        self.phie_curve = QComboBox()

        self.cutoff_value_lbl = QLabel(CUTOFF_LBL)

        self.cutoff_value_textbox = QLineEdit(constants.SW_CUTOFF_DEFAULT_VALUE)

        self.limit_curve_label_layout = QHBoxLayout()

        self.limit_curve_label_layout.addWidget(self.phie_curve_lbl)

        self.limit_curve_label_layout.addWidget(self.phie_curve)

        self.limit_curve_values_layout = QHBoxLayout()

        self.limit_curve_values_layout.addWidget(self.cutoff_value_lbl)

        self.limit_curve_values_layout.addWidget(self.cutoff_value_textbox,
                                                 alignment=Qt.AlignmentFlag.AlignRight)

        self.add_layout_to_layout(self.limit_curve_label_layout)

        self.add_layout_to_layout(self.limit_curve_values_layout)

        self.curve_selectors.append(self.phie_curve)

    def rw_method_selected(self):
        self.dual_water_RWb_constant_lbl.setEnabled(self.rwb_is_constant_rb.isChecked())

        self.dual_water_rwb_constant_textbox.setEnabled(self.rwb_is_constant_rb.isChecked())

        self.dual_water_RWb_factor_lbl.setEnabled(self.rwb_is_array_rb.isChecked())

        self.dual_water_rwb_factor_textbox.setEnabled(self.rwb_is_array_rb.isChecked())

        self.dual_water_rwb_temperature_cbo.setEnabled(self.rwb_with_temperature_rb.isChecked())

        self.rwb_celcius_temperature_rb.setEnabled(self.rwb_with_temperature_rb.isChecked())

        self.rwb_farenheit_temperature_rb.setEnabled(self.rwb_with_temperature_rb.isChecked())

    def dual_water_rwb_group_1_section(self, dual_water_layout):
        self.rwb_radio_group_box = QGroupBox(constants.RWB_METHOD_LBL)

        self.rwb_method_layout = QVBoxLayout()

        self.rwb_radio_group_box.setLayout(self.rwb_method_layout)

        self.rwb_is_constant_rb = QRadioButton(constants.RWb_CONSTANT_METHOD_LBL)

        self.rwb_is_constant_rb.setChecked(True)

        self.rwb_is_constant_rb.toggled.connect(self.rw_method_selected)

        self.rwb_method_layout.addWidget(self.rwb_is_constant_rb)

        self.rwb_is_array_rb = QRadioButton(constants.RWb_FACTOR_METHOD_LBL)

        self.rwb_is_constant_rb.toggled.connect(self.rw_method_selected)

        self.rwb_method_layout.addWidget(self.rwb_is_array_rb)

        self.rwb_with_temperature_rb = QRadioButton(constants.RWb_WITH_TEMPERATURE_METHOD_LBL)

        self.rwb_with_temperature_rb.toggled.connect(self.rw_method_selected)

        self.rwb_method_layout.addWidget(self.rwb_with_temperature_rb)

        dual_water_layout.addWidget(self.rwb_radio_group_box)

    def dual_water_rwb_temperature_group_section(self, dual_water_layout):
        self.rwb_with_temperature_group_box = QGroupBox()

        rwb_with_temperature_layout = QVBoxLayout()

        self.rwb_celcius_temperature_rb = QRadioButton(constants.CELCIUS_LBL)

        self.rwb_celcius_temperature_rb.setChecked(True)

        rwb_with_temperature_layout.addWidget(self.rwb_celcius_temperature_rb)

        self.rwb_farenheit_temperature_rb = QRadioButton(constants.FARENHEIT_LBL)

        rwb_with_temperature_layout.addWidget(self.rwb_farenheit_temperature_rb)

        self.rwb_with_temperature_group_box.setLayout(rwb_with_temperature_layout)

        dual_water_layout.addWidget(self.rwb_with_temperature_group_box)

    def dual_water_rwb_section(self, dual_water_layout):
        dual_water_layout.add_blank_line()

        self.dual_water_rwb_group_1_section(dual_water_layout)

        self.dual_water_RWb_constant_lbl = QLabel(constants.RWb_CONSTANT_LBL)

        self.dual_water_rwb_constant_textbox = QLineEdit(constants.RWb_DEFAULT_VALUE)

        self.dual_water_rwb_constant_layout = QHBoxLayout()

        self.dual_water_rwb_constant_layout.addWidget(self.dual_water_RWb_constant_lbl)

        self.dual_water_rwb_constant_layout.addWidget(self.dual_water_rwb_constant_textbox)

        self.dual_water_RWb_factor_lbl = QLabel(constants.RWb_FACTOR_LBL)

        self.dual_water_rwb_factor_textbox = QLineEdit(constants.RWb_DEFAULT_VALUE)

        self.dual_water_rwb_factor_layout = QHBoxLayout()

        self.dual_water_rwb_factor_layout.addWidget(self.dual_water_RWb_factor_lbl)

        self.dual_water_rwb_factor_layout.addWidget(self.dual_water_rwb_factor_textbox)

        dual_water_layout.addLayout(self.dual_water_rwb_constant_layout)

        dual_water_layout.addLayout(self.dual_water_rwb_factor_layout)

        self.dual_water_rwb_temperature_cbo = QComboBox()

        self.curve_selectors.append(self.dual_water_rwb_temperature_cbo)

        dual_water_layout.addWidget(self.dual_water_rwb_temperature_cbo)

        self.dual_water_rwb_temperature_group_section(dual_water_layout)

        self.add_blank_line()

        self.rw_method_selected()

    def get_sw_archie(self):
        phi = self.get_partial_curve(self.archie_phi_cbo.currentText())

        rw = self.get_constant_curve_data(self.archie_rw_cbo,
                                          self.archie_rw_textbox,
                                          "saturación de agua.")

        rt = self.get_partial_curve(self.archie_rt_cbo.currentText())

        if rt is None:
            AlertWindow(get_curve_error_alert(constants.RT_LBL))

            return None, ""

        a = self.archie_a_constant_textbox.text()

        m = self.archie_m_constant_textbox.text()

        n = self.archie_n_constant_textbox.text()

        if not is_number(a) or not is_number(m) or not is_number(n):
            missing_constants_or_curves_alert(self.tab_name)

            return None, ""

        return get_sw_archie(float(a), float(n), float(m), phi,
                             rw, rt, self.limit_curve_cb.isChecked()),\
            f"{self.tab_name} {constants.SW_ARCHIE}"

    def get_sw_dual_water(self):
        phi_e = self.get_partial_curve(self.dual_water_phi_e_cbo.currentText())

        phi_t = self.get_partial_curve(self.dual_water_phi_t_cbo.currentText())

        rw = self.get_constant_curve_data(self.dual_water_rw_cbo,
                                          self.dual_water_rw_textbox,
                                          "saturación de agua.")

        rt = self.get_partial_curve(self.dual_water_rt_cbo.currentText())

        if rt is None:
            AlertWindow(get_curve_error_alert(constants.RT_LBL))

            return None, ""

        a = self.dual_water_a_constant_textbox.text()

        m = self.dual_water_m_constant_textbox.text()

        n = self.dual_water_n_constant_textbox.text()

        seed = self.dual_water_seed_constant_textbox.text()

        rwb_constant = self.dual_water_rwb_constant_textbox.text()

        rwb_factor = self.dual_water_rwb_factor_textbox.text()

        if not is_number(a) or not is_number(m) or not is_number(n) \
                or not is_number(seed) or not is_number(rwb_constant) or not is_number(rwb_factor):
            missing_constants_or_curves_alert(self.tab_name)

            return None, ""

        if self.rwb_is_constant_rb.isChecked():
            rwb = [float(rwb_constant)] * len(self.depth_curve)

        elif self.rwb_is_array_rb.isChecked():
            rwb = rw * float(rwb_factor)

        else:
            temperature = self.get_partial_curve(self.dual_water_rwb_temperature_cbo.currentText())

            if self.rwb_celcius_temperature_rb \
                   .isChecked():
                temperature = celcius_to_farenheit(temperature)

            rwb = 0.000126 * (temperature - 16.7) * (temperature + 504.4)

        return get_sw_dual_water(float(a), float(m), float(n), float(seed),
                                 rwb, phi_e, phi_t, rw,
                                 rt, self.limit_curve_cb.isChecked()), \
            f"{self.tab_name} {constants.SW_DUAL_WATER}"

    def get_sw_simandoux(self):
        phi = self.get_partial_curve(self.simandoux_phi_cbo.currentText())

        vshale = self.get_partial_curve(self.simandoux_vshale_cbo.currentText())

        rw = self.get_constant_curve_data(self.simandoux_rw_cbo,
                                          self.simandoux_rw_textbox,
                                          "saturación de agua.")

        rt = self.get_partial_curve(self.simandoux_rt_cbo.currentText())

        if rt is None:
            AlertWindow(get_curve_error_alert(constants.RT_LBL))

            return None, ""

        a = self.simandoux_a_constant_textbox.text()

        m = self.simandoux_m_constant_textbox.text()

        r_shale = self.simandoux_r_shale_constant_textbox.text()

        if not is_number(a) or not is_number(m) or not is_number(r_shale):
            missing_constants_or_curves_alert(self.tab_name)

            return None, ""

        return get_sw_simandoux(float(a), float(m), float(r_shale), phi,
                                rw, rt, vshale, self.limit_curve_cb.isChecked()), \
            f"{self.tab_name} {constants.SW_SIMANDOUX}"

    def get_sw_modified_simandoux(self):
        phi = self.get_partial_curve(self.modified_simandoux_phi_cbo.currentText())

        vshale = self.get_partial_curve(self.modified_simandoux_vshale_cbo.currentText())

        rw = self.get_constant_curve_data(self.modified_simandoux_rw_cbo,
                                          self.modified_simandoux_rw_textbox,
                                          "saturación de agua.")

        rt = self.get_partial_curve(self.modified_simandoux_rt_cbo.currentText())

        if rt is None:
            AlertWindow(get_curve_error_alert(constants.RT_LBL))

            return None, ""

        a = self.modified_simandoux_a_constant_textbox.text()

        m = self.modified_simandoux_m_constant_textbox.text()

        n = self.modified_simandoux_n_constant_textbox.text()

        r_shale = self.modified_simandoux_r_shale_constant_textbox.text()

        seed = self.modified_simandoux_seed_constant_textbox.text()

        if not is_number(a) or not is_number(m) or not is_number(n) \
                or not is_number(r_shale) or not is_number(r_shale) or not is_number(seed):
            missing_constants_or_curves_alert(self.tab_name)

            return None, ""

        return get_sw_modified_simandoux(float(a), float(m), float(n), float(r_shale),
                                         float(seed), phi, vshale, rw,
                                         rt, self.limit_curve_cb.isChecked()), \
            f"{self.tab_name} {constants.SW_MODIFIED_SIMANDOUX}"

    def get_sw_indonesia(self):
        phi = self.get_partial_curve(self.indonesia_phi_cbo.currentText())

        rw = self.get_constant_curve_data(self.indonesia_rw_cbo,
                                          self.indonesia_rw_textbox,
                                          "saturación de agua.")

        rt = self.get_partial_curve(self.indonesia_rt_cbo.currentText())

        vshale = self.get_partial_curve(self.indonesia_vshale_cbo.currentText())

        if rt is None:
            AlertWindow(get_curve_error_alert(constants.RT_LBL))

            return None, ""

        a = self.indonesia_a_constant_textbox.text()

        n = self.indonesia_m_constant_textbox.text()

        m = self.indonesia_m_constant_textbox.text()

        r_shale = self.indonesia_r_shale_constant_textbox.text()

        if not is_number(a) or not is_number(m) or not is_number(r_shale) or not is_number(n):
            missing_constants_or_curves_alert(self.tab_name)

            return None, ""

        return get_sw_indonesia(float(a), float(m), float(r_shale), float(n),
                                phi, rw, rt, vshale,
                                self.limit_curve_cb.isChecked()), \
            f"{self.tab_name} {constants.SW_INDONESIA}"

    def get_sw_fertl(self):
        phi = self.get_partial_curve(self.fertl_phi_cbo.currentText())

        rt = self.get_partial_curve(self.fertl_rt_cbo.currentText())

        rw = self.get_constant_curve_data(self.fertl_rw_cbo,
                                          self.fertl_rw_textbox,
                                          "saturación de agua.")

        vshale = self.get_partial_curve(self.fertl_vshale_cbo.currentText())

        if rt is None:
            AlertWindow(get_curve_error_alert(constants.RT_LBL))

            return None, ""

        a = self.fertl_a_constant_textbox.text()

        m = self.fertl_m_constant_textbox.text()

        alpha = self.fertl_alpha_constant_textbox.text()

        if not is_number(a) or not is_number(m) or not is_number(alpha):
            missing_constants_or_curves_alert(self.tab_name)

            return None, ""

        return get_sw_fertl(float(a), float(m), float(alpha), phi,
                            rw, rt, vshale, self.limit_curve_cb.isChecked()), \
            f"{self.tab_name} {constants.SW_FERTL}"

    def sw_style_config_section(self,
                                section_header):
        self.curve_to_save_style_lbl = QLabel(section_header)

        self.style_layout = QHBoxLayout()

        self.curve_to_save_color = color_combo_box()

        self.curve_to_save_line = line_combo_box()

        self.curve_to_save_marker = marker_combo_box()

        self.add_blank_line()

        self.add_widget_to_layout(self.curve_to_save_style_lbl)

        self.style_layout.addWidget(self.curve_to_save_color)

        self.style_layout.addWidget(self.curve_to_save_line)

        self.style_layout.addWidget(self.curve_to_save_marker)

        self.add_layout_to_layout(self.style_layout)

    def use_default_seed_dw(self):
        if self.dual_water_seed_cb.isChecked():
            self.dual_water_seed_constant_textbox.setEnabled(False)

            self.dual_water_seed_constant_lbl.setEnabled(False)

            current_seed_value = self.dual_water_seed_constant_textbox.text()

            if current_seed_value != constants.SEED_DEFAULT_VALUE:
                self.dw_seed_previous_value = current_seed_value

            self.dual_water_seed_constant_textbox.setText(constants.SEED_DEFAULT_VALUE)

        else:
            self.dual_water_seed_constant_textbox.setEnabled(True)

            self.dual_water_seed_constant_lbl.setEnabled(True)

            self.dual_water_seed_constant_textbox.setText(self.dw_seed_previous_value)

    def use_default_seed_ms(self):
        if self.modified_simandoux_seed_cb.isChecked():
            self.modified_simandoux_seed_constant_textbox.setEnabled(False)

            self.modified_simandoux_seed_constant_lbl.setEnabled(False)

            current_seed_value = self.modified_simandoux_seed_constant_textbox.text()

            if current_seed_value != constants.SEED_DEFAULT_VALUE:
                self.ms_seed_previous_value = current_seed_value

            self.modified_simandoux_seed_constant_textbox.setText(constants.SEED_DEFAULT_VALUE)

        else:
            self.modified_simandoux_seed_constant_textbox.setEnabled(True)

            self.modified_simandoux_seed_constant_lbl.setEnabled(True)

            self.modified_simandoux_seed_constant_textbox.setText(self.ms_seed_previous_value)

    def preview(self):
        if not super().preview():
            return

        current = self.sw_calculation_cbo.currentText()

        try:
            porosity_curve = self.get_partial_curve(self.phie_curve.currentText())

            result_curve, curve_name = self.calculations[current]["calculation"]()

            if result_curve is None:
                return

            if not is_number(self.cutoff_value_textbox.text()):
                return missing_constants_alert()

            cutoff_value = float(self.cutoff_value_textbox.text())

            self.curve_to_save = filter_by_cutoff(porosity_curve,
                                                  cutoff_value,
                                                  result_curve,
                                                  constants.SW_CUTOFF_REPLACE_VALUE)

        except ZeroDivisionError:
            return AlertWindow(ZERO_DIVISION_ERROR)

        except OverflowError:
            return AlertWindow(TOO_LARGE_ERROR)

        if self.curve_to_save is None:
            return

        self.add_curve_with_y_label({
                'tab_name': self.tab_name,

                'track_name': curve_name,

                'curve_name': curve_name,

                'x_axis': self.curve_to_save,

                'y_axis':  self.depth_curve,

                "x_label": SW_LBL,

                "y_label": self.get_y_label(),

                'color': self.curve_to_save_color.currentText(),

                'line_style': self.curve_to_save_line.currentText(),

                'line_marker': self.curve_to_save_marker.currentText(),

                'line_width': 1,

                'add_axis': True
            })

        self.well \
            .graphicWindow \
            .draw_tracks(self.tab_name)
