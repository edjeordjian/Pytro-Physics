"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from scipy.optimize import fsolve

from services.tools.number_service import get_parsed_adimentional, celcius_to_farenheit, farenheit_to_celcius


def get_so_sg(sw):
    return 1 - sw


def get_rw(rwc, tc, T, celcius_temp, celcius_scalar):
    if celcius_scalar != celcius_temp:
        if celcius_scalar:
            tc = celcius_to_farenheit(tc)

        else:
            tc = farenheit_to_celcius(tc)

    if celcius_temp:
        k = 21.5

    else:
        k = 6.77

    return rwc * (tc + k) / (T + k)


def get_sw_archie(a, n, m, phi,
                  rw, rt, limit_values):
    archie_data = ( (a * rw) / ( (phi ** m) * rt) ) ** (1/n)

    if limit_values:
        return get_parsed_adimentional(archie_data)

    return archie_data


def _get_sw_dual_water(sw, a, m, n,
                       r_wb_value, phi_t_value, phi_e_value, rw_value,
                       rt_value):
    #swt = min(0.999, max(0.001, sw[0]))
    swt = sw

    #Qv = ((a_qv / phi_t_value) + (b_qv))

    #Y = (Qv * phi_t_value * (1 / (1 - phi_t_value)))

    #mm = (m + c_m * (0.258 * Y + 0.2 * (1 - np.exp(-16.4 * Y))))

    mm = m

    Swb = (1 - (phi_e_value / phi_t_value))

    A = ((phi_t_value) ** (mm)) * (1 / ((a) * rw_value))

    B = (phi_t_value ** mm) * (Swb/a) * ((1/r_wb_value) - (1/rw_value))

    C = ((-1) / (rt_value))

    return A * ((swt) ** (n)) + B * ((swt) ** (n - 1)) + C


def get_sw_dual_water(a, m, n, seed,
                      r_wb, phi_e, phi_t, rw,
                      rt, limit_values):
    sw_t = []

    for i in range(len(phi_t)):
        sw_t.append(fsolve(_get_sw_dual_water,
                           seed,
                           args=(a, m, n, r_wb[i],
                                 phi_t[i], phi_e[i], rw[i], rt[i]))[0])

    sw_b = 1 - phi_e / phi_t

    sw_data = ((np.array(sw_t) - sw_b) / (1 - sw_b))

    if limit_values:
        return get_parsed_adimentional(sw_data)

    return sw_data


def _get_sw_modified_simandoux(sw, a, m, n,
                               r_sh, phi_value, v_sh_value, rw_value,
                               rt_value):
    #swt = min(0.999, max(0.001, sw[0]))
    swt = sw

    aux1 = (swt ** n) * ((phi_value ** m) / (a * rw_value))

    aux2 = swt * (v_sh_value / r_sh)

    aux3 = 1 / rt_value

    return aux1 + aux2 - aux3


def get_sw_modified_simandoux(a, m, n, r_sh,
                              seed, phi, v_sh, rw,
                              rt, limit_values):
    result = []

    for i in range(len(phi)):
        result.append(fsolve(_get_sw_modified_simandoux,
                             seed,
                             args=(a, m, n, r_sh,
                                   phi[i], v_sh[i], rw[i], rt[i]))[0])

    if limit_values:
        return get_parsed_adimentional(result)

    return result


def get_sw_simandoux(a, m, r_shale, phi,
                     rw, rt, vshale, limit_values):
    sw_simandoux = (a * rw) / ( 2 * (phi ** m) ) \
                             * ( ( ( ( (vshale / r_shale) ** 2 ) + ( 4 * (phi ** m) ) / (a * rw * rt) ) ** 0.5 )
                             - vshale / r_shale )

    if limit_values:
        return get_parsed_adimentional(sw_simandoux)

    return sw_simandoux


def get_sw_indonesia(a, m, r_shale, n,
                     phi, rw, rt, vshale,
                     limit_values):
    numerator = (1 / rt) ** 0.5

    denominator = ( vshale ** (1 - 0.5 * vshale) ) / (r_shale ** 0.5) + ( ( (phi ** m) / (a * rw) ) ** 0.5 )

    result = (numerator / denominator) ** (2 / n)

    if limit_values:
        return get_parsed_adimentional(result)

    return result


def get_sw_fertl(a, m, alpha, phi,
                 rw, rt, vshale, limit_values):
    sw_fertl = ( phi ** (-m / 2) ) \
        * ( ( ( (a * rw / rt) + ( (alpha * vshale * 0.5) ** 2 ) ) ** 0.5) - alpha * vshale * 0.5 )

    if limit_values:
        return get_parsed_adimentional(sw_fertl)

    return sw_fertl
