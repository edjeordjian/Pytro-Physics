"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.ipr_service import (get_h_from_curve, get_k_from_curve, get_darcy, get_voguel,
                                  get_brown, get_klins_clark, get_fetkovich)

import numpy as np


def test_get_h_from_curve():
    assert get_h_from_curve(np.array([1, 0, 1]), 2, 4) == 1.3333333333333333


def test_get_k_from_curve():
    assert get_k_from_curve(np.array([1.0, 2.0, 3.0])) == 2.0140168333797046


def test_get_darcy():
    config = get_darcy(mu_0=1, 
                       b_0=1, 
                       re=1, 
                       rw=1, 
                       s=1, 
                       pr=1, 
                       k=1, 
                       h=1, 
                       q0_max=1, 
                       precision=5)
    assert config.get("x_axis", None) is not None
    assert config.get("y_axis", None) is not None

    assert config.get("x_axis", None)[0] == 1.0
    assert config.get("y_axis", None)[0] == -34.31073446327684


def test_get_voguel():
    config = get_voguel(pr=1, 
                        q0_max=1, 
                        precision=5)
    assert config.get("x_axis", None) is not None
    assert config.get("y_axis", None) is not None

    assert config.get("x_axis", None)[0] == 1.0
    assert config.get("y_axis", None)[0] == 0


def test_get_brown():
    config = get_brown(mu_0=1, 
                       b_0=1, 
                       re=1, 
                       rw=1, 
                       s=1, 
                       pr=1, 
                       pb=3, 
                       k=1, 
                       h=1, 
                       q0_max=None, 
                       precision=5)
    assert config.get("x_axis", None) is not None
    assert config.get("y_axis", None) is not None

    assert config.get("x_axis", None)[0] == -0.009440000000000004
    assert config.get("y_axis", None)[0] == 0


def test_get_klins_clark():
    config = get_klins_clark(pr=1, 
                             pb=1, 
                             q0_max=1, 
                             precision=5)
    assert config.get("x_axis", None) is not None
    assert config.get("y_axis", None) is not None

    assert config.get("x_axis", None)[0] == 1.0
    assert config.get("y_axis", None)[0] == 0


def test_get_fetkovich():
    config = get_fetkovich(mu_0=1, 
                           b_0=1, 
                           re=1, 
                           rw=1, 
                           s=1, 
                           pr=1, 
                           pb=1, 
                           n=1, 
                           k=1, 
                           h=1, 
                           q0_max=1, 
                           precision=5)
    assert config.get("x_axis", None) is not None
    assert config.get("y_axis", None) is not None

    assert config.get("x_axis", None)[0] == 0.01416
    assert config.get("y_axis", None)[0] == 0
