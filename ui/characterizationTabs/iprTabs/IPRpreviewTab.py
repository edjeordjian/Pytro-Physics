"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QMessageBox, QPushButton, QComboBox)
from PyQt6.QtCore import Qt

from functools import reduce

import constants.VSHALE_MENU_CONSTANTS as VSHALE_MENU_CONSTANTS

from constants.messages_constants import MISSING_WELL

from services.tools.json_service import are_similarl_json_lists
from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone

from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow
from ui.style.StyleCombos import (color_combo_box, line_combo_box)
from ui.visual_components.combo_handler import update_cbos
from ui.style.button_styles import PREVIEW_BUTTON_STYLE


class IPRPreviewTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("IPR Preview")

        self.ipr_cbos = []

        self.ipr_curves = []

        self.setLayout(self.gridLayout)

        self.draw_section()

        self.delete_section()


    def draw_section(self):
        self.ipr_curve_to_draw_label = QLabel("Curva IPR para graficar:")
        self.ipr_curve_to_draw_cbo = QComboBox()
        self.ipr_curve_to_draw_cbo.setPlaceholderText("N/A")

        self.ipr_curve_to_draw_layout = QHBoxLayout()
        self.ipr_curve_to_draw_layout \
            .addWidget(self.ipr_curve_to_draw_label)
        self.ipr_curve_to_draw_layout \
            .addWidget(self.ipr_curve_to_draw_cbo)
        self.ipr_curve_to_draw_layout \
            .addWidget(QLabel(""))

        self.add_layout_to_layout(self.ipr_curve_to_draw_layout)

        self.ipr_style_lbl = QLabel("Color y Tipo de Linea: ")
        self.ipr_color_cbo = color_combo_box()
        self.ipr_color_cbo.setCurrentIndex(0)
        self.ipr_line_style_cbo = line_combo_box()
        self.ipr_line_style_cbo.setCurrentIndex(0)

        self.ipr_style_layout = QHBoxLayout()
        self.ipr_style_layout.addWidget(self.ipr_style_lbl)
        self.ipr_style_layout.addWidget(self.ipr_color_cbo)
        self.ipr_style_layout.addWidget(self.ipr_line_style_cbo)

        self.add_layout_to_layout(self.ipr_style_layout)

        self.preview_btn = QPushButton(VSHALE_MENU_CONSTANTS.PREVIEW_BUTTON)
        self.preview_btn.setStyleSheet(PREVIEW_BUTTON_STYLE)
        self.preview_btn.clicked.connect(
            lambda checked: self.preview_ipr()
        )

        self.add_widget_to_layout(self.preview_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.ipr_cbos \
            .extend([self.ipr_curve_to_draw_cbo])
        
        self.add_blank_line()


    def delete_section(self):
        self.ipr_curve_to_delete_label = QLabel("Curva IPR para borrar:")
        self.ipr_curve_to_delete_cbo = QComboBox()
        self.ipr_curve_to_delete_cbo.setPlaceholderText("N/A")

        self.ipr_curve_to_delete_layout = QHBoxLayout()
        self.ipr_curve_to_delete_layout \
            .addWidget(self.ipr_curve_to_delete_label)
        self.ipr_curve_to_delete_layout \
            .addWidget(self.ipr_curve_to_delete_cbo)
        self.ipr_curve_to_delete_layout \
            .addWidget(QLabel(""))

        self.add_layout_to_layout(self.ipr_curve_to_delete_layout)

        self.delete_btn = QPushButton("Borrar curva")
        self.delete_btn.setStyleSheet(PREVIEW_BUTTON_STYLE)
        self.delete_btn.clicked.connect(
            lambda checked: self.delete_ipr()
        )

        self.add_widget_to_layout(self.delete_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        self.ipr_cbos \
            .extend([self.ipr_curve_to_delete_cbo])
        
        self.add_blank_line()


    def get_ipr(self):
        curve_name = self.ipr_curve_to_draw_cbo.currentText()
        return reduce(lambda x, y: x if x["name"] == curve_name else y, self.well.wellModel.ipr_curves)


    def preview_ipr(self):
        if not super().preview():
            return

        if len(self.well.wellModel.ipr_curves) == 0:
            AlertWindow("No hay curva de IPR para graficar")
            return

        config_aux = self.get_ipr()

        config = {
            'title': 'IPR - ' + config_aux['name'],
            'x_axis_title': "Q0 [bbl/d]",
            'y_axis_title': "Pwf [psia]",
            'flex_size': 6,
            'invert_x': False,
            'invert_y': False,
            'log_x': False,
            'log_y': False,
            'scatter_groups': [],
            'line_groups': [{
                    'x_axis': config_aux['x_axis'],
                    'y_axis': config_aux['y_axis'],
                    'color': self.ipr_color_cbo.currentText(),
                    'line': self.ipr_line_style_cbo.currentText()
                }
            ]
        }

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])

    def delete_ipr(self):
        if not super().preview():
            return
        
        if len(self.well.wellModel.ipr_curves) == 0:
            AlertWindow("No hay curva de IPR para borrar")
            return

        self.confirmMsg = QMessageBox()
        self.confirmMsg.setIcon(QMessageBox.Icon.Question)
        self.confirmMsg.setText("¿Estas seguro de borrar la curva: " + str(self.ipr_curve_to_delete_cbo.currentText()) + "?")
        self.confirmMsg.setWindowTitle("Confirmar borrado")
        self.confirmMsg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
        buttonY = self.confirmMsg.button(QMessageBox.StandardButton.Yes)
        buttonY.setText('Si')
        buttonN = self.confirmMsg.button(QMessageBox.StandardButton.Cancel)
        buttonN.setText('Cancelar')
        self.confirmMsg.exec()
        if self.confirmMsg.clickedButton() == buttonY:
            self._delete_curve_confirmed()
        else: 
            InformationWindow("No se borro la Curva " + str(self.ipr_curve_to_delete_cbo.currentText()))


    def _delete_curve_confirmed(self):
        self.well.wellModel.delete_ipr_curve(self.ipr_curve_to_delete_cbo.currentText())
        print("Curva " + str(self.ipr_curve_to_delete_cbo.currentText()) + " Borrada")
        InformationWindow("Curva " + str(self.ipr_curve_to_delete_cbo.currentText()) + " Borrada")
        self.update_tab(self.well)

    def update_tab(self, well=None, force_update=False):
        if (not super().update_tab(well, force_update=force_update)) and are_similarl_json_lists(self.ipr_curves,
                                                                      self.well.wellModel.ipr_curves):
            return

        self.ipr_curves = self.well \
            .wellModel \
            .ipr_curves \
            .copy()

        update_cbos(self.ipr_cbos,
                    self.ipr_curves,
                    lambda ipr_curve: ipr_curve["name"])
