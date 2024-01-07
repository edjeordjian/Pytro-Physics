"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6 import QtCore

import os

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path.pop()

current_path.pop()

current_path.pop()

current_path = "/".join(current_path)

#sys.path.append(current_path)

from ui.visual_components.data_menu_handler import load_view

from main import MainWindow

left_click = QtCore.Qt.MouseButton.LeftButton


def set_current_path(current_path):
    current_path.pop()

    current_path.pop()

    current_path.pop()

    current_path = "/".join(current_path)

    #sys.path.append(current_path)

    return current_path


def get_graphic_window(window):
    return window.wells[window.selected_well].graphicWindow


def load_view_to_window(qtbot, graphic_window, current_path, view_name):
    load_view(graphic_window, f"{current_path}/tests/ui/test_files/{view_name}")

    qtbot.wait(3500)


def init_config(qtbot, current_path, test_well="test_well/LAS_1048.las"):
    window = MainWindow()

    window.load_well(f"{current_path}/tests/ui/{test_well}")

    qtbot.wait(3500)

    qtbot.addWidget(window)

    return window


def load_tab_preview(qtbot, tab):
    tab.preview()

    qtbot.wait(3500)
