"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from constants.sw_constants import RW_TAB_FULL_NAME

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, get_graphic_window)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)


def test_rw_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "rw.view")

    assert 0.8297736010252029 == graphic_window.curve_tracks[0] \
               .configs[RW_TAB_FULL_NAME]["x_axis"][-1]

    assert "Negro" == window.tabs[2] \
               .tabs[4] \
               .tabs[1] \
               .rw_color \
               .currentText()
