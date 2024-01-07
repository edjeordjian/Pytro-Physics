"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants.permeability_constants import (XGBOOST_TRACK_NAME, RANDOM_FOREST_TRACK_NAME, ADA_TRACK_NAME,
    TIMUR_TRACK_NAME, COATES_TRACK_NAME, TIXIER_TRACK_NAME, COATES_AND_DUMANOIR_TRACK_NAME)

from constants.swirr_constants import SWIRR_DISPLAY_NAME

LOG_LBL = "log"

VIEW_EXTENSION = ".view"

las_extention = ".las"

csv_extention = ".csv"

txt_extention = ".txt"

new_column_suffix = "_dup"

number_of_decimals = 4

loading_pop_up_timeout_ms = 950

# Causes bug with dots line for some reason
initial_loading_pop_up = False

APPEND_CURVE_ACTION = 'append curve'

ADD_CURVE_ACTION = 'add curve'

AXIS_ACTION = 'add_axis'

FILL_ACTION = 'fill_between_curves'

LEGEND_ACTION = 'add_legend'

SCATTERPLOT_ACTION = 'add crossplot'

APPEND_RECTANGLE = 'append rectangle'

COLOR_CROSSPLOT_ACTION = 'color crossplot'

HISTOGRAM_ACTION = "histogram"

FONT_SIZE: int = 10

GROUP_RANGE_ERROR = "Los valores del intervalo de profundidad deben ser números positivos en rango"

PPM_LABEL = "PPM"

METERS_LBL = "m"

FEETS_LBL = "ft"

FARENHEIT_UNIT_LBL = "F"

CELCIUS_UNIT_LBL = "C"

DEFAULT_SCATTERPLOT_CONFIG = {
    'scatter_curve': True,

    'line_width': 4
}

# [Permeability], [Swirr]
TRACK_NAMES = [
    XGBOOST_TRACK_NAME, RANDOM_FOREST_TRACK_NAME, ADA_TRACK_NAME, TIMUR_TRACK_NAME,
    COATES_TRACK_NAME, TIXIER_TRACK_NAME, COATES_AND_DUMANOIR_TRACK_NAME, SWIRR_DISPLAY_NAME
]

RECTANGLE_NAME_PREFIX = "Rectangle_"

LAYOUT_LEFT_PADDING = 6

LAYOUT_TOP_PADDING = 6

LAYOUT_RIGHT_PADDING = 14

LAYOUT_BOTTOM_PADDING = 14

X_PADDING_IMAGES = 20

Y_PADDING_IMAGES = 0

X_EXPORT_DELTA = 6

X_EXPORT_DELTA_2 = 6

BLANK_LABEL_FONT_SIZE = '26pt'

NO_INTERNET_CONNECTION = 'Se requiere conexión a internet para usar el programa en su período de prueba.'

END_BETA_TEXT = 'Terminó el período de prueba del programa. <br> Para una versión actualizada, contactarse ' + \
                ' con Nicolás Fandos (nfandos@fi.uba.ar) o Esteban Djeordjian (edjeordjian@gmail.com).'

ABOUT_TEXT = 'Hecho por Nicolás Fandos (nfandos@fi.uba.ar) y Esteban Djeordjian (edjeordjian@gmail.com), gracias a <br>' + \
             ' Dr. Luis Stinco, Ing. Pablo Deymonnaz, Nicolás Argañaraz y Joaquín Piloni. <br><br>' + \
             'Versión 1.4 - Agosto de 2023. Bajo licencia GNU GPL 3.0 or later.' + \
             '<br>' + \
             '<br>' + \
             '<a href="https://docs.google.com/document/d/1-L4RuKuVRD_mC9W9YvTi1JJvO69khrDnG6o0xAerdlM"' + \
             '   >Manual de usuario</a>' \
             '' \
             '<br>' + \
             '<a href="https://drive.google.com/drive/u/0/folders/1QKQuP-9DJgcg2tbX92ewqIIxLyw_qMtS"' + \
             '   >Descarga del programa</a>'

GRAPHIC_WINDOW_NAME = "Curvas de profundidad"

GENERIC_WINDOW_NAME = "Pytrophysics - Visualización"

DEFAULT_FORCED_MIN = 0.001

DEFAULT_FORCED_MAX = 0.999

LOADING_LBL = "Cargando"

PLEASE_WAIT_LBL = "Por favor espere"

SAVED_CURVE_LBL = "Curva guardada"

TRACK_TITLE_LENGTH = 12

depth_change_multiplier = {
    FEETS_LBL: 1/0.304800609601,
    METERS_LBL: 0.304800609601,
}
