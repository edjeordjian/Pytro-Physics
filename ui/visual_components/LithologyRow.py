"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QWidget, QLineEdit, QHBoxLayout, QCheckBox,
                             QPushButton, QLabel)

from constants.LITHOLOGY_CONSTANTS import (RHO_B_LABEL, SONIC_LABEL, PEF_LABEL, NEUTRON_LABEL,
                                           NEUTRON_FRACTION_LBL)

from constants.pytrophysicsConstants import COLOR_CONSTANTS

from constants.tab_constants import NAME_LBL, DELETE_LBL

from ui.style.BrushFill import BRUSH_FILLS, get_brush_fills

from ui.style.button_styles import SAVE_BUTTON_STYLE, DELETE_BUTTON_STYLE

from ui.style.StyleCombos import color_combo_box, marker_combo_box, line_combo_box, brush_fill_combo_box

from ui.visual_components.layout_handler import add_to_layout


def get_serialized_lithologies(lithology_rows):
    serialized_lithologies = []

    for row in lithology_rows:
        serialized_lithologies.append({
            "name": row.name_text_box
                .text(),

            "color": row.color_cbo
                .currentText(),

            "fill": row.fill_cbo
                .currentText(),

            "density": row.density_text_box
                .text(),

            "sonic": row.sonic_text_box
                .text(),

            "neutron": row.neutron_text_box
                .text(),

            "neutron_fraction": str(row.neutron_check
                                    .isChecked()),

            "pef": row.pef_text_box
                .text()
        })

    return serialized_lithologies


class LithologyRow(QWidget):
    def __init__(self,
                 config,
                 add_layout_fn,
                 remove_row_fn):
        super().__init__()

        self.label_layout = QHBoxLayout()

        self.name_label = QLabel("Nombre")

        self.density_label = QLabel("Densidad (\u03C1)")

        self.sonic_label = QLabel(SONIC_LABEL)

        self.pef_label = QLabel(PEF_LABEL)

        self.neutron_label = QLabel(NEUTRON_LABEL)

        add_to_layout(self.label_layout, [self.name_label, self.density_label, self.sonic_label,
                                          self.pef_label, self.neutron_label])

        add_layout_fn(self.label_layout)

        self.units_layout = QHBoxLayout()

        self.blank_unit_label = QLabel("")

        self.density_unit_label = QLabel("[g/cm3]")

        self.sonic_unit_label = QLabel("[µs/ft]")

        self.pef_unit_label = QLabel("[VARNs/e]")

        self.neutron_unit_label = QLabel("[%]")

        add_to_layout(self.units_layout, [self.blank_unit_label, self.density_unit_label, self.sonic_unit_label,
                                          self.pef_unit_label, self.neutron_unit_label])

        add_layout_fn(self.units_layout)

        self.text_box_layout = QHBoxLayout()

        self.combo_layout = QHBoxLayout()

        self.name_text_box = QLineEdit(config["name"])

        self.name_text_box \
            .setPlaceholderText(NAME_LBL)

        self.density_text_box = QLineEdit(config["density"])

        self.density_text_box \
            .setPlaceholderText(RHO_B_LABEL)

        self.sonic_text_box = QLineEdit(config["sonic"])

        self.sonic_text_box \
            .setPlaceholderText(SONIC_LABEL)

        self.pef_text_box = QLineEdit(config["pef"])

        self.pef_text_box \
            .setPlaceholderText(PEF_LABEL)

        self.neutron_text_box = QLineEdit(config["neutron"])

        self.neutron_text_box \
            .setPlaceholderText(NEUTRON_LABEL)

        self.neutron_check = QCheckBox()

        self.neutron_check \
            .setText(NEUTRON_FRACTION_LBL)

        if config["neutron_fraction"] \
                .lower() == "true":
            self.neutron_check \
                .setChecked(True)

            self.neutron_unit_label.setText("[Fracción]")

        self.neutron_layout = QHBoxLayout()

        self.neutron_layout \
            .addWidget(self.neutron_text_box)

        self.neutron_layout \
            .addWidget(self.neutron_check)

        self.color_cbo = color_combo_box()

        self.color_cbo \
            .setCurrentIndex(list(COLOR_CONSTANTS.values())
                             .index(config["color"]))

        self.fill_cbo = brush_fill_combo_box()

        self.fill_cbo \
            .setCurrentIndex(get_brush_fills().index(config["fill"]))

        self.delete_btn = QPushButton(DELETE_LBL)

        self.delete_btn.setStyleSheet(DELETE_BUTTON_STYLE)

        self.delete_btn \
            .clicked \
            .connect(lambda: (
            remove_row_fn(self)))

        self.text_box_layout \
            .addWidget(self.name_text_box)

        self.text_box_layout \
            .addWidget(self.density_text_box)

        self.text_box_layout \
            .addWidget(self.sonic_text_box)

        self.text_box_layout \
            .addWidget(self.pef_text_box)

        self.text_box_layout \
            .addLayout(self.neutron_layout)

        add_layout_fn(self.text_box_layout)

        self.combo_layout \
            .addWidget(self.color_cbo)

        self.combo_layout \
            .addWidget(self.fill_cbo)

        self.combo_layout \
            .addWidget(self.delete_btn)

        add_layout_fn(self.combo_layout)

    def get_name(self):
        return self.name_text_box \
            .text()

    def delete(self,
               delete_layout_fn):
        delete_layout_fn(self.text_box_layout)

        delete_layout_fn(self.combo_layout)

        delete_layout_fn(self.label_layout)

        delete_layout_fn(self.units_layout)

    def get_numeric_inputs(self):
        return [
            self.density_text_box, self.sonic_text_box, self.neutron_text_box, self.pef_text_box
        ]
