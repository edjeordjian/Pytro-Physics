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


def test_rhomma_umma_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[3]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "rhomma_umma.view")

    assert graphic_window.curve_tracks[0] \
        .configs["Crossplot RHOMA-UMAA"]["scatter_groups"][0]["x_axis"][2000]

    assert tab.depthCustomRb \
        .isChecked()

    assert tab.forceDepthZCb \
        .isChecked()

    assert "3000" == tab.customMaxDepthQle \
        .text()

def test_rhomma_umma_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[3]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "rhomma_umma.view")

    load_tab_preview(qtbot, tab)
    
    assert "3000" == tab.customMaxDepthQle \
        .text()
