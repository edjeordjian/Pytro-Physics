"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from services.temperature_service import get_geothermal_gradient, get_temperature


def test_geothermal_gradient():
    assert 0.3333333333333333 == get_geothermal_gradient(5, 4, 3)


def test_get_temperature():
    assert 9975 == get_temperature(10, np.array(1000), 3, 5)
