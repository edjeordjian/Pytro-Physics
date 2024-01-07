"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QPushButton, QLabel, QLineEdit, QHBoxLayout,
                             QGroupBox, QRadioButton, QVBoxLayout, QGridLayout)

from constants import MENU_CONSTANTS

from constants.MENU_CONSTANTS import SAVE_CURVE_BUTTON, CURVE_NAME_LABEL_2
from constants.general_constants import SAVED_CURVE_LBL

from constants.messages_constants import MISSING_CURVE_NAME, MISSING_WELL

from constants.pytrophysicsConstants import READ_MODE_WELL_NAME, SEE_WINDOW_LBL

from constants.tab_constants import DEPTH_LBL, ALL_FILE_LBL, CUSTOM_FILE_LBL

from services.constant_service import get_qle_group_name

from services.tools.string_service import is_positive_integer

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell

from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow

from ui.style.button_styles import PREVIEW_BUTTON_STYLE

from ui.visual_components.group_handler import set_enable_group_fields


class QWidgetWithWellGroups(QWidgetWithWell):
    def __init__(self,
                 tab_name):
        super().__init__(tab_name)

    def depth_section(self):
        self.depthGrpBox = QGroupBox(DEPTH_LBL)

        self.depthLayout = QVBoxLayout()

        self.depthFullLasRb = QRadioButton(ALL_FILE_LBL)

        self.depthFullLasRb.setChecked(True)

        self.depthFullLasRb.toggled.connect(self.on_selected)

        self.depthLayout \
            .addWidget(self.depthFullLasRb)

        self.depthCustomRb = QRadioButton(CUSTOM_FILE_LBL)

        self.depthCustomRb \
            .toggled \
            .connect(self.on_selected)

        self.depthLayout \
            .addWidget(self.depthCustomRb)

        self.depthGrpBox \
            .setLayout(self.depthLayout)

        self.gridLayout \
            .addWidget(self.depthGrpBox,
                       self.lines,
                       0,
                       1,
                       1)

        self.add_blank_column(column=2)

        self.add_layout_to_layout(self.depthLayout)

        self.add_blank_line()

    def groups_section(self,
                       additional_groups={}):
        self.groupsLbl = QLabel(MENU_CONSTANTS.GROUPS_LABEL)

        self.groupsQle = QLineEdit(self)

        self.groupsLayout = QHBoxLayout()

        self.groupsQle \
            .textChanged[str]\
            .connect(self.enable_number_of_groups)

        self.groupsQle \
            .setPlaceholderText("1")

        self.groupsQle \
            .setEnabled(False)

        self.groupsLayout.addWidget(self.groupsLbl,
                                    0)

        self.groupsLayout.addWidget(self.groupsQle,
                                    1)

        self.groupsLayout.addWidget(QLabel(""),
                                    2)

        self.gridLayout.addLayout(self.groupsLayout,
                                  self.lines,
                                  0,
                                  1,
                                  2)

        self.lines += 1

        self.add_blank_line()

        self.number_of_grups = 8

        self.groups = []

        group_first_column = {
            False: 0,
            True: 2
        }

        group_second_column = {
            False: 1,
            True: 3
        }

        for i in range(self.number_of_grups):
            group = {
                "Enabled": i == 0,
                "Group Label": QLabel("Grupo " + str(i + 1)),
                "Min Depth Label": QLabel(MENU_CONSTANTS.MIN_DEPTH_LABEL),
                "Min Depth QLE": QLineEdit(self),
                "Max Depth Label": QLabel(MENU_CONSTANTS.MAX_DEPTH_LABEL),
                "Max Depth QLE": QLineEdit(self),
                "Grid Layout": QGridLayout(self)
            }

            even_row = i % 2 == 0

            group["Grid Layout"].addWidget(group["Group Label"],
                                           1,
                                           group_first_column[even_row],
                                           alignment=Qt.AlignmentFlag.AlignLeft)

            group["Grid Layout"].addWidget(group["Min Depth Label"],
                                           2,
                                           group_first_column[even_row],
                                           alignment=Qt.AlignmentFlag.AlignLeft)

            group["Grid Layout"].addWidget(group["Min Depth QLE"],
                                           2,
                                           group_second_column[even_row],
                                           alignment=Qt.AlignmentFlag.AlignLeft)

            group["Grid Layout"].addWidget(group["Max Depth Label"],
                                           3,
                                           group_first_column[even_row],
                                           alignment=Qt.AlignmentFlag.AlignLeft)

            group["Grid Layout"].addWidget(group["Max Depth QLE"],
                                           3,
                                           group_second_column[even_row],
                                           alignment=Qt.AlignmentFlag.AlignLeft)

            self.numeric_inputs.extend([group["Min Depth QLE"], group["Max Depth QLE"]])

            row_idx = 3

            for field in additional_groups.keys():
                group[f"{field} Label"] = QLabel(field)

                group[get_qle_group_name(field)] = QLineEdit(additional_groups[field])

                row_idx += 1

                group["Grid Layout"].addWidget(group[f"{field} Label"],
                                               row_idx,
                                               group_first_column[even_row],
                                               alignment=Qt.AlignmentFlag.AlignLeft)

                group["Grid Layout"].addWidget(group[f"{field} QLE"],
                                               row_idx,
                                               group_second_column[even_row],
                                               alignment=Qt.AlignmentFlag.AlignLeft)

                self.numeric_inputs.append(group[get_qle_group_name(field)])

            if i > 0:
                set_enable_group_fields(group,
                                        False)

            self.gridLayout.addLayout(group["Grid Layout"], self.lines + int(i / 2), i % 2)

            self.groups.append(group)

        self.lines += int(self.number_of_grups / 2) + 1

    def save_and_draw_section(self):
        self.previewBtn = QPushButton(MENU_CONSTANTS.PREVIEW_BUTTON)

        self.previewBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.previewBtn \
            .clicked \
            .connect(
                lambda checked: self.preview()
            )

        self.add_blank_line()

        self.previewLayout = QHBoxLayout()

        self.seeWindowBtn = QPushButton(SEE_WINDOW_LBL)

        self.seeWindowBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.seeWindowBtn \
            .clicked \
            .connect(lambda: self.see_window())

        self.previewLayout.addWidget(self.previewBtn)

        self.previewLayout.addWidget(self.seeWindowBtn)

        self.add_layout_to_layout(self.previewLayout,
                                  column=1)

        self.add_blank_line()

        self.curveNameLbl = QLabel(CURVE_NAME_LABEL_2)

        self.curveNameQle = QLineEdit(self)

        self.curveNameLayout = QHBoxLayout()

        self.curveNameLayout \
            .addWidget(self.curveNameLbl,
                       alignment=Qt.AlignmentFlag.AlignLeft)

        self.curveNameLayout \
            .addWidget(self.curveNameQle,
                       alignment=Qt.AlignmentFlag.AlignRight)

        self.add_layout_to_layout(self.curveNameLayout)

        self.save_button = QPushButton(SAVE_CURVE_BUTTON)

        self.save_button \
            .clicked \
            .connect(
            lambda checked: self.save_curve()
        )

        self.add_widget_to_layout(self.save_button)

        self.add_blank_line()

    def save_curve(self):
        curve_name = self.curveNameQle \
            .text()

        if len(curve_name) == 0:
            return AlertWindow(MISSING_CURVE_NAME)

        self.well \
            .wellModel \
            .append_curve(curve_name,
                          self.curve_to_save)

        self.update_tab(self.well,
                        self.use_data_in_curve_selectors)

        InformationWindow(SAVED_CURVE_LBL)

    def on_selected(self):
        radio_button = self.sender()

        if radio_button.isChecked():
            print("You have selected : " + radio_button.text())

        self.groupsQle.setEnabled(self.depthCustomRb.isChecked())

        self.enable_number_of_groups(self.groupsQle.text())

    def preview(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            AlertWindow(MISSING_WELL)

            return False

        self.replace_commas_in_numeric_inputs()

        return True

    def enable_number_of_groups(self, text):
        for group in self.groups[1::]:
            set_enable_group_fields(group,
                                    False)

        if not self.groupsQle.isEnabled() or not is_positive_integer(text):
            return

        end = min(len(self.groups),
                  int(text))

        for i in range(1, end):
            set_enable_group_fields(self.groups[i],
                                    True)
