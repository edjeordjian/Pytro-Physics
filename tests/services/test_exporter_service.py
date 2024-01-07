"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.exporter_service import export_png_file

import os

from tests.tests_helper import (set_current_path, init_config, load_view_to_window)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)

def test_export_png_file(qtbot):
    window = init_config(qtbot, current_path)

    tab = window.tabs[2] \
                .tabs[8] \
                .tabs[0]

    graphic_window = tab.window

    load_view_to_window(qtbot, graphic_window, current_path, "crossplot_general.view")

    png_file_name = export_png_file(graphic_window.curve_tracks[0].first_item(), "test_image", 0)

    # Byte size of the exported png image
    assert os.stat(png_file_name).st_size > 20000

    os.remove(png_file_name)
