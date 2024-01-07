"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from constants.pytrophysicsConstants import LINE_TYPE_CONSTANTS

from services.tools.json_service import get_key_index


class LineTypes:
    def __init__(self):
        self.lineTypes = {
            LINE_TYPE_CONSTANTS["SOLID_LINE"]: Qt.PenStyle.SolidLine,
            LINE_TYPE_CONSTANTS["DASH_LINE"]: Qt.PenStyle.DashLine,
            LINE_TYPE_CONSTANTS["DOT_LINE"]: Qt.PenStyle.DotLine,
            LINE_TYPE_CONSTANTS["DASH_DOT_LINE"]: Qt.PenStyle.DashDotLine,
            LINE_TYPE_CONSTANTS["DASH_DOT_DOT_LINE"]: Qt.PenStyle.DashDotDotLine
        }

    def getLineType(self, lineType):
        return self.lineTypes[lineType]

    def get_line_index(self, line_name):
        return get_key_index(self.lineTypes, line_name)

    def getLineTypeList(self):
        return self.lineTypes.keys()
