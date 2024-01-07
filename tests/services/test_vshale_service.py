"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.vshale_service import (get_sp_vshale, get_gr_vshale, get_resistivity_vshale,
                                     get_neutron_density_vshale, get_linear_correlation, 
                                     get_larionov_1_correlation, get_larionov_2_correlation, 
                                     get_steiber_correlation, get_clavier_hoyle_meunier_correlation)

import numpy as np


def test_sp_vshale():
    assert get_sp_vshale(np.array([1.5]), 1, 2)[0] == 0.5


def test_gr_vshale():
    assert get_gr_vshale(np.array([1.5]), 1, 2)[0] == 0.5


def test_resistivity_vshale():
    assert get_resistivity_vshale(np.array([1.5]), 1, 2)[0] == 0.5849625007211562


def test_neutron_density_vshale():
    assert 0.999 == get_neutron_density_vshale(np.array([0.5]), np.array([1.5]), 1, 2)[0]


def test_linear_correlation():
    assert 0.5 == get_linear_correlation(np.array([0.5]))[0]


def test_get_larionov_1_correlation():
    assert 0.21621515358679566 == get_larionov_1_correlation(np.array([0.5]))[0]


def test_get_larionov_2_correlation():
    assert 0.33 == get_larionov_2_correlation(np.array([0.5]))[0]


def test_get_steiber_correlation():
    assert 0.25 == get_steiber_correlation(np.array([0.5]))[0]


def test_get_clavier_hoyle_meunier_correlation():
    assert 0.3071611722815881 == get_clavier_hoyle_meunier_correlation(np.array([0.5]))[0]
