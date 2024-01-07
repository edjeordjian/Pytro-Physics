"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""
import os

from functools import reduce

import xgboost as xgb

import numpy as np

from scipy.optimize import fsolve

from sklearn.ensemble import RandomForestRegressor

from sklearn.ensemble import AdaBoostRegressor

#NOTE: This line is commented when compiling the code for debugging
#      but it should be uncommented when genereating the dist version with pyinstaller
# from sklearn_local.model_selection import GridSearchCV

#NOTE: This line should be commented when generating the dist version with pyinstaller
from sklearn.model_selection import GridSearchCV

from sklearn.preprocessing import RobustScaler

from sklearn.tree import DecisionTreeRegressor

from numpy import sqrt, log10

from pandas import DataFrame

from constants.numerical_constants import APP_MIN

from services.tools.pandas_service import set_nan_in_array_if_another_is_nan


def get_train_x_y_test(dataset,
                       feature_names,
                       curve_to_predict):
    x_test = dataset[feature_names].copy()

    x_test.fillna(x_test.mean(), inplace=True)

    feature_names.append(curve_to_predict)

    dataset_without_nans = dataset[feature_names].dropna(subset=[curve_to_predict])

    y_train = dataset_without_nans[curve_to_predict].copy()

    dataset_without_nans.fillna(dataset_without_nans.mean(), inplace=True)

    x_train = dataset_without_nans.loc[:, dataset_without_nans.columns != curve_to_predict]

    return x_train, y_train, x_test


def get_train_validation_split(x_set,
                               y_set,
                               x_test,
                               fraction):
    data = DataFrame(x_set)

    data["y"] = y_set

    if fraction != 1:
        sample = data.sample(frac=fraction,
                             random_state=1)

        x_train = sample.loc[:, sample.columns != 'y']

        y_train = sample["y"].to_list()

        validation_x = data.drop(sample.index)

        validation_x = validation_x.loc[:, sample.columns != 'y']

        joined = data.join(sample, lsuffix='_left', rsuffix='_right', how='inner')

        validation = data[~data.index.isin(joined.index)]

        validation_y = validation["y"].to_list()

    else:
        x_train = data.loc[:, data.columns != 'y']

        y_train = data["y"].to_list()

        validation_x = x_test

        validation_y = None

    return x_train, \
        y_train, \
        validation_x, \
        validation_y


def get_data_from_config(config):
    fraction = config.get("fraction",
                          1)

    return get_train_validation_split(config["x_train"],
                                      config["y_train"],
                                      config["x_test"],
                                      fraction)


def xgboost_hyperparameter_search(iterations, x_train, y_train):
    random_grid = {
        "n_estimators": [100, 500, 1000],

        "max_depth": [3, 4, 5],

        "gamma": [3, 4, 5],

        "learning_rate": [0.3, 0.4, 0.5],

        "min_child_weight": [1, 2, 3],
    }

    cores = max(os.cpu_count() - 2, 1)

    search = GridSearchCV(estimator=xgb.XGBRegressor(),
                          param_grid=random_grid,
                          verbose=1,
                          n_jobs=cores)

    search.fit(x_train, y_train)

    return search.best_params_


# https://xgboost.readthedocs.io/en/stable/python/python_intro.html
# https://xgboost.readthedocs.io/en/stable/parameter.html
# https://xgboost.readthedocs.io/en/latest/python/python_api.html#module-xgboost.sklearn
def xgboost_permeability(config):
    hyperparameters = {
        "max_depth": config["max_depth"],

        "learning_rate": config["learning_rate"],

        "gamma": config["gamma"],

        "min_child_weight": config["min_child_weight"],

        "n_estimators": config["n_estimators"]
    }

    if config["search_hyperparameters"]:
        hyperparameters = xgboost_hyperparameter_search(config.get("iterations", 0),
                                                              config["x_train"],
                                                              config["y_train"])

    base_hyperparameters = {
        "random_state": 1,

        "n_jobs": -1
    }

    hyperparameters.update(base_hyperparameters)

    regresor = xgb.XGBRegressor(**hyperparameters)

    x_train_split, y_train_split, x_test_split, y_test_split = get_data_from_config(config)

    regresor.fit(x_train_split, y_train_split)

    y_to_predict = y_test_split

    x_split_20_predicted = regresor.predict(x_test_split)

    config["fraction"] = 1

    x_train, y_train, x_test, y_test = get_data_from_config(config)

    regresor = xgb.XGBRegressor(**hyperparameters)

    regresor.fit(x_train, y_train)

    predicted_curve = regresor.predict(x_test)

    return np.power(10, y_to_predict), np.power(10, x_split_20_predicted), np.power(10, predicted_curve), hyperparameters


