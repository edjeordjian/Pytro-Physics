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


def test_rho_shale_scatterplot_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[1]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "rho_shale.view")

    assert np.isnan(graphic_window.curve_tracks[0] \
        .configs["Crossplot Densidad-Sonico"]["scatter_groups"][0]["x_axis"][2000])

    assert tab.depthCustomRb \
        .isChecked()

    assert tab.forceDepthZCb \
        .isChecked()

    assert "2600" == tab.customMaxDepthQle \
        .text()

def test_rho_shale_scatterplot_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[1]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "rho_shale.view")

    load_tab_preview(qtbot, tab)

    assert "2600" == tab.customMaxDepthQle \
        .text()

