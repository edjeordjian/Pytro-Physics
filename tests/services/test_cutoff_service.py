"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.cutoff_service import (get_cutoff_general, get_cutoff_general_using_thc,
                                        get_cutoff_general_using_cutoff, 
                                        get_thickness_rectangles,
                                        get_cutoff_rectangles)

import numpy as np


def test_get_cutoff_general():
    assert get_cutoff_general(curves_list=[], 
                              cutoff_list=[[3.5]],
                              values_below_cutoff_list=[[True]], 
                              main_curve=np.array([2, 3, 4]), 
                              depth_curve=np.array([0, 1, 2]))[0] == 2


def test_get_cutoff_general_using_thc():
    assert get_cutoff_general_using_thc(curves_list=[], 
                                        cutoff_list=[[3.5]],
                                        values_below_cutoff_list=[[True]], 
                                        main_curve=np.array([2, 3, 4]), 
                                        depth_curve=np.array([0, 1, 2]), 
                                        thc_value=70, 
                                        increasing=True, 
                                        values_below_cutoff=True)["main_curve"][0] == 1


def test_get_cutoff_general_using_cutoff():
    assert get_cutoff_general_using_cutoff(curves_list=[], 
                                           cutoff_list=[[3.5]],
                                           values_below_cutoff_list=[[True]], 
                                           main_curve=np.array([2, 3, 4]), 
                                           depth_curve=np.array([0, 1, 2]), 
                                           cutoff_value=3.5, 
                                           increasing=True, 
                                           values_below_cutoff=True)["main_curve"][0] == 1


def test_get_thickness_rectangles():
    config = get_thickness_rectangles(np.array([0, 1, 0]), np.array([0, 1, 2]))
    assert config[0].get("x", None) is not None
    assert config[0].get("y", None) is not None
    assert config[0].get("value", None) is not None

    assert config[0].get("x", None)[0] == 0
    assert config[0].get("y", None)[0] == 0
    assert config[0].get("value", None) == 0


def test_get_cutoff_rectangles():
    config = get_cutoff_rectangles(np.array([2, 3, 4]), np.array([0, 1, 0]), np.array([0, 1, 2]))
    assert config[0].get("x", None) is not None
    assert config[0].get("y", None) is not None
    assert config[0].get("value", None) is not None

    assert config[0].get("x", None)[0] == 2
    assert config[0].get("y", None)[0] == 0
    assert config[0].get("value", None) == 0