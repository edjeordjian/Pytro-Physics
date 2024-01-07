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


def test_fetkovich_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[10] \
                .tabs[4]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "fetkovich.view")

    assert 0.00000008993329460197583 == graphic_window.curve_tracks[0] \
        .configs["IPR - Fetkovich"]["line_groups"][0]["x_axis"][-1]

    assert not tab.depthCustomRb \
        .isChecked()

    assert "1.7" == tab.damageFactorQle \
        .text()

    assert "" == tab.customMaxDepthQle \
        .text()

    assert tab.iprColorCbo \
              .currentText() == "Verde"


def test_fetkovich_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[10] \
                .tabs[4]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "fetkovich.view")

    load_tab_preview(qtbot, tab)

    assert 8.173300573597263e-08 == graphic_window.curve_tracks[0] \
        .configs["IPR - Fetkovich"]["line_groups"][0]["x_axis"][-1]
