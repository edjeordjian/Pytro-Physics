"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6 import QtGui, QtCore

import pyqtgraph as pg

from ui.style.LineColors import getColor


class RectangleComponent(pg.GraphicsObject):
    def __init__(self, config):
        super().__init__()
        self.config = config

        color_tuple = getColor(config["color"])

        self.pen = pg.mkPen(color=color_tuple, width=0)

        self.brush = QtGui.QColor(color_tuple[0],
                                  color_tuple[1],
                                  color_tuple[2])

        # (x, y, width, height)
        self.rect = QtCore.QRectF(config['x_min'],
                                  config['y_min'],
                                  config['x_max'] - config['x_min'],
                                  config['y_max'] - config['y_min'])

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen)

        painter.setBrush(self.brush)

        painter.drawRect(self.rect)
