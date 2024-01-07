"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""


class ColoredRectangle:
    def __init__(self, config):
        self.curve = config["curve"]

        self.config = config

    def get_curve(self):
        return self.curve
