"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QPushButton, QComboBox, QCheckBox, QInputDialog, QLineEdit)

from PyQt6.QtCore import Qt

from constants.general_constants import DEFAULT_SCATTERPLOT_CONFIG

from constants.messages_constants import (TRACK_MISSING, NEW_TRACK_TITLE, NAME_OF_THE_NEW_TRACK, MISSING_WELL,
                                          FILL_REVERSE_CURVE, MISSING_CURVE, MISSING_MARKER_IN_SCATTER,
                                          CONFIRM_DELETION_LBL, KEEP_SCALE_ERROR, INVALID_NUMERIC_INPUT)
from constants.porosity_constants import ADJUST_RANGE_LBL, DEFAULT_ADJUSTED_MAX_LBL, ADJUSTED_MAX_LBL, \
    DEFAULT_ADJUSTED_MIN_LBL, ADJUSTED_MIN_LBL

from constants.tab_constants import EVERY_TAB
from services.tools.number_service import get_log10
from services.tools.string_service import are_numbers, is_positive_number, is_number

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
from ui.style.button_styles import SAVE_BUTTON_STYLE

from constants.pytrophysicsConstants import (TOP_MENU_CONSTANTS, LINE_MARKER_CONSTANTS, SEE_ALL_LBL, DELETE_ALL_LBL)

from ui.popUps.YesOrNoQuestion import YesOrNoQuestion

from ui.popUps.alertWindow import AlertWindow
from ui.style.LineColors import get_color_index
from ui.style.LineMarkers import LineMarkers
from ui.style.LineTypes import LineTypes

from ui.style.StyleCombos import color_combo_box, marker_combo_box, line_combo_box

from ui.visual_components.combo_handler import update_curve_list, disable_elements_with_component


