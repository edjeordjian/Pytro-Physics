"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

def get_geothermal_gradient(bht, env_temperature, z_bht):
    return (bht - env_temperature) / z_bht


def get_temperature(gg_value, depth_curve, z_bht, bht):
    return gg_value * (depth_curve - z_bht) + bht