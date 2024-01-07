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

from constants.tab_constants import (SP_CURVE_NAME, GR_CURVE_NAME, 
                                     RESISTIVITY_CURVE_NAME, NEUTRON_CURVE_NAME, 
                                     DENSITY_CURVE_NAME)


def test_vshale_sp_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "vshale_sp.view")

    assert 94.881 == graphic_window.curve_tracks[0] \
               .configs[SP_CURVE_NAME]["x_axis"][0]

    tab = window.tabs[2] \
               .tabs[0] \
               .tabs[0]

    load_tab_preview(qtbot, tab)

    assert "Verde" == tab.curveColorCbo \
               .currentText()


def test_gr_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "vshale_gr.view")

    assert 79.22 == graphic_window.curve_tracks[0] \
               .configs[GR_CURVE_NAME]["x_axis"][0]

    tab = window.tabs[2] \
               .tabs[0] \
               .tabs[1]
    
    load_tab_preview(qtbot, tab)

    assert "Verde" == tab.curveColorCbo \
               .currentText()
    

def test_vshale_resistivity_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "vshale_resistivity.view")

    assert 6.333 == graphic_window.curve_tracks[0] \
               .configs[RESISTIVITY_CURVE_NAME]["x_axis"][0]

    tab = window.tabs[2] \
               .tabs[0] \
               .tabs[2]

    load_tab_preview(qtbot, tab)

    assert "Verde" == tab.curveColorCbo \
               .currentText()
    

def test_vshale_neutron_density_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "vshale_neutron_density.view")

    assert 0.327 == graphic_window.curve_tracks[0] \
               .configs[NEUTRON_CURVE_NAME]["x_axis"][0]
    
    assert 2.455 == graphic_window.curve_tracks[1] \
               .configs[DENSITY_CURVE_NAME]["x_axis"][0]

    tab = window.tabs[2] \
               .tabs[0] \
               .tabs[3]
    
    load_tab_preview(qtbot, tab)

    assert "Verde" == tab.curveNeutronColorCbo \
               .currentText()

    assert "Violeta" == tab.curveDensityColorCbo \
               .currentText()