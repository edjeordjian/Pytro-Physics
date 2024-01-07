"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QPushButton, QHBoxLayout

from constants.LITHOLOGY_CONSTANTS import ADD_LITHOLOGY_LBL
from constants.pytrophysicsConstants import DEFAULT_LITHOLOGY_CONFIG
from constants.tab_constants import LITOLOGY_EDITOR_TAB, SAVE_LBL
from constants.messages_constants import REPEATED_LITYLOGY_NAME
from services.tools.list_service import get_uniques_and_duplicated, list_to_str
from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
from ui.popUps.alertWindow import AlertWindow
from ui.visual_components.LithologyRow import LithologyRow, get_serialized_lithologies
from ui.style.button_styles import SAVE_BUTTON_STYLE


class LithologyEditorTab(QWidgetWithWell):
    def __init__(self):
        super().__init__(LITOLOGY_EDITOR_TAB)

        self.lithologies = []

        self.setLayout(self.gridLayout)

        self.add_lithology_btn = QPushButton(ADD_LITHOLOGY_LBL)

        self.add_lithology_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.add_lithology_btn \
            .clicked \
            .connect(lambda x: self.add_lithology_row(DEFAULT_LITHOLOGY_CONFIG))

        self.save_lithologies_btn = QPushButton(SAVE_LBL)
        self.save_lithologies_btn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.save_lithologies_btn \
            .clicked \
            .connect(self.save_lithologies)

        self.btn_layout = QHBoxLayout()

        self.btn_layout \
            .addWidget(self.add_lithology_btn,
                       alignment=Qt.AlignmentFlag
                       .AlignRight)

        self.btn_layout \
            .addWidget(self.save_lithologies_btn,
                       alignment=Qt.AlignmentFlag
                       .AlignLeft)

        self.add_layout_to_layout(self.btn_layout)

        self.add_blank_line()

        self.lithology_configs = []

    def remove_lithologies(self):
        self.lithology_configs = get_serialized_lithologies(self.lithologies)

        for lithology in self.lithologies:
            lithology.delete(self.remove_layout_from_layout)

    def remove_lithology_row(self,
                             lithology_to_delete):
        self.remove_lithologies()

        self.lithology_configs = list(
            filter(lambda config: config['name'] != lithology_to_delete.get_name(),
                   self.lithology_configs)
        )

        self.create_lithology_rows()

    def add_lithology_row(self,
                          config,
                          add_config=True):
        if add_config:
            self.lithology_configs \
                .append(config)

        row = LithologyRow(config,
                           self.add_layout_to_layout,
                           self.remove_lithology_row)

        self.lithologies \
            .append(row)

        self.numeric_inputs.extend(row.get_numeric_inputs())

        self.add_blank_line()

        self.add_blank_line()

    def save_lithologies(self):
        self.set_ever_updated()

        names = list(map(lambda lithology_row: lithology_row.get_name(),
                         self.lithologies))

        unique, duplicated = get_uniques_and_duplicated(names)

        if len(duplicated) != 0:
            AlertWindow(f"{REPEATED_LITYLOGY_NAME}: {list_to_str(duplicated)}")

            return

        self.replace_commas_in_numeric_inputs()

        self.well \
            .wellModel \
            .set_lithologies(get_serialized_lithologies(self.lithologies))

        self.well \
            .wellModel \
            .save_lithologies()

    def update_tab(self, well=None, force_update=False):
        if force_update:
            return

        if not super().update_tab(well):
            return

        self.remove_lithologies()

        self.lithology_configs = []

        for lithology in self.well \
                .wellModel \
                .get_lithologies():
            self.lithology_configs \
                .append(lithology)

        self.create_lithology_rows()

    def create_lithology_rows(self):
        self.lithologies = []

        self.reset_lines(2)

        for config in self.lithology_configs:
            self.add_lithology_row(config,
                                   False)
