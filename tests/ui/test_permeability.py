"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from math import inf

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, get_graphic_window)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)

from constants.permeability_constants import (XGBOOST_TRACK_NAME, RANDOM_FOREST_TRACK_NAME, ADA_TRACK_NAME,
                                              TIMUR_TRACK_NAME, TIXIER_TRACK_NAME, COATES_TRACK_NAME,
                                              COATES_AND_DUMANOIR_TRACK_NAME)


class TestPermeability:
    def test_xgboost_view(self, qtbot):
        window = init_config(qtbot, current_path)

        graphic_window = get_graphic_window(window)

        load_view_to_window(qtbot, graphic_window, current_path, "xgboost.view")

        assert 0.12563191413150288 == graphic_window.curve_tracks[1] \
                   .configs[XGBOOST_TRACK_NAME]["x_axis"][-1]

        assert "Verde" == window.tabs[2] \
                   .tabs[5] \
                   .tabs[1] \
                   .curve_to_save_color \
                   .currentText()

        assert window.tabs[2] \
                   .tabs[5] \
                   .tabs[1] \
                   .depthCustomRb \
                   .isChecked()

    def test_random_forest_view(self, qtbot):
        window = init_config(qtbot, current_path)

        graphic_window = get_graphic_window(window)

        load_view_to_window(qtbot, graphic_window, current_path, "random_forest.view")

        assert 6.851593011492067 == graphic_window.curve_tracks[1] \
                   .configs[RANDOM_FOREST_TRACK_NAME]["x_axis"][-1]

        assert "Naranja" == window.tabs[2] \
                   .tabs[5] \
                   .tabs[0] \
                   .curve_to_save_color \
                   .currentText()

        assert window.tabs[2] \
                   .tabs[5] \
                   .tabs[0] \
                   .depthCustomRb \
                   .isChecked()

    def test_ada_view(self, qtbot):
        window = init_config(qtbot, current_path)

        graphic_window = get_graphic_window(window)

        load_view_to_window(qtbot, graphic_window, current_path, "ada.view")

        assert -0.0163737128754655 == graphic_window.curve_tracks[1] \
                   .configs[ADA_TRACK_NAME]["x_axis"][-1]

        assert "Azul" == window.tabs[2] \
                   .tabs[5] \
                   .tabs[2] \
                   .curve_to_save_color \
                   .currentText()

        assert window.tabs[2] \
                   .tabs[5] \
                   .tabs[2] \
                   .depthCustomRb \
                   .isChecked()

    def test_tixier_view(self, qtbot):
        window = init_config(qtbot, current_path)

        graphic_window = get_graphic_window(window)

        load_view_to_window(qtbot, graphic_window, current_path, "tixier.view")

        assert -inf == graphic_window.curve_tracks[0] \
            .configs[TIXIER_TRACK_NAME]["x_axis"][-1]

        assert "Azul" == window.tabs[2] \
            .tabs[5] \
            .tabs[4] \
            .curve_to_save_color \
            .currentText()

        assert window.tabs[2] \
            .tabs[5] \
            .tabs[4] \
            .depthCustomRb \
            .isChecked()

    def test_timur_view(self, qtbot):
        window = init_config(qtbot, current_path)

        graphic_window = get_graphic_window(window)

        load_view_to_window(qtbot, graphic_window, current_path, "timur.view")

        assert 0.0 == graphic_window.curve_tracks[0] \
            .configs[TIMUR_TRACK_NAME]["x_axis"][-1]

        assert "Rojo" == window.tabs[2] \
            .tabs[5] \
            .tabs[5] \
            .curve_to_save_color \
            .currentText()

        assert window.tabs[2] \
            .tabs[5] \
            .tabs[5] \
            .depthCustomRb \
            .isChecked()

    def test_coates_view(self, qtbot):
        window = init_config(qtbot, current_path)

        graphic_window = get_graphic_window(window)

        load_view_to_window(qtbot, graphic_window, current_path, "coates.view")

        assert -inf == graphic_window.curve_tracks[0] \
            .configs[COATES_TRACK_NAME]["x_axis"][-1]

        assert "Azul" == window.tabs[2] \
            .tabs[5] \
            .tabs[6] \
            .curve_to_save_color \
            .currentText()

        assert window.tabs[2] \
            .tabs[5] \
            .tabs[6] \
            .depthCustomRb \
            .isChecked()

    def test_coates_dumanoir_view(self, qtbot):
        window = init_config(qtbot, current_path)

        graphic_window = get_graphic_window(window)

        load_view_to_window(qtbot, graphic_window, current_path, "coates_dumanoir.view")

        assert -inf == graphic_window.curve_tracks[0] \
            .configs[COATES_AND_DUMANOIR_TRACK_NAME]["x_axis"][-1]

        assert "Azul" == window.tabs[2] \
            .tabs[5] \
            .tabs[7] \
            .curve_to_save_color \
            .currentText()

        assert window.tabs[2] \
            .tabs[5] \
            .tabs[7] \
            .depthCustomRb \
            .isChecked()
