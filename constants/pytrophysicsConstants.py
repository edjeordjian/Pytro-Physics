"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

TOP_MENU_CONSTANTS = {
    "CURVE_LABEL": "Curvas: ",
    "CURVE_CBO_PLACEHOLDER": "Modificar curva",
    "TRACK_LABEL": "Pista: ",
    "TRACK_CBO_PLACEHOLDER": "Pista",
    "LINE_COLOR_LABEL": "Color: ",
    "LOG_AXIS_LABEL": "Log",
    "LINE_TYPE_LABEL": "Línea: ",
    "LINE_MARKER_LABEL": "Estilo: ",
    "CURVE_NAME_LABEL": "Nombre de la curva: ",
    "SCATTERPLOT_LABEL": "Core: ",
    "ADD_CURVE_BUTTON": "Agregar curva",
    "CHANGE_CURVE_BUTTON": "Modificar curva",
    "FILL_CURVES_LABEL": "Area entre curvas",
    "USER_CURVE_CBO_PLACEHOLDER": "Elige curva",
    "DELETE_CURVE_BUTTON": "Borrar curva",
    "FILL_BETWEEN_LINES_BUTTON": "Llenar area entre curvas",
    "NEW_TRACK_LABEL": "Nueva pista",
    "DELETE_TRACK_BUTTON": "Borrar pista",
    "DELETE_FILL_TEXT": "Borrar rellenado",
    "CHOOSE_PLACEHOLDER": "Elegir...",
    "ADD_NEW_CURVE": "Agregar curva",
    "KEEP_SCALE": "Mantener escala",
    "REVERSE_X_LABEL": "      Invertir eje X"
}

VSHALE_MENU_CONSTANTS = {
    "METHOD_LABEL": "Metodo: ",
    "METHOD_CBO_PLACEHOLDER": "Elige metodo",
    "CURVE_LABEL": "Curvas: ",
    "CURVE_CBO_PLACEHOLDER": "Elige curva",
    "DEPTH_LABEL": "Profunidad:",
    "DEPTH_FULL_LAS": "Todo el LAS: ",
    "DEPTH_personalizado": "Personalizado: ",
    "GROUPS_LABEL": "Grupos: ",
    "GROUP_1_LABEL": "Grupo 1",
    "GROUP_2_LABEL": "Grupo 2",
    "MIN_DEPTH_LABEL": "zi:",
    "MAX_DEPTH_LABEL": "zf:",
    "MIN_GR_LABEL": "GRmin: ",
    "MAX_GR_LABEL": "GRmax: ",
    "CORRELATION_LABEL": "Correlacion: ",
    "CORRELATION_CBO_PLACEHOLDER": "Elegir correlacion",
    "PREVIEW_BUTTON": "Preview",
    "CURVE_NAME_LABEL": "Nombre",
    "SAVE_CURVE_BUTTON": "Guardar curva",
}

COLOR_CONSTANTS = {
    "BLACK": "Negro",
    "RED": "Rojo",
    "YELLOW": "Amarillo",
    "BLUE": "Azul",
    "GREEN": "Verde",
    "VIOLET": "Violeta",
    "ORANGE": "Naranja",
    "MAGENTA": "Magenta",
    "BROWN": "Marron",
    "PINK": "Rosa",
    "LIGHT_BLUE": "Celeste",
    "TEAL": "Verde azulado",
    "OLIVE": "Oliva",
    "CORAL": "Coral",
    "GREY": "Gris",
    "RUST": "Oxido",
    "WHITE": "Blanco"
}

ENGLISH_COLOR = {v: k.lower() for k, v in COLOR_CONSTANTS.items()}

LINE_TYPE_CONSTANTS ={
    "SOLID_LINE": "Solida",
    "DASH_LINE": "Guion",
    "DOT_LINE": "Punto",
    "DASH_DOT_LINE": "Guion y punto",
    "DASH_DOT_DOT_LINE": "Guion y doble punto",
}

