"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import json

import numpy as np

import pandas as pd


# https://bobbyhadz.com/blog/python-typeerror-object-of-type-ndarray-is-not-json-serializable
class ExtendedJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Series) or isinstance(obj, np.ndarray):
            return obj.tolist()

        if isinstance(obj, np.int32):
            return int(obj)

        return json.JSONEncoder.default(self, obj)
