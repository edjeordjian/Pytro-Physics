"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

import numpy as np

import pandas as pd

from scipy.optimize import minimize, LinearConstraint

from multiprocessing import Pool

from constants.LITHOLOGY_CONSTANTS import RHOwsh, RHOf, PHIemax, DTwsh, DTcoal, DTanhy, DTf, PEf, NEUTRONf


def DTCO_equations(p,
                   xi,
                   lithologies):
    v1, v2, v3, v4, \
    v5, v6, v7, v8,\
    phie_e = p

    E = np.empty(4)

    w1 = 1
    w2 = 1
    w3 = 1
    w4 = 1

    E[0] = (
            (
                (
                  (
                    (
                     float(lithologies[0]["density"]) * xi["vshale"] +
                     float(lithologies[1]["density"]) * (v1) +
                     float(lithologies[2]["density"]) * (v2) +
                     float(lithologies[3]["density"]) * (v3) +
                     float(lithologies[4]["density"]) * (v4) +
                     float(lithologies[5]["density"]) * (v5) +
                     float(lithologies[6]["density"]) * (v6) +
                     float(lithologies[7]["density"]) * (v7) +
                     float(lithologies[8]["density"]) * (v8) +
                     RHOf * phie_e
                     ) / xi["rho"] - 1
                  ) if xi["rho"] != 0 else 0
                ) * 100
            ) ** 2
        ) * (w1 / (w1 + w2 + w3 + w4))

    E[1] = (
            (
              (
                (
                (
                 float(lithologies[0]["sonic"]) * xi["vshale"] +
                 float(lithologies[1]["sonic"]) * (v1) +
                 float(lithologies[2]["sonic"]) * (v2) +
                 float(lithologies[3]["sonic"]) * (v3) +
                 float(lithologies[4]["sonic"]) * (v4) +
                 float(lithologies[5]["sonic"]) * (v5) +
                 float(lithologies[6]["sonic"]) * (v6) +
                 float(lithologies[7]["sonic"]) * (v7) +
                 float(lithologies[8]["sonic"]) * (v8) +
                 DTf * phie_e
                 ) / xi["dt"] - 1
              ) if xi["dt"] != 0 else 0
              ) * 100
            ) ** 2
           ) * (w2 / (w1 + w2 + w3 + w4))

    E[2] = (
            (
             (
                (
                (
                 float(lithologies[0]["density"]) * float(lithologies[1]["pef"]) * xi["vshale"] +
                 float(lithologies[1]["density"]) * float(lithologies[1]["pef"]) * (v1) +
                 float(lithologies[2]["density"]) * float(lithologies[2]["pef"]) * (v2) +
                 float(lithologies[3]["density"]) * float(lithologies[3]["pef"]) * (v3) +
                 float(lithologies[4]["density"]) * float(lithologies[4]["pef"]) * (v4) +
                 float(lithologies[5]["density"]) * float(lithologies[5]["pef"]) * (v5) +
                 float(lithologies[6]["density"]) * float(lithologies[6]["pef"]) * (v6) +
                 float(lithologies[7]["density"]) * float(lithologies[7]["pef"]) * (v7) +
                 float(lithologies[8]["density"]) * float(lithologies[8]["pef"]) * (v8) +
                 (RHOf * PEf) * phie_e
                 ) / (xi["pef"] * xi["rho"]) - 1
             ) if (xi["rho"] and xi["pef"]) != 0 else 0
             ) * 100
      ) ** 2
    ) * (w3 / (w1 + w2 + w3 + w4))

    lit_0_denominator = 100 if lithologies[0]["neutron_fraction"] else 1
    lit_1_denominator = 100 if lithologies[1]["neutron_fraction"] else 1
    lit_2_denominator = 100 if lithologies[2]["neutron_fraction"] else 1
    lit_3_denominator = 100 if lithologies[3]["neutron_fraction"] else 1
    lit_4_denominator = 100 if lithologies[4]["neutron_fraction"] else 1
    lit_5_denominator = 100 if lithologies[5]["neutron_fraction"] else 1
    lit_6_denominator = 100 if lithologies[6]["neutron_fraction"] else 1
    lit_7_denominator = 100 if lithologies[7]["neutron_fraction"] else 1
    lit_8_denominator = 100 if lithologies[8]["neutron_fraction"] else 1

    E[3] = (
            (
             (
              (
                (
                float(lithologies[0]["neutron"]) * xi["vshale"] / lit_0_denominator +
                float(lithologies[1]["neutron"]) * (v1) / lit_1_denominator +
                float(lithologies[2]["neutron"]) * (v2) / lit_2_denominator +
                float(lithologies[3]["neutron"]) * (v3) / lit_3_denominator +
                float(lithologies[4]["neutron"]) * (v4) / lit_4_denominator +
                float(lithologies[5]["neutron"]) * (v5) / lit_5_denominator +
                float(lithologies[6]["neutron"]) * (v6) / lit_6_denominator +
                float(lithologies[7]["neutron"]) * (v7) / lit_7_denominator +
                float(lithologies[8]["neutron"]) * (v8) / lit_8_denominator +
                NEUTRONf * phie_e
                ) / xi["neutron"] - 1
              ) if xi["neutron"] != 0 else 0
             ) * 100
            ) ** 2
           ) * (w4 / (w1 + w2 + w3 + w4))

    return (E[0] + E[1] + E[2] + E[3])


