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


def test_lithologies_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "lithologies.view")

    assert 0.7108258426966294 == graphic_window.curve_tracks[0] \
               .configs['Vshale']["x_axis"][0]

    assert 0.03185 == graphic_window.curve_tracks[1] \
               .configs['Porosidad']["x_axis"][0]

    assert 63.847374749973696 == graphic_window.curve_tracks[2] \
               .configs['DT Matriz']["x_axis"][0]

    assert 2.7756552517889372 == graphic_window.curve_tracks[3] \
               .configs['RHO Matriz']["x_axis"][0]

    assert "Vshale" == window.tabs[2] \
               .tabs[1] \
               .tabs[0] \
               .vshale_lithology_cbo \
               .currentText()


def test_lithologies_2_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "lithologies.view")

    tab = window.tabs[2] \
               .tabs[1] \
               .tabs[0]
    
    load_tab_preview(qtbot, tab)

    assert "Vshale" == tab \
               .vshale_lithology_cbo \
               .currentText()

