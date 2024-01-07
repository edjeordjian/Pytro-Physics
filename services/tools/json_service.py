"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import json

from services.tools.ExtendedJsonEncoder import ExtendedJsonEncoder


def remove_from_dictionary(a_dictionary,
                           to_remove):
    for key in to_remove:
        if a_dictionary.get(key, None) is not None:
            a_dictionary.pop(key)


def get_list_of_values(a_dict):
    return list(a_dict.values())


def get_list_of_items(a_dict,
                      keys):
    items = []

    for key in keys:
        if a_dict.get(key,
                      None) is not None:
            items.append((key,
                          a_dict[key]))

    return items


def are_similarl_json_lists(list_a,
                            list_b):
    if list_a is None and list_b is None:
        return True

    if (list_a is None) or (list_b is None) or len(list_a) != len(list_b):
        return False

    for i in range(len(list_a)):
        if not are_similar_jsons(list_a[i],
                                 list_b[i]):
            return False

    return True


def are_similar_jsons(json_a,
                      json_b):
    keys_a = json_a.keys()

    keys_b = json_b.keys()

    if len(keys_a) != len(keys_b):
        return False

    for key in keys_a:
        try:
            json_b[key]

        except KeyError:
            return False

    return True


def write_json_dumps(file, content):
    # indent=4 makes files much bigger if there are curves
    file.write(json.dumps(content, cls=ExtendedJsonEncoder))


def save_json(url,
              content,
              write_mode="w"):
    json_file = open(url, write_mode)

    write_json_dumps(json_file, content)

    json_file.close()


def read_json(url):
    json_file = open(url, "r")

    json_content = json.loads(json_file.read())

    json_file.close()

    return json_content


def get_key_index(a_dict, key):
    if len(key) == 0:
        return 0

    return list(a_dict.keys()).index(key)
