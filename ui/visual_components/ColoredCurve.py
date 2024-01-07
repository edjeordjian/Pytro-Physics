"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""


class ColoredCurve:
    def __init__(self, config):
        self.base_name = config["curve_name"]

        self.color_name = config["color_name"]

        self.marker_name = config["line_marker"]

        self.style_name = config["style"]

        self.curve = config["curve"]

        self.axis = config["add_axis"]

        self.is_scatter = config["scatter_curve"]

        self.is_log = config["is_log"]

        self.is_y_log = config["is_y_log"]

        self.is_reverse = config["is_reverse"]

        self.x_label = config["x_label"]

        self.cummulative = config["cummulative"]

        self.original_x_data = config["x_axis"]

        self.original_y_data = config["y_axis"]

    def get_name(self):
        return self.base_name + " ("\
               + self.color_name\
               + ")"

    def get_color_name(self):
        return self.color_name

    def get_marker_name(self):
        return self.marker_name

    def get_style_name(self):
        return self.style_name

    def is_cummulative(self):
        return self.cummulative

    def has_axis(self):
        return self.axis

    def get_is_cummulative(self):
        return self.cummulative

    def get_curve(self):
        return self.curve

    def get_x_data(self):
        return self.original_x_data
    
    def get_y_data(self):
        return self.original_y_data

    def get_is_log(self):
        return self.is_log

    def get_is_reverse(self):
        return self.is_reverse

