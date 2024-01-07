"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from scipy.stats import mode

def normal_mean(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        return np.sum(curve_data)/len(curve_data)
    else:
        return None


def normal_sigma(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        sample_mean = normal_mean(curve_data)
        return np.sqrt(((np.sum(curve_data) - sample_mean)**2) / (len(curve_data)))
    else:
        return None


# https://stats.stackexchange.com/questions/438536/how-to-estimate-log-normal-distribution-parameters-from-a-set-of-data
def log_normal_mean(curve_data):
    curve_data[curve_data==0] = np.nan
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        log_curve_data = np.log(curve_data)
        return normal_mean(log_curve_data)
    else:
        return None


def log_normal_sigma(curve_data):
    curve_data[curve_data==0] = np.nan
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        log_curve_data = np.log(curve_data)
        return normal_sigma(log_curve_data)
    else:
        return None


def triangular_min(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        return min(curve_data)
    else:
        return None


def triangular_mode(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        return mode(curve_data, keepdims=True)[0][0]
    else:
        return None


def triangular_max(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        return max(curve_data)
    else:
        return None


#https://stats.stackexchange.com/questions/497086/how-to-find-a-good-estimator-for-lambda-in-exponential-distibution
def exponential_beta(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        return normal_mean(curve_data)
    else:
        return None


def uniform_min(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        return min(curve_data)
    else:
        return None


def uniform_max(curve_data):
    curve_data = curve_data[~np.isnan(curve_data)]
    if len(curve_data) > 0:
        return max(curve_data)
    else:
        return None
