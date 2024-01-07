"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.DTCO_service import get_DTCO_variables

import numpy as np


def test_get_DTCO_variables():
    lithology_1 = {'color': 'Amarillo', 'density': '2.65', 'fill': 'Sólido', 'name': 'Arenisca', 'neutron': '-4',
                   'neutron_fraction': 'False', 'pef': '1.81', 'sonic': '53'}

    lithology_2 = {'color': 'Violeta', 'density': '2.87', 'fill': 'Sólido', 'name': 'Dolomita', 'neutron': '4',
                   'neutron_fraction': 'False', 'pef': '3.14', 'sonic': '43'}

    lithology_3 = {'color': 'Azul', 'density': '2.71', 'fill': 'Sólido', 'name': 'Caliza', 'neutron': '0',
                   'neutron_fraction': 'False', 'pef': '5.08', 'sonic': '47.5'}

    blank_lithology = {'name': '', 'color': 'Blanco', 'fill': 'Sólido', 'density': '0', 'sonic': '0', 'neutron': '0',
                       'neutron_fraction': 'False', 'pef': '0'}

    vshale_lithology = {
        "name": "Vshale",
        "color": "Verde",
        "fill": "Línea horizontal",
        "density": "2.6",
        "sonic": "64.5",
        "neutron": "1.6",
        "neutron_fraction": "False",
        "pef": "5.08"
    }

    data = {
        "rho_b": np.array([0.1]),

        "dt": np.array([0.1]),

        "pef": np.array([0.1]),

        "neutron": np.array([0.1]),

        "vshale": np.array([0.1]),

        "lithology1": lithology_1,

        "lithology2": lithology_2,

        "lithology3": lithology_3,

        "lithology4": blank_lithology,

        "lithology5": blank_lithology,

        "lithology6": blank_lithology,

        "lithology7": blank_lithology,

        "lithology8": blank_lithology,

        "carbon": None,

        "rhodsh": 2.78,

        "anhydrit": None,

        "carbon_idx": -1,

        "anhidrit_idx": -1
    }

    lithologies = [
        vshale_lithology,
        lithology_1, lithology_2, lithology_3, blank_lithology,
        blank_lithology, blank_lithology, blank_lithology, blank_lithology
    ]

    result_dict = get_DTCO_variables(data,
                                     lithologies)

    assert result_dict["vshale"][0] == 0.0814606741573034

    assert result_dict["phie"][0] == 0.18539

    assert result_dict["lean_lit1"][0] == 0.225