def random_forest_hyperparameter_search(iterations, x_train, y_train):
    # https://stats.stackexchange.com/questions/403749/randomized-search-on-big-dataset
    # Percentage of possibilities covered (approximation) iterations / combinations
    random_grid = {
        "n_estimators": [50, 75, 100],

        "max_depth": [50, 75, 100],

        "min_samples_split": [0.01, 0.02, 0.05],

        "min_samples_leaf": [1, 2, 3],

        "min_weight_fraction_leaf": [0, 0.1, 0.2],

        "bootstrap": [True]
    }

    cores = max(os.cpu_count() - 2, 1)

    search = GridSearchCV(estimator=RandomForestRegressor(),
                          param_grid=random_grid,
                          verbose=1,
                          n_jobs=cores)

    search.fit(x_train, y_train)

    return search.best_params_


def random_forest_permeability(config):
    hyperparameters = {
        "max_depth": config["max_depth"],

        "n_estimators": config["n_estimators"],

        "min_samples_split": config["min_samples_split"],

        "min_samples_leaf": config["min_samples_leaf"],

        "min_weight_fraction_leaf": config["min_weight_fraction_leaf"],

        "bootstrap": True
    }

    if config["search_hyperparameters"]:
        hyperparameters = random_forest_hyperparameter_search(config.get("iterations", 0),
                                                              config["x_train"],
                                                              config["y_train"])

    base_hyperparameters = {
        "random_state": 1,

        "n_jobs": -1
    }

    hyperparameters.update(base_hyperparameters)

    regresor = RandomForestRegressor(**hyperparameters)

    x_train_split, y_train_split, x_test_split, y_test_split = get_data_from_config(config)

    regresor.fit(x_train_split, y_train_split)

    y_to_predict = y_test_split

    x_split_20_predicted = regresor.predict(x_test_split)

    config["fraction"] = 1

    x_train, y_train, x_test, y_test = get_data_from_config(config)

    regresor = RandomForestRegressor(**hyperparameters)

    regresor.fit(x_train, y_train)

    #_ = get_parsed_adimentional(y_test)

    predicted_curve = regresor.predict(x_test)

    return np.power(10, y_to_predict), np.power(10, x_split_20_predicted), np.power(10, predicted_curve), hyperparameters


def ada_boost_hyperparameter_search(iterations, x_train, y_train):
    random_grid = {
        "n_estimators": [100, 500, 1000],

        "learning_rate": [0.1, 0.5, 1.0]
    }

    cores = max(os.cpu_count() - 2, 1)

    search = GridSearchCV(estimator=AdaBoostRegressor(DecisionTreeRegressor(max_depth=10,
                                                                            random_state=1),
                                                      random_state=1),
                          param_grid=random_grid,
                          verbose=1,
                          n_jobs=cores)

    search.fit(x_train, y_train)

    return search.best_params_


def ada_bossting_permeability(config):
    hyperparameters = {
        "learning_rate": config["learning_rate"],

        "n_estimators": config["n_estimators"]
    }

    if config["search_hyperparameters"]:
        hyperparameters = ada_boost_hyperparameter_search(config.get("iterations", 0),
                                                          config["x_train"],
                                                          config["y_train"])

    base_hyperparameters = {
        "random_state": 1,

        "n_jobs": -1
    }

    hyperparameters.update(base_hyperparameters)

    regressor = AdaBoostRegressor(DecisionTreeRegressor(max_depth=10,
                                                        random_state=1),
                                  n_estimators=hyperparameters["n_estimators"],
                                  learning_rate=hyperparameters["learning_rate"],
                                  loss=config["loss"],
                                  random_state=1)

    x_train_split, y_train_split, x_test_split, y_test_split = get_data_from_config(config)

    x_scaler = RobustScaler()

    x_scaler.fit(x_train_split)

    x_train_transformed = x_scaler.transform(x_train_split)

    regressor.fit(x_train_transformed, y_train_split)

    y_to_predict = y_test_split

    x_test_transformed = x_scaler.transform(x_test_split)

    x_split_20_predicted = regressor.predict(x_test_transformed)

    regressor = AdaBoostRegressor(DecisionTreeRegressor(max_depth=10,
                                                        random_state=1),
                                  n_estimators=hyperparameters["n_estimators"],
                                  learning_rate=hyperparameters["learning_rate"],
                                  loss=config["loss"],
                                  random_state=1)

    config["fraction"] = 1

    x_train, y_train, x_test, y_test = get_data_from_config(config)

    x_scaler = RobustScaler()

    x_scaler.fit(x_train)

    x_train_transformed = x_scaler.transform(x_train)

    regressor.fit(x_train_transformed, y_train)

    x_test_transformed = x_scaler.transform(x_test)

    predicted_curve = regressor.predict(x_test_transformed)

    return np.power(10, y_to_predict), \
        np.power(10, x_split_20_predicted), \
        np.power(10, predicted_curve), \
        hyperparameters


