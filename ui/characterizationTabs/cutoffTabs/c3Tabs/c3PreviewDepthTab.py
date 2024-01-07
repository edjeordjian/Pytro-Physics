"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QGridLayout, QRadioButton,
                             QGroupBox, QPushButton, QComboBox, QLineEdit,
                             QVBoxLayout)
from PyQt6.QtCore import Qt

from constants.messages_constants import MISSING_WELL
from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS, LINE_TYPE_CONSTANTS, COLOR_CONSTANTS, \
    READ_MODE_WELL_NAME, SEE_WINDOW_LBL
from constants.tab_constants import CUTOFF_3_TAB_NAME, CUTOFF_3_CURVE_NAME

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
import constants.VSHALE_MENU_CONSTANTS as VSHALE_MENU_CONSTANTS
from ui.popUps.alertWindow import AlertWindow

from services.tools.string_service import is_number

from ui.style.StyleCombos import color_combo_box, line_combo_box
from ui.style.button_styles import PREVIEW_BUTTON_STYLE
from ui.visual_components.constant_curves_handler import add_rectangle_to


class C3PreviewDepthTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("C3 Preview")

        self.prev_well_name = ""

        self.prev_well_update_amount = -1

        self.selectedCurve = ""

        self.initUI()

        self.numeric_inputs.extend([self.cutoffValueQle,
                                    self.customMaxDepthQle, self.customMinDepthQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.curveLineCbo, self.curveColorCbo,
             self.cutoffValueQle])

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################

        row = 0

        self.curveLbl = QLabel("Variable de entrada (Saturacion de Agua SW):")
        self.curveCbo = QComboBox(self)
        self.curveCbo.setPlaceholderText(VSHALE_MENU_CONSTANTS.CURVE_CBO_PLACEHOLDER)
        self.curve_selectors.append(self.curveCbo)

        self.curveLayout = QHBoxLayout()
        self.curveLayout.addWidget(self.curveLbl)
        self.curveLayout.addWidget(self.curveCbo)
        self.gridLayout.addLayout(self.curveLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.curveColorCbo = color_combo_box()
        self.curveLineCbo = line_combo_box()

        self.curveStyleLayout = QHBoxLayout()
        self.curveStyleLayout.addWidget(self.curveColorCbo)
        self.curveStyleLayout.addWidget(self.curveLineCbo)
        self.gridLayout.addLayout(self.curveStyleLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        #https://geekscoders.com/courses/pyqt6-tutorials/lessons/how-to-create-qradiobutton-in-pyqt6/

        self.depthGrpBox = QGroupBox("Profundidad")
        #self.grpbox.setFont(QFont("Times New Roman", 15))

        # this is vbox layout
        self.depthLayout = QVBoxLayout()

        # these are the radiobuttons
        self.depthFullLasRb = QRadioButton("Todo el LAS")
        self.depthFullLasRb.setChecked(True)
        #self.depthFullLasRb.setFont(QFont("Times New Roman", 14))
        self.depthFullLasRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthFullLasRb)

        self.depthCustomRb = QRadioButton("personalizado")
        #self.depthCustomRb.setFont(QFont("Times New Roman", 14))
        self.depthCustomRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthCustomRb)

        self.depthGrpBox.setLayout(self.depthLayout)

        self.gridLayout.addWidget(self.depthGrpBox, row, 0, 1, 1)

        ########################################################################

        self.customMinDepthLbl = QLabel("Profundidad mín.: ")
        self.customMinDepthQle = QLineEdit(self)
        self.customMinDepthLayout = QHBoxLayout()
        self.customMinDepthLayout.addWidget(self.customMinDepthLbl)
        self.customMinDepthLayout.addWidget(self.customMinDepthQle)
        self.customMinDepthQle.setEnabled(False)

        self.customMaxDepthLbl = QLabel("Profundidad máx.:")
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle)
        self.customMaxDepthQle.setEnabled(False)

        self.customDepthLayout = QVBoxLayout()
        self.customDepthLayout.addLayout(self.customMinDepthLayout)
        self.customDepthLayout.addLayout(self.customMaxDepthLayout)
        self.gridLayout.addLayout(self.customDepthLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

        self.cutoffValueLbl = QLabel("Valor de Cutoff:")
        self.cutoffValueQle = QLineEdit()
        self.cutoffValueQle.setPlaceholderText("Valor positivo")

        self.cutoffValueLayout = QHBoxLayout()
        self.cutoffValueLayout.addWidget(self.cutoffValueLbl)
        self.cutoffValueLayout.addWidget(self.cutoffValueQle)        
        self.gridLayout.addLayout(self.cutoffValueLayout, row, 0, 1, 1)

        ########################################################################

        row += 1
        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2)
        
        ########################################################################

        row += 1

        self.previewBtn = QPushButton(VSHALE_MENU_CONSTANTS.PREVIEW_BUTTON)
        self.previewBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)
        self.previewBtn.clicked.connect(
            lambda checked: self.preview()
        )
        
        self.previewLayout = QHBoxLayout()

        self.seeWindowBtn = QPushButton(SEE_WINDOW_LBL)

        self.seeWindowBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.seeWindowBtn \
            .clicked \
            .connect(lambda: self.see_window())

        self.previewLayout.addWidget(self.previewBtn)

        self.previewLayout.addWidget(self.seeWindowBtn)

        self.gridLayout.addLayout(self.previewLayout, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)


    def on_selected(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return

        self.customMinDepthQle \
            .setEnabled(self.depthCustomRb
                        .isChecked())

        self.customMaxDepthQle \
            .setEnabled(self.depthCustomRb
                        .isChecked())

        if self.depthCustomRb \
                .isChecked():
            self.customMinDepthQle \
                .setPlaceholderText(str(
                min(self.well.wellModel.get_depth_curve())
            ))

            self.customMaxDepthQle \
                .setPlaceholderText(str(
                max(self.well.wellModel.get_depth_curve())
            ))

    def preview(self):
        if not super().preview():
            return

        if (not is_number(self.cutoffValueQle.text())) or float(self.cutoffValueQle.text()) < 0:
            AlertWindow("El valor de cutoff ingresado es invalido, ingrese un numero positivo (Se usa punto '.' como separador decimal)")
            return

        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))

        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        x_title = self.well \
            .wellModel \
            .get_label_for(self.curveCbo.currentText())

        config_curve = {
            'tab_name': self.tab_name,
            'track_name': 'C3',
            'curve_name': CUTOFF_3_CURVE_NAME,
            "x_label": x_title,
            "y_label": self.get_y_label(),

            'x_axis': self.well.wellModel.get_partial_ranged_df_curve(self.curveCbo.currentText(), minDepth, maxDepth, "", ""),
            'y_axis': self.well.wellModel.get_depth_curve(),

            'color': self.curveColorCbo.currentText(),
            'line_style': self.curveLineCbo.currentText(),
            'line_marker': LINE_MARKER_CONSTANTS["NONE"],
            'line_width': 1,
            'add_axis': True
        }

        self.add_curve_with_y_label(config_curve)

        config = {
                    "y0": str(min(depth_curve)),
                    "y1": str(max(depth_curve)),
                    "x0": self.cutoffValueQle.text(),
                    "x1": self.cutoffValueQle.text(),

                    "color": COLOR_CONSTANTS["RED"],
                    "line": LINE_TYPE_CONSTANTS["SOLID_LINE"],

                    'tab_name': config_curve['tab_name'],
                    'track_name': config_curve['track_name']
                }

        add_rectangle_to(self.well.graphicWindow,
                         config,
                         config["track_name"])

        self.well.graphicWindow.draw_tracks(self.tab_name)


    def update_tab(self, well=None, force_update=False):
        if force_update:
            return

        if not super().update_tab(well):
            return

        for item_index in reversed(range(self.curveCbo.count())):
            self.curveCbo.removeItem(item_index)

        for curveName in self.well.wellModel.get_curve_names():
            self.curveCbo.addItem(curveName)

        if len(self.well.wellModel.get_curve_names()) == 0:
            return

        self.window = self.well \
            .graphicWindow

        self.curveCbo.setCurrentIndex(0)


    def obtain_tab_name(self):
        return self.tab_name
