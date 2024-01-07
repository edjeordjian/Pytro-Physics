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

from constants.tab_constants import TEMPERATURE_TAB_NAME


def test_temperature_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "temperature.view")

    assert 9.749 == graphic_window.curve_tracks[0] \
               .configs[TEMPERATURE_TAB_NAME]["x_axis"][-1]

    tab = window.tabs[2] \
               .tabs[4] \
               .tabs[0] \
                   
    load_tab_preview(qtbot, tab)

    assert "Verde" == tab.curveColorCbo \
               .currentText()
