"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QComboBox

from constants.permeability_constants import K_PHI_LBL, K_CORE_LBL, K_LBL, PHI_CORE_LBL, MD_LBL

from constants.sw_constants import POROSITY_E, PHI_CORE

from services.permeability_service import get_k_phi

from ui.GraphicWindow import GraphicWindow

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections


class PermeabilityKPhi(QWidgetWithSections):
    def __init__(self):
        super().__init__(K_PHI_LBL)

        self.init_ui(K_PHI_LBL)

    def init_ui(self,
                name):
        self.curves_section()

        super().init_ui(name)

        self.scatter_window = None

        #self.numeric_inputs.append(self.constant_textbox)

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.curve_to_save_marker, self.curve_to_save_line,
             self.curve_to_save_color, self.log_checkbox])

    def curves_section(self):
        self.permeability_layout = QVBoxLayout()

        self.permeability_layout.addWidget(QLabel(K_CORE_LBL))

        self.permeability_cbo = QComboBox()

        self.permeability_layout.addWidget(self.permeability_cbo)

        self.add_layout_to_layout(self.permeability_layout)

        self.phie_core_layout = QVBoxLayout()

        self.phie_core_cbo = QComboBox()

        self.phie_core_layout.addWidget(QLabel(PHI_CORE))

        self.phie_core_layout.addWidget(self.phie_core_cbo)

        self.add_layout_to_layout(self.phie_core_layout)

        self.phie_layout = QVBoxLayout()

        self.phie_layout.addWidget(QLabel(POROSITY_E))

        self.phie_cbo = QComboBox()

        self.phie_layout.addWidget(self.phie_cbo)

        self.add_layout_to_layout(self.phie_layout)

        self.curve_selectors.extend([self.permeability_cbo, self.phie_cbo, self.phie_core_cbo])

    def update_tab(self, well=None, force_update=False):
        if well is not None and (self.well is None or self.well.graphicWindow != well.graphicWindow):
            self.scatter_window = GraphicWindow(well.graphicWindow.get_tab_serialization,
                                                well.graphicWindow.set_tabs,
                                                well.graphicWindow.get_depth_unit,
                                                view_id=self.tab_name,
                                                stand_alone=True)

        if super().update_tab(well, force_update):
            return

    def preview(self):
        if not super().preview():
            return

        permeability = self.well \
            .wellModel \
            .get_partial_curve(self.permeability_cbo
                               .currentText(),
                               self.depth_curve_min,
                               self.depth_curve_max,
                               to_list=False)

        phie_core = self.well \
            .wellModel \
            .get_partial_curve(self.phie_core_cbo
                               .currentText(),
                               self.depth_curve_min,
                               self.depth_curve_max,
                               to_list=False)

        phie = self.well \
            .wellModel \
            .get_partial_curve(self.phie_cbo
                               .currentText(),
                               self.depth_curve_min,
                               self.depth_curve_max,
                               to_list=False)
        
        x_label = K_LBL

        given_x, self.curve_to_save, m, b, k_core_values, phi_core_values = get_k_phi(permeability,
                                                                                      phie_core,
                                                                                      phie)

        self.unit_to_save = MD_LBL

        min_phi = min(phi_core_values)

        max_phi = max(phi_core_values)

        x_values = np.arange(min_phi, max_phi, (max_phi - min_phi)/1000)

        x_values = list(x_values)

        x_values.append(max_phi)

        self.scatter_window.add_scatterplot({
            'tab_name': K_PHI_LBL,

            'track_name': K_PHI_LBL,

            'curve_name': K_PHI_LBL,

            "x_axis": phi_core_values,

            "y_axis": k_core_values,

            "left_label": K_CORE_LBL,

            "bottom_label": PHI_CORE_LBL,

            "custom_curve": True,

            "x_values": x_values,

            "y_values": np.exp(b + m * np.log(x_values)),

            "is_y_log": True
        })

        self.add_curve_with_y_label({
            'tab_name': K_PHI_LBL,

            'track_name': K_PHI_LBL,

            'curve_name': K_PHI_LBL,

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

        self.scatter_window.draw_tracks(self.tab_name)

        self.window.draw_tracks(self.tab_name)
