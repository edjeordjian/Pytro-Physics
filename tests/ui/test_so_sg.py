"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, get_graphic_window)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)

from constants.tab_constants import SO_SG_TAB_NAME


def test_so_sg_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "so_sg.view")

    assert -9.029 == graphic_window.curve_tracks[0] \
               .configs[SO_SG_TAB_NAME]["x_axis"][-1]

    assert "Azul" == window.tabs[2] \
               .tabs[4] \
               .tabs[3] \
               .curveColorCbo \
               .currentText()
