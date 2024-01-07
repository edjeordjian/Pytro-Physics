"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""


def get_qle_group_name(constant):
    return f"{constant} QLE"


def get_depth_lbl(unit):
    return f"Profundidad [{unit}]"


def only_ascci_for(name):
    return f"Unidad no válida para {name}. Solo se permite caracteres ASCII."
