"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PIL import Image

# Avoids
# PIL.Image.DecompressionBombError: Image size (248224536 pixels) exceeds limit of 178956970 pixels, could be decompression bomb DOS attack.
Image.MAX_IMAGE_PIXELS = None


def pt_to_px(length_pt, dpi):
    return (length_pt*dpi) / 72


def px_to_ft(length, dpi):
    return length / dpi / 12


def px_to_m(length, dpi):
    return length * 2.54 / dpi * 0.01


def get_scale_format(value):
    value_str = "{:.20f}".format(value).replace("0.", "")

    digits = 0

    last_digit_idx = 0

    in_beginning = True

    for i in range(len(value_str)):
        if value_str[i] == '0' and in_beginning:
            continue

        if in_beginning:
            first_digit_idx = i

            in_beginning = False

        digits += 1

        last_digit_idx = i

        if digits == 4:
            break

    if last_digit_idx == 0:
        return "0"

    # The dot arises on scientific notation
    digits_value = value_str[first_digit_idx:last_digit_idx + 1]

    scaling_factor = round( pow(10, last_digit_idx + 1) / int(digits_value) )

    return str(f"1/{scaling_factor}")


def get_image_width_and_height(path_to_image):
    image = Image.open(path_to_image)

    image_width = image.width

    image_height = image.height

    image.close()

    return image_width, image_height