def get_next_DTCO_solution(xi):
    bounds = xi["bounds"]

    PHIsh = ((RHOwsh - xi["rhodsh"]) / (RHOf - xi["rhodsh"]))

    DTdsh = ((DTwsh - (DTf) * (PHIsh)) / (1 - PHIsh))

    lithologies = xi["lithologies"]

    if xi["carbon"] is not None and xi["rho"] <= xi["carbon"]:
        result = [0, 0, 0, 0,
                  0, 0, 0, 0,
                  0, 0, xi["carbon"], DTcoal,
                  0]

        if xi["carbon_idx"] > 0:
            result[xi["carbon_idx"]] = 1

        return tuple(result)

    if xi["anhydrit"] is not None and xi["rho"] >= xi["anhydrit"]:
        result = [0, 0, 0, 0,
                  0, 0, 0, 0,
                  0, 0, xi["anhydrit"], DTanhy,
                  0]

        if xi["anhidrit_idx"] > 0:
            result[xi["anhidrit_idx"]] = 1

        return tuple(result)

    if xi["vshale"] == 1:
        return (0, 0, 0, 0,
                0, 0, 0, 0,
                PHIsh, 0, xi["rhodsh"], DTdsh,
                1 - PHIsh)

    #initial points
    vi = (1 - xi["vshale"])/4

    pGuess = np.array([vi, vi, vi, vi, vi, vi, vi, vi, vi])

    # Constrain
    linear_constraint = LinearConstraint([[1, 1, 1, 1, 1, 1, 1, 1, 1]], [1 - xi["vshale"]], [1 - xi["vshale"]])

    # Solve the constrained optimization problem
    p = minimize(lambda p: np.linalg.norm(DTCO_equations(p, xi, lithologies)),
                 x0=pGuess,
                 bounds=bounds,
                 constraints=[linear_constraint])

    v1 = round(min(1, max(0, p.x[0])), 5)
    v2 = round(min(1, max(0, p.x[1])), 5)
    v3 = round(min(1, max(0, p.x[2])), 5)
    v4 = round(min(1, max(0, p.x[3])), 5)
    v5 = round(min(1, max(0, p.x[4])), 5)
    v6 = round(min(1, max(0, p.x[5])), 5)
    v7 = round(min(1, max(0, p.x[6])), 5)
    v8 = round(min(1, max(0, p.x[7])), 5)
    phie = round(min(PHIsh, max(0, p.x[8])), 5)

    total = v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + xi["vshale"] * (1 - PHIsh)

    phit = (phie + PHIsh * xi["vshale"])

    rhomma = (v1 * float(lithologies[1]["density"])
              + v2 * float(lithologies[2]["density"])
              + v3 * float(lithologies[3]["density"])
              + v4 * float(lithologies[4]["density"])
              + v5 * float(lithologies[5]["density"])
              + v6 * float(lithologies[6]["density"])
              + v7 * float(lithologies[7]["density"])
              + v8 * float(lithologies[8]["density"])
              + xi["vshale"] * (1 - PHIsh) * xi["rhodsh"]) / total

    dtma = (v1 * float(lithologies[1]["sonic"])
              + v2 * float(lithologies[2]["sonic"])
              + v3 * float(lithologies[3]["sonic"])
              + v4 * float(lithologies[4]["sonic"])
              + v5 * float(lithologies[5]["sonic"])
              + v6 * float(lithologies[6]["sonic"])
              + v7 * float(lithologies[7]["sonic"])
              + v8 * float(lithologies[8]["sonic"])
              + xi["vshale"] * (1 - PHIsh) * DTwsh) / total

    vdsh = xi["vshale"] * (1 - PHIsh)

    return (v1, v2, v3, v4,
            v5, v6, v7, v8,
            phit, phie, rhomma, dtma,
            vdsh)