class CurvesWindow(QWidgetWithWell):
    def __init__(self):
        super().__init__("Curves window")

        self.gridLayout = QGridLayout()
        # Esto es para agrupar elementos y que no ocupen toda la pantalla
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        row = 0

        ########################### TRACKS ################################
        self.track_title = QLabel(TOP_MENU_CONSTANTS["TRACK_CBO_PLACEHOLDER"])

        self.trackCbo = QComboBox(self)
        self.trackCbo.setPlaceholderText(TOP_MENU_CONSTANTS["CHOOSE_PLACEHOLDER"])
        self.trackCbo.textActivated[str].connect(self.select_track)

        self.trackLayout = QVBoxLayout()
        self.trackLayout.addWidget(self.track_title)
        self.trackLayout.addWidget(self.trackCbo)
        self.gridLayout.addLayout(self.trackLayout, row, 0)

        row += 1

        self.track_button_layout = QHBoxLayout(self)

        self.track_button_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.add_track_button = QPushButton(TOP_MENU_CONSTANTS['NEW_TRACK_LABEL'])
        self.add_track_button.setStyleSheet(SAVE_BUTTON_STYLE)

        self.add_track_button \
            .clicked \
            .connect(
            lambda checked: self.addTrack()
        )

        self.delete_track_button = QPushButton(TOP_MENU_CONSTANTS['DELETE_TRACK_BUTTON'])
        self.delete_track_button.setStyleSheet(SAVE_BUTTON_STYLE)

        self.delete_track_button \
            .clicked \
            .connect(
            lambda checked: self.removeTrack()
        )

        self.track_button_layout.addWidget(self.delete_track_button)

        self.track_button_layout.addWidget(self.add_track_button)

        self.gridLayout.addLayout(self.track_button_layout, row, 0)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        ########################### NEW CURVE ################################
        self.curve_to_add_cbo = QComboBox()

        self.add_curve_color = color_combo_box()

        self.add_curve_line = line_combo_box()

        self.add_curve_marker = marker_combo_box()

        self.add_curve_label = QLabel(TOP_MENU_CONSTANTS["ADD_NEW_CURVE"])

        self.gridLayout.addWidget(self.add_curve_label, row, 0)

        row += 1

        self.gridLayout.addWidget(self.curve_to_add_cbo, row, 0)

        self.new_curve_custom_config_layout = QHBoxLayout()

        self.new_curve_custom_config_layout.addWidget(self.add_curve_color)

        self.new_curve_custom_config_layout.addWidget(self.add_curve_line)

        self.new_curve_custom_config_layout.addWidget(self.add_curve_marker)

        self.gridLayout.addLayout(self.new_curve_custom_config_layout, row, 1)

        row += 1

        self.create_curve_btn = QPushButton(TOP_MENU_CONSTANTS["ADD_CURVE_BUTTON"])
        
        self.create_curve_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.create_curve_btn.clicked.connect(
            lambda: self.append_new_curve()
        )

        self.gridLayout.addWidget(self.create_curve_btn, row, 0)

        self.add_curve_log_label = QLabel(TOP_MENU_CONSTANTS["LOG_AXIS_LABEL"])

        self.add_curve_log_checkbox = QCheckBox('', self)

        self.add_curve_reverse_x_label = QLabel(TOP_MENU_CONSTANTS["REVERSE_X_LABEL"])

        self.add_curve_reverse_x_checkbox = QCheckBox('', self)

        self.add_curve_cummulative_label = QLabel(TOP_MENU_CONSTANTS["KEEP_SCALE"])

        self.add_curve_cummulative_checkbox = QCheckBox()

        self.create_curve_layout = QHBoxLayout()

        self.create_curve_layout.addWidget(self.add_curve_log_label)

        self.create_curve_layout.addWidget(self.add_curve_log_checkbox)

        self.create_curve_layout.addWidget(self.add_curve_reverse_x_label)

        self.create_curve_layout.addWidget(self.add_curve_reverse_x_checkbox)

        self.create_curve_layout.addWidget(self.add_curve_cummulative_label)

        self.create_curve_layout.addWidget(self.add_curve_cummulative_checkbox)

        self.gridLayout.addLayout(self.create_curve_layout, row, 1)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        ########################### CURVES ################################
        self.curve_vertical_layout = QVBoxLayout()
        self.curve_title = QLabel(TOP_MENU_CONSTANTS["CURVE_CBO_PLACEHOLDER"])
        self.curve_vertical_layout.addWidget(self.curve_title)

        self.gridLayout \
            .addLayout(self.curve_vertical_layout,
                       row,
                       0)

        row += 1

        self.curveCbo = QComboBox(self)

        self.curveCbo.currentIndexChanged.connect(self.adjust_curve_options)

        self.curveCbo.setPlaceholderText(TOP_MENU_CONSTANTS["CHOOSE_PLACEHOLDER"])

        self.curveLayout = QHBoxLayout()

        self.colorStyleCbo = color_combo_box()

        self.lineTypeCbo = line_combo_box()

        self.markerStyleCbo = marker_combo_box()

        self.curveLayout.addWidget(self.curveCbo)

        self.gridLayout.addLayout(self.curveLayout, row, 0)

        self.curveLayout2 = QHBoxLayout()

        self.curveLayout2.addWidget(self.colorStyleCbo)
        self.curveLayout2.addWidget(self.lineTypeCbo)
        self.curveLayout2.addWidget(self.markerStyleCbo)

        self.gridLayout.addLayout(self.curveLayout2, row, 1)

        row += 1

        self.curve_custom_config_layout = QHBoxLayout()

        self.logCurveLbl = QLabel(TOP_MENU_CONSTANTS["LOG_AXIS_LABEL"])

        self.logCurveChb = QCheckBox('', self)

        self.reverseXLbl = QLabel(TOP_MENU_CONSTANTS["REVERSE_X_LABEL"])

        self.reverseXChb = QCheckBox('', self)

        self.cummulative_lbl = QLabel(TOP_MENU_CONSTANTS["KEEP_SCALE"])

        self.cummulative_checkbox = QCheckBox()

        self.curve_custom_config_layout.addWidget(self.logCurveLbl)
        self.curve_custom_config_layout.addWidget(self.logCurveChb)
        self.curve_custom_config_layout.addWidget(self.reverseXLbl)
        self.curve_custom_config_layout.addWidget(self.reverseXChb)
        self.curve_custom_config_layout.addWidget(self.cummulative_lbl)
        self.curve_custom_config_layout.addWidget(self.cummulative_checkbox)

        self.gridLayout.addLayout(self.curve_custom_config_layout, row, 0)

        row += 1

        self.adjusted_layout = QVBoxLayout()

        self.adjust_range_layout = QHBoxLayout()

        self.x_adjusted_label = QLabel(ADJUST_RANGE_LBL)

        self.x_adjusted_cb = QCheckBox()

        self.x_adjusted_cb.toggled.connect(self.show_adjusted_values)

        self.x_adjusted_cb.setChecked(False)

        self.adjust_range_layout.addWidget(self.x_adjusted_label)

        self.adjust_range_layout.addWidget(self.x_adjusted_cb)

        self.adjusted_layout.addLayout(self.adjust_range_layout)

        self.x_min_layout = QHBoxLayout()

        self.x_adjusted_min_label = QLabel(ADJUSTED_MIN_LBL)

        self.x_adjusted_min_textbox = QLineEdit(DEFAULT_ADJUSTED_MIN_LBL)

        self.x_min_layout.addWidget(self.x_adjusted_min_label)

        self.x_min_layout.addWidget(self.x_adjusted_min_textbox,
                                    alignment=Qt.AlignmentFlag.AlignLeft)

        self.adjusted_layout.addLayout(self.x_min_layout)

        self.x_max_layout = QHBoxLayout()

        self.x_adjusted_max_label = QLabel(ADJUSTED_MAX_LBL)

        self.x_adjusted_max_textbox = QLineEdit(DEFAULT_ADJUSTED_MAX_LBL)

        self.x_max_layout.addWidget(self.x_adjusted_max_label)

        self.x_max_layout.addWidget(self.x_adjusted_max_textbox,
                                    alignment=Qt.AlignmentFlag.AlignLeft)

        self.adjusted_layout.addLayout(self.x_max_layout)

        self.gridLayout.addLayout(self.adjusted_layout, row, 0)

        self.show_adjusted_values()

        row += 1

        self.curve_button_layout = QHBoxLayout()

        self.deleteCurveBtn = QPushButton(TOP_MENU_CONSTANTS["DELETE_CURVE_BUTTON"])
        self.deleteCurveBtn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.deleteCurveBtn.clicked.connect(
            lambda: self.delete_curve()
        )

        self.change_curve_btn = QPushButton(TOP_MENU_CONSTANTS["CHANGE_CURVE_BUTTON"])
        self.change_curve_btn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.change_curve_btn.clicked.connect(
            lambda: self.change_curve()
        )

        self.curve_button_layout.addWidget(self.deleteCurveBtn)

        self.curve_button_layout.addWidget(self.change_curve_btn)

        self.gridLayout.addLayout(self.curve_button_layout, row, 0)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        row = self.init_fill_between_curves_section(row)

        self.show()

    def adjust_curve_options(self):
        colored_curve = self.curveCbo.currentData()

        if colored_curve is None:
            return

        self.colorStyleCbo.setCurrentIndex(get_color_index(colored_curve.get_color_name()))

        self.lineTypeCbo.setCurrentIndex(LineTypes().get_line_index(colored_curve.get_style_name()))

        self.markerStyleCbo.setCurrentIndex(LineMarkers().get_marker_index(colored_curve.get_marker_name()))

        self.logCurveChb.setChecked(colored_curve.get_is_log())

        self.reverseXChb.setChecked(colored_curve.get_is_reverse())

        self.cummulative_checkbox.setChecked(colored_curve.get_is_cummulative())

    def show_adjusted_values(self):
        disable_elements_with_component(self.x_adjusted_cb, [
            self.x_adjusted_min_textbox,
            self.x_adjusted_max_textbox,
            self.x_adjusted_min_label,
            self.x_adjusted_max_label
        ])

    def init_fill_between_curves_section(self,
                                         row):
        self.userCurveLbl2 = QLabel(TOP_MENU_CONSTANTS["FILL_CURVES_LABEL"])
        self.userCurveCbo2 = QComboBox(self)
        self.userCurveCbo2.setPlaceholderText(TOP_MENU_CONSTANTS["CHOOSE_PLACEHOLDER"])

        self.userCurveLayout2 = QVBoxLayout()

        self.userCurveCbo3 = QComboBox(self)
        self.userCurveCbo3.setPlaceholderText(TOP_MENU_CONSTANTS["CHOOSE_PLACEHOLDER"])

        self.userCurveLayout2.addWidget(self.userCurveLbl2)
        self.userCurveLayout2.addWidget(self.userCurveCbo2)
        self.userCurveLayout2.addWidget(self.userCurveCbo3)

        self.gridLayout.addLayout(self.userCurveLayout2, row, 0)

        row += 1

        self.fill_color_label = QLabel(TOP_MENU_CONSTANTS["LINE_COLOR_LABEL"])

        self.gridLayout.addWidget(self.fill_color_label, row, 0)

        row += 1

        self.fill_color = color_combo_box()

        self.gridLayout.addWidget(self.fill_color, row, 0)

        row += 1

        self.fill_btns_layout = QHBoxLayout(self)

        self.fillBetweenLinesBtn = QPushButton(TOP_MENU_CONSTANTS["FILL_BETWEEN_LINES_BUTTON"])
        self.fillBetweenLinesBtn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.fillBetweenLinesBtn.clicked.connect(
            lambda checked: self.fillBetweenLines()
        )

        self.delete_fill_btn = QPushButton(TOP_MENU_CONSTANTS["DELETE_FILL_TEXT"])
        self.delete_fill_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.delete_fill_btn.clicked.connect(
            lambda: self.remove_fill_between_lines()
        )

        self.fill_btns_layout.addWidget(self.fillBetweenLinesBtn)

        self.fill_btns_layout.addWidget(self.delete_fill_btn)

        self.gridLayout.addLayout(self.fill_btns_layout, row, 0)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0)

        row += 1

        self.see_curves_btn = QPushButton(SEE_ALL_LBL)
        self.see_curves_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.see_curves_btn \
            .clicked \
            .connect(lambda: self.see_all_curves())

        self.gridLayout.addWidget(self.see_curves_btn, row, 0)

        row += 1

        self.delete_curves_btn = QPushButton(DELETE_ALL_LBL)
        self.delete_curves_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.delete_curves_btn \
            .clicked \
            .connect(lambda: self.delete_all_curves())

        self.gridLayout.addWidget(self.delete_curves_btn, row, 0)

        row += 1

        return row

    def see_all_curves(self):
        if self.well is None:
            return AlertWindow(MISSING_WELL)

        self.well \
            .graphicWindow \
            .show()

    def delete_all_curves(self):
        if self.well is None:
            return AlertWindow(MISSING_WELL)

        YesOrNoQuestion(CONFIRM_DELETION_LBL,
                        lambda: (self.well
                                     .graphicWindow
                                     .remove_every_track(),
                                 self._update_tab()),
                        lambda: None)

    def addTrack(self):
        if not self.well:
            AlertWindow(MISSING_WELL)

            return

        track_name, \
        ok_btn_pressed = QInputDialog.getText(self,
                                              NEW_TRACK_TITLE,
                                              NAME_OF_THE_NEW_TRACK)

        if not ok_btn_pressed:
            return

        try:
            curve_track = self.well \
                              .graphicWindow \
                              .create_curve_track(track_name,
                                                  track_name)

            if curve_track is None:
                return

        except ValueError as exception:
            AlertWindow(str(exception))

            return

        self.update_tab(self.well)

        curve_track = self.well \
            .graphicWindow \
            .get_curve_track(track_name)

        curve_track.set_to_update()

        self._update_tab()

        self.draw(curve_track)

        self.trackCbo.setCurrentIndex(self.trackCbo.count() - 1)

    def removeTrack(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return

        track_name = self.trackCbo \
            .currentText()

        self.well \
            .graphicWindow \
            .remove_curve_track(track_name)

        self._update_tab()

        self.update_tab(self.well)

    def change_curve(self):
        curve = self.curveCbo \
            .currentData()

        track = self.trackCbo \
            .currentData()

        if track is None:
            return AlertWindow(TRACK_MISSING)

        if curve is None:
            return AlertWindow(MISSING_CURVE)

        if curve.is_scatter and self.markerStyleCbo.currentText() == LINE_MARKER_CONSTANTS["NONE"]:
            return AlertWindow(MISSING_MARKER_IN_SCATTER)

        x_adjusted_min = self.x_adjusted_min_textbox.text()

        x_adjusted_max = self.x_adjusted_max_textbox.text()

        if self.x_adjusted_cb.isChecked():
            if not are_numbers([x_adjusted_min, x_adjusted_max],
                               number_check_fn=is_positive_number
                               if ((self.logCurveChb.isChecked() and not curve.is_log) or curve.is_log)
                               else is_number):
                return AlertWindow(INVALID_NUMERIC_INPUT)

            x_adjusted_min = float(x_adjusted_min)

            x_adjusted_max = float(x_adjusted_max)

            if self.logCurveChb.isChecked():
                x_adjusted_min = get_log10(x_adjusted_min)

                x_adjusted_max = get_log10(x_adjusted_max)

        x_axis = curve.get_x_data()
        y_axis_orig = curve.get_y_data()

        y_axis = self.well.wellModel.get_depth_curve()

        if len(y_axis) == 0:
            y_axis = y_axis_orig

        config = {
            'tab_name': track.tab_name,
            'track_name': track.track_name,
            'curve_name': curve.base_name,
            'add_axis': curve.has_axis(),

            'x_axis': x_axis,
            'y_axis': y_axis,

            "y_label": self.get_y_label(),
            "x_label": curve.x_label,

            'color': self.colorStyleCbo.currentText(),
            'line_style': self.lineTypeCbo.currentText(),
            'line_marker': self.markerStyleCbo.currentText(),
            'line_width': 1,

            "is_log": self.logCurveChb.isChecked(),
            "is_reverse": self.reverseXChb.isChecked(),
            "cummulative": self.cummulative_checkbox.isChecked(),

            'x_adjusted': self.x_adjusted_cb.isChecked(),
            'x_adjusted_min': x_adjusted_min,
            'x_adjusted_max': x_adjusted_max
        }

        if curve.is_scatter:
            config.update(DEFAULT_SCATTERPLOT_CONFIG)

        result = self.well \
                     .graphicWindow \
                     .add_curve(config)

        if len(result) != 0:
            return AlertWindow(result)

        # EVERY track, to avoid delete ephimeral curves
        self.draw()

    def append_new_curve(self):
        track = self.trackCbo \
            .currentData()

        if track is None:
            AlertWindow(TRACK_MISSING)
            return

        name = self.curve_to_add_cbo \
            .currentText()

        x_axis = self.well \
            .wellModel \
            .get_df_curve(name)

        y_axis = self.well \
            .wellModel \
            .get_depth_curve()

        is_log = self.add_curve_log_checkbox.isChecked()

        is_reverse = self.add_curve_reverse_x_checkbox.isChecked()

        is_cummulative = self.add_curve_cummulative_checkbox.isChecked()

        if track.get_number_of_configs() == 0 and is_cummulative:
            return AlertWindow(KEEP_SCALE_ERROR)

        config = {
            'tab_name': track.tab_name,
            'track_name': track.track_name,
            'curve_name': name,
            'add_axis': True,

            'x_axis': x_axis,
            'y_axis': y_axis,

            "x_label": self.well.wellModel.get_label_for(name),
            "y_label": self.get_y_label(),

            'color': self.add_curve_color.currentText(),
            'line_style': self.add_curve_line.currentText(),
            'line_marker': self.add_curve_marker.currentText(),
            'line_width': 1,

            "is_log": is_log,
            "is_reverse": is_reverse,
            "cummulative": is_cummulative
        }

        self.well \
            .graphicWindow \
            .append_curve(config)

        # EVERY track, to avoid delete ephimeral curves
        self.draw()

    def delete_curve(self):
        curve_to_delete = self.curveCbo. \
            currentText()

        if len(curve_to_delete) == 0:
            return

        track = self.trackCbo \
            .currentData() \

        track.delete_curve_config(curve_to_delete)

        # EVERY track, to avoid delete ephimeral curves
        self.draw()

    def use_fill_config(self,
                        fn):
        if not self.well:
            return AlertWindow(MISSING_WELL)

        track = self.trackCbo \
            .currentData() \

        curve_name_1 = self.userCurveCbo2 \
            .currentText()

        curve_name_2 = self.userCurveCbo3 \
            .currentText()

        if len(curve_name_1) == 0 or len(curve_name_2) == 0:
            return AlertWindow(MISSING_CURVE)

        curve_data_1 = self.userCurveCbo2 \
            .currentData()

        curve_data_2 = self.userCurveCbo3 \
            .currentData()

        if curve_data_1.is_reverse != curve_data_2.is_reverse:
            AlertWindow(FILL_REVERSE_CURVE)
            return

        config = {
            'track_name': track.track_name,
            'curve_name_1': curve_name_1,
            'curve_name_2': curve_name_2,
            'color': self.fill_color
                .currentText(),
            'ephimeral': False,
            'semi_fill': False,
            'cummulative': curve_data_1.get_is_cummulative() or curve_data_2.get_is_cummulative(),
            'fill': "Sólido"
        }

        fn(config)

        # EVERY track, to avoid delete ephimeral curves
        self.draw()

    def fillBetweenLines(self):
        self.use_fill_config(self.well
                             .graphicWindow
                             .add_fill_between_curves)

    def remove_fill_between_lines(self):
        self.use_fill_config(self.well
                             .graphicWindow
                             .remove_fill_between_curves)

    def select_track(self):
        self.update_combos(lambda selector: self.update_selector(selector))

    def update_selector(self,
                        selector):
        if selector.count() - 1 >= 0:
            current_index = selector.currentIndex()

        else:
            current_index = -1

        selector.clear()

        if self.trackCbo \
                .currentData() is not None:
            for name, curve in self.trackCbo \
                    .currentData() \
                    .get_curves_with_names():
                selector.addItem(name,
                                 curve)

        if selector.count() - 1 >= 0:
            selector.setCurrentIndex(current_index)

    def update_curve_list(self):
        self.curve_to_add_cbo \
            .clear()

        for curve_name in self.well \
                .wellModel \
                .get_curve_names():
            self.curve_to_add_cbo \
                .addItem(curve_name,
                         curve_name)

    def update_tab(self, well):
        super().update_tab(well)

        self._update_tab()

    def _update_tab(self):
        if self.trackCbo.count() - 1 > 0:
            current_index = self.trackCbo.currentIndex()

        else:
            current_index = -1

        self.trackCbo.clear()

        for track in self.well \
                .graphicWindow \
                .get_curve_tracks():
            self.trackCbo \
                .addItem(track.track_name,
                         track)

        if self.trackCbo.count() - 1 > 0:
            self.trackCbo.setCurrentIndex(current_index)

        update_curve_list(self.curve_to_add_cbo,
                          self.well)

        self.update_combos(lambda selector: self.update_selector(selector))

    def update_combos(self,
                      function):
        combos = [
            self.curveCbo,
            self.userCurveCbo2,
            self.userCurveCbo3,
        ]

        for combo in combos:
            function(combo)

    def toggleWindow(self, window):
        if self.well is None:
            return

        if window.isVisible():
            window.hide()
            window.stopRefreshing()

        else:
            window.show()
            window.show()
            window.startRefreshing()

    def draw(self,
             track=None):
        self.well \
            .graphicWindow \
            .draw_tracks(EVERY_TAB if track is None else track.tab_name)

        self.update_combos(lambda selector: self.update_selector(selector))
