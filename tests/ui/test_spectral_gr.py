"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

import numpy as np

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, load_tab_preview)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)


def test_GR_1_view(qtbot):
    window = init_config(qtbot, current_path, "test_well_2/torio_potasio.las")

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[4]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "GR_1_torio_potasio.view")

    assert 0.33999999999999997 == graphic_window.curve_tracks[0] \
        .configs["Identificacion Mineral - GR Espectral"]["scatter_groups"][0]["x_axis"][-1]

    assert False == tab.depthCustomRb \
        .isChecked()

    assert tab.forceDepthZCb \
        .isChecked()

    assert "" == tab.customMaxDepthQle \
        .text()


def test_GR_2_view(qtbot):
    window = init_config(qtbot, current_path, "test_well_2/torio_potasio.las")

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[5]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "gr_2.view")

    assert np.isnan(graphic_window.curve_tracks[0] \
        .configs["Identificacion Mineral - GR Espectral "]["scatter_groups"][0]["x_axis"][-1])

    assert tab.depthCustomRb \
        .isChecked()

    assert tab.forceDepthZCb \
        .isChecked()

    assert "5200" == tab.customMaxDepthQle \
        .text()


def test_GR_3_view(qtbot):
    window = init_config(qtbot, current_path, "test_well_2/torio_potasio.las")

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[4]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "GR_1_torio_potasio.view")

    load_tab_preview(qtbot, tab)
    
    assert "" == tab.customMaxDepthQle \
        .text()


def test_GR_4_view(qtbot):
    window = init_config(qtbot, current_path, "test_well_2/torio_potasio.las")

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[5]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "gr_2.view")

    load_tab_preview(qtbot, tab)
    
    assert "5200" == tab.customMaxDepthQle \
        .text()
