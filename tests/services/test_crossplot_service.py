"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.crossplot_service import (mm, minimizador, AxisMatrix, get_pef_density,
                                        get_neutron_density, get_sonic_neutron, get_sonic_density,
                                        getMN, get_rhoma_umaa, get_picket, get_hingle, 
                                        get_mineral_identification_1, get_mineral_identification_2,
                                        get_buckles)

import numpy as np

def test_mm_1():
    assert mm(3, 2, 4, 6, 1, 2, 3) == 1.5

def test_mm_2():
    assert mm(5, 2, 4, 6, 1, 2, 3) == 2.5

def test_minimizador():
    assert minimizador(np.array([3]), np.array([1.5]), np.array([2.5]), 2, 4, 6, 1, 2, 3) == 27.5625

def test_AxisMatrix_1():
    assert AxisMatrix(3, 2, 4, 6, 1, 2, 3) == 1.5

def test_AxisMatrix_2():
    assert AxisMatrix(5, 2, 4, 6, 1, 2, 3) == 2.5

def test_get_pef_density():
    config = get_pef_density(np.array([1.5]), np.array([2.5]))
    assert config.get("x_sand", None) is not None
    assert config.get("y_sand", None) is not None
    assert config.get("x_dolomite", None) is not None
    assert config.get("y_dolomite", None) is not None
    assert config.get("x_limestone", None) is not None
    assert config.get("y_limestone", None) is not None
    assert config.get("x_minimized", None) is not None
    assert config.get("y_minimized", None) is not None
    assert config.get("rho_matrix", None) is not None
    assert config.get("dt_matrix", None) is not None
    
    assert config.get("x_sand", None)[0] == 1.8
    assert config.get("y_sand", None)[0] == 2.65
    assert config.get("x_dolomite", None)[0] == 3.15
    assert config.get("y_dolomite", None)[0] == 2.87
    assert config.get("x_limestone", None)[0] == 5.05
    assert config.get("y_limestone", None)[0] == 2.71
    assert config.get("x_minimized", None)[0] == 1.4998794153645747
    assert config.get("y_minimized", None)[0] == 2.5
    assert config.get("rho_matrix", None)[0] == 2.6022915104166646
    assert config.get("dt_matrix", None)[0] == 55.16856770833341


def test_get_neutron_density():
    config = get_neutron_density(np.array([1.5]), np.array([2.5]))
    assert config.get("x_sand", None) is not None
    assert config.get("y_sand", None) is not None
    assert config.get("x_dolomite", None) is not None
    assert config.get("y_dolomite", None) is not None
    assert config.get("x_limestone", None) is not None
    assert config.get("y_limestone", None) is not None
    assert config.get("x_minimized", None) is not None
    assert config.get("y_minimized", None) is not None
    assert config.get("rho_matrix", None) is not None
    
    assert config.get("x_sand", None)[0] == -0.02
    assert config.get("y_sand", None)[0] == 2.65
    assert config.get("x_dolomite", None)[0] == 0.025
    assert config.get("y_dolomite", None)[0] == 2.87
    assert config.get("x_limestone", None)[0] == 0
    assert config.get("y_limestone", None)[0] == 2.71
    assert config.get("x_minimized", None)[0] == 0.2639999999999998
    assert config.get("y_minimized", None)[0] == 2.5
    assert config.get("rho_matrix", None)[0] == 2.87


def test_get_sonic_neutron():
    config = get_sonic_neutron(np.array([1.5]), np.array([2.5]))
    assert config.get("x_sand", None) is not None
    assert config.get("y_sand", None) is not None
    assert config.get("x_dolomite", None) is not None
    assert config.get("y_dolomite", None) is not None
    assert config.get("x_limestone", None) is not None
    assert config.get("y_limestone", None) is not None
    assert config.get("x_minimized", None) is not None
    assert config.get("y_minimized", None) is not None
    assert config.get("dt_matrix", None) is not None
    
    assert config.get("x_sand", None)[0] == -0.02
    assert config.get("y_sand", None)[0] == 53
    assert config.get("x_dolomite", None)[0] == 0.025
    assert config.get("y_dolomite", None)[0] == 43
    assert config.get("x_limestone", None)[0] == 0
    assert config.get("y_limestone", None)[0] == 47.50
    assert config.get("x_minimized", None)[0] == 1.4999812001753878
    assert config.get("y_minimized", None)[0] == 2.5
    assert config.get("dt_matrix", None)[0] == -65.33710897640337


def test_get_sonic_density():
    config = get_sonic_density(np.array([1.5]), np.array([2.5]))
    assert config.get("x_sand", None) is not None
    assert config.get("y_sand", None) is not None
    assert config.get("x_dolomite", None) is not None
    assert config.get("y_dolomite", None) is not None
    assert config.get("x_limestone", None) is not None
    assert config.get("y_limestone", None) is not None
    assert config.get("x_minimized", None) is not None
    assert config.get("y_minimized", None) is not None
    assert config.get("dt_matrix", None) is not None
    
    assert config.get("x_sand", None)[0] == 56
    assert config.get("y_sand", None)[0] == 2.65
    assert config.get("x_dolomite", None)[0] == 43
    assert config.get("y_dolomite", None)[0] == 2.87
    assert config.get("x_limestone", None)[0] == 47
    assert config.get("y_limestone", None)[0] == 2.71
    assert config.get("x_minimized", None)[0] == 1.5000266011342092
    assert config.get("y_minimized", None)[0] == 2.5
    assert config.get("dt_matrix", None)[0] == 22.54886036457132


def test_getMN():
    config = getMN(np.array([1.5]), np.array([3.5]), np.array([2.5]), 189, 1, 1)
    assert config.get("m_anhydrite", None) is not None
    assert config.get("n_anhydrite", None) is not None
    assert config.get("m_limestone", None) is not None
    assert config.get("n_limestone", None) is not None
    assert config.get("m_dolomite", None) is not None
    assert config.get("n_dolomite", None) is not None
    assert config.get("m_sandstone", None) is not None
    assert config.get("n_sandstone", None) is not None
    assert config.get("m_cast", None) is not None
    assert config.get("n_cast", None) is not None
    assert config.get("m", None) is not None
    assert config.get("n", None) is not None
    
    assert config.get("m_anhydrite", None) == 0.7
    assert config.get("n_anhydrite", None) == 0.52
    assert config.get("m_limestone", None) == 0.83
    assert config.get("n_limestone", None) == 0.58
    assert config.get("m_dolomite", None) == 0.78
    assert config.get("n_dolomite", None) == 0.52
    assert config.get("m_sandstone", None) == 0.82
    assert config.get("n_sandstone", None) == 0.62
    assert config.get("m_cast", None) == 1.04
    assert config.get("n_cast", None) == 0.29
    assert config.get("m", None)[0] == 1.2366666666666666
    assert config.get("n", None)[0] == -0.3333333333333333


def test_get_rhoma_umaa():
    config = get_rhoma_umaa(np.array([1.5]), np.array([3.5]), np.array([2.5]), 1, 1)
    assert config.get("rhoma_sandstone", None) is not None
    assert config.get("umaa_sandstone", None) is not None
    assert config.get("rhoma_dolomite", None) is not None
    assert config.get("umaa_dolomite", None) is not None
    assert config.get("rhoma_limestone", None) is not None
    assert config.get("umaa_limestone", None) is not None
    assert config.get("rhoma", None) is not None
    assert config.get("umaa", None) is not None
    
    assert config.get("rhoma_sandstone", None) == 2.65
    assert config.get("umaa_sandstone", None) == 4.8
    assert config.get("rhoma_dolomite", None) == 2.87
    assert config.get("umaa_dolomite", None) == 9
    assert config.get("rhoma_limestone", None) == 2.714
    assert config.get("umaa_limestone", None) == 13.8
    assert config.get("rhoma", None)[0] == -2.0
    assert config.get("umaa", None)[0] == -14.5


def test_get_picket():
    config = get_picket(np.array([1.5]), np.array([2.5]), 1, 1, 2)
    assert config.get("log_rt", None) is not None
    assert config.get("log_phie", None) is not None
    assert config.get("sw", None) is not None

    assert config.get("log_rt", None)[0][0] == 0.17609125905568124
    assert config.get("log_phie", None)[0][0][0] == 0.22184874961635637
    assert config.get("sw", None)[0] == 1


def test_get_hingle():
    config = get_hingle(np.array([1.5]), np.array([2.5]), 1, 1, 2)
    assert config.get("phie", None) is not None
    assert config.get("rt_1m", None) is not None
    assert config.get("sw", None) is not None

    assert config.get("phie", None)[0][0] == 1.5
    assert config.get("rt_1m", None)[0][0][0] == 0
    assert config.get("sw", None)[0] == 0


def test_get_mineral_identification_1():
    config = get_mineral_identification_1()
    assert config.get("lines", None) is not None
    assert config.get("words", None) is not None

    assert config.get("lines", None)[0].get("k", None) is not None
    assert config.get("words", None)[0].get("k", None) is not None
    assert config.get("lines", None)[0].get("th", None) is not None
    assert config.get("words", None)[0].get("th", None) is not None
    assert config.get("lines", None)[0].get("name", None) is not None
    assert config.get("words", None)[0].get("name", None) is not None

    assert config.get("lines", None)[0].get("k", None)[0] == 0
    assert config.get("words", None)[0].get("k", None) == 0.1
    assert config.get("lines", None)[0].get("th", None)[0] == 0
    assert config.get("words", None)[0].get("th", None) == 17
    assert config.get("lines", None)[0].get("name", None) == 'Th/K = 25'
    assert config.get("words", None)[0].get("name", None) == 'Min.\nPesados'


def test_get_mineral_identification_2():
    config = get_mineral_identification_2()
    assert config.get("rectangles", None) is not None
    assert config.get("words", None) is not None

    assert config.get("rectangles", None)[0].get("x", None) is not None
    assert config.get("words", None)[0].get("x", None) is not None
    assert config.get("rectangles", None)[0].get("y", None) is not None
    assert config.get("words", None)[0].get("y", None) is not None
    assert config.get("rectangles", None)[0].get("name", None) is not None
    assert config.get("words", None)[0].get("name", None) is not None

    assert config.get("rectangles", None)[0].get("x", None)[0] == np.log10(0.8)
    assert config.get("words", None)[0].get("x", None) == np.log10(0.8)
    assert config.get("rectangles", None)[0].get("y", None)[0] == 7.5
    assert config.get("words", None)[0].get("y", None) == 7.5
    assert config.get("rectangles", None)[0].get("name", None) == 'Glauconita'
    assert config.get("words", None)[0].get("name", None) == 'Glauconita'



def test_get_buckles():
    config = get_buckles()
    assert config.get("buckles", None) is not None

    assert config.get("buckles", None)[0].get("x", None) is not None
    assert config.get("buckles", None)[0].get("y", None) is not None
    assert config.get("buckles", None)[0].get("name", None) is not None

    assert config.get("buckles", None)[0].get("x", None)[0] == 0.50
    assert config.get("buckles", None)[0].get("y", None)[0] == 0.08
    assert config.get("buckles", None)[0].get("name", None) == 'BUCKL = 0.04'
