"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import traceback

from PyQt6.QtGui import QIcon, QAction

from PyQt6.QtWidgets import (QFileDialog, QComboBox, QRadioButton, QLineEdit,
                             QCheckBox, QSlider)

from constants.general_constants import VIEW_EXTENSION

from constants.messages_constants import DATA_SAVED, COULD_NOT_READ_FILE, INVALID_VIEW

from constants.tab_constants import EVERY_TAB

from constants.views_constants import (COMBO_TYPE_LBL, RADIO_TYPE_LBL, TEXTBOX_TYPE_LBL, LIST_TYPE_LBL,
                                       MULTI_COMBO_TYPE_LBL, SLIDER_TYPE_LBL)

from services.tools.file_service import clean_file, create_file, file_is_empty

from services.tools.json_service import save_json, read_json, write_json_dumps

from services.tools.logger_service import log_error

from ui.popUps.InfoWindow import InfoWindow

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.loading_handler import loading_pop_up

from ui.visual_components.MultiComboBox import MultiComboBox

view_browser_options = {
    'header': 'Guardar vista',
    'default_name': 'pantalla.view',
    'extension': 'View file (.view);'
}


def add_option_to_menu(instance, menu, icon_route, file_extention, action_function):
    export_action = QAction(QIcon(icon_route),
                            file_extention,
                            instance)

    export_action.triggered \
        .connect(action_function)

    menu.addAction(export_action)


def save_state(windows, full_route):
    clean_file(full_route)

    create_file(full_route)

    state_file = open(full_route, "a")

    state_file.write("[ \n")

    for i in range(len(windows)):
        write_json_dumps(state_file, get_view_content_to_save(windows[i]))

        if i != len(windows) - 1:
            state_file.write(",\n")

    state_file.write("] \n")

    state_file.close()

    InfoWindow(DATA_SAVED)


def load_state(windows, full_route):
    if file_is_empty(full_route):
        return

    content = read_json(full_route)

    i = 0

    for component in content:
        if len(component["content"]) != 0:
            _set_view_state(windows[i], component["content"], component["tabs"])

        i += 1


def save_view(instance):
    full_route, _ = QFileDialog.getSaveFileName(instance,
                                                view_browser_options['header'],
                                                view_browser_options['default_name'],
                                                view_browser_options['extension'])

    if len(full_route) == 0:
        return

    file_name = full_route.split("/")[-1]

    if VIEW_EXTENSION not in file_name:
        full_route += VIEW_EXTENSION

    content = get_view_content_to_save(instance)

    save_json(full_route, content)

    InfoWindow(DATA_SAVED)


def get_view_content_to_save(instance):
    return {
        "id": instance.get_view_id(),

        "content": instance.get_serialized_curve_tracks(),

        "tabs": instance.get_tab_serialization()
    }


def load_view(instance, file_uri=None, tab_update_fn=None):
    if file_uri is None:
        file_uri = QFileDialog.getOpenFileName(instance, 'Abrir vista', "", "Archivo view (*.view)")[0]

    if len(file_uri) == 0:
        return AlertWindow("Se debe especificar un archivo")

    file_name = file_uri.split("/")[-1]

    if VIEW_EXTENSION not in file_name:
        return AlertWindow(f"Formato inválido: debe ser '{VIEW_EXTENSION}'")

    loading_pop_up('Cargando vista',
                   lambda: (set_view_state(instance, file_uri),
                            tab_update_fn() if tab_update_fn is not None else ()))


def _set_view_state(instance, view_state, tab_state):
    instance.set_view(view_state)

    instance.set_tabs(tab_state)

    instance.draw_tracks(EVERY_TAB)


def set_view_state(instance, file_uri):
    try:
        serialized_state = read_json(file_uri)

        if serialized_state["id"] != instance.get_view_id():
            return AlertWindow(INVALID_VIEW)

    except Exception:
        log_error(traceback.format_exc())

        return AlertWindow(COULD_NOT_READ_FILE)

    _set_view_state(instance, serialized_state["content"], serialized_state["tabs"])


def serialize_qt_attribute(attribute, name=None):
    data = None

    if isinstance(attribute, MultiComboBox):
        data = {
            "value": attribute.currentIndexes(),
            "type": MULTI_COMBO_TYPE_LBL
        }

    elif isinstance(attribute, QComboBox):
        data = {
            "value": attribute.currentIndex(),
            "type": COMBO_TYPE_LBL
        }

    elif isinstance(attribute, QRadioButton) or isinstance(attribute, QCheckBox):
        data = {
            "value": attribute.isChecked(),
            "type": RADIO_TYPE_LBL
        }

    elif isinstance(attribute, QLineEdit):
        data = {
            "value": attribute.text(),
            "type": TEXTBOX_TYPE_LBL
        }

    elif isinstance(attribute, QSlider):
        data = {
            "value": attribute.value(),
            "type": SLIDER_TYPE_LBL
        }

    elif isinstance(attribute, type([])):
        values = []

        for entry in attribute:
            case = []

            for key in entry.keys():
                serialized = serialize_qt_attribute(entry[key], key)

                if serialized is not None:
                    case.append(serialized)

            values.append(case)

        data = {
            "value": values,
            "type": LIST_TYPE_LBL
        }

    if data is not None:
        data.update({
            "name": name
        })

    return data


def deserialize_qt_attributes(instance, entry_list, is_dictionary=False):
    for entry in entry_list:
        if is_dictionary:
            attribute = instance[entry["name"]]

        else:
            attribute = getattr(instance, entry["name"])

            instance.set_ever_updated()

        value = entry["value"]

        # Refactor: this could be a dictionary mapping
        if entry["type"] == MULTI_COMBO_TYPE_LBL:
            attribute.setIndexes(value)

        elif entry["type"] == COMBO_TYPE_LBL:
            if value <= attribute.count() - 1:
                attribute.setCurrentIndex(value)

        elif entry["type"] == RADIO_TYPE_LBL:
            attribute.setChecked(value)

        elif entry["type"] == TEXTBOX_TYPE_LBL:
            attribute.setText(value)

        elif entry["type"] == SLIDER_TYPE_LBL:
            attribute.setValue(value)

        elif entry["type"] == LIST_TYPE_LBL:
            for i in range(len(value)):
                deserialize_qt_attributes(attribute[i], value[i], True)

        else:
            log_error(f"Element not found: {entry['type']}")
