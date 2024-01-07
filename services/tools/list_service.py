"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from collections import OrderedDict

import itertools

import numpy as np


def last_element(a_list):
    count = len(a_list)

    if count == 0:
        return None

    return a_list[count - 1]


def first_element(a_list):
    return None if len(a_list) == 0 else a_list[0]


def get_uniques(a_list):
    return list(OrderedDict.fromkeys(a_list))


# https://stackoverflow.com/a/20037408/1048186
def flat_map(func, *iterable):
    return itertools.chain.from_iterable(map(func, *iterable))


def get_sublist_and_complement(a_list,
                               condition):
    return list(filter(lambda element: condition(element),
                       a_list)), \
           list(filter(lambda element: not condition(element),
                       a_list))


def get_uniques_and_duplicated(a_list):
    uniques = get_uniques(a_list)

    duplicated = remove_list_from_list(a_list,
                                       uniques)

    return uniques, duplicated


def list_to_str(a_list):
    return ''.join(a_list)


def replace_in_list(a_list,
                    old,
                    new):
    if old is None or new is None:
        return

    i = a_list.index(old)

    a_list.insert(i,
                  new)

    a_list.pop(i + 1)


def _naive_compare(a,
                   b):
    return a == b


def remove_list_from_list(list_a,
                          list_b,
                          comparison_fn=_naive_compare):
    new_list = []

    for a in list_a:
        if len(
                list(
                    filter(lambda b: comparison_fn(a,
                                                   b),
                           list_b)
                )
        ) == 0:
            new_list.append(a)

    return new_list


def get_list_without_nones(a_list):
    return list(
        filter(lambda x: x is not None,
               a_list)
    )


def remove_near_values(a_list, value, delta):
    without_neighbors = []

    for i in range(len(a_list)):
        if abs(a_list[i] - value) > delta * value:
            without_neighbors.append(a_list[i + 1])

    return without_neighbors


def list_to_numpy(a_list):
    return np.array(list(map(lambda x: np.nan if x is None else x, a_list)))
