"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import re


def check_number(value,
                 fn):
    try:
        fn(value)
        return True
    except ValueError:
        return False


def is_number(value):
    return check_number(value,
                        float)


def are_numbers(values,
                number_check_fn=is_number):
    return len(
        list(
            filter(lambda value: not number_check_fn(value), values)
        )
    ) == 0


def is_integer(value):
    return check_number(value,
                        int)


def is_number_between(value,
                      min_value,
                      max_value,
                      value_fn=float,
                      closed_range=False):
    if closed_range:
        return is_number(value) and (min_value <= value_fn(value) <= max_value)

    return is_number(value) and (min_value < value_fn(value) < max_value)


def is_positive_number(value):
    return is_number_between(value, 0, float('inf'), float,  False)


def is_positive_integer(value):
    return is_number_between(value, 0, float('inf'), int, False)


def is_no_negative_number(value):
    return is_number_between(value, 0, float('inf'), float, True)


def is_no_negative_integer(value):
    return is_number_between(value, 0, float('inf'), int, True)


def is_ascii(s):
    try:
        s.encode('ascii')

        return True

    except UnicodeEncodeError:
        return False


def remove_characters(a_string, characters):
    new_string = a_string

    for character in characters:
        new_string = new_string.replace(character, "")

    return new_string


def re_round_value(value, number_of_decimals):
    if number_of_decimals != 0 and len(str(value).split(".")) > 1:
        decimal = str(value).split(".")[1]

        zeroes = "0" * (number_of_decimals - 1)

        regex_zeroes = f"(^{zeroes}[1-9]*$)"

        cases_zeroes = [(mObj.start(1), mObj.end(1) - 1) for mObj in re.finditer(regex_zeroes, decimal)]

        nines = "9" * (number_of_decimals - 1)

        regex_nines = f"(^{nines}[1-9]*$)"

        cases_nines = [(mObj.start(1), mObj.end(1) - 1) for mObj in re.finditer(regex_nines, decimal)]

        if len(cases_zeroes) != 0 or len(cases_nines) != 0:
            return re_round_value(round(value, number_of_decimals - 1), number_of_decimals - 1)

    return value
