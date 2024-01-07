"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

import numpy as np

from constants.tab_constants import (CUTOFF_3_CURVE_NAME, CUTOFF_C3_TITLE, CUTOFF_C1_TITLE, CUTOFF_C2_TITLE,
                                     CUTOFF_C4_TITLE)

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, 
                                get_graphic_window, load_tab_preview)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)


def test_cutoff_c3_preview_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "c3_preview.view")

    assert 1.0 == graphic_window.curve_tracks[0] \
        .configs[CUTOFF_3_CURVE_NAME]["x_axis"][-1]

    assert "Rojo" == window.tabs[2] \
        .tabs[7] \
        .tabs[2] \
        .tabs[1] \
        .curveColorCbo \
        .currentText()

    assert window.tabs[2] \
        .tabs[7] \
        .tabs[2] \
        .tabs[1] \
        .depthCustomRb \
        .isChecked()


def test_c3_cutoff_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[2] \
                .tabs[0]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c3_cutoff.view")

    assert 0.9716 == graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C3_TITLE]["line_groups"][2]["x_axis"][-1]

    assert "Verde" == tab.c3CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "0.9716" == tab.cutoffValueQle \
        .text()


def test_c3_cutoff_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[2] \
                .tabs[0]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c3_cutoff.view")

    load_tab_preview(qtbot, tab)

    assert 0.8864 == graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C3_TITLE]["line_groups"][2]["x_axis"][-1]

    assert "Verde" == tab.c3CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "0.8864" == tab.cutoffValueQle \
        .text()


def test_c1_cutoff_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[0]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c1.view")

    assert 0.4473 == graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C1_TITLE]["line_groups"][2]["x_axis"][-1]

    assert "Azul" == tab.c1CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "0.4473" == tab.cutoffValueQle \
        .text()


def test_c1_cutoff_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[0]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c1.view")

    load_tab_preview(qtbot, tab)

    assert 2.7768 == graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C1_TITLE]["line_groups"][2]["x_axis"][-1]

    assert "Azul" == tab.c1CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "2.7768" == tab.cutoffValueQle \
        .text()


def test_c2_cutoff_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[1]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c2.view")

    assert 0.0233 == graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C2_TITLE]["line_groups"][2]["x_axis"][-1]

    assert "Verde" == tab.c2CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "0.0233" == tab.cutoffValueQle \
        .text()


def test_c2_cutoff_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[1]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c2.view")

    load_tab_preview(qtbot, tab)

    assert np.isnan([graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C2_TITLE]["line_groups"][2]["x_axis"][-1]])

    assert "Verde" == tab.c2CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "nan" == tab.cutoffValueQle \
        .text()


def test_c4_cutoff_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[3]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c4.view")

    assert 28.31 == graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C4_TITLE]["line_groups"][2]["x_axis"][-1]

    assert "Azul" == tab.c4CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "28.31" == tab.cutoffValueQle \
        .text()


def test_c4_cutoff_2_view(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[7] \
                .tabs[3]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "c4.view")

    load_tab_preview(qtbot, tab)

    assert np.isnan([graphic_window.curve_tracks[0] \
        .configs[CUTOFF_C4_TITLE]["line_groups"][2]["x_axis"][-1]])

    assert "Azul" == tab.c4CutoffColorCbo \
        .currentText()

    assert tab.depthCustomRb \
        .isChecked()

    assert "nan" == tab.cutoffValueQle \
        .text()


def test_pay_flag_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "thickness.view")

    assert 0.436 == graphic_window.curve_tracks[0] \
        .configs["VSH_GR"]["x_axis"][-1]

    assert "Azul" == window.tabs[2] \
        .tabs[7] \
        .tabs[4] \
        .c1CurveColorCbo \
        .currentText()

    assert window.tabs[2] \
        .tabs[7] \
        .tabs[4] \
        .depthCustomRb \
        .isChecked()