def get_tixier_permeability(porosity,
                            swirr,
                            constant):
    return pow(constant * pow(porosity, 3) * (1 / swirr), 2)


def get_coates_permeability(porosity,
                            swirr,
                            constant):
    return pow(constant * pow(porosity, 2) * (1 - swirr) / swirr, 2)


def get_timur_permeability(porosity,
                           swirr,
                           constant):
    porosity_percentage = porosity * 100

    swirr_percentage = swirr * 100

    return constant * pow(porosity_percentage, 4.4) / pow(swirr_percentage, 2)


def _get_coates_and_dumanoir(n, swirr, porosity, ph,
                             a, resistivity, vshale, rshale,
                             w_constants):
    ph_coef = (0.077 + 1.55 * ph - 0.627 * pow(ph, 2))

    res_tirr, w = n

    next_res_tirr = 1 / (np.power(swirr, w)
                         * (np.power(porosity, w) / a * resistivity)
                         + swirr * (vshale / rshale))

    next_w = sqrt((w_constants[0] - porosity)
                  + w_constants[1]
                  * np.power(log10( (resistivity / res_tirr) * (1 / ph_coef) )
                        + w_constants[2], 2))

    return (next_res_tirr, next_w)


def get_coates_and_dumanoir(data_config):
    ph = data_config["resistivity_hydrocarbon"]

    ph_coef = (0.077 + 1.55 * ph - 0.627 * pow(ph, 2))

    c = data_config["c_constants"][0] \
        + data_config["c_constants"][1] * ph \
        - data_config["c_constants"][2] * pow(ph, 2)

    swirr = data_config["swirr"]

    porosity = data_config["porosity"]

    resistivity = data_config["resistivity"]

    a = data_config["a"]

    vshale = data_config["vshale"]

    rshale = data_config["rshale"]

    w_constants = data_config["w_constants"]

    resistivity_tirr, w, porosity_powered = [], [], []

    for i in range(len(resistivity)):
        next_sol = fsolve(_get_coates_and_dumanoir,
                          (a, a),
                          args=(swirr[i], porosity[i], ph[i], a,
                                resistivity[i], vshale[i], rshale[i], w_constants))

        resistivity_tirr.append(next_sol[0])

        w.append(next_sol[1])

        porosity_powered.append(pow(data_config["porosity"][i], 2 * w[i]))

    coates_dumanoir = pow(c * porosity_powered
                            * (1 / np.power(w, 4))
                            * np.array(resistivity_tirr)
                            / data_config["resistivity"]
                            * ph_coef,
                          2)

    return coates_dumanoir


def get_k_phi(k_core_base, phi_core_base, phie):
    k_core, phi_core = set_nan_in_array_if_another_is_nan(k_core_base, phi_core_base)

    k_core_values = k_core[~np.isnan(k_core)]

    phi_core_values = phi_core[~np.isnan(phi_core)]

    Log_x_true = np.log(phi_core_values)

    Log_y_true = np.log(k_core_values)

    Log_y_true[Log_y_true == np.log(0)] = APP_MIN

    N = len(k_core_values)

    sumaxy = reduce(lambda a, b: a + b, Log_x_true * Log_y_true)

    sumax = reduce(lambda a, b: a + b, Log_x_true)

    sumay = reduce(lambda a, b: a + b, Log_y_true)

    sumax2 = reduce(lambda a, b: a + b, Log_x_true * Log_x_true)

    m = (N * sumaxy - sumax * sumay) / (N * sumax2 - sumax * sumax)

    b = (sumay - m * sumax) / N

    return phi_core, np.exp(b + np.log(phie) * m), m, b, k_core_values, phi_core_values
