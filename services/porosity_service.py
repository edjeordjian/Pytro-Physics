"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import pandas as pd

from numpy import sqrt

from constants.general_constants import DEFAULT_FORCED_MIN, DEFAULT_FORCED_MAX

from services.tools.number_service import get_parsed_adimentional


def get_porosity_with_density(density,
                              density_log,
                              rho_matrix,
                              forced_min=DEFAULT_FORCED_MIN,
                              forced_max=DEFAULT_FORCED_MAX):
    return get_parsed_adimentional((rho_matrix - density) / (rho_matrix - density_log),
                                   forced_min,
                                   forced_max)


def get_porosity_asquith_gibson(density,
                                porosity,
                                forced_min=DEFAULT_FORCED_MIN,
                                forced_max=DEFAULT_FORCED_MAX):
    df = pd.DataFrame()

    df['density'] = density

    df['porosity'] = porosity

    df.loc[df['density'] <= df['porosity'], 'result'] = 0.5 * (df['density'] + df['porosity'])

    df.loc[df['density'] > df['porosity'], 'result'] = sqrt(0.5 * (df['density'] * df['density'] +
                                                                   df['porosity'] * df['porosity']))

    return get_parsed_adimentional(df['result'].to_list(),
                                   forced_min,
                                   forced_max)


def get_porosity_by_wyllie(dt_log,
                           dt_flow,
                           bcp,
                           dt_matrix,
                           forced_min=DEFAULT_FORCED_MIN,
                           forced_max=DEFAULT_FORCED_MAX):
    return get_parsed_adimentional((dt_matrix - dt_log) / ((dt_matrix - dt_flow) * bcp),
                                   forced_min,
                                   forced_max)


def get_porosity_by_gardner_hunt_raymer(dt_log,
                                        dt_matrix,
                                        forced_min=DEFAULT_FORCED_MIN,
                                        forced_max=DEFAULT_FORCED_MAX):
    return get_parsed_adimentional(0.625 * (dt_log - dt_matrix) / dt_log,
                                   forced_min,
                                   forced_max)


def get_effective_porosity(density,
                           vshale,
                           forced_min=DEFAULT_FORCED_MIN,
                           forced_max=DEFAULT_FORCED_MAX):
    return get_parsed_adimentional(density * (1 - vshale),
                                   forced_min,
                                   forced_max)
