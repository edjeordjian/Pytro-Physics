"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import os

from tests.tests_helper import (set_current_path, init_config, load_view_to_window, get_graphic_window)

current_path = os.path \
    .abspath(__file__) \
    .split("\\")

current_path = set_current_path(current_path)


def test_export_pdf(qtbot):
    window = init_config(qtbot, current_path)

    graphic_window = get_graphic_window(window)

    load_view_to_window(qtbot, graphic_window, current_path, "vshale_sp.view")

    pdf_name = "a.pdf"

    graphic_window.export()

    graphic_window.exportScaleDefaultCb.setChecked(False)
    graphic_window.updateScaleSelection()
    graphic_window.exportScaleCbo.setCurrentIndex(11)
    graphic_window.exportAllTracksCb.setChecked(True)
    graphic_window.updateExportAllTracks()
    graphic_window.exportPDFRb.setChecked(True)
    graphic_window.exportPNGRb.setChecked(False)
    graphic_window.exportTypeSelection()
    graphic_window.exportPDFPaperSizeCbo.setCurrentIndex(1)
    graphic_window.export_to_pdf("a", show_popup=False)

    assert os.stat(pdf_name).st_size > 40000
    os.remove(pdf_name)

