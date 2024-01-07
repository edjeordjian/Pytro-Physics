"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from services.tools.number_service import get_parsed_adimentional


def get_sp_vshale(sp, forced_clean_value, forced_shale_value):
    parsed_sp = sp.ravel()

    parsed_without_nans = parsed_sp[~np.isnan(parsed_sp)]

    if len(parsed_without_nans) == 0:
        return parsed_sp

    sp_clean = np.min(parsed_without_nans)

    sp_shale = np.max(parsed_without_nans)

    if forced_clean_value is not None:
        sp_clean = float(forced_clean_value)

    if forced_shale_value is not None:
        sp_shale = float(forced_shale_value)

    if sp_clean == sp_shale:
        return [1] * len(sp)

    vclay = ((sp_clean - sp) / (sp_clean - sp_shale))

    return get_parsed_adimentional(vclay)


def get_gr_vshale(gr, forced_clean_value, forced_shale_value):
    parsed_gr = gr.ravel()

    parsed_without_nans = parsed_gr[~np.isnan(parsed_gr)]

    if len(parsed_without_nans) == 0:
        return parsed_gr

    gr_clean = np.min(parsed_without_nans)

    gr_shale = np.max(parsed_without_nans)

    if forced_clean_value is not None:
        gr_clean = float(forced_clean_value)

    if forced_shale_value is not None:
        gr_shale = float(forced_shale_value)

    if gr_clean == gr_shale:
        return [1] * len(gr)

    vclay = ((gr - gr_clean) / (gr_shale - gr_clean))

    return get_parsed_adimentional(vclay)


def get_resistivity_vshale(rt, forced_clean_value, forced_shale_value):
    parsed_rt = rt.ravel()

    parsed_without_nans = parsed_rt[~np.isnan(parsed_rt)]

    if len(parsed_without_nans) == 0:
        return parsed_rt

    rt_clean = np.min(parsed_without_nans)

    rt_shale = np.max(parsed_without_nans)

    if forced_clean_value is not None:
        rt_clean = float(forced_clean_value)

    if forced_shale_value is not None:
        rt_shale = float(forced_shale_value)

    if rt_shale == rt_clean:
        return [1] * len(rt)

    vclay = ((np.log(rt) - np.log(rt_clean)) / (np.log(rt_shale) - np.log(rt_clean)))

    return get_parsed_adimentional(vclay)


def get_neutron_density_vshale(phi_n, phi_d, forced_phi_n_shale_value, forced_phi_d_shale_value):
    parsed_phi_n = phi_n.ravel()
    parsed_phi_d = phi_d.ravel()

    if len(parsed_phi_n[~np.isnan(parsed_phi_n)]) == 0:
        return parsed_phi_n

    if len(parsed_phi_d[~np.isnan(parsed_phi_d)]) == 0:
        return parsed_phi_d

    phi_n_shale = np.max(parsed_phi_n[~np.isnan(parsed_phi_n)])

    phi_d_shale = np.max(parsed_phi_d[~np.isnan(parsed_phi_d)])

    if forced_phi_n_shale_value is not None:
        phi_n_shale = float(forced_phi_n_shale_value)
    
    if forced_phi_d_shale_value is not None:
        phi_d_shale = float(forced_phi_d_shale_value)

    if phi_n_shale == phi_d_shale:
        return [1] * len(phi_n)

    vclay = ((phi_n - phi_d) / (phi_n_shale - phi_d_shale))

    return get_parsed_adimentional(vclay)


def get_linear_correlation(ish):
    parsed_ish = ish.ravel()
    return get_parsed_adimentional(parsed_ish)


def get_larionov_1_correlation(ish):
    parsed_ish = ish.ravel()

    two_array = np.zeros(len(parsed_ish)) + 2

    vclay = 0.083 * (np.power(two_array, 3.7 * parsed_ish) - 1)

    return get_parsed_adimentional(vclay)


def get_larionov_2_correlation(ish):
    parsed_ish = ish.ravel()

    two_array = np.zeros(len(parsed_ish)) + 2

    vclay = 0.33 * (np.power(two_array, 2 * parsed_ish) - 1)

    return get_parsed_adimentional(vclay)


def get_steiber_correlation(ish):
    parsed_ish = ish.ravel()

    vclay = (parsed_ish/(3 - (2 * parsed_ish)))

    return get_parsed_adimentional(vclay)


def get_clavier_hoyle_meunier_correlation(ish):
    parsed_ish = ish.ravel()

    # two_array = np.zeros(len(parsed_ish)) + 2
    partial_vclay = (parsed_ish + 0.7) ** 2
    vclay = 1.7 - ((3.38 - partial_vclay) ** 0.5)

    return get_parsed_adimentional(vclay)
