"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.permeability_service import get_k_phi, get_coates_and_dumanoir, get_timur_permeability, \
    get_coates_permeability, get_tixier_permeability, ada_bossting_permeability, get_train_x_y_test, \
    xgboost_permeability, random_forest_permeability

import numpy as np

import pandas as pd

from services.tools.number_service import are_float_equal


def test_get_k_phi():
    phi_core, \
        predicted, \
        m, \
        b, \
        k_core_values, \
        phi_core_values = get_k_phi(np.array([10, 11]),
                                    np.array([5, 6]),
                                    np.array([3, 4]))

    assert 5 == phi_core[0]

    assert are_float_equal(7.656435641989978, predicted[0])

    assert are_float_equal(0.5227586988632897, m)

    assert are_float_equal(1.4612374239887402, b)

    assert 10 == k_core_values[0]

    assert 5 == phi_core_values[0]


def test_get_coates_and_dumanoir():
    data_config = {
        "porosity": np.array([1]),
        "resistivity_hydrocarbon": np.array([2]),
        "swirr": np.array([3]),
        "a": 4,
        "vshale": np.array([5]),
        "rshale": np.array([6]),
        "resistivity": np.array([7]),
        "w_constants": [1, 2, 3],
        "c_constants": [4, 5, 6]
    }

    assert are_float_equal(2.0953488461029502e-10,
                           get_coates_and_dumanoir(data_config)[0])


def test_get_timur_permeability():
    assert are_float_equal(16682283.805297691,
                           get_timur_permeability(np.array([5]),
                                                  np.array([3]),
                                                  np.array(2))[0])


def test_get_coates_permeability():
    assert are_float_equal(1111.1111111111113,
                           get_coates_permeability(np.array([5]),
                                                   np.array([3]),
                                                   np.array(2))[0])


def test_get_tixier_permeability():
    assert are_float_equal(6944.444444444443,
                           get_tixier_permeability(np.array([5]),
                                                   np.array([3]),
                                                   np.array(2))[0])


def test_ada_bossting_permeability():
    dataset = pd.DataFrame(data={
        "A": np.array([23, 24, 25, 26]),

        "B": np.array([24, 25, 26, 27]),

        "y": np.array([25, 26, 27, 29])
    })

    x_train, y_train, x_test = get_train_x_y_test(dataset,
                                                  ["A", "B"],
                                                  "y")

    config = {
            "learning_rate": 100,

            "n_estimators":  100,

            'loss': "linear",

            "x_train": x_train,

            "y_train": y_train,

            "x_test": x_test,

            "fraction": 0.8,

            "search_hyperparameters": False,

            # "iterations": 1000
        }

    y_to_predict, \
        split_20_predicted, \
        predicted_curve, \
        hyperparameters = ada_bossting_permeability(config)

    assert are_float_equal(-469762048, y_to_predict[0])


def test_ada_bossting_permeability_searching_hyperparameters():
    dataset = pd.DataFrame(data={
        "A": np.array([23, 24, 25, 26, 11]),

        "B": np.array([24, 25, 26, 27, 12]),

        "y": np.array([25, 26, 27, 29, 13])
    })

    x_train, y_train, x_test = get_train_x_y_test(dataset,
                                                  ["A", "B"],
                                                  "y")

    config = {
            "learning_rate": 100,

            "n_estimators":  100,

            'loss': "linear",

            "x_train": x_train,

            "y_train": y_train,

            "x_test": x_test,

            "fraction": 0.8,

            "search_hyperparameters": True,

            # "iterations": 1000
        }

    y_to_predict, \
        split_20_predicted, \
        predicted_curve, \
        hyperparameters = ada_bossting_permeability(config)

    assert are_float_equal(-1610612736, y_to_predict[0])


def test_xgboost_permeability():
    dataset = pd.DataFrame(data={
        "A": np.array([23, 24, 25, 26]),

        "B": np.array([24, 25, 26, 27]),

        "y": np.array([25, 26, 27, 29])
    })

    x_train, y_train, x_test = get_train_x_y_test(dataset,
                                                  ["A", "B"],
                                                  "y")

    config = {
            "max_depth": 100,

            "learning_rate": 100,

            "gamma": 100,

            "min_child_weight": 100,

            "n_estimators": 100,

            'loss': "linear",

            "x_train": x_train,

            "y_train": y_train,

            "x_test": x_test,

            "fraction": 0.8,

            "search_hyperparameters": False,

            # "iterations": 1000
        }

    y_to_predict, \
        split_20_predicted, \
        predicted_curve, \
        hyperparameters = xgboost_permeability(config)

    assert are_float_equal(-469762048, y_to_predict[0])


def test_xgboost_permeability_with_hyperparameters():
    dataset = pd.DataFrame(data={
        "A": np.array([23, 24, 25, 26, 11]),

        "B": np.array([24, 25, 26, 27, 21]),

        "y": np.array([25, 26, 27, 29, 31])
    })

    x_train, y_train, x_test = get_train_x_y_test(dataset,
                                                  ["A", "B"],
                                                  "y")

    config = {
            "max_depth": 10,

            "learning_rate": 10,

            "gamma": 10,

            "min_child_weight": 10,

            "n_estimators": 10,

            'loss': "linear",

            "x_train": x_train,

            "y_train": y_train,

            "x_test": x_test,

            "fraction": 0.8,

            "search_hyperparameters": True,

            # "iterations": 1000
        }

    y_to_predict, \
        split_20_predicted, \
        predicted_curve, \
        hyperparameters = xgboost_permeability(config)

    assert are_float_equal(-1610612736, y_to_predict[0])


def test_random_forest_permeability():
    dataset = pd.DataFrame(data={
        "A": np.array([23, 24, 25, 26]),

        "B": np.array([24, 25, 26, 27]),

        "y": np.array([25, 26, 27, 29])
    })

    x_train, y_train, x_test = get_train_x_y_test(dataset,
                                                  ["A", "B"],
                                                  "y")

    config = {
            "max_depth": 100,

            "n_estimators": 10,

            "min_samples_split": 0.5,

            "min_samples_leaf": 0.5,

            "min_weight_fraction_leaf": 0.5,

            "bootstrap": True,

            'loss': "linear",

            "x_train": x_train,

            "y_train": y_train,

            "x_test": x_test,

            "fraction": 0.8,

            "search_hyperparameters": False,

            # "iterations": 1000
        }

    y_to_predict, \
        split_20_predicted, \
        predicted_curve, \
        hyperparameters = random_forest_permeability(config)

    assert are_float_equal(-469762048, y_to_predict[0])


def test_random_forest_permeability_with_hyperparameters():
    dataset = pd.DataFrame(data={
        "A": np.array([23, 24, 25, 26, 11]),

        "B": np.array([24, 25, 26, 27, 12]),

        "y": np.array([25, 26, 27, 29, 13])
    })

    x_train, y_train, x_test = get_train_x_y_test(dataset,
                                                  ["A", "B"],
                                                  "y")

    config = {
            "max_depth": 100,

            "n_estimators": 10,

            "min_samples_split": 0.5,

            "min_samples_leaf": 0.5,

            "min_weight_fraction_leaf": 0.5,

            "bootstrap": True,

            'loss': "linear",

            "x_train": x_train,

            "y_train": y_train,

            "x_test": x_test,

            "fraction": 0.8,

            "search_hyperparameters": True,

            # "iterations": 1000
        }

    y_to_predict, \
        split_20_predicted, \
        predicted_curve, \
        hyperparameters = random_forest_permeability(config)

    assert are_float_equal(-1610612736, y_to_predict[0])

