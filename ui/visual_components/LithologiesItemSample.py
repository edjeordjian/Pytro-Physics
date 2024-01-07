"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtGui import QBrush

from PyQt6 import QtCore, QtGui

from pyqtgraph import ItemSample

import pyqtgraph.functions as fn


class LithologiesItemSample(ItemSample):
    def paint(self, p, *args):
        opts = self.item.opts
        if opts.get('antialias'):
            p.setRenderHint(p.RenderHint.Antialiasing)

        opts['fillBrush'] = QBrush(opts['pen'].color())

        p.setBrush(fn.mkBrush(opts['fillBrush']))

        p.setPen(fn.mkPen(opts['pen']))

        p.drawPolygon(QtGui.QPolygonF(
            [QtCore.QPointF(2, 2),
             QtCore.QPointF(2, 19),
             QtCore.QPointF(19, 19),
             QtCore.QPointF(19, 2)]))
