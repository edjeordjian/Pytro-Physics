"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from services.image_service import (pt_to_px, px_to_ft, px_to_m, get_scale_format,
                                    get_image_width_and_height)

from PIL import Image 

from os import remove


def test_pt_to_px():
    assert pt_to_px(2, 72) == 2


def test_px_to_ft():
    assert px_to_ft(144, 12) == 1


def test_px_to_m():
    assert px_to_m(2, 92) == 0.0005521739130434783


def test_get_scale_format():
    assert get_scale_format(0.1) == "1/10"


def test_get_image_width_and_height():
    new_png = Image.new('RGB', (11, 12), (255, 255, 255))
    new_png.save("test_image_width_and_height.png")
    new_png.close()
    width, height = get_image_width_and_height("test_image_width_and_height.png")
    assert width == 11
    assert height == 12
    remove("test_image_width_and_height.png")
