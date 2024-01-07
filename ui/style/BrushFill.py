"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

BRUSH_FILLS = {
            "Sólido":  Qt.BrushStyle.SolidPattern,
            "Puntos": Qt.BrushStyle.Dense7Pattern,
            "Cuadriculado": Qt.BrushStyle.CrossPattern,
            "Enrejado": Qt.BrushStyle.DiagCrossPattern,
            "Enrejado fino": Qt.BrushStyle.DiagCrossPattern,
            "Línea horizontal": Qt.BrushStyle.HorPattern,
            "Línea vertical": Qt.BrushStyle.VerPattern,
            "Diagonal derecha": Qt.BrushStyle.FDiagPattern,
            "Diagonal izquierda": Qt.BrushStyle.BDiagPattern,
        }


def get_brush_fill(name):
    return BRUSH_FILLS[name]


def get_brush_fills():
    return list(BRUSH_FILLS.keys())
