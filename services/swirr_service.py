"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from services.tools.number_service import get_parsed_adimentional


def get_swirr_timur(porosity,
                    permeability,
                    constant):
    swirr = np.sqrt(constant * pow(porosity * 100, 4.4) / permeability) / 100

    return get_parsed_adimentional(swirr)


def get_swirr_buckles(sw, kbuck, phie, vshale):
    swirr = np.minimum(sw, kbuck / phie / (1 - vshale))

    return get_parsed_adimentional(swirr)
