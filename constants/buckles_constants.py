"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

BUCKLES_BASE_X = [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.05, 0.04]

BUCKLES_PREFIX_LBL = "BUCKL = "

BUCKLES_DICT = {
    'buckles': [
        {'x': BUCKLES_BASE_X,
         'y': [0.08, 0.09, 0.10, 0.11, 0.13, 0.16, 0.20, 0.27, 0.40, 0.80, 1.00],
         'name': 'BUCKL = 0.04'},

        {'x': [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.06],
         'y': [0.12, 0.13, 0.15, 0.17, 0.20, 0.24, 0.30, 0.40, 0.60, 1.00],
         'name': 'BUCKL = 0.06'},

        {'x': [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10, 0.08],
         'y': [0.16, 0.18, 0.20, 0.23, 0.27, 0.32, 0.40, 0.53, 0.80, 1.00],
         'name': 'BUCKL = 0.08'},

        {'x': [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.10],
         'y': [0.20, 0.22, 0.25, 0.29, 0.33, 0.40, 0.50, 0.67, 1.00],
         'name': 'BUCKL = 0.1'},

        {'x': [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.12],
         'y': [0.24, 0.27, 0.30, 0.34, 0.40, 0.48, 0.60, 0.80, 1.00],
         'name': 'BUCKL = 0.12'},

        {'x': [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.15, 0.14],
         'y': [0.28, 0.31, 0.35, 0.40, 0.47, 0.56, 0.70, 0.93, 1.00],
         'name': 'BUCKL = 0.14'},

        {'x': [0.50, 0.45, 0.40, 0.35, 0.30, 0.25, 0.20, 0.16],
         'y': [0.32, 0.36, 0.40, 0.46, 0.53, 0.64, 0.80, 1.00],
         'name': 'BUCKL = 0.16'}
    ]
}

CUSTOM_BUCKLES_LBL = "Hipérbola personalizada"

VALUE_LBL = "Valor:"
