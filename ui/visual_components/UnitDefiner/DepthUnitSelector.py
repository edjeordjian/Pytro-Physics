"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtGui import QIcon

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QComboBox

from constants.general_constants import METERS_LBL, FEETS_LBL

from constants.media_constants import VIEW_ICON_ROUTE

from ui.visual_components.UnitDefiner.UnitSelectable import UnitSelectable


class DepthUnitSelector(UnitSelectable):
    def __init__(self, column_name, layout):
        super().__init__()
        
        self.layout = QHBoxLayout()

        self.setWindowIcon(QIcon(VIEW_ICON_ROUTE))

        self.label = QLabel(column_name)

        self.unit_combo_box = QComboBox()

        self.unit_combo_box.addItem(METERS_LBL, METERS_LBL)

        self.unit_combo_box.addItem(FEETS_LBL, FEETS_LBL)

        self.layout \
            .addWidget(self.label)

        self.layout \
            .addWidget(self.unit_combo_box)

        layout.addLayout(self.layout)

    def get_unit(self):
        return self.unit_combo_box \
                   .currentText()

    def get_name(self):
        return self.label \
                   .text()
