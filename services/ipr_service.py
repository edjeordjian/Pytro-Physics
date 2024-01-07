"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from scipy.optimize import fsolve

from functools import reduce


def get_h_from_curve(h, min_depth, max_depth):
    h = h[~np.isnan(h)]
    return (float(max_depth) - float(min_depth)) * np.sum(h) / len(h)


def get_k_from_curve(k):
    # Remove 0s, since we will calculate the log of each value of the array
    k[k == 0] = np.nan

    k = k[~np.isnan(k)]

    # Assuming k follows a log normal distribution, we need this two parameters to get the mean
    mu = np.sum(list(map(lambda x: np.log(x), k))) / len(k)
    sigma_squared = np.sum(list(map(lambda x: (np.log(x) - mu) ** 2, k))) / len(k)

    # Return the mean of a log normal distribution
    log_normal_mean = np.exp(mu + (sigma_squared/2))
    return log_normal_mean


def get_darcy(mu_0, b_0, re, rw, s, pr, k, h, q0_max, precision):

    j = (0.00708 * k * h) / (mu_0 * b_0 * (np.log(re/rw) - 0.75 + s))

    pwf_min = 0 if q0_max is None else (pr - (q0_max/j))

    pwf = np.linspace(pwf_min, pr, num = precision, endpoint=False)

    q0 = j * (pr - pwf)

    config = {
        "x_axis": list(q0),
        "y_axis": list(pwf)
    }

    return config


def _pwf_min_voguel(pwf, pr):
    return (0.8 * ((pwf / pr) ** 2)) + (0.2 * (pwf / pr))


def get_voguel(pr, q0_max, precision):

    # Para hallar pwf_min usar fsolve de scipy
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html

    pwf_min = fsolve(_pwf_min_voguel, 0, args=(pr))

    pwf_min = reduce(lambda x, y: x if x >= 0 else y, pwf_min)
    if pwf_min < 0:
        return None

    pwf = np.linspace(pwf_min, pr, num = precision, endpoint=False)

    q0 = (1 - 0.2 * (pwf / pr) - 0.8 * ((pwf / pr) ** 2)) * q0_max

    config = {
        "x_axis": list(q0),
        "y_axis": list(pwf)
    }

    return config


def _pwf_min_brown(pwf, j, pr, pb, q0_max):
    return j * ((pr - pb) + (pb/1.8) * (1 - 0.2 * (pwf / pr) - 0.8 * ((pwf / pr) ** 2))) - q0_max


def get_brown(mu_0, b_0, re, rw, s, pr, pb, k, h, q0_max, precision):
    j = (0.00708 * k * h) / (mu_0 * b_0 * (np.log(re/rw) - 0.75 + s))

    if q0_max is None:
        pwf_min = [0]
        q0_max = _pwf_min_brown(0, j, pr, pb, 0)
    else:
        pwf_min = fsolve(_pwf_min_brown, 0, args=(j, pr, pb, q0_max))

    pwf_min = reduce(lambda x, y: x if x >= 0 else y, pwf_min)
    if pwf_min < 0:
        return None

    pwf = np.linspace(pwf_min, pr, num = precision, endpoint=False)

    q0 = map(lambda pwf: (j * (pr - pwf)) if (pb <= pwf) else (j * ((pr - pb) + (pb/1.8) * (1 - 0.2 * (pwf / pb) - 0.8 * ((pwf / pb) ** 2)))), pwf)

    #q0_list = remove_jumps(list(q0),
    #                       'q0',
    #                       0.01)

    config = {
        "x_axis": list(q0),
        "y_axis": list(pwf)
    }

    return config


def _pwf_min_klins_clark(pwf, pr, d):
    return (0.705 * ((pwf / pr) ** d)) + (0.295 * (pwf / pr))


def get_klins_clark(pr, pb, q0_max, precision):

    d = (0.28 + 0.72 * (pr/pb)) * (1.24 + 0.001 * pb)

    pwf_min = fsolve(_pwf_min_klins_clark, 0, args=(pr, d))

    pwf_min = reduce(lambda x, y: x if x >= 0 else y, pwf_min)
    if pwf_min < 0:
        return None

    pwf = np.linspace(pwf_min, pr, num = precision, endpoint=False)

    q0 = (1 - 0.295 * (pwf / pr) - 0.705 * ((pwf / pr) ** d)) * q0_max

    #print(q0)
    #print(pwf)

    config = {
        "x_axis": list(q0),
        "y_axis": list(pwf)
    }

    return config


def _pwf_min_fetkovich_1(pwf, c, pr, n, q0_max):
    return (c * (((pr ** 2) - (pwf ** 2)) ** n)) - q0_max


def _get_fetkovich_1(c, pr, n, q0_max, precision):
    if q0_max is None:
        pwf_min = [0]

    else:
        pwf_min = fsolve(_pwf_min_fetkovich_1, 0, args=(c, pr, n, q0_max))

    pwf_min = reduce(lambda x, y: x if x >= 0 else y, pwf_min)
    if pwf_min < 0:
        return None

    pwf = np.linspace(pwf_min, pr, num = precision, endpoint=False)

    q0 = map(lambda pwf: (c * (((pr ** 2) - (pwf ** 2)) ** n)), pwf)

    #jump_coef = 1/len(pwf)
    #jump_coef = 0.01

    #q0_list = remove_jumps(list(q0),
    #                       'q0',
    #                       jump_coef)

    config = {
        "x_axis": list(q0),
        "y_axis": list(pwf)
    }

    return config


def _pwf_min_fetkovich_2(pwf, j, c, pr, pb, q0_max):
    return (j * (pr - pb)) + (c * ((pb ** 2) - (pwf ** 2))) - q0_max


def _get_fetkovich_2(j, c, pr, pb, q0_max, precision):
    if q0_max is None:
        pwf_min = [0]

    else:
        pwf_min = fsolve(_pwf_min_fetkovich_2, 0, args=(j, c, pr, pb, q0_max))

    pwf_min = reduce(lambda x, y: x if x >= 0 else y, pwf_min)
    if pwf_min < 0:
        return None

    pwf = np.linspace(pwf_min, pr, num = precision, endpoint=False)

    q0 = map(lambda pwf: (j * (pr - pwf)) if (pb <= pwf) else ((j * (pr - pb)) + (c * ((pb ** 2) - (pwf ** 2)))), pwf)

    #q0_list = remove_jumps(list(q0),
    #                       'q0',
    #                       0.01)

    config = {
        "x_axis": list(q0),
        "y_axis": list(pwf)
    }

    return config


def get_fetkovich(mu_0, b_0, re, rw, s, pr, pb, n, k, h, q0_max, precision):
    j = (0.00708 * k * h) / (mu_0 * b_0 * (np.log(re/rw) - 0.75 + s))
    c = j / (2*pb)

    if pr < pb:
        return _get_fetkovich_1(c, pr, n, q0_max, precision)

    else:
        return _get_fetkovich_2(j, c, pr, pb, q0_max, precision)

