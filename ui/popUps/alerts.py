"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants.messages_constants import MISSING_CURVES_OR_VALUES, MISSING_CONSTANTS, INVALID_NUMERIC_INPUT

from ui.popUps.alertWindow import AlertWindow


def get_positive_value_error_alert(value):
    if value is None or len(value) == 0:
        return AlertWindow("Falta ingresar un valor. Ingresar un número positivo.")

    return AlertWindow(f"El valor de {value} es inválido. Ingresar un número positivo.")


def get_curve_error_alert(value):
    return AlertWindow(f"La curva de {value} es inválida.")


def missing_constants_or_curves_alert(value):
    return AlertWindow(f"{MISSING_CURVES_OR_VALUES} {value}")


def missing_constants_alert():
    return AlertWindow(f"{MISSING_CONSTANTS}")


def get_alert_from_label(text):
    return AlertWindow(f"{text}: {INVALID_NUMERIC_INPUT}")
