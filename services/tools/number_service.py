"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import re

import numpy as np
import pandas as pd

from constants.general_constants import DEFAULT_FORCED_MIN, DEFAULT_FORCED_MAX, number_of_decimals, \
    depth_change_multiplier

from constants.numerical_constants import APP_MIN

from numpy import log10, isnan

from services.tools.string_service import is_number, re_round_value

# Never implemented
""" def is_integer(float_number):
    parts = str(float_number).split(".")

    if len(parts) == 1 or parts[1] == "0":
        return True

    cases = [(mObj.start(1), mObj.end(1) - 1) for mObj in re.finditer(r'(^000*[1-9]+$)', parts[1])]

    if len(cases) != 0:
        return True

    return int(parts[1]) == 0

# Never implemented
def count_decimals(float_number):
    parts = str(float_number).split(".")

    if len(parts) == 1 or parts[1] == "0":
        return 0, False

    cases = [(mObj.start(1), mObj.end(1) - 1) for mObj in re.finditer(r'(^[1-9]+000+[1-9]+$)', parts[1])]

    if len(cases) != 0:
        decimals = len(parts[1][0:parts[1].index("000")])

        return decimals, False

    cases = [(mObj.start(1), mObj.end(1) - 1) for mObj in re.finditer(r'(^[1-9]+999+[1-9]+$)', parts[1])]

    if len(cases) != 0:
        decimals = len(parts[1][0:parts[1].index("999")])

        return decimals + 1, True

    return len(parts[1]), False

# Never implemented
def get_rounded_float(number):
    if is_integer(number):
        return int(number)

    decimals, re_round = count_decimals(number)

    value = round(number, decimals)

    if re_round:
        value = round(value, decimals - 1)

    return value
"""


def get_parsed_adimentional(a_curve, forced_min=DEFAULT_FORCED_MIN, forced_max=DEFAULT_FORCED_MAX):
    x_df = pd.DataFrame(a_curve, columns=["x"])

    x_df['x'].loc[(x_df['x'] < forced_min)] = forced_min

    x_df['x'].loc[(x_df['x'] > forced_max)] = forced_max

    return x_df['x'].to_numpy()


def filter_by_cutoff(cutoff_curve, cutoff_value, calculation_curve, value_to_replace):
    df = pd.DataFrame(data={
        'cutoff_curve': cutoff_curve,
        'calculation_curve': calculation_curve
    })

    df['calculation_curve'].loc[(df['cutoff_curve'] < cutoff_value)] = value_to_replace

    return df['calculation_curve'].to_list()


def celcius_to_farenheit(celcius):
    return (celcius * 9/5) + 32


def farenheit_to_celcius(farenheit):
    return (farenheit - 32) * 5/9


def get_log10(value):
    if value <= 0 or not is_number(value):
        return APP_MIN

    return log10(value)


def are_float_equal(n1, n2, delta=0.0001):
    return abs(n1 - n2) < delta


def min_with_nans(numpy_arr):
    return min(numpy_arr[~isnan(numpy_arr)])


def max_with_nans(numpy_arr):
    return max(numpy_arr[~isnan(numpy_arr)])


def change_ft_mts_list(a_list, depth_unit):
    return change_ft_mts(np.array(a_list), depth_unit)


def change_ft_mts(value, depth_unit):
    return re_round_value((value * depth_change_multiplier[depth_unit]), number_of_decimals)
