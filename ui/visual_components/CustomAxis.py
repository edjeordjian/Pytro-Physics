"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""


class CustomAxis:
    def __init__(self, axis, viewbox, curve_name,
                 cummulative, blank, x_adjusted, 
                 x_adjusted_min, x_adjusted_max):
        self.axis = axis

        self.viewbox = viewbox

        self.name = curve_name

        self.cummulative = cummulative

        self.blank = blank

        self.x_adjusted = x_adjusted

        self.x_adjusted_min = x_adjusted_min
        
        self.x_adjusted_max = x_adjusted_max

    def is_cummulative(self):
        return self.cummulative

    def add_item(self, item):
        self.viewbox \
            .addItem(item)

        self.axis.linkToView(self.viewbox)

    def get_name(self):
        return self.name

    def get_axis(self):
        return self.axis

    def is_blank(self):
        return self.blank

    def set_geometry(self, bounding_rect):
        self.viewbox \
            .setGeometry(bounding_rect)

    def get_limits(self):
        return self.axis.range
    
    def set_x_range_viewbox(self, x_min, x_max):
        self.viewbox.setXRange(x_min, x_max, padding=0.0)
        self.x_adjusted_min = x_min
        self.x_adjusted_max = x_max
    
    def set_y_range_viewbox(self, y_min, y_max):
        self.viewbox.setYRange(y_min, y_max, padding=0.0)

    def is_x_adjusted(self):
        return self.x_adjusted

    def get_x_adjusted_limits(self):
        return [self.x_adjusted_min, self.x_adjusted_max]
