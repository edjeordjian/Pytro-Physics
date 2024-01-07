"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from tests.tests_helper import (set_current_path)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)

"""
def test_axies_drawing(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[0] \
                .tabs[0]

    graphic_window = tab.window

    tab.curveCbo.setCurrentIndex(10)

    tab.previewBtn.click()

    tab = window.tabs[1].tab

    tab.curve_to_add_cbo.setCurrentIndex(2)

    tab.trackCbo.currentIndex()

    # WHY DOES THIS DOES NOT WORK????
    tab.trackCbo.setCurrentIndex(1)

    tab.create_curve_btn.click()

    qtbot.wait(100000)

    assert 1 == len(graphic_window.curve_tracks[0] \
                    .axis_configs)

    assert 2 == len(graphic_window.curve_tracks[1] \
        .axis_configs)

    tab.trackCbo.setCurrentIndex(0)

    tab.create_curve_btn.click()

    assert 2 == len(graphic_window.curve_tracks[0] \
                    .axis_configs)

    assert 2 == len(graphic_window.curve_tracks[1] \
        .axis_configs)

    tab.trackCbo.setCurrentIndex(1)

    tab.create_curve_btn.click()

    assert 2 == len(graphic_window.curve_tracks[0] \
                    .axis_configs)

    assert 3 == len(graphic_window.curve_tracks[1] \
        .axis_configs)
"""