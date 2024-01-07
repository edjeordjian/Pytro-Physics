"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from scipy.optimize import minimize

from constants.buckles_constants import BUCKLES_DICT

from services.tools.pandas_service import set_nan_in_array_if_another_is_nan


def mm(c, c1, c2, c3, m1, m2, m3):
    if (c <= c2):
        mm = ((m2 - m1)/(c2 - c1))*(c - c1) + m1
    else:
        mm = ((m3 - m2)/(c3 - c2))*(c - c2) + m2
    return mm


def minimizador(c, x, y, c1, c2, c3, m1, m2, m3):
    x, y = set_nan_in_array_if_another_is_nan(x, y)
    x = x[~np.isnan(x.astype(np.float))]
    y = y[~np.isnan(y.astype(np.float))]
    m = mm(c[0], c1, c2, c3, m1, m2, m3)
    C = (np.ones(len(y)))*c[0]
    x_predicted = (m*(np.array(y)) + C).tolist()
    x_true = x
    ress = (np.array(x_predicted) - np.array(x_true)).tolist()
    residuo = 0
    for i in ress:
        residuo = residuo + (i)*(i)
    return residuo


# c1 < c2 < c3, RHOMatrix1 < RHOMatrix2 < RHOMatrix3
def AxisMatrix(c, c1, c2, c3, AxisMatrix1, AxisMatrix2, AxisMatrix3):
    if c <= c2:
        return (((AxisMatrix2 - AxisMatrix1)/(c2 - c1)) * (c - c1)) + AxisMatrix1
    #else:
    return  (((AxisMatrix3 - AxisMatrix2)/(c3 - c2)) * (c - c2)) + AxisMatrix2



# TODO: Revisar tabla RHO vs DT: 
# https://docs.google.com/presentation/d/1iBaEejSEfcH8-aJujLqTU7GK-XD4k7sv/edit#slide=id.p139

# c1, c2, c3 ordenada al origen segun RHO=f(PEF)

# rho_sand = [2.65, 2.62, 2.57, 2.52, 2.44, 2.36, 2.28, 2.20, 2.12, 2.05, 1.97, 1.90]
# dt_sand = [53.00, 55.40, 58.74, 62.08, 68.76, 75.44, 82.12, 88.80, 95.48, 102.16, 108.84, 115.52]
# rho_dolomite = [2.87, 2.86, 2.81, 2.74, 2.66, 2.56, 2.46, 2.35, 2.23, 2.12]
# dt_dolomite = [43, 46.74, 54.23, 61.72, 69.21, 76.69, 84.18, 91.67, 99.15, 106.64]
# rho_limestone = [2.71, 2.67, 2.63, 2.55, 2.47, 2.39, 2.31, 2.23, 2.15, 2.07, 1.99]
# dt_limestone = [47.50, 51.04, 54.58, 61.65, 68.73, 75.80, 82.88, 89.95, 97.03, 104.10, 111.18]


# Densidad PEF
def get_pef_density(pef, rho):
    
    # https://calculadorasonline.com/calculadora-de-regresion-lineal-simple/

    # Arena: y = −1.129 + 2.083x
    # Dolomita: y = −0.798 + 1.154x
    # Caliza: y = −0.971 + 0.725x

    # y = mx + c
    # x = y*(1/m) + (-1*c/m)

    # Arena (x=f(y)): x = 0.542 + 0.48y
    # Dolomita (x=f(y)): x = 0.692 + 0.8666y
    # Caliza (x=f(y)): x = 1.3393 + 1.3792y

    c1 = 0.542  # Ordenada al origen Arena (x=f(y))
    c2 = 0.692  # Ordenada al origen Dolomita (x=f(y))
    c3 = 1.3393 # Ordenada al origen Caliza (x=f(y))

    m1 = 0.48   # Pendiente Arena (x=f(y))
    m2 = 0.8666 # Pendiente Dolomita (x=f(y))
    m3 = 1.3792 # Pendiente Caliza (x=f(y))

    x_sand = np.array([1.8, 1.75, 1.7, 1.65, 1.6, 1.55, 1.5, 1.45])
    y_sand = np.array([2.65, 2.5, 2.4, 2.3, 2.2, 2.1, 2, 1.9])
    x_dolomite = np.array([3.15, 3, 2.95, 2.9, 2.8, 2.7, 2.6, 2.5, 2.4])
    y_dolomite = np.array([2.87, 2.7, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2])
    x_limestone = np.array([5.05, 4.95, 4.8, 4.65, 4.5, 4.35, 4.25, 4.1])
    y_limestone = np.array([2.71, 2.6, 2.5, 2.4, 2.3, 2.2, 2.1, 2])

    Ajuste = minimize(minimizador, [c2], args=(pef, rho, c1, c2, c3, m1, m2, m3), method='nelder-mead', options={'maxiter': 200})
    Cajuste = Ajuste.x[0] #Ordenada al origen
    Majuste = mm(Cajuste, c1, c2, c3, m1, m2, m3) #Pendiente

    # max x_sand < max x_dolomite < max x_limestone
    pefVals = [x_sand[0], x_dolomite[0], x_limestone[0]]
    rhoVals = [y_sand[0], y_dolomite[0], y_limestone[0]]

    PEFMatrix = AxisMatrix(Cajuste, c1, c2, c3, pefVals[0], pefVals[1], pefVals[2])
    RHOMatrix = AxisMatrix(Cajuste, c1, c2, c3, rhoVals[0], rhoVals[1], rhoVals[2])
    # Para los valores DTMatrix se uso los datos de la tabla Sonico-Densidad (RHO vs DT)
    DTMatrix = AxisMatrix(Cajuste, c1, c2, c3, 53, 43, 47.5)

    # PEFmatrix = PEFmatriz(Cajuste)
    # RHOBmatrix = RHOBmatriz(Cajuste) # Devuelvo esto en caso de densidad-pef y densidad-neutron
    # DTmatrix = DTmatriz(Cajuste)     # Devuelvo esto en caso de densidad-pef y sonico-neutron

    
    # VOLAR LA PARTE DE LOS GRUPOS
    # (Al volar eso tambien vuela la parte de cuantil de regresion, esa variable ya no se usa)
    
    yAxisPaso1 = min(rho[~np.isnan(rho)])    
    if Majuste < 0:
        yAxisPaso1 = max(rho[~np.isnan(rho)])
    xAxispaso1 = (Majuste * yAxisPaso1 + Cajuste)

    config = {
        'x_sand': x_sand,
        'y_sand': y_sand,
        'x_dolomite': x_dolomite,
        'y_dolomite': y_dolomite,
        'x_limestone': x_limestone,
        'y_limestone': y_limestone,
        'x_minimized': np.array([xAxispaso1,PEFMatrix]),
        'y_minimized': np.array([yAxisPaso1,RHOMatrix]),
        'rho_matrix': np.zeros(len(rho)) + RHOMatrix,
        'dt_matrix': np.zeros(len(rho)) + DTMatrix
    }

    return config


# Densidad Neutron
def get_neutron_density(nphi, rho):

    # Arena: y = 2.609 − 1.605x
    # Dolomita: y = 2.976 − 1.802x
    # Caliza: y = 2.710 − 1.600x

    # y = mx + c
    # x = y*(1/m) + (-1*c/m)

    # Arena (x=f(y)): x = 1.6255 - 0.623y
    # Dolomita (x=f(y)): x = 1.6515 - 0.555y
    # Limestone (x=f(y)): x = 1.6937 - 1.625y

    c1 = 1.6255  # Ordenada al origen Arena (x=f(y))
    c2 = 1.6515  # Ordenada al origen Dolomita (x=f(y))
    c3 = 1.6937  # Ordenada al origen Caliza (x=f(y))

    m1 = -0.623   # Pendiente Arena (x=f(y))
    m2 = -0.555   # Pendiente Dolomita (x=f(y))
    m3 = -1.625   # Pendiente Caliza (x=f(y))

    x_sand = np.array([-0.02, 0.00, 0.03, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45])
    y_sand = np.array([2.65, 2.62, 2.57, 2.52, 2.44, 2.36, 2.28, 2.20, 2.12, 2.05, 1.97, 1.90])
    x_dolomite = np.array([0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45])
    y_dolomite = np.array([2.87, 2.860, 2.81, 2.74, 2.66, 2.56, 2.46, 2.35, 2.23, 2.12])
    x_limestone = np.array([0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45])
    y_limestone = np.array([2.71, 2.67, 2.630, 2.55, 2.47, 2.39, 2.31, 2.23, 2.15, 2.07, 1.99])

    Ajuste = minimize(minimizador, [c2], args=(nphi, rho, c1, c2, c3, m1, m2, m3), method='nelder-mead', options={'maxiter': 200})
    Cajuste = Ajuste.x[0]
    Majuste = mm(Cajuste, c1, c2, c3, m1, m2, m3)

    #PEFmatrix = PEFmatriz(Cajuste)
    #RHOBmatrix = RHOBmatriz(Cajuste)
    #DTmatrix = DTmatriz(Cajuste)

    #RHOBpaso1 = min(rho)
    #PEFpaso1 = (Majuste * RHOBpaso1 + Cajuste)

    # max x_sand < max x_dolomite < max x_limestone
    nphiVals = [x_sand[0], x_dolomite[0], x_limestone[0]]
    rhoVals = [y_sand[0], y_dolomite[0], y_limestone[0]]

    NPHIMatrix = AxisMatrix(Cajuste, c1, c2, c3, nphiVals[0], nphiVals[1], nphiVals[2])
    RHOMatrix = AxisMatrix(Cajuste, c1, c2, c3, rhoVals[0], rhoVals[1], rhoVals[2])

    yAxisPaso1 = min(rho[~np.isnan(rho)])    
    if Majuste >= 0:
        yAxisPaso1 = max(rho[~np.isnan(rho)])
    xAxispaso1 = (Majuste * yAxisPaso1 + Cajuste)

    config = {
        'x_sand': x_sand,
        'y_sand': y_sand,
        'x_dolomite': x_dolomite,
        'y_dolomite': y_dolomite,
        'x_limestone': x_limestone,
        'y_limestone': y_limestone,
        'x_minimized': np.array([xAxispaso1, NPHIMatrix]),
        'y_minimized': np.array([yAxisPaso1, RHOMatrix]),
        'rho_matrix': np.zeros(len(rho)) + RHOMatrix,
    }

    return config


# Sonico neutron
def get_sonic_neutron(nphi, dt):

    # Arena (x=f(y)): x = -0.4137 + 0.0075y
    # Dolomita (x=f(y)): x = -0.2622 + 0.0067y
    # Limestone (x=f(y)): x = -0.3357 + 0.0071y

    c1 = -0.4137  # Ordenada al origen Arena (x=f(y))
    c2 = -0.3357 # Ordenada al origen Caliza (x=f(y))
    c3 = -0.2622  # Ordenada al origen Dolomita (x=f(y))

    m1 = 0.0075   # Pendiente Arena (x=f(y))
    m2 = 0.0071   # Pendiente Caliza (x=f(y))
    m3 = 0.0067   # Pendiente Dolomita (x=f(y))

    x_sand = np.array([-0.02, 0.00, 0.03, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45])
    y_sand = np.array([53.00, 55.40, 58.74, 62.08, 68.76, 75.44, 82.12, 88.80, 95.48, 102.16, 108.84, 115.52])
    x_dolomite = np.array([0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45])
    y_dolomite = np.array([43, 46.74, 54.23, 61.72, 69.21, 76.69, 84.18, 91.67, 99.15, 106.64])
    x_limestone = np.array([0, 0.025, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45])
    y_limestone = np.array([47.50, 51.04, 54.58, 61.65, 68.73, 75.80, 82.88, 89.95, 97.03, 104.10, 111.18])

    Ajuste = minimize(minimizador, [c2], args=(nphi, dt, c1, c2, c3, m1, m2, m3), method='nelder-mead', options={'maxiter': 200})
    Cajuste = Ajuste.x[0]
    Majuste = mm(Cajuste, c1, c2, c3, m1, m2, m3)

    # PEFmatrix = PEFmatriz(Cajuste)
    # RHOBmatrix = RHOBmatriz(Cajuste)
    # DTmatrix = DTmatriz(Cajuste)

    # RHOBpaso1 = min(dt)
    # PEFpaso1 = (Majuste * RHOBpaso1 + Cajuste)

    nphiVals = [x_sand[0], x_limestone[0], x_dolomite[0]]
    dtVals = [y_sand[0], y_limestone[0], y_dolomite[0]]

    NPHIMatrix = AxisMatrix(Cajuste, c1, c2, c3, nphiVals[0], nphiVals[1], nphiVals[2])
    DTMatrix = AxisMatrix(Cajuste, c1, c2, c3, dtVals[0], dtVals[1], dtVals[2])

    print("LEN dt ", len(dt))
    print("dt: ", dt)
    print("LEN dt sin nans ", len(dt[~np.isnan(dt)]))

    yAxisPaso1 = min(dt[~np.isnan(dt)])    
    if Majuste >= 0:
        yAxisPaso1 = max(dt[~np.isnan(dt)])
    xAxispaso1 = (Majuste * yAxisPaso1 + Cajuste)

    config = {
        'x_sand': x_sand,
        'y_sand': y_sand,
        'x_dolomite': x_dolomite,
        'y_dolomite': y_dolomite,
        'x_limestone': x_limestone,
        'y_limestone': y_limestone,
        'x_minimized': np.array([xAxispaso1,NPHIMatrix]),
        'y_minimized': np.array([yAxisPaso1,DTMatrix]),
        'dt_matrix': np.zeros(len(dt)) + DTMatrix
    }

    return config

# Densidad Sonico
def get_sonic_density(dt, rho):

    # x = m*y + c

    # Arena (x=f(y)): x = 272.582 − 83.260y
    # Dolomita (x=f(y)): x = 282.527 − 81.529y
    # Limestone (x=f(y)): x = 287.172 − 88.439y

    c1 = 272.582  # Ordenada al origen Arena (x=f(y))
    c2 = 282.527  # Ordenada al origen Dolomita (x=f(y))
    c3 = 287.172 # Ordenada al origen Caliza (x=f(y))

    m1 = -83.260   # Pendiente Arena (x=f(y))
    m2 = -81.529   # Pendiente Dolomita (x=f(y))
    m3 = -88.439   # Pendiente Caliza (x=f(y))

    x_sand = np.array([56, 69, 82, 96, 109, 116])
    y_sand = np.array([2.65, 2.485, 2.32, 2.155, 1.99, 1.908])
    x_dolomite = np.array([43, 58, 72, 87, 101, 109])
    y_dolomite = np.array([2.87, 2.683, 2.496, 2.309, 2.122, 2.029])
    x_limestone = np.array([47, 61, 75, 90, 104, 111])
    y_limestone = np.array([2.71, 2.539, 2.368, 2.197, 2.026, 1.941])

    Ajuste = minimize(minimizador, [c2], args=(dt, rho, c1, c2, c3, m1, m2, m3), method='nelder-mead', options={'maxiter': 200})
    Cajuste = Ajuste.x[0]
    Majuste = mm(Cajuste, c1, c2, c3, m1, m2, m3)

    print("Ajuste: dt=", Majuste, "*RHO + ", Cajuste)

    # PEFmatrix = PEFmatriz(Cajuste)
    # RHOBmatrix = RHOBmatriz(Cajuste)
    # DTmatrix = DTmatriz(Cajuste)

    # RHOBpaso1 = min(dt)
    # PEFpaso1 = (Majuste * RHOBpaso1 + Cajuste)

    dtVals = [x_sand[0], x_limestone[0], x_dolomite[0]]
    rhoVals = [y_sand[0], y_limestone[0], y_dolomite[0]]

    DTMatrix = AxisMatrix(Cajuste, c1, c2, c3, dtVals[0], dtVals[1], dtVals[2])
    RHOMatrix = AxisMatrix(Cajuste, c1, c2, c3, rhoVals[0], rhoVals[1], rhoVals[2])

    yAxisPaso1 = min(rho[~np.isnan(rho)])    
    if Majuste >= 0:
        yAxisPaso1 = max(rho[~np.isnan(rho)])
    xAxispaso1 = (Majuste * yAxisPaso1 + Cajuste)

    config = {
        'x_sand': x_sand,
        'y_sand': y_sand,
        'x_dolomite': x_dolomite,
        'y_dolomite': y_dolomite,
        'x_limestone': x_limestone,
        'y_limestone': y_limestone,
        'x_minimized': np.array([xAxispaso1,DTMatrix]),
        'y_minimized': np.array([yAxisPaso1,RHOMatrix]),
        'rho_matrix': np.zeros(len(rho)) + RHOMatrix,
        'dt_matrix': np.zeros(len(rho)) + DTMatrix
    }

    return config


def getMN(phi_n, dt, rho, dt_f, rho_f, nphi_f):

    m_anhydrite = 0.7
    n_anhydrite = 0.52

    m_limestone = 0.83
    n_limestone = 0.58

    m_dolomite = 0.78
    n_dolomite = 0.52

    m_sandstone = 0.82
    n_sandstone = 0.62

    m_cast = 1.04
    n_cast = 0.29

    m = ((dt_f - dt) * 0.01) / (rho - rho_f)
    n = (nphi_f - phi_n) / (rho - rho_f)

    config = {
        "m_anhydrite": m_anhydrite,
        "n_anhydrite": n_anhydrite,
        "m_limestone": m_limestone,
        "n_limestone": n_limestone,
        "m_dolomite": m_dolomite,
        "n_dolomite": n_dolomite,
        "m_sandstone": m_sandstone,
        "n_sandstone": n_sandstone,
        "m_cast": m_cast,
        "n_cast": n_cast,
        "m": m,
        "n": n,
    }

    return config


def get_rhoma_umaa(phi_dn, pef, rho, pef_f, rho_f):

    rhoma_sandstone = 2.65
    umaa_sandstone = 4.8

    rhoma_dolomite = 2.87
    umaa_dolomite = 9

    rhoma_limestone = 2.714
    umaa_limestone = 13.8

    rhoma = (rho - phi_dn * rho_f) / (1 - phi_dn)
    umaa = ((pef * rho) - (phi_dn * pef_f)) / (1 - phi_dn)

    config = {
        "rhoma_sandstone": rhoma_sandstone,
        "umaa_sandstone": umaa_sandstone,
        "rhoma_dolomite": rhoma_dolomite,
        "umaa_dolomite": umaa_dolomite,
        "rhoma_limestone": rhoma_limestone,
        "umaa_limestone": umaa_limestone,
        "rhoma": rhoma,
        "umaa": umaa,
    }

    return config


def get_picket(rt, rw, a, m, n):
    sw_values = [1, 0.5, 0.3, 0.15]

    log_rt_values = []
    log_phie_values = []

    for sw in sw_values:
        min_rt = max(min(rt[~np.isnan(rt)]), -2)
        max_rt = max(rt[~np.isnan(rt)])

        log_rt_values.append([np.log10(min_rt), np.log10(max_rt)])
        log_phie_values.append([(np.log10(a) + np.log10(rw) - (n * np.log10(sw)) - np.log10(min_rt)) / m,
                                 (np.log10(a) + np.log10(rw) - (n * np.log10(sw)) - np.log10(max_rt)) / m])
    
    config = {
        'log_rt': log_rt_values,
        'log_phie': log_phie_values,
        'sw': sw_values
    }
    return config


def get_hingle(phie, rw, a, m, n):
    sw_values = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    
    phie_values = []
    rt_1m_values = []

    for sw in sw_values:
        min_phie = max(min(phie[~np.isnan(phie)]), 0)
        max_phie = max(phie[~np.isnan(phie)])

        phie_values.append([min_phie, max_phie])
        rt_1m_values.append([(((sw ** n) / (a * rw) ) ** (1/m)) * min_phie,
                             (((sw ** n) / (a * rw) ) ** (1/m)) * max_phie])


    config = {
        'phie': phie_values,
        'rt_1m': rt_1m_values,
        'sw': sw_values
    }
    return config


def get_mineral_identification_1():
    
    lines = [
        { 'k': [0, 1], 'th': [0, 25], 'name': 'Th/K = 25' },
        { 'k': [0, 2.1], 'th': [0, 25], 'name': 'Th/K = 12' },
        { 'k': [0, 5], 'th': [0, 17], 'name': 'Th/K = 3.5' },
        { 'k': [0, 5], 'th': [0, 10], 'name': 'Th/K = 2' },
        { 'k': [0, 5], 'th': [0, 7], 'name': 'Th/K = 1' },
        { 'k': [0, 5], 'th': [0, 3.17], 'name': 'Th/K = 0.6' },
        { 'k': [0, 5], 'th': [0, 1.8], 'name': 'Th/K = 0.3' }
    ]

    words = [
        { 'k': 0.1, 'th': 17, 'name': 'Min.\nPesados' },
        { 'k': 0.8, 'th': 19, 'name': 'Caolinita' },
        { 'k': 0.2, 'th': 3, 'name': 'Clorita' },
        { 'k': 0.7, 'th': 8, 'name': 'Montmorilonita' },
        { 'k': 2.1, 'th': 6, 'name': 'Ilita' },
        { 'k': 2.2, 'th': 3, 'name': 'Glauconita' },
        { 'k': 3.3, 'th': 6.2, 'name': 'Micas' },
        { 'k': 3.6, 'th': 2.5, 'name': 'Feldespato' },
        { 'k': 3.4, 'th': 1, 'name': 'Evaporitas de Potasio' },
    ]


    config = {"lines": lines, "words": words}

    return config


def get_mineral_identification_2():
    rectangles = [
        {'x': np.log10([0.8, 0.8, 1.4, 1.4, 0.8]), 'y': [7.5, 5.5, 5.5, 7.5, 7.5], 'name': 'Glauconita'},
        {'x': np.log10([1.9, 1.9, 3.1, 3.1, 1.9]), 'y': [6.3, 6.1, 6.1, 6.3, 6.3], 'name': 'Biotita'},
        {'x': np.log10([10, 10, 30, 30, 10]), 'y': [6.3, 6.15, 6.15, 6.3, 6.3], 'name': 'Clorita'},
        {'x': np.log10([2.3, 2.3, 5, 5, 2.3]), 'y': [3.75, 3.45, 3.45, 3.75, 3.75], 'name': 'Ilita'},
        {'x': np.log10([4.5, 4.5, 9.5, 9.5, 4.5]), 'y': [3.95, 2, 2, 3.95, 3.95], 'name': 'Mixed Layer'},
        {'x': np.log10([4.5, 4.5, 9.5, 9.5, 4.5]), 'y': [2.2, 2, 2, 2.2, 2.2], 'name': 'Montmorilonita'},
        {'x': np.log10([10, 10, 30, 30, 10]), 'y': [1.9, 1.8, 1.8, 1.9, 1.9], 'name': 'Caolinita'},
        {'x': np.log10([1.8, 1.8, 3.1, 3.1, 1.8]), 'y': [2.4, 2.2, 2.2, 2.4, 2.4], 'name': 'Muscovita'},
    ]

    words = [
        { 'x': np.log10(0.8), 'y': 7.5, 'name': 'Glauconita' },
        { 'x': np.log10(1.9), 'y': 6.35, 'name': 'Biotita' },
        { 'x': np.log10(10), 'y': 6.35, 'name': 'Clorita' },
        { 'x': np.log10(2.3), 'y': 3.8, 'name': 'Ilita' },
        { 'x': np.log10(4.5), 'y': 4, 'name': 'Mixed Layer' },
        { 'x': np.log10(4.5), 'y': 2.3, 'name': 'Montmorilonita' },
        { 'x': np.log10(10), 'y': 2, 'name': 'Caolinita' },
        { 'x': np.log10(1.8), 'y': 2.45, 'name': 'Muscovita' },
    ]

    config = {
        'rectangles': rectangles,
        'words': words
    }

    return config


def get_buckles():
    return BUCKLES_DICT