def get_DTCO_variables(DTCO_data,
                       lithologies):
    _curves = [DTCO_data["rho_b"],
              DTCO_data["dt"],
              DTCO_data["pef"],
              DTCO_data["neutron"],
              DTCO_data["vshale"]]

    curves_to_use = list(
        filter(lambda curve: curve is not None,
               _curves)
    )

    if curves_to_use == 0 or DTCO_data["vshale"] is None:
        return {
            "vshale": [],

            "phie":  [],

            "lean_lit1":  [],

            "lean_lit2":  [],

            "lean_lit3":  [],

            "lean_lit4":  [],

            "lean_lit5":  [],

            "lean_lit6":  [],

            "lean_lit7":  [],

            "lean_lit8":  [],

            "lit1":  [],

            "lit2":  [],

            "lit3":  [],

            "lit4":  [],

            "lit5":  [],

            "lit6":  [],

            "lit7":  [],

            "lit8":  [],

            "cummulative_porosity":  [],

            "rho":  [],

            "dt":  []
        }

    v_shale = None

    PHIsh = ((RHOwsh - DTCO_data["rhodsh"]) / (RHOf - DTCO_data["rhodsh"]))

    if DTCO_data["vshale"] is not None:
        v_shale = list(
            map(lambda v: round(min(1, max(0, v)), 5),
                DTCO_data["vshale"])
        )

    #v_shale = list(
    #    map(lambda v: 1 - PHIsh if v == 1 else v,
    #        v_shale)
    #)

    bounds = np.array([(0.001, 0.999) if DTCO_data["lithology1"] is not None else (0.000, 0.000),
                       (0.001, 0.999) if DTCO_data["lithology2"] is not None else (0.000, 0.000),
                       (0.001, 0.999) if DTCO_data["lithology3"] is not None else (0.000, 0.000),
                       (0.001, 0.999) if DTCO_data["lithology4"] is not None else (0.000, 0.000),
                       (0.001, 0.999) if DTCO_data["lithology5"] is not None else (0.000, 0.000),
                       (0.001, 0.999) if DTCO_data["lithology6"] is not None else (0.000, 0.000),
                       (0.001, 0.999) if DTCO_data["lithology7"] is not None else (0.000, 0.000),
                       (0.001, 0.999) if DTCO_data["lithology8"] is not None else (0.000, 0.000),
                       (0, PHIemax)])

    DTCO_data_copy = pd.DataFrame()

    DTCO_data_copy["rho_b"] = DTCO_data["rho_b"].copy() if DTCO_data["rho_b"] is not None else None

    DTCO_data_copy["dt"] = DTCO_data["dt"].copy() if DTCO_data["dt"] is not None else None

    DTCO_data_copy["pef"] = DTCO_data["pef"].copy() if DTCO_data["pef"] is not None else None

    DTCO_data_copy["neutron"] = DTCO_data["neutron"].copy() if DTCO_data["neutron"] is not None else None

    DTCO_data_copy["vshale"] = DTCO_data["vshale"].copy() if DTCO_data["vshale"] is not None else None

    DTCO_data_copy["rho_b"] = DTCO_data_copy["rho_b"].replace(np.nan, 0)

    DTCO_data_copy["dt"] = DTCO_data_copy["dt"].replace(np.nan, 0)

    DTCO_data_copy["pef"] = DTCO_data_copy["pef"].replace(np.nan, 0)

    DTCO_data_copy["neutron"] = DTCO_data_copy["neutron"].replace(np.nan, 0)

    DTCO_data_copy["vshale"] = DTCO_data_copy["vshale"].replace(np.nan, 0)

    rho_b = DTCO_data_copy["rho_b"] if DTCO_data["rho_b"] is not None \
                               else [0] * len(curves_to_use[0]),

    dt = DTCO_data_copy["dt"] if DTCO_data["dt"] is not None \
                         else [0] * len(curves_to_use[0]),

    pef = DTCO_data_copy["pef"] if DTCO_data["pef"] is not None \
                           else [0] * len(curves_to_use[0]),

    neutron = DTCO_data_copy["neutron"] if DTCO_data["neutron"] is not None \
                                   else [0] * len(curves_to_use[0]),

    vshale = DTCO_data_copy["vshale"] if DTCO_data["vshale"] is not None \
                                       else [0] * len(curves_to_use[0])

    xi = [{
            "rho": rho_b[0][i],
            "dt":  dt[0][i],
            "pef": pef[0][i],
            "neutron": neutron[0][i],
            "vshale": vshale[i],
            "bounds": bounds,
            "lithologies": lithologies,
            "carbon": DTCO_data["carbon"],
            "anhydrit": DTCO_data["anhydrit"],
            "rhodsh": DTCO_data["rhodsh"],
            "carbon_idx": DTCO_data["carbon_idx"],
            "anhidrit_idx": DTCO_data["anhidrit_idx"]
        }

        for i in range(0, len(curves_to_use[0]))
    ]

    # https://github.com/ultralytics/yolov3/issues/1643
    # on Windows NumPythonProcesses*MemoryPerProcess < RAM + PageFileSize must be true or you will hit this error:
    # [WinError 1455] The paging file is too small for this operation to complete
    cores = max(os.cpu_count() - 2, 1)

    pool = Pool(processes=cores)

    result = pool.map(get_next_DTCO_solution,
                      xi)

    pool.close()

    pool.join()

    # Without multiprocessing:
    #result = []

    #for i in xi:
    #    result.append(get_next_DTCO_solution(i))

    result_df = pd.DataFrame(result,
                             columns=["lithology1", "lithology2", "lithology3", "lithology4",
                                      "lithology5", "lithology6", "lithology7", "lithology8",
                                      "porosity", "phie", "rho", "dt",
                                      "vshale"])

    vshale = result_df["vshale"]

    V1 = vshale + result_df["lithology1"]

    V2 = V1 + result_df["lithology2"]

    V3 = V2 + result_df["lithology3"]

    V4 = V3 + result_df["lithology4"]

    V5 = V4 + result_df["lithology5"]

    V6 = V5 + result_df["lithology6"]

    V7 = V6 + result_df["lithology7"]

    V8 = V7 + result_df["lithology8"]

    #  phit = (v40 + (PHIsh)*(Vsh))
    porosity = V8 + result_df["phie"]

    rho = result_df["rho"]

    dt = result_df["dt"]

    volumes = [porosity.to_list(),
               V1.to_list(), V2.to_list(), V3.to_list(), V4.to_list(),
               V5.to_list(), V6.to_list(), V7.to_list(), V8.to_list(),
               vshale.to_list(), rho.to_list(), dt.to_list()]

    # Cannot refactor pool use in a separated method
    #pool = Pool(processes=cores)

    #volumes = pool.map(get_lists_to_return,
    #                   volume_list)

    #pool.close()

    #pool.join()

    lean_lithologies = [result_df["phie"].to_list(),
                        result_df["lithology1"].to_list(), result_df["lithology2"].to_list(),
                        result_df["lithology3"].to_list(), result_df["lithology4"].to_list(),
                        result_df["lithology5"].to_list(), result_df["lithology6"].to_list(),
                        result_df["lithology7"].to_list(), result_df["lithology8"].to_list(),
                        result_df["vshale"].to_list(), result_df["rho"].to_list(), result_df["dt"].to_list()]

    #pool = Pool(processes=cores)

    #lean_lithologies = pool.map(get_lists_to_return,
    #                            lithologies_list)

    #pool.close()

    #pool.join()

    return {
        "vshale": lean_lithologies[9],

        "phie": lean_lithologies[0],

        "lean_lit1": lean_lithologies[1],

        "lean_lit2": lean_lithologies[2],

        "lean_lit3": lean_lithologies[3],

        "lean_lit4": lean_lithologies[4],

        "lean_lit5": lean_lithologies[5],

        "lean_lit6": lean_lithologies[6],

        "lean_lit7": lean_lithologies[7],

        "lean_lit8": lean_lithologies[8],

        "lit1": volumes[1],

        "lit2": volumes[2],

        "lit3": volumes[3],

        "lit4": volumes[4],

        "lit5": volumes[5],

        "lit6": volumes[6],

        "lit7": volumes[7],

        "lit8": volumes[8],

        "cummulative_porosity": volumes[0],

        "rho": lean_lithologies[10],

        "dt": lean_lithologies[11]
    }


# Seems to have the same performance as to_numpy
#def get_lists_to_return(series):
#    return series.to_list()

