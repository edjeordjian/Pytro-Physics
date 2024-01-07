"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants.pytrophysicsConstants import COLORMAP_CONSTANTS


class Colormaps:
    def __init__(self):
        self.colormaps = {
            COLORMAP_CONSTANTS["CIVIDIS"]: "cividis",
            COLORMAP_CONSTANTS["INFERNO"]: "inferno",
            COLORMAP_CONSTANTS["CET-L1"]: "CET-L1",
            COLORMAP_CONSTANTS["CET-L4"]: "CET-L4",
            COLORMAP_CONSTANTS["CET-CBTL1"]: "CET-CBTL1",
            COLORMAP_CONSTANTS["CET-L5"]: "CET-L5",
            COLORMAP_CONSTANTS["CET-D2"]: "CET-D2",
            COLORMAP_CONSTANTS["CET-L6"]: "CET-L6",
            COLORMAP_CONSTANTS["CET-L7"]: "CET-L7",
            COLORMAP_CONSTANTS["CET-L9"]: "CET-L9",
            COLORMAP_CONSTANTS["CET-R4"]: "CET-R4",
            COLORMAP_CONSTANTS["CET-C6"]: "CET-C6",

        }

    def getColormap(self, colormap):
        return self.colormaps[colormap]

    def getColormapList(self):
        return self.colormaps.keys()
