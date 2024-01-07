"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from img2pdf import mm_to_pt, in_to_pt


ORIGINAL_SIZE = "Original"

png_browser_options = {
    'header': 'Guardar PNG',
    'default_name': 'imagen',
    'extension': 'PNG files (.png);'
}

pdf_browser_options = {
    'header': 'Guardar PDF',
    'default_name': 'archivo',
    'extension': 'PDF files (.pdf);'
}

pdf_paper_size = {
    ORIGINAL_SIZE: ORIGINAL_SIZE,
    "A4": (mm_to_pt(210), mm_to_pt(297)),
    "A3": (mm_to_pt(297), mm_to_pt(420)),
    "A2": (mm_to_pt(420), mm_to_pt(594)),
    "A1": (mm_to_pt(594), mm_to_pt(841)),
    "A0": (mm_to_pt(841), mm_to_pt(1189)),
    "Oficio": (in_to_pt(8.5), in_to_pt(14)),
    "Tabloide": (in_to_pt(11), in_to_pt(17))
}

paper_width_in_cm = {
    ORIGINAL_SIZE: ORIGINAL_SIZE,
    "A4": "21 cm  (A4)",
    "A3": "29,7 cm  (A3)",
    "A2": "42 cm  (A2)",
    "A1": "59,4 cm  (A1)",
    "A0": "84,1 cm  (A0)",
    "Oficio": "21,6 cm  (Carta/Oficio)",
    "Tabloide": "27,94 cm  (Tabloide)"
}

NORMAL_DPI = 96

HIGH_DPI = 300

VERY_HIGH_DPI = 500

DPIS = {
    "Normal (96)": NORMAL_DPI,
    "Alto (300)": HIGH_DPI,
    "Muy alto (500)": VERY_HIGH_DPI
}

scales = ["1/20", "1/40", "1/60", "1/100",
          "1/200", "1/240", "1/500", "1/600",
          "1/1000", "1/1200", "1/2500", "1/5000"]

IMAGE_WIDTH_LBL = "Ancho:"

DPIS_LBL = "DPI"