LINE_MARKER_CONSTANTS = {
    "NONE": "Sin marcador",
    "DOT": "Punto",
    "DOWN_TRIANGLE": "Triangulo Abajo",
    "UP_TRIANGLE": "Triangulo Arriba",
    "LEFT_TRIANGLE": "Triangulo Izquierda",
    "RIGHT_TRIANGLE": "Triangulo Derecha",
    "SQUARE": "Cuadrado",
    "PENTAGON": "Pentagono",
    "HEXAGON": "Hexagono",
    "STAR": "Estrella",
    "CROSS": "Cruz",
    "DIAMOND": "Rombo",
    "DOWN_ARROW": "Flecha abajo",
    "UP_ARROW": "Flecha arriba",
    "LEFT_ARROW": "Flecha izquierda",
    "RIGHT_ARROW": "Flecha derecha",
}

COLORMAP_CONSTANTS = {
    "CIVIDIS": "Escala Azul-Amarillo",
    "INFERNO": "Escala Violeta-Amarillo",
    "CET-L1": "Escala Gris-Blanco",
    "CET-L4": "Escala Rojo-Amarillo",
    "CET-CBTL1": "Escala Marron-Rojo-Celeste",
    "CET-L5": "Escala Verde-Amarillo",
    "CET-D2": "Escala Verde-Violeta",
    "CET-L6": "Escala Azul-Blanco",
    "CET-L7": "Escala Azul-Violeta-Blanco",
    "CET-L9": "Escala Azul-Verde-Blanco",
    "CET-R4": "Escala Azul-Amarillo-Rojo",
    "CET-C6": "Escala Multicolor"
}

DEFAULT_LITHOLOGIES = [
    {
        "name": "Arenisca",
        "color": "Amarillo",
        "fill": "Puntos",
        "density": "2.65",
        "sonic": "55",
        "neutron": "-4",
        "neutron_fraction": "False",
        "pef": "1.81"
    },
    {
        "name": "Caliza",
        "color": "Azul",
        "fill": "Diagonal derecha",
        "density": "2.71",
        "sonic": "47.5",
        "neutron": "0",
        "neutron_fraction": "False",
        "pef": "5.08"
    },
    {
        "name": "Vshale",
        "color": "Verde",
        "fill": "Línea horizontal",
        "density": "2.6",
        "sonic": "64.5",
        "neutron": "1.6",
        "neutron_fraction": "False",
        "pef": "5.08"
    },
    {
        "name": "Dolomita",
        "color": "Violeta",
        "fill": "Diagonal izquierda",
        "density": "2.87",
        "sonic": "43",
        "neutron": "4",
        "neutron_fraction": "False",
        "pef": "3.14"
    },
    {
        "name": "Anhidrita",
        "color": "Rosa",
        "fill": "Enrejado fino",
        "density": "2.98",
        "sonic": "50",
        "neutron": "1",
        "neutron_fraction": "False",
        "pef": "5.06"
    },
    {
        "name": "Sal",
        "color": "Rojo",
        "fill": "Cuadriculado",
        "density": "2.03",
        "sonic": "67",
        "neutron": "-3",
        "neutron_fraction": "False",
        "pef": "4.65"
    },
    {
        "name": "Carbon",
        "color": "Negro",
        "fill": "Sólido",
        "density": "1.27",
        "sonic": "120",
        "neutron": "50",
        "neutron_fraction": "False",
        "pef": "0.17"
    },
    {
        "name": "Yeso",
        "color": "Violeta",
        "fill": "Enrejado",
        "density": "2.37",
        "sonic": "54",
        "neutron": "60",
        "neutron_fraction": "False",
        "pef": "3.42"
    }
 ]

DEFAULT_LITHOLOGY_CONFIG = {
    "name": "",
    "color": "Blanco",
    "fill": "Sólido",
    "density": "0",
    "sonic": "0",
    "neutron": "0",
    "neutron_fraction": "False",
    "pef": "0"
}

LITHOLOGY_FILE_NAME = "litologias.json"

IPR_FILE_NAME = "ipr"

STATE_FILE_NAME = "estado"

SEE_ALL_LBL = "Ver curvas de profundidad"

DELETE_ALL_LBL = "Quitar curvas de profundidad"

SEE_WINDOW_LBL = "Ver ventana"

CUTOFF_LBL = "Cutoff:"

READ_MODE_WELL_NAME = "modo_lectura"

READ_MODE_BASE_PATH = f"./{READ_MODE_WELL_NAME}"

READ_MODE_WELL_PARTIAL_URL = f"/{READ_MODE_WELL_NAME}/{READ_MODE_WELL_NAME}.las"

APP_NAME = "Pytrophysics"
