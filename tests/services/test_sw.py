"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.sw_service import (get_so_sg, get_rw, get_sw_archie, get_sw_dual_water,
                                 get_sw_modified_simandoux, get_sw_simandoux, 
                                 get_sw_indonesia, get_sw_fertl)

import numpy as np


def test_get_so_sg():
    assert get_so_sg(np.array([0.3, 0.6, 0.9]))[0] == 0.7


def test_get_rw():
    assert get_rw(5, np.array([0.3, 0.6, 0.9]), 
                     np.array([0.1, 0.2, 0.3]), True, True)[0] == 5.046296296296296


def test_get_sw_archie():
    assert get_sw_archie(1, 2, 2, np.array([0.3, 0.6, 0.9]), 
                                  np.array([0.1, 0.2, 0.3]), 
                                  np.array([0.2, 0.3, 0.4]), False)[0] == 2.3570226039551585


def test_get_sw_dual_water():
    assert get_sw_dual_water(1, 2, 2, 3, 
                             np.array([0.3, 0.6, 0.9]), 
                             np.array([0.1, 0.2, 0.3]), 
                             np.array([0.2, 0.3, 0.4]), 
                             np.array([0.5, 0.6, 0.7]), 
                             np.array([0.3, 0.6, 0.9]), False)[0] == 11.58091375187368


def test_get_sw_modified_simandoux():
    assert get_sw_modified_simandoux(1, 2, 2, 5, 3, 
                             np.array([0.3, 0.6, 0.9]), 
                             np.array([0.1, 0.2, 0.3]), 
                             np.array([0.2, 0.3, 0.4]), 
                             np.array([0.5, 0.6, 0.7]), False)[0] == 2.0860800026983277


def test_get_sw_simandoux():
    assert get_sw_simandoux(1, 2, 5, 
                             np.array([0.3, 0.6, 0.9]), 
                             np.array([0.1, 0.2, 0.3]), 
                             np.array([0.2, 0.3, 0.4]), 
                             np.array([0.5, 0.6, 0.7]), False)[0] == 2.3021216859914384


def test_get_sw_indonesia():
    assert get_sw_indonesia(1, 2, 5, 2, 
                             np.array([0.3, 0.6, 0.9]), 
                             np.array([0.1, 0.2, 0.3]), 
                             np.array([0.2, 0.3, 0.4]), 
                             np.array([0.5, 0.6, 0.7]), False)[0] == 1.840994144956234


def test_get_sw_fertl():
    assert get_sw_fertl(1, 2, 0.5, 
                             np.array([0.3, 0.6, 0.9]), 
                             np.array([0.1, 0.2, 0.3]), 
                             np.array([0.2, 0.3, 0.4]), 
                             np.array([0.5, 0.6, 0.7]), False)[0] == 1.9769011027241787
