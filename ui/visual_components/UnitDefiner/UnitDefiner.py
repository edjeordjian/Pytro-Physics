"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import traceback

import pyautogui

from PyQt6.QtWidgets import QVBoxLayout, QPushButton

from constants.tab_constants import SAVE_LBL

from services.constant_service import only_ascci_for

from services.tools.logger_service import log_error

from services.tools.string_service import is_ascii

from ui.popUps.alertWindow import AlertWindow

from ui.visual_components.UnitDefiner.ColumnUnitRow import ColumnUnitRow

from ui.ScrollableWidget import ScrollableWidget

from ui.visual_components.UnitDefiner.DepthUnitSelector import DepthUnitSelector


class UnitDefiner(ScrollableWidget):
    def __init__(self, df, merge_fn, close_fn):
        super().__init__(QVBoxLayout())

        self.close_fn = close_fn

        width, height = pyautogui.size()

        self.df = df

        self.merge_fn = merge_fn

        n_columns = len(df.columns)

        window_width = min(width, 25 * n_columns)

        window_height = min(height, 25 * n_columns)

        self._init_scroll_area(int(width / 3),
                               int(height / 3),
                               window_width,
                               window_height,
                               "Elegir unidades")

        self.unit_rows = []

        if len(df.columns) == 0:
            return

        self.unit_rows \
            .append(DepthUnitSelector(df.columns[0],
                                      self.layout))

        for i in range(1, n_columns):
            self.unit_rows \
                .append(ColumnUnitRow(df.columns[i],
                                      self.layout))

        self.save_button = QPushButton(SAVE_LBL)

        self.layout.addWidget(self.save_button)

        self.show()

        self.save_button \
            .clicked \
            .connect(self.close)

    def save_units(self):
        column_data = {}

        depth_unit = ""

        for i in range(
                    len(self.unit_rows)):
            unit_row = self.unit_rows[i]

            if not is_ascii(unit_row.get_unit()):
                AlertWindow(only_ascci_for(unit_row.get_name()))

                return False

            if i == 0:
                depth_unit = unit_row.get_unit()

            column_data[unit_row.get_name()] = unit_row.get_unit()

        try:
            self.merge_fn(self.df, column_data, depth_unit)

            return True

        except Exception:
            log_error(traceback.format_exc())

            return False

    def closeEvent(self, event):
        self.save_units()

        self.close_fn()

        super().closeEvent(event)
