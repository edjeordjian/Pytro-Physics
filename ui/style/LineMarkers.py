"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS

from services.tools.json_service import get_key_index


class LineMarkers:
    def __init__(self):
        self.markers = {
            LINE_MARKER_CONSTANTS["NONE"]: None,
            LINE_MARKER_CONSTANTS["DOT"]: "o",
            LINE_MARKER_CONSTANTS["DOWN_TRIANGLE"]: "t",
            LINE_MARKER_CONSTANTS["UP_TRIANGLE"]: "t1",
            LINE_MARKER_CONSTANTS["LEFT_TRIANGLE"]: "t3",
            LINE_MARKER_CONSTANTS["RIGHT_TRIANGLE"]: "t2",
            LINE_MARKER_CONSTANTS["SQUARE"]: "s",
            LINE_MARKER_CONSTANTS["PENTAGON"]: "p",
            LINE_MARKER_CONSTANTS["HEXAGON"]: "h",
            LINE_MARKER_CONSTANTS["STAR"]: "star",
            LINE_MARKER_CONSTANTS["CROSS"]: "+",
            LINE_MARKER_CONSTANTS["DIAMOND"]: "d",
            LINE_MARKER_CONSTANTS["DOWN_ARROW"]: "arrow_down",
            LINE_MARKER_CONSTANTS["UP_ARROW"]: "arrow_up",
            LINE_MARKER_CONSTANTS["LEFT_ARROW"]: "arrow_left",
            LINE_MARKER_CONSTANTS["RIGHT_ARROW"]: "arrow_right"
        }

    def getLineMarker(self, marker):
        return self.markers[marker]

    def getLineMarkerList(self):
        return self.markers.keys()

    def get_marker_index(self, marker_name):
        return get_key_index(self.markers, marker_name)
