"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import pandas as pd

import numpy as np


def remove_jumps(list_to_change,
                 col_name,
                 jump):
    df = pd.DataFrame(list_to_change,
                      columns=[col_name])

    difference = 1

    starting_idx = 0

    initial_value = float('inf')

    while difference != 0:
        q0_list = df[col_name].to_list()

        difference = 0

        for i in range(starting_idx, len(q0_list) - 1):
            if q0_list[i] - q0_list[i + 1] > jump:

                initial_value = q0_list[i]

                starting_idx = i + 1

                difference = q0_list[i + 1] - q0_list[i]

                break

        if difference == 0:
            break

        df[df[col_name] >= initial_value] += difference

    return q0_list


def get_series_in_range(df_curve, depth_label, curve_name, min_depth,
                        max_depth, to_list):
    series = np.where(df_curve[depth_label].between(float(min_depth),
                                                    float(max_depth)),
                      df_curve[curve_name],
                      np.nan)

    if to_list:
        return series.tolist()

    return series


def set_nan_in_array_if_another_is_nan(array1, array2):
    df = pd.DataFrame(data={"0": array1, "1": array2})
    df["aux"] = ~(df[df.columns[0]].isna()|df[df.columns[1]].isna())
    df["aux"].replace(False, np.nan, inplace=True)
    df[df.columns[0]] = df[df.columns[0]] * df["aux"]
    df[df.columns[1]] = df[df.columns[1]] * df["aux"]
    df[df.columns[0]].replace("nan", np.nan, inplace=True)
    df[df.columns[1]].replace("nan", np.nan, inplace=True)
    return df[df.columns[0]].astype("float").to_numpy(), df[df.columns[1]].astype("float").to_numpy()
