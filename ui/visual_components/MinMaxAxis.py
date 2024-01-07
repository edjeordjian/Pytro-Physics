"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import math

import numpy as np

from pyqtgraph import AxisItem

from services.tools.number_service import get_rounded_float

# Never actually used. Is not that easy to adjust the labels in the axes.
class MinMaxAxis(AxisItem):
    def __init__(self, orientation, min_for_axis, max_for_axis,
                 pen=None, textPen=None, linkView=None, parent=None,
                 maxTickLength=-5, showValues=True, text='', units='',
                 unitPrefix='', **args):
        super().__init__(orientation, pen, textPen, linkView,
                         parent, maxTickLength, showValues, text,
                         units, unitPrefix)

        self.min_for_axis = math.floor(min_for_axis) if not np.isnan(min_for_axis) else None

        self.max_for_axis = math.ceil(max_for_axis) if not np.isnan(max_for_axis) else None

    def tickValues(self, minVal, maxVal, size):
        values = []

        for i in [25, 50, 75]:
            value = get_rounded_float(self.min_for_axis + i * 0.01 * (self.max_for_axis - self.min_for_axis))

            values.append(value)

        return [(self.max_for_axis - self.min_for_axis, [self.min_for_axis, self.max_for_axis]),
                ((self.max_for_axis - self.min_for_axis)/3, values)]
