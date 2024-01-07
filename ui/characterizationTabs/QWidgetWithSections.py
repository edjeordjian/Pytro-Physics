"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QPushButton, QLabel, QLineEdit, QHBoxLayout,
                             QGroupBox, QRadioButton, QVBoxLayout, QCheckBox)

from constants import MENU_CONSTANTS

from constants.MENU_CONSTANTS import SAVE_CURVE_BUTTON, CURVE_NAME_LABEL_2

from constants.general_constants import GROUP_RANGE_ERROR

from constants.messages_constants import MISSING_CURVE_NAME, MISSING_CURVE_TO_SAVE, MISSING_WELL, \
    CURVE_ALREADY_EXISTS_QUESTION_LBL

from constants.permeability_constants import LOG_LABEL

from constants.porosity_constants import POROSITY_STYLE_LBL

from constants.pytrophysicsConstants import READ_MODE_WELL_NAME, SEE_WINDOW_LBL

from constants.tab_constants import (DEPTH_LBL, ALL_FILE_LBL, CUSTOM_FILE_LBL, MIN_DEPTH_LBL,
                                     MAX_DEPTH_LBL)

from services.tools.string_service import is_number, is_positive_number

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
from ui.popUps.YesOrNoQuestion import YesOrNoQuestion

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.alerts import get_positive_value_error_alert

from ui.popUps.informationWindow import InformationWindow

from ui.style.StyleCombos import color_combo_box, line_combo_box, marker_combo_box

from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE

from numpy import float64

import pandas as pd


