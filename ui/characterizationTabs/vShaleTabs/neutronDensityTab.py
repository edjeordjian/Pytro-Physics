"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from functools import reduce

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox, QPushButton,
                             QComboBox, QLineEdit)

from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS, READ_MODE_WELL_NAME, SEE_WINDOW_LBL
from constants.tab_constants import ND_TAB_NAME, NEUTRON_CURVE_NAME, DENSITY_CURVE_NAME, VSHALE_LBL
from constants.messages_constants import (MISSING_CURVE_NAME, MISSING_CURVE_TO_SAVE,
                                          CURVE_ALREADY_EXISTS_QUESTION_LBL)

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
import constants.VSHALE_MENU_CONSTANTS as VSHALE_MENU_CONSTANTS
from ui.popUps.alertWindow import AlertWindow
from services.vshale_service import get_neutron_density_vshale
from services.tools.string_service import is_number, is_positive_integer
from ui.popUps.informationWindow import InformationWindow
from ui.popUps.YesOrNoQuestion import YesOrNoQuestion
from ui.style.StyleCombos import color_combo_box, line_combo_box
from ui.style.button_styles import QLE_NAME_STYLE, SAVE_BUTTON_STYLE, PREVIEW_BUTTON_STYLE
from ui.visual_components.combo_handler import update_curve_list
from ui.visual_components.group_handler import set_enable_group_fields

import numpy as np


class NeutronDensityTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("Neutrón densidad")

        self.prev_well_update_amount = -1

        self.tab_name = "Neutrón densidad"

        self.selectedCurveNeutron = None

        self.selectedCurveDensity = None

        self.setLayout(self.gridLayout)

        self.initUI()

    def initUI(self):
        row = 0

        self.curveNeutronLbl = QLabel("Curva Neutron: ")
        self.curveNeutronCbo = QComboBox(self)
        self.curveNeutronCbo.setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)
        self.curveNeutronCbo.textActivated[str].connect(self.selectCurveNeutron)
        self.curve_selectors.append(self.curveNeutronCbo)

        self.curveNeutronColorCbo = color_combo_box()
        self.curveNeutronLineCbo = line_combo_box()

        self.curveNeutronLayout = QHBoxLayout()
        self.curveNeutronLayout.addWidget(self.curveNeutronLbl)
        self.curveNeutronLayout.addWidget(self.curveNeutronCbo)
        self.curveNeutronLayout.addWidget(self.curveNeutronColorCbo)
        self.curveNeutronLayout.addWidget(self.curveNeutronLineCbo)
        self.gridLayout.addLayout(self.curveNeutronLayout, row, 0, 1, 2)


        ########################################################################

        row += 1

        self.curveDensityLbl = QLabel("Curva Densidad: ")
        self.curveDensityCbo = QComboBox(self)
        self.curveDensityCbo.setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)
        self.curveDensityCbo.textActivated[str].connect(self.selectCurveDensity)
        self.curve_selectors.append(self.curveDensityCbo)

        self.curveDensityColorCbo = color_combo_box()
        self.curveDensityLineCbo = line_combo_box()

        self.curveDensityLayout = QHBoxLayout()
        self.curveDensityLayout.addWidget(self.curveDensityLbl)
        self.curveDensityLayout.addWidget(self.curveDensityCbo)
        self.curveDensityLayout.addWidget(self.curveDensityColorCbo)
        self.curveDensityLayout.addWidget(self.curveDensityLineCbo)
        self.gridLayout.addLayout(self.curveDensityLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.depthGrpBox = QGroupBox(VSHALE_MENU_CONSTANTS.DEPTH_LABEL)
        #self.grpbox.setFont(QFont("Times New Roman", 15))

        # this is vbox layout
        self.depthLayout = QHBoxLayout()

        # these are the radiobuttons
        self.depthFullLasRb = QRadioButton(VSHALE_MENU_CONSTANTS.DEPTH_FULL_LAS)
        self.depthFullLasRb.setChecked(True)
        #self.depthFullLasRb.setFont(QFont("Times New Roman", 14))
        self.depthFullLasRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthFullLasRb)

        self.depthCustomRb = QRadioButton(VSHALE_MENU_CONSTANTS.DEPTH_CUSTOM)
        #self.depthCustomRb.setFont(QFont("Times New Roman", 14))
        self.depthCustomRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthCustomRb)

        self.depthGrpBox.setLayout(self.depthLayout)

        self.gridLayout.addWidget(self.depthGrpBox, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.groupsLbl = QLabel(VSHALE_MENU_CONSTANTS.GROUPS_LABEL)
        self.groupsQle = QLineEdit(self)
        self.groupsLayout = QHBoxLayout()
        self.groupsQle.textChanged[str].connect(self.enableGroupAmount)
        self.groupsQle.setPlaceholderText("1")
        self.groupsQle.setEnabled(False)
        self.groupsLayout.addWidget(self.groupsLbl)
        self.groupsLayout.addWidget(self.groupsQle, alignment=Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addLayout(self.groupsLayout, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1
        groupAmount = 8

        self.groups = []
        for i in range(groupAmount):
            group = {
                "Enabled": i == 0,
                "Group Label": QLabel("Grupo " + str(i + 1)),
                "Min Depth Label": QLabel(VSHALE_MENU_CONSTANTS.MIN_DEPTH_LABEL),
                "Min Depth QLE": QLineEdit(self),
                "Max Depth Label": QLabel(VSHALE_MENU_CONSTANTS.MAX_DEPTH_LABEL),
                "Max Depth QLE": QLineEdit(self),
                "Neutron Shale Label": QLabel("PHI Neutron Shale: "),
                "Neutron Shale QLE": QLineEdit(self),
                "Density Shale Label": QLabel("PHI Densidad Shale: "),
                "Density Shale QLE": QLineEdit(self),
                "Grid Layout": QGridLayout(self),
            }

            group["Min Depth QLE"].setStyleSheet(QLE_NAME_STYLE)
            group["Max Depth QLE"].setStyleSheet(QLE_NAME_STYLE)
            group["Neutron Shale QLE"].setStyleSheet(QLE_NAME_STYLE)
            group["Density Shale QLE"].setStyleSheet(QLE_NAME_STYLE)

            group["Grid Layout"].addWidget(group["Group Label"], 1, 1)
            group["Grid Layout"].addWidget(group["Min Depth Label"], 2, 1)
            group["Grid Layout"].addWidget(group["Min Depth QLE"], 2, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            group["Grid Layout"].addWidget(group["Max Depth Label"], 3, 1)
            group["Grid Layout"].addWidget(group["Max Depth QLE"], 3, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            group["Grid Layout"].addWidget(group["Neutron Shale Label"], 4, 1)
            group["Grid Layout"].addWidget(group["Neutron Shale QLE"], 4, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            group["Grid Layout"].addWidget(group["Density Shale Label"], 5, 1)
            group["Grid Layout"].addWidget(group["Density Shale QLE"], 5, 2, alignment=Qt.AlignmentFlag.AlignLeft)

            if i > 0:
                set_enable_group_fields(group,
                                        False)

            self.gridLayout.addLayout(group["Grid Layout"], row + int(i/2), i % 2)

            self.groups.append(group)

            self.numeric_inputs.extend([group["Min Depth QLE"], group["Max Depth QLE"],
                                        group["Density Shale QLE"], group["Neutron Shale QLE"]])

        ########################################################################

        row += int(groupAmount/2) + 1

        self.previewBtn = QPushButton(VSHALE_MENU_CONSTANTS.PREVIEW_BUTTON)

        self.previewBtn.clicked.connect(
            lambda checked: self.preview()
        )

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 1)

        row += 1

        self.previewBtn \
            .setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.previewLayout = QHBoxLayout()

        self.seeWindowBtn = QPushButton(SEE_WINDOW_LBL)

        self.seeWindowBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.seeWindowBtn \
            .clicked \
            .connect(lambda: self.see_window())

        self.previewLayout.addWidget(self.previewBtn)

        self.previewLayout.addWidget(self.seeWindowBtn)

        self.gridLayout.addLayout(self.previewLayout, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        ########################################################################

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 1)

        row += 1

        self.curveNameLbl = QLabel(VSHALE_MENU_CONSTANTS.CURVE_NAME_LABEL)
        self.curveNameQle = QLineEdit(self)
        self.curveNameQle.textChanged[str].connect(self.setVShaleCurveName)
        self.curveNameLayout = QHBoxLayout()
        self.curveNameLayout.addWidget(self.curveNameLbl)

        self.curveNameQle.setStyleSheet(QLE_NAME_STYLE)

        self.curveNameLayout.addWidget(self.curveNameQle, alignment=Qt.AlignmentFlag.AlignLeft)

        self.gridLayout.addLayout(self.curveNameLayout, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1

        self.saveCurveBtn = QPushButton(VSHALE_MENU_CONSTANTS.SAVE_CURVE_BUTTON)
        self.saveCurveBtn.clicked.connect(
            lambda checked: self.saveCurve()
        )

        self.saveCurveBtn \
            .setStyleSheet(SAVE_BUTTON_STYLE)

        self.gridLayout.addWidget(self.saveCurveBtn, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        if self.selectedCurveNeutron != None and self.selectedCurveDensity != None:
            self.groups[0]["Min Depth QLE"].setPlaceholderText(str(min(self.well.wellModel.get_depth_curve())))
            self.groups[0]["Max Depth QLE"].setPlaceholderText(str(max(self.well.wellModel.get_depth_curve())))
            self.groups[0]["Neutron Shale QLE"].setPlaceholderText(str(max(self.well.get_df_curve(self.selectedCurveNeutron))))
            self.groups[0]["Density Shale QLE"].setPlaceholderText(str(max(self.well.get_df_curve(self.selectedCurveDensity))))

        self.add_serializable_attributes([self.curveNeutronCbo, self.curveNeutronColorCbo, self.curveNeutronLineCbo,
                                          self.curveDensityCbo, self.curveDensityColorCbo, self.curveDensityLineCbo,
                                          self.depthFullLasRb, self.depthCustomRb, self.groupsQle, self.groups])

    def selectCurveNeutron(self):
        self.selectedCurveNeutron = self.curveNeutronCbo.currentText()

        depth_curve = self.well.wellModel.get_depth_curve()

        data_curve = self.well.wellModel.get_df_curve(self.selectedCurveNeutron)

        data_curve = data_curve[~np.isnan(data_curve)]

        for i in range(len(self.groups)):
            self.groups[i]["Min Depth QLE"].setPlaceholderText(str(min(depth_curve)))

            self.groups[i]["Max Depth QLE"].setPlaceholderText(str(max(depth_curve)))

            self.groups[i]["Neutron Shale QLE"].setPlaceholderText("CURVA SIN DATOS" if len(data_curve) == 0 else str(max(data_curve)))


    def selectCurveDensity(self):
        self.selectedCurveDensity = self.curveDensityCbo.currentText()

        depth_curve = self.well.wellModel.get_depth_curve()

        data_curve = self.well.wellModel.get_df_curve(self.selectedCurveDensity)

        data_curve = data_curve[~np.isnan(data_curve)]

        for i in range(len(self.groups)):
            self.groups[i]["Min Depth QLE"].setPlaceholderText(str(min(depth_curve)))

            self.groups[i]["Max Depth QLE"].setPlaceholderText(str(max(depth_curve)))

            self.groups[i]["Density Shale QLE"].setPlaceholderText("CURVA SIN DATOS" if len(data_curve) == 0 else str(max(data_curve)))

    # method or slot for the toggled signal
    def on_selected(self):
        radio_button = self.sender()

        if radio_button.isChecked():
            print("Se eligió" + radio_button.text())

        self.groupsQle.setEnabled(self.depthCustomRb.isChecked())
        self.enableGroupAmount(self.groupsQle.text())

    def enableGroupAmount(self, text):
        for group in self.groups[1::]:
            set_enable_group_fields(group,
                                    False)

        if (self.groupsQle.isEnabled() and is_positive_integer(text)):
            for i in range(1, min(len(self.groups), int(text))):
                set_enable_group_fields(self.groups[i],
                                        True)

    def setVShaleCurveName(self, text):
        self.vshale_curve_name = text

    def preview(self):
        if not super().preview():
            return

        self.replace_commas_in_numeric_inputs()

        config_curve = {
            'tab_name': self.tab_name,
            'track_name': 'Neutron',
            'curve_name': NEUTRON_CURVE_NAME,

            'x_axis': self.well.wellModel.get_df_curve(self.selectedCurveNeutron),
            'y_axis': self.well.wellModel.get_depth_curve(),
            "x_label": self.well.wellModel.get_label_for(self.selectedCurveNeutron),
            "y_label": self.get_y_label(),

            'color': self.curveNeutronColorCbo.currentText(),
            'line_style': self.curveNeutronLineCbo.currentText(),
            'line_marker': LINE_MARKER_CONSTANTS["NONE"],
            'track_number': 1
        }

        config_curve_2 = {
            'tab_name': self.tab_name,
            'track_name': 'Densidad',
            'curve_name': DENSITY_CURVE_NAME,

            'x_axis': self.well.wellModel.get_df_curve(self.selectedCurveDensity),
            'y_axis': self.well.wellModel.get_depth_curve(),
            "x_label": self.well.wellModel.get_label_for(self.selectedCurveNeutron),
            "y_label": self.get_y_label(),

            'color': self.curveDensityColorCbo.currentText(),
            'line_style': self.curveDensityLineCbo.currentText(),
            'line_marker': LINE_MARKER_CONSTANTS["NONE"],
            'track_number': 1
        }

        config_vshale = {
            'tab_name': self.tab_name,
            'track_name': ND_TAB_NAME,
            'curve_name': ND_TAB_NAME,

            'x_axis': self.get_vshale(),
            'y_axis': self.well.wellModel.get_depth_curve(),
            "x_label": VSHALE_LBL,
            "y_label": self.get_y_label(),

            'color': 'Naranja',
            'line_style': 'Solida',
            'line_marker': LINE_MARKER_CONSTANTS["NONE"],
            'line_width': 1
        }

        self.well.graphicWindow.add_curve(config_curve)

        self.well.graphicWindow.add_curve(config_curve_2)

        self.well.graphicWindow.add_curve(config_vshale)

        self.well.graphicWindow.draw_tracks(self.tab_name)

    def get_vshale(self):
        print("Curva elegida: ", self.selectedCurveNeutron)
        print("Esa curva tiene len: ", len(self.well.wellModel.get_df_curve(self.selectedCurveNeutron)))
        print("Curva elegida: ", self.selectedCurveDensity)
        print("Esa curva tiene len: ", len(self.well.wellModel.get_df_curve(self.selectedCurveDensity)))

        # Curvas VShale por grupo
        vshale_neutron_density_groups = []

        for group in self.groups:
            if group["Min Depth QLE"].isEnabled():
                forced_phi_n_shale_value = group["Neutron Shale QLE"].text() if is_number(group["Neutron Shale QLE"].text()) else None

                forced_phi_d_shale_value = group["Density Shale QLE"].text() if is_number(group["Density Shale QLE"].text()) else None

                vshale_neutron_density_groups.append(get_neutron_density_vshale(self.well.wellModel.get_partial_ranged_df_curve(self.selectedCurveNeutron,
                                                                                            group["Min Depth QLE"].text(),
                                                                                            group["Max Depth QLE"].text(),
                                                                                            "",
                                                                                            group["Neutron Shale QLE"].text()),
                                                                                self.well.wellModel.get_partial_ranged_df_curve(self.selectedCurveDensity,
                                                                                            group["Min Depth QLE"].text(),
                                                                                            group["Max Depth QLE"].text(),
                                                                                            "",
                                                                                            group["Density Shale QLE"].text()),
                                                                                forced_phi_n_shale_value,
                                                                                forced_phi_d_shale_value))

        return reduce(self.well.wellModel.combine_curves, vshale_neutron_density_groups)


    def saveCurve(self):
        if not super().preview():
            return

        curve_name = self.vshale_curve_name

        if len(curve_name) == 0:
            return AlertWindow(MISSING_CURVE_NAME)

        self.curve_to_save = self.get_vshale()
        
        if self.curve_to_save is None:
            return AlertWindow(MISSING_CURVE_TO_SAVE)

        saved_ok = self.well \
                       .wellModel \
                       .append_curve(curve_name,
                                     self.curve_to_save)

        if not saved_ok:
            YesOrNoQuestion(CURVE_ALREADY_EXISTS_QUESTION_LBL,
                            lambda: (self.well
                                        .wellModel
                                        .append_curve(curve_name,
                                                      self.curve_to_save,
                                                      force_name=True),
                                    self.update_tab(self.well),
                                    InformationWindow("Curva guardada")),
                            lambda: (InformationWindow("No se guardo la curva"))
            )
        else:
            self.update_tab(self.well)
            InformationWindow("Curva guardada")


    def update_tab(self, well=None, force_update=False):
        if well is not None and well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return

        if not force_update:
            if not super().update_tab(well):
                return

            update_curve_list(self.curveNeutronCbo,
                              self.well)

            update_curve_list(self.curveDensityCbo,
                              self.well)

            if len(self.well.wellModel.get_curve_names()) == 0:
                return

        if self.well is None:
            return

        self.window = self.well \
            .graphicWindow

        if self.curveNeutronCbo \
               .currentIndex() < 0:
            self.curveNeutronCbo.setCurrentIndex(0)

        self.selectedCurveNeutron = self.well \
            .wellModel \
            .get_curve_names()[self.curveNeutronCbo
                                   .currentIndex()]

        self.selectCurveNeutron()

        if self.curveDensityCbo \
               .currentIndex() < 0:
            self.curveDensityCbo.setCurrentIndex(0)

        self.selectedCurveDensity = self.well \
            .wellModel \
            .get_curve_names()[self.curveDensityCbo
                                   .currentIndex()]

        self.selectCurveDensity()

    def obtain_tab_name(self):
        return self.tab_name
