"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.swirr_service import get_swirr_timur, get_swirr_buckles

import numpy as np


def test_get_swirr():
    assert 0.999 == get_swirr_timur(np.array([100]),
                                    np.array([110]),
                                    1.2)[0]


def test_get_swirr_buckles():
    assert 0.001 == get_swirr_buckles(np.array([100]),
                                      np.array([100]),
                                      np.array([100]),
                                      np.array([100]))[0]