class QWidgetWithSections(QWidgetWithWell):
    def __init__(self,
                 tab_name):
        super().__init__(tab_name)

        self.unit_to_save = ""

        self.curve_to_save = None

        self.setLayout(self.gridLayout)

    def init_ui(self,
                name):
        self.curve_to_save_style_section(f"{POROSITY_STYLE_LBL} {name}")

        self.depth_section()

        self.save_and_draw_section()

    def curve_to_save_style_section(self,
                                    section_header):
        self.curve_to_save_style_lbl = QLabel(section_header)

        self.curve_to_save_color = color_combo_box()

        self.curve_to_save_line = line_combo_box()

        self.curve_to_save_marker = marker_combo_box()

        self.add_widget_to_layout(self.curve_to_save_style_lbl)

        self.add_widget_to_layout(self.curve_to_save_color,
                                  column=0,
                                  alignment=Qt.AlignmentFlag.AlignLeft,
                                  next_line=False)

        self.add_widget_to_layout(self.curve_to_save_line,
                                  column=1,
                                  alignment=Qt.AlignmentFlag.AlignLeft,
                                  next_line=False)

        self.add_widget_to_layout(self.curve_to_save_marker,
                                  alignment=Qt.AlignmentFlag.AlignLeft,
                                  column=2)

        self.add_blank_line()

        self.log_label = QLabel(LOG_LABEL)

        self.log_checkbox = QCheckBox()

        self.log_layout = QHBoxLayout()

        self.log_layout.addWidget(self.log_label)

        self.log_layout.addWidget(self.log_checkbox)

        self.add_layout_to_layout(self.log_layout)

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

        self.numeric_inputs.extend([self.customMinDepthQle,
                                    self.customMaxDepthQle])

    def save_and_draw_section(self, btn_column=1):
        self.previewBtn = QPushButton(MENU_CONSTANTS.PREVIEW_BUTTON)

        self.previewBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.previewBtn \
            .clicked \
            .connect(
            lambda: self.preview()
        )

        self.previewLayout = QHBoxLayout()

        self.seeWindowBtn = QPushButton(SEE_WINDOW_LBL)

        self.seeWindowBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.seeWindowBtn \
            .clicked \
            .connect(lambda: self.see_window())

        self.previewLayout.addWidget(self.previewBtn)

        self.previewLayout.addWidget(self.seeWindowBtn)

        self.add_layout_to_layout(self.previewLayout,
                                  column=btn_column)

        self.add_blank_line()

        self.curveNameLbl = QLabel(CURVE_NAME_LABEL_2)

        self.curveNameQle = QLineEdit(self)

        self.curveNameLayout = QHBoxLayout()

        self.curveNameLayout \
            .addWidget(self.curveNameLbl)

        self.curveNameLayout \
            .addWidget(self.curveNameQle)

        self.add_layout_to_layout(self.curveNameLayout)

        self.save_button = QPushButton(SAVE_CURVE_BUTTON)

        self.save_button \
            .clicked \
            .connect(
            lambda checked: self.save_curve()
        )

        self.save_button.setStyleSheet(SAVE_BUTTON_STYLE)

        self.add_widget_to_layout(self.save_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.add_blank_line()

    def save_curve(self):
        curve_name = self.curveNameQle \
            .text()

        if len(curve_name) == 0:
            return AlertWindow(MISSING_CURVE_NAME)

        if self.curve_to_save is None:
            return AlertWindow(MISSING_CURVE_TO_SAVE)

        saved_ok = self.well \
                       .wellModel \
                       .append_curve(curve_name,
                                     self.curve_to_save,
                                     unit=self.unit_to_save)

        if not saved_ok:
            YesOrNoQuestion(CURVE_ALREADY_EXISTS_QUESTION_LBL,
                            lambda: (self.well
                                        .wellModel
                                        .append_curve(curve_name,
                                                      self.curve_to_save,
                                                      unit=self.unit_to_save,
                                                      force_name=True),
                                    self.update_tab(self.well,
                                                    self.use_data_in_curve_selectors),
                                    InformationWindow("Curva guardada")),
                            lambda: (InformationWindow("No se guardó la curva"))
            )

        else:
            self.update_tab(self.well,
                        self.use_data_in_curve_selectors)
            InformationWindow("Curva guardada")


    def on_selected(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return

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

    def preview(self):
        if not super().preview():
            return False

        self.log_lbl = " (ln)"

        len_min = len(self.customMinDepthQle.text())

        len_max = len(self.customMaxDepthQle.text())

        self.depth_curve = self.well.wellModel.get_depth_curve()

        self.depth_curve_min = min(self.depth_curve)

        self.depth_curve_max = max(self.depth_curve)

        self.replace_commas_in_numeric_inputs()

        if not self.depthCustomRb \
                .isChecked():
            return True

        if (len_min != 0 and (not is_number(self.customMinDepthQle.text())
                              or len_max == 0
                              or float(self.customMinDepthQle.text()) < self.depth_curve_min)):
            AlertWindow(GROUP_RANGE_ERROR)

            return False

        if (len_max != 0 and (not is_number(self.customMaxDepthQle.text())
                              or len_min == 0
                              or float(self.customMaxDepthQle.text()) > self.depth_curve_max)):
            AlertWindow(GROUP_RANGE_ERROR)

            return False

        if len_min != 0:
            self.depth_curve_min = float(self.customMinDepthQle.text())

            self.depth_curve_max = float(self.customMaxDepthQle.text())

        return True

    def set_curve_to_save(self,
                          curve_data,
                          data_is_full_size=True,
                          unit=""):
        df_aux_to_save = pd.DataFrame(data={
            "depth": self.depth_curve
        })

        df_aux_to_save = df_aux_to_save.set_index("depth")

        if not data_is_full_size:
            df_aux_to_save["to_save"] = None

            df_aux_to_save["to_save"].loc[self.depth_curve_min:self.depth_curve_max] = curve_data

        else:
            df_aux_to_save["to_save"] = curve_data

        self.unit_to_save = unit

        self.curve_to_save = df_aux_to_save["to_save"].to_numpy(dtype=float64)

    def get_constant_curve_data(self,
                                cbo_input,
                                textbox_input,
                                constant_name):
        matrix = cbo_input.currentText()

        constant = textbox_input.text()

        if len(constant) != 0:
            if not is_positive_number(constant):
                return get_positive_value_error_alert(constant_name)

            return float(constant)

        return self.get_partial_curve(matrix)

    def get_partial_curve(self,
                          text):
        return self.well.wellModel.get_partial_curve(text,
                                                     self.depth_curve_min,
                                                     self.depth_curve_max,
                                                     to_list=False)

    def get_partial_constant_curve(self, constant):
        return [constant] * len(self.well
                                    .wellModel
                                    .get_depth_curve())

    def update_tab(self, well=None, force_update=False):
        if force_update or not super().update_tab(well):
            return False

        self.window = self.well \
                          .graphicWindow

        return True
