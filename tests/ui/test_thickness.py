"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from tests.tests_helper import (set_current_path, init_config, 
                                load_view_to_window, get_graphic_window, 
                                load_tab_preview)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)


def test_thickness_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "thickness.view")

    assert 4 == len(graphic_window.curve_tracks)

    assert len(graphic_window.curve_tracks[2]
               .axis_configs) == 1

    tab = window.tabs[2] \
        .tabs[7] \
        .tabs[4]

    assert tab.depthCustomRb \
        .isChecked()

    assert tab.c1CutoffQle\
              .text() == "0.4473"


def test_thickness_2_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "thickness_2.view")

    assert 8 == len(graphic_window.curve_tracks)

    assert len(graphic_window.curve_tracks[2]
               .axis_configs) == 1

    tab = window.tabs[2] \
        .tabs[7] \
        .tabs[4]

    load_tab_preview(qtbot, tab)

    assert tab.c1CutoffQle\
              .text() == "0.6"
    
    assert tab.c2CutoffQle\
              .text() == "0.15"
    
    assert tab.c3CutoffQle\
              .text() == "0.5"
    
    assert tab.c4CutoffQle\
              .text() == "0.1"