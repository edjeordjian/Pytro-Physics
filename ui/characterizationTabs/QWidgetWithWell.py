"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QWidget, QLabel, QGridLayout

from constants.messages_constants import MISSING_WELL
from constants.pytrophysicsConstants import READ_MODE_WELL_NAME
from services.constant_service import get_depth_lbl
from ui.popUps.alertWindow import AlertWindow

from ui.visual_components.combo_handler import update_curve_list
from ui.visual_components.data_menu_handler import serialize_qt_attribute


class QWidgetWithWell(QWidget):
    def __init__(self, tab_name):
        super().__init__()

        self.tab_name = tab_name

        self.well = None

        self.use_data_in_curve_selectors = False

        self.prev_well_name = ""

        self.prev_well_update_amount = -1

        self.selectedCurve = ""

        self.curve_selectors = []

        self.serializable_attribtues = []

        self.numeric_inputs = []

        self.lines = 3

        self.blank_lines = []

        self.ever_updated = False

        self.gridLayout = QGridLayout()

        self.gridLayout.setAlignment(Qt.AlignmentFlag
                                     .AlignTop)

    def see_window(self):
        if self.well is None:
             return AlertWindow(MISSING_WELL)

        self.window \
            .show()

    def get_name(self):
        return self.tab_name

    def should_update(self, well):
        if self.well is None:
            self.well = well

        well_name = well \
            .wellModel \
            .get_name()

        well_updates = well \
            .wellModel \
            .get_amount_of_updates()

        if (well_name != self.prev_well_name) or (self.prev_well_update_amount != well_updates):
            self.prev_well_name = well_name
            self.prev_well_update_amount = well_updates
            return True

        if len(well.wellModel.get_curve_names()) == 0:
            return False

        return False

    def update_tab(self, well=None, force_update=False, use_data=False):
        if force_update:
            return False

        prev_well_name = self.prev_well_name

        if not self.should_update(well):
            return False

        self.well = well

        print("Update ", self.tab_name, " con: ", self.well.wellModel.get_name())

        reset_cbo_index = False

        if (well.wellModel.get_name() != prev_well_name):
            reset_cbo_index = True

        for cbo in self.curve_selectors:
            update_curve_list(cbo,
                              self.well,
                              use_data)
            if reset_cbo_index:
                cbo.setCurrentIndex(0)                              

        return True

    def add_blank_line(self):
        self.blank_lines \
            .append(QLabel(""))

        self.add_widget_to_layout(self.blank_lines[-1])

    def delete_blank_lines(self):
        for line in self.blank_lines:
            self.remove_widget(line)

    # What was the alternative to blank text for an empty column???
    def add_blank_column(self,
                         layout=None,
                         length=0,
                         column=1):
        blank_text = "".join([" " for i in range(length)])

        if layout is not None:
            layout.addWidget(QLabel(blank_text))

            self.add_layout_to_layout(layout,
                                      column=column)

        else:
            self.add_widget_to_layout(QLabel(blank_text),
                                      column=column)

    def add_layout_to_layout(self,
                             layout,
                             column=0,
                             next_line=True):
        self.gridLayout \
            .addLayout(layout,
                       self.lines,
                       column)

        if next_line:
            self.lines += 1

    def add_layout_with_span_to_layout(self,
                                       layout,
                                       column=0,
                                       next_line=True,
                                       rowspan=0,
                                       colspan=0):
        self.gridLayout \
            .addLayout(layout,
                       self.lines,
                       column,
                       rowspan,
                       colspan)

        if next_line:
            self.lines += 1

    def remove_layout_from_layout(self,
                                  layout):
        for i in range(self.gridLayout
                               .count()):
            layout_item = self.gridLayout \
                .itemAt(i)

            if layout_item.layout() == layout:
                self.delete_item_from_layout(layout_item.layout())

                self.gridLayout \
                    .removeItem(layout_item)

                break

    def delete_item_from_layout(self,
                                layout):
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.setParent(None)

            else:
                self.delete_item_from_layout(item.layout())

    def add_widget_to_layout(self,
                             widget,
                             column=0,
                             next_line=True,
                             alignment=None):

        if alignment is not None:
            self.gridLayout \
                .addWidget(widget,
                           self.lines,
                           column,
                           alignment=alignment)

        else:
            self.gridLayout \
                .addWidget(widget,
                           self.lines,
                           column)

        if next_line:
            self.lines += 1

    def remove_widget(self,
                      widget):
        self.gridLayout \
            .removeWidget(widget)

    def reset_lines(self,
                    base_lines):
        self.lines = 3 + base_lines

    def get_y_label(self):
        return get_depth_lbl(self.well.wellModel.get_depth_unit())

    def add_curve_with_y_label(self,
                               config):
        config.update({
            "y_label": self.get_y_label()
        })

        self.window.add_curve(config)

    def get_view_id(self):
        return self.tab_name

    def get_view_serialization(self):
        return {
            self.tab_name: [serialize_qt_attribute(getattr(self, attribute), attribute)
                            for attribute in self.serializable_attribtues]
        }

    def add_serializable_attributes(self, attributes):
        attribute_names = list(
            map(lambda x: x[0],
                filter(lambda x: x[1] in attributes,
                       list(vars(self).items())
                       )
                )
        )

        for name in attribute_names:
            self.serializable_attribtues \
                .append(name)

    def get_tabs(self):
        return [self]

    def replace_commas_in_numeric_inputs(self):
        for textbox in self.numeric_inputs:
            textbox.setText(textbox.text().replace(",", "."))

    def is_ever_updated(self):
        return self.ever_updated

    def set_ever_updated(self, value=True):
        self.ever_updated = value

    def preview(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            AlertWindow(MISSING_WELL)
            return False

        self.set_ever_updated()

        return True
