"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

import numpy as np

from tests.tests_helper import (set_current_path, init_config, 
                                load_view_to_window, load_tab_preview)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)


def test_picket_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[7]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "picket.view")

    assert np.isnan(graphic_window.curve_tracks[0] \
        .configs["Crossplot Picket"]["scatter_groups"][0]["x_axis"][-1])

    assert tab.depthCustomRb \
        .isChecked()

    assert tab.forceDepthZCb \
        .isChecked()

    assert "2500" == tab.customMaxDepthQle \
        .text()

def test_picket_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[7]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "picket.view")

    load_tab_preview(qtbot, tab)

    assert "2500" == tab.customMaxDepthQle \
        .text()
