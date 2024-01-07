"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from tests.tests_helper import (set_current_path, init_config, 
                                load_view_to_window, load_tab_preview)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)


def test_darcy_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[10] \
                .tabs[0]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "darcy.view")

    assert 0.011111111111137776 == graphic_window.curve_tracks[0] \
        .configs["IPR - Darcy"]["line_groups"][0]["x_axis"][-1]

    assert tab.depthCustomRb \
        .isChecked()

    assert "1.5" == tab.damageFactorQle \
        .text()

    assert "2500" == tab.customMaxDepthQle \
        .text()


def test_darcy_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[10] \
                .tabs[0]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "darcy.view")

    load_tab_preview(qtbot, tab)

    assert 0.0111111111111108 == graphic_window.curve_tracks[0] \
        .configs["IPR - Darcy"]["line_groups"][0]["x_axis"][-1]
