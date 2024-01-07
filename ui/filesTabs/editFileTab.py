"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt, QAbstractTableModel, QTimer

from PyQt6.QtWidgets import (QPushButton, QVBoxLayout, QHBoxLayout, QTableView,
                             QLabel)

from constants.edit_file_constants import PREVISUALIZATION_TAB_NAME, SINGLE_CURVE_TRACK_PREFFIX

from constants.messages_constants import MISSING_WELL

from constants.pytrophysicsConstants import READ_MODE_WELL_NAME

from constants.tab_constants import EVERY_TAB

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell

from constants.general_constants import loading_pop_up_timeout_ms

from ui.popUps.LoadingWindow import LoadingWindow

from ui.popUps.informationWindow import InformationWindow

from ui.popUps.alertWindow import AlertWindow

import numpy as np


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:
                value = self._data.iloc[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == Qt.ItemDataRole.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    #def headerData(self, col, orientation, role):
    #    if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
    #        return self._data.columns[col]
    
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                if section < len(self._data
                                     .columns):
                    return str(self._data.columns[section])

            if orientation == Qt.Orientation.Vertical:
                if section < len(self._data
                                     .index):
                    return str(self._data.index[section])

    def flags(self, index):
        return Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsEditable



# Guide: https://www.pythonguis.com/tutorials/pyqt6-qtableview-modelviews-numpy-pandas/
"""
class EditFileTab(QTableView):
    def __init__(self):
        super().__init__()
        self.well = None
    
    def update(self, well):
        self.well = well
        self.model = TableModel(self.well.wellModel.get_DF())
        self.setModel(self.model)

    # TODO: ESTO CAPAZ DEBERIA SER UN WIDGET, QUE CONTENGA UN LAYOUT CON LA TABLA ENCIMA DE UN BOTON QUE SEA GUARDAR, QUE GUARDAR REFLEJE LOS CAMBIOS
    #       SOBRE EL DATAFRAME HECHOS AL EDITAR (LO QUE SE EDITO ES EL SELF.MODEL)
"""


class EditFileTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("Editar LAS")
        self.well = None

        self.initUI()
    
    def initUI(self):
        self.tableView = QTableView()
        
        self.layout = QHBoxLayout()

        self.layout.addWidget(self.tableView)

        self.depthUnitLabel = QLabel("")

        self.depthUnitChangeButton = QPushButton("")

        self.depthUnitLabel.hide()

        self.depthUnitChangeButton.hide()

        self.depthUnitChangeButton.clicked.connect(
            lambda checked: self.changeDepthUnit()
        )

        self.depthUnitLabel.hide()

        self.depthUnitChangeButton.hide()

        self.saveChangesButton = QPushButton("Guardar cambios")

        self.buttonsLayout = QVBoxLayout()

        self.buttonsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        see_every_curve_button = QPushButton("Ver todas las curvas del pozo")

        see_every_curve_button.clicked.connect(self.show_every_curve)

        self.buttonsLayout.addWidget(see_every_curve_button)

        self.buttonsLayout.addWidget(QLabel(""))

        delete_curves = QPushButton("Borrar curvas previsualizadas")

        delete_curves.clicked.connect(self.delete_curves_previsualization)

        self.buttonsLayout.addWidget(delete_curves)

        self.buttonsLayout.addWidget(QLabel(""))

        self.buttonsLayout.addWidget(QLabel(""))

        self.buttonsLayout.addWidget(QLabel(""))

        self.buttonsLayout.addWidget(self.depthUnitLabel)

        self.buttonsLayout.addWidget(self.depthUnitChangeButton)

        self.buttonsLayout.addWidget(QLabel(""))

        self.buttonsLayout.addWidget(self.saveChangesButton)

        self.saveChangesButton.clicked.connect(
            lambda checked: self.saveChanges()
        )

        self.layout.addLayout(self.buttonsLayout)

        self.setLayout(self.layout)

    def show_every_curve(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return AlertWindow(MISSING_WELL)

        pop_up = LoadingWindow('Cargando...')

        QTimer.singleShot(loading_pop_up_timeout_ms, lambda: (
            self._show_every_curve(),

            pop_up.close()
        ))

    def delete_curves_previsualization(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return AlertWindow(MISSING_WELL)

        self.well \
            .graphicWindow \
            .remove_tracks(PREVISUALIZATION_TAB_NAME)

        self.well \
            .graphicWindow \
            .draw_tracks(EVERY_TAB)

    def _show_every_curve(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return AlertWindow(MISSING_WELL)

        well_model = self.well \
            .wellModel

        graphic_window = self.well \
            .graphicWindow

        curve_names = well_model.get_curve_names()

        for curve_name in curve_names:
            graphic_window.add_curve({
                'tab_name': PREVISUALIZATION_TAB_NAME,

                'track_name': f"{SINGLE_CURVE_TRACK_PREFFIX} {curve_name}",

                "curve_name": curve_name,

                "x_axis": well_model.get_df_curve(curve_name),

                'y_axis': well_model.get_depth_curve(),

                "x_label": well_model.get_label_for(curve_name),

                "y_label": self.get_y_label(),
            })

        graphic_window.draw_tracks(PREVISUALIZATION_TAB_NAME)

    def saveChanges(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return
        self.well.wellModel.set_df(self.table_data)
        self.well.set_df(self.table_data.replace(self.well.get_null_value(), np.nan))
        InformationWindow("Cambios guardados")

    def changeDepthUnit(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return

        old_unit = self.well \
            .wellModel \
            .get_depth_unit()

        self.well.wellModel.change_depth_unit()

        new_unit = self.well \
            .wellModel \
            .get_depth_unit()

        self.update_tab(self.well)

        depth_curve = self.well \
            .wellModel \
            .get_depth_curve()

        self.well \
            .graphicWindow \
            .draw_tracks_with_new_unit(depth_curve, old_unit, new_unit)

        InformationWindow("Cambios guardados")

    def update_tab(self, well):
        if not super().update_tab(well):
            return

        self.well = well

        self.table_data = self.well.wellModel.get_DF() \
            .replace(np.nan, well.wellModel.get_null_value())

        self.model = TableModel(self.table_data)

        self.tableView.setModel(self.model)

        if len(str(well.wellModel.get_depth_unit())) == 0:
            self.depthUnitLabel.hide()
            self.depthUnitChangeButton.hide()
            self.depthUnitLabel.hide()
            self.depthUnitChangeButton.hide()

        else:
            self.depthUnitLabel.show()
            self.depthUnitChangeButton.show()
            self.depthUnitLabel.show()
            self.depthUnitChangeButton.show()

            if "m" in str(well.wellModel.get_depth_unit()).lower():
                self.depthUnitLabel.setText("Profundidad representada en Metros")
                self.depthUnitChangeButton.setText("Cambiar profundidad a Pies")
            else:
                self.depthUnitLabel.setText("Profundidad representada en Pies")
                self.depthUnitChangeButton.setText("Cambiar profundidad a Metros")
