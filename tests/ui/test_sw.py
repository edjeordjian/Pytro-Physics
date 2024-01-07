"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, 
                                get_graphic_window, load_tab_preview)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)

from constants.sw_constants import SW_CALCULATION_TAB_NAME, SW_DUAL_WATER


def test_sw_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "sw_dual_water.view")

    assert 9.803776568288404 == graphic_window.curve_tracks[0] \
               .configs[f"{SW_CALCULATION_TAB_NAME} {SW_DUAL_WATER}"]["x_axis"][-1]

    tab = window.tabs[2] \
                .tabs[4] \
                .tabs[2]

    load_tab_preview(qtbot, tab)

    assert "Negro" == tab.curve_to_save_color \
                        .currentText()

    assert "4" == tab.dual_water_m_constant_textbox \
                    .text()
