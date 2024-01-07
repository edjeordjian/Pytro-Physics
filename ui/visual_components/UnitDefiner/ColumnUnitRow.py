"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QLabel, QLineEdit, QHBoxLayout

from constants.media_constants import VIEW_ICON_ROUTE

from ui.visual_components.UnitDefiner.DepthUnitSelector import UnitSelectable


class ColumnUnitRow(UnitSelectable):
    def __init__(self, column_name, layout):
        super().__init__()

        self.layout = QHBoxLayout()

        self.label = QLabel(column_name)

        self.setWindowIcon(QIcon(VIEW_ICON_ROUTE))

        self.unit_textbox = QLineEdit()

        self.layout \
            .addWidget(self.label)

        self.layout \
            .addWidget(self.unit_textbox)

        layout.addLayout(self.layout)

    def get_unit(self):
        return self.unit_textbox.text()

    def get_name(self):
        return self.label.text()
