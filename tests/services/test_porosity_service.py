"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.porosity_service import (get_porosity_with_density, get_porosity_asquith_gibson,
                                       get_porosity_by_wyllie, get_porosity_by_gardner_hunt_raymer,
                                       get_effective_porosity)

import numpy as np


def test_get_porosity_with_density():
    assert get_porosity_with_density(np.array([0.2, 0.3, 0.4]), 2, 3, 0, 1)[0] == 1.0


def test_get_porosity_asquith_gibson():
    assert get_porosity_asquith_gibson(np.array([0.3, 0.6, 0.9]), np.array([0.1, 0.2, 0.3]), 0, 1)[0] == 0.22360679774997896


def test_get_porosity_by_wyllie():
    assert get_porosity_by_wyllie(4, 6, 9, np.array([1.0, 2.0, 3.0]), 0, 1)[0] == 0.06666666666666667


def test_get_porosity_by_gardner_hunt_raymer():
    assert get_porosity_by_gardner_hunt_raymer(3, np.array([1.0, 2.0, 3.0]), 0, 1)[0] == 0.4166666666666667


def test_get_effective_porosity():
    assert get_effective_porosity(np.array([1.0, 2.0, 3.0]), np.array([0.5, 0.6, 0.3]), 0, 1)[0] == 0.5
