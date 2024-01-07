"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, get_graphic_window)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)

from constants.porosity_constants import TOTAL_POROSITY_BY_WYLLIE_NAME


def test_porosity_asquith_gibson_view(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "porosity_wyllie.view")

    assert 0.13442981047221333 == graphic_window.curve_tracks[0] \
               .configs[TOTAL_POROSITY_BY_WYLLIE_NAME]["x_axis"][-1]

    assert "Verde" == window.tabs[2] \
               .tabs[2] \
               .tabs[2] \
               .porosity_color \
               .currentText()
