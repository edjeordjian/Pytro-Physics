"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from pyqtgraph import exporters


def export_png_file(item,
                    file_name,
                    index):
    exporter = exporters.ImageExporter(item)

    new_png_file_name = file_name + '_00' \
                        + str(index) \
                        + '.png'

    if not exporter.export(new_png_file_name):
        return ""

    return new_png_file_name
