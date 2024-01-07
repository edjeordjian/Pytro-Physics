"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt

from constants.messages_constants import MISSING_WELL
from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS, READ_MODE_WELL_NAME, SEE_WINDOW_LBL
from constants.tab_constants import SP_TAB_NAME, SP_CURVE_NAME, GR_TAB_NAME, VSHALE_LBL
from constants.messages_constants import MISSING_CURVE_NAME, MISSING_CURVE_TO_SAVE, MISSING_WELL, \
    CURVE_ALREADY_EXISTS_QUESTION_LBL

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
import constants.VSHALE_MENU_CONSTANTS as VSHALE_MENU_CONSTANTS
from services.vshale_service import get_sp_vshale
from services.tools.string_service import is_number, is_positive_integer
from ui.characterizationTabs.vShaleTabs.previewer.singleCurveVShalePreviewer import SingleCurveVShalePreviewer
from ui.style.StyleCombos import color_combo_box, line_combo_box
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow
from ui.popUps.YesOrNoQuestion import YesOrNoQuestion

from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE
from ui.visual_components.combo_handler import update_curve_list
from ui.visual_components.group_handler import set_enable_group_fields

import numpy as np

from functools import reduce

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QGridLayout, QRadioButton,
                             QGroupBox, QCheckBox, QPushButton, QComboBox,
                             QLineEdit)


class SPTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("SP")

        self.prev_well_name = ""

        self.prev_well_update_amount = -1

        self.selectedCurve = ""

        self.setLayout(self.gridLayout)

        self.initUI()

    def initUI(self):
        row = 0

        self.curveLbl = QLabel("Curva SP: ")
        self.curveCbo = QComboBox(self)
        self.curveCbo.setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)
        self.curveCbo.textActivated[str].connect(self.selectCurve)
        self.curveColorCbo = color_combo_box()
        self.curveLineCbo = line_combo_box()
        self.curve_selectors.append(self.curveCbo)

        self.curveLayout = QHBoxLayout()
        self.curveLayout.addWidget(self.curveLbl)
        self.curveLayout.addWidget(self.curveCbo)
        self.curveLayout.addWidget(self.curveColorCbo)
        self.curveLayout.addWidget(self.curveLineCbo)
        self.gridLayout.addLayout(self.curveLayout, row, 0, 1, 2)

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
                "Min Curve Label": QLabel("SP Clean: "),
                "Min Curve QLE": QLineEdit(self),
                "Max Curve Label": QLabel("SP Shale: "),
                "Max Curve QLE": QLineEdit(self),
                "Grid Layout": QGridLayout(self),
                "Color": color_combo_box(),
                "Line": line_combo_box()
                #"Marker": marker_combo_box(),
            }

            group["Min Depth QLE"].setStyleSheet(QLE_NAME_STYLE)
            group["Min Curve QLE"].setStyleSheet(QLE_NAME_STYLE)
            group["Max Depth QLE"].setStyleSheet(QLE_NAME_STYLE)
            group["Max Curve QLE"].setStyleSheet(QLE_NAME_STYLE)

            group["Grid Layout"].addWidget(group["Group Label"], 1, 1)
            group["Grid Layout"].addWidget(group["Min Depth Label"], 2, 1)
            group["Grid Layout"].addWidget(group["Min Depth QLE"], 2, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            group["Grid Layout"].addWidget(group["Max Depth Label"], 3, 1)
            group["Grid Layout"].addWidget(group["Max Depth QLE"], 3, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            group["Grid Layout"].addWidget(group["Min Curve Label"], 4, 1)
            group["Grid Layout"].addWidget(group["Min Curve QLE"], 4, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            group["Grid Layout"].addWidget(group["Max Curve Label"], 5, 1)
            group["Grid Layout"].addWidget(group["Max Curve QLE"], 5, 2, alignment=Qt.AlignmentFlag.AlignLeft)
            group["Grid Layout"].addWidget(group["Color"], 6, 1)
            group["Grid Layout"].addWidget(group["Line"], 6, 2)
            #group["Grid Layout"].addWidget(group["Marker"], 6, 2)

            if i > 0:
                set_enable_group_fields(group,
                                        False)

            self.gridLayout.addLayout(group["Grid Layout"], row + int(i/2), i % 2)

            self.groups.append(group)

            self.numeric_inputs.extend([group["Min Depth QLE"], group["Max Depth QLE"],
                                        group["Max Curve QLE"], group["Min Curve QLE"]])

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

        self.add_serializable_attributes([self.curveCbo, self.curveColorCbo, self.curveLineCbo, self.depthFullLasRb,
                                          self.depthCustomRb, self.groupsQle, self.groups])

    def selectCurve(self):
        self.selectedCurve = self.curveCbo.currentText()

        depth_curve = self.well.wellModel.get_depth_curve()

        data_curve = self.well.wellModel.get_df_curve(self.selectedCurve)

        data_curve = data_curve[~np.isnan(data_curve)]

        for i in range(len(self.groups)):
            self.groups[i]["Min Depth QLE"].setPlaceholderText(str(min(depth_curve)))

            self.groups[i]["Max Depth QLE"].setPlaceholderText(str(max(depth_curve)))

            self.groups[i]["Min Curve QLE"].setPlaceholderText("CURVA SIN DATOS" if len(data_curve) == 0 else str(min(data_curve)))

            self.groups[i]["Max Curve QLE"].setPlaceholderText("CURVA SIN DATOS" if len(data_curve) == 0 else str(max(data_curve)))

    def on_selected(self):
        radio_button = self.sender()
        
        if radio_button.isChecked():
            print("Se eligió : " + radio_button.text())

        self.groupsQle.setEnabled(self.depthCustomRb.isChecked())

        self.enableGroupAmount(self.groupsQle.text())

    def enableGroupAmount(self, text):
        for group in self.groups[1::]:
            set_enable_group_fields(group,
                                    False)

        if (self.groupsQle.isEnabled() and is_positive_integer(text)):
            for i in range(1, min(len(self.groups), int(text))):
                set_enable_group_fields(self.groups[i], True)

    def setVShaleCurveName(self, text):
        self.vshale_curve_name = text

    def preview(self):
        if not super().preview():
            return

        self.replace_commas_in_numeric_inputs()

        config_curve = {
            'tab_name': self.tab_name,
            'track_name': self.tab_name,
            'curve_name': SP_CURVE_NAME,

            'x_axis': self.well.wellModel.get_df_curve(self.selectedCurve),
            'y_axis': self.well.wellModel.get_depth_curve(),
            "x_label": self.well.wellModel.get_label_for(self.selectedCurve),
            "y_label": self.get_y_label(),

            'color': self.curveColorCbo.currentText(),
            'line_style': self.curveLineCbo.currentText(),
            'line_marker': LINE_MARKER_CONSTANTS["NONE"],
            'line_width': 1
        }

        config_vshale = {
            'tab_name': self.tab_name,
            'track_name': SP_TAB_NAME,
            'curve_name': SP_TAB_NAME,

            'x_axis': self.get_vshale(),
            'y_axis': self.well.wellModel.get_depth_curve(),
            "x_label": VSHALE_LBL,
            "y_label": self.get_y_label(),

            'color': 'Naranja',
            'line_style': 'Solida',
            'line_marker': LINE_MARKER_CONSTANTS["NONE"],
            'line_width': 1
        }

        self.previewWidget = SingleCurveVShalePreviewer(self.well.graphicWindow,
                                                        config_curve,
                                                        config_vshale,
                                                        self.groups,
                                                        self.tab_name)

    def get_vshale(self):
        print("Curva elegida: ", self.selectedCurve)
        print("Esa curva tiene len: ", len(self.well.wellModel.get_df_curve(self.selectedCurve)))

        vshale_sp_groups = []

        for group in self.groups:
            if group["Min Depth QLE"].isEnabled():
                forced_clean_value = group["Min Curve QLE"].text() if is_number(group["Min Curve QLE"].text()) else None

                forced_shale_value = group["Max Curve QLE"].text() if is_number(group["Max Curve QLE"].text()) else None

                curve_data = self.well.wellModel.get_partial_ranged_df_curve(
                        self.selectedCurve,
                        group["Min Depth QLE"].text(),
                        group["Max Depth QLE"].text(),
                        group["Min Curve QLE"].text(),
                        group["Max Curve QLE"].text())

                vshale_sp_groups.append(
                        get_sp_vshale(curve_data,
                                      forced_clean_value,
                                      forced_shale_value))

        return reduce(self.well.wellModel.combine_curves,
                      vshale_sp_groups)


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

            update_curve_list(self.curveCbo,
                              self.well)

            if len(self.well.wellModel.get_curve_names()) == 0:
                return

        if self.well is None:
            return

        self.selectedCurve = self.well \
            .wellModel \
            .get_curve_names()[self.curveCbo
                                   .currentIndex()]

        self.window = self.well \
                          .graphicWindow

        self.selectCurve()

    def obtain_tab_name(self):
        return self.tab_name
