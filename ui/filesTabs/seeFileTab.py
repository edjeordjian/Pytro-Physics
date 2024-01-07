"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QVBoxLayout,
    QTextEdit
)

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell


class SeeFileTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("Ver LAS")

        self.initUI()
    
    def initUI(self):
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)

        self.seeFileWidget = QTextEdit()

        self.seeFileWidget.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)

        self.seeFileWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.seeFileWidget.setReadOnly(True)

        self.layout.addWidget(self.seeFileWidget)
    
    def update_tab(self, well):
        if not super().update_tab(well):
            return

        self.seeFileWidget.setText(self.well.wellModel.get_raw_data())
