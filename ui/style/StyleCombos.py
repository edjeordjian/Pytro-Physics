"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import QComboBox

from constants.pytrophysicsConstants import (COLOR_CONSTANTS, LINE_MARKER_CONSTANTS, TOP_MENU_CONSTANTS,
                                             LINE_TYPE_CONSTANTS, COLORMAP_CONSTANTS)

from ui.style.BrushFill import BRUSH_FILLS


def color_combo_box():
    return _combo_box(TOP_MENU_CONSTANTS["LINE_COLOR_LABEL"],
                      COLOR_CONSTANTS)


def colormap_combo_box():
    return _combo_box("Colormap",
                      COLORMAP_CONSTANTS)


def marker_combo_box():
    return _combo_box(TOP_MENU_CONSTANTS["LINE_TYPE_LABEL"],
                      LINE_MARKER_CONSTANTS)


def line_combo_box():
    return _combo_box(TOP_MENU_CONSTANTS["LINE_MARKER_LABEL"],
                      LINE_TYPE_CONSTANTS)


def brush_fill_combo_box():
    return _combo_box_from_list("Rellanado",
                                BRUSH_FILLS)


def _combo_box(name,
               dictionary):
    combo_box = QComboBox()

    combo_box.setPlaceholderText(name)

    for key, value in dictionary.items():
        combo_box.addItem(value)

    combo_box.setCurrentIndex(0)

    return combo_box


def _combo_box_from_list(name,
                         a_list):
    combo_box = QComboBox()

    combo_box.setPlaceholderText(name)

    for element in a_list:
        combo_box.addItem(element)

    combo_box.setCurrentIndex(0)

    return combo_box

