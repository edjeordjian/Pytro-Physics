"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.histogram_service import (normal_mean, normal_sigma, log_normal_mean, log_normal_sigma,
                                        triangular_min, triangular_mode, triangular_max,
                                        exponential_beta, uniform_min, uniform_max)

import numpy as np

def test_normal_mean():
    assert normal_mean(np.array([1, 2, 3])) == 2


def test_normal_sigma():
    assert normal_sigma(np.array([1, 2, 3])) == 2.309401076758503


def test_log_normal_mean():
    assert log_normal_mean(np.array([3.0, 5.0, 7.0])) == 1.5513201167191744


def test_log_normal_sigma():
    assert log_normal_sigma(np.array([3.0, 5.0, 7.0])) == 1.791310173974194


def test_triangular_min():
    assert triangular_min(np.array([0, 1, 2])) == 0


def test_triangular_mode():
    assert triangular_mode(np.array([0, 1, 1, 2])) == 1


def test_triangular_max():
    assert triangular_max(np.array([0, 1, 2])) == 2


def test_exponential_beta():
    assert exponential_beta(np.array([0, 1, 2])) == 1


def test_uniform_min():
    assert uniform_min(np.array([0, 1, 2])) == 0


def test_uniform_max():
    assert uniform_max(np.array([0, 1, 2])) == 2

