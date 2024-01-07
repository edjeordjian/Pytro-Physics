"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants.pytrophysicsConstants import COLOR_CONSTANTS

from services.tools.json_service import get_key_index

colors = {
            COLOR_CONSTANTS["BLACK"]: (0, 0, 0),
            COLOR_CONSTANTS["RED"]: (255, 0, 0),
            COLOR_CONSTANTS["YELLOW"]: (232, 208, 16),
            COLOR_CONSTANTS["BLUE"]: (0, 114, 181),
            COLOR_CONSTANTS["GREEN"]: (0, 161, 112),
            COLOR_CONSTANTS["VIOLET"]: (100, 83, 148),
            COLOR_CONSTANTS["ORANGE"]: (246, 125, 0),
            COLOR_CONSTANTS["MAGENTA"]: (255, 2, 136),
            COLOR_CONSTANTS["BROWN"]: (108, 79, 60),
            COLOR_CONSTANTS["PINK"]: (249, 118, 152),
            COLOR_CONSTANTS["LIGHT_BLUE"]: (98, 175, 255),
            COLOR_CONSTANTS["TEAL"]: (0, 166, 140),
            COLOR_CONSTANTS["OLIVE"]: (191, 216, 51),
            COLOR_CONSTANTS["CORAL"]: (233, 137, 126),
            COLOR_CONSTANTS["GREY"]: (147, 149, 151),
            COLOR_CONSTANTS["RUST"]: (181, 90, 48),
            COLOR_CONSTANTS["WHITE"]: (255, 255, 255)
        }


def getColor(colorName):
    return colors[colorName]


def get_color_index(color_name):
    return get_key_index(colors, color_name)


def get_color_values(color_name):
    r, g, b = getColor(color_name)

    return r, g, b
