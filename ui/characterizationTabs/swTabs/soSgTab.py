"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QMainWindow, QWidget, QLabel,
        QFileDialog, QHBoxLayout, QVBoxLayout, QGridLayout,
        QRadioButton,QGroupBox,
        QPushButton, QComboBox, QCheckBox, QLineEdit, QApplication)
from PyQt6.QtCore import Qt, QTimer

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.messages_constants import MISSING_WELL
from constants.porosity_constants import SO_SG_LBL
from constants.pytrophysicsConstants import READ_MODE_WELL_NAME, SEE_WINDOW_LBL
from constants.tab_constants import EVERY_TAB, SO_SG_TAB_NAME

from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow
from ui.style.StyleCombos import (color_combo_box, marker_combo_box, line_combo_box)
from services.sw_service import get_so_sg
from ui.style.button_styles import (PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE_2)


class SoSgTab(QWidgetWithWell):
    def __init__(self):
        super().__init__(SO_SG_TAB_NAME)
        self.graphWindow = None

        self.initUI()

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################

        row = 0

        self.curveLbl = QLabel("Curva SW: ")
        self.curveCbo = QComboBox(self)
        self.curveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.curveCbo)

        self.curveLayout = QHBoxLayout()
        self.curveLayout.addWidget(self.curveLbl)
        self.curveLayout.addWidget(self.curveCbo)
        self.gridLayout.addLayout(self.curveLayout, row, 0, 1, 2)

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
        self.curveStyleLbl = QLabel("Estilo de la curva:")
        self.gridLayout.addWidget(self.curveStyleLbl, row, 0, 1, 2)

        ########################################################################

        row += 1
        self.curveStyleLayout = QHBoxLayout()

        self.curveColorCbo = color_combo_box()
        self.curveLineCbo = line_combo_box()
        self.curveMarkerCbo = marker_combo_box()

        self.curveStyleLayout.addWidget(self.curveColorCbo)
        self.curveStyleLayout.addWidget(self.curveLineCbo)
        self.curveStyleLayout.addWidget(self.curveMarkerCbo)

        self.gridLayout.addLayout(self.curveStyleLayout, row, 0, 1, 2)

        ########################################################################

        row += 1

        self.previewBtn = QPushButton(CROSSPLOTS_CONSTANTS.PREVIEW_BUTTON)

        self.previewBtn.clicked.connect(
            lambda checked: self.preview()
        )

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 1)

        row += 1

        self.previewBtn \
            .setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.previewLayout = QHBoxLayout()

        self.seeWindowBtn = QPushButton(SEE_WINDOW_LBL)

        self.seeWindowBtn.setStyleSheet(PREVIEW_BUTTON_STYLE)

        self.seeWindowBtn \
            .clicked \
            .connect(lambda: self.see_window())

        self.previewLayout.addWidget(self.previewBtn)

        self.previewLayout.addWidget(self.seeWindowBtn)

        self.gridLayout.addLayout(self.previewLayout, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        ########################################################################

        row += 1

        self.nameLbl = QLabel("Nombre: ")
        self.nameQle = QLineEdit(self)
        self.nameLayout = QHBoxLayout()
        self.nameLayout.addWidget(self.nameLbl)
        self.nameLayout.addWidget(self.nameQle)

        row += 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 1)

        row += 1

        self.nameQle.setStyleSheet(QLE_NAME_STYLE_2)

        self.gridLayout.addLayout(self.nameLayout, row, 0, 1, 1, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1

        self.saveCurveBtn = QPushButton("Guardar curva")

        self.saveCurveBtn.clicked.connect(
            lambda checked: self.saveCurve()
        )

        self.saveCurveBtn.setStyleSheet(SAVE_BUTTON_STYLE)

        self.gridLayout.addWidget(self.saveCurveBtn, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        self.add_serializable_attributes(
            self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb, self.customMinDepthQle,
                                    self.customMaxDepthQle, self.curveMarkerCbo, self.curveLineCbo,
                                    self.curveColorCbo])

    def on_selected(self):
        if self.well is None or self.well.wellModel.get_name() == READ_MODE_WELL_NAME:
            return

        self.customMinDepthQle.setEnabled(self.depthCustomRb.isChecked())

        self.customMaxDepthQle.setEnabled(self.depthCustomRb.isChecked())

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

    def getSoSg(self):
        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        sw_curve = self.well.wellModel.get_partial_ranged_df_curve(self.curveCbo.currentText(), minDepth, maxDepth, "", "")

        return get_so_sg(sw_curve)

    def _preview(self, soSgCurve):
        depthCurve = self.well.wellModel.get_depth_curve()

        self.add_curve_with_y_label({
            'tab_name': self.tab_name,
            'track_name': "Saturacion Petroleo/Saturacion Gas",
            'curve_name': SO_SG_TAB_NAME,
            'x_axis': soSgCurve,
            'y_axis': depthCurve,
            "x_label": SO_SG_LBL,
            "y_label": self.get_y_label(),
            'color': self.curveColorCbo.currentText(),
            'line_style': self.curveLineCbo.currentText(),
            'line_marker': self.curveMarkerCbo.currentText(),
            'add_axis': True
        })
        
        self.well.graphicWindow.draw_tracks(self.tab_name)

    def preview(self):
        if not super().preview():
            return
        
        soSgCurve = self.getSoSg()
        if soSgCurve is None:
            return
        
        self._preview(soSgCurve)

    def saveCurve(self):
        if not super().preview():
            return

        if str(self.nameQle.text()) == "":
            AlertWindow("El nombre de la curva no puede ser vacio")
            return

        if str(self.nameQle.text()).upper() in set(self.well.wellModel.get_curve_names()):
            AlertWindow("Ya existe una curva con ese nombre")
            return

        soSgCurve = self.getSoSg()
        if soSgCurve is None:
            return
        
        self.well.wellModel.append_curve(self.nameQle.text(), soSgCurve)

        InformationWindow("Curva guardada")

    def update_tab(self, well=None, force_update=False):
        if force_update:
            return

        if not super().update_tab(well):
            return

        self.window = self.well \
            .graphicWindow

        self.curveCbo.setCurrentIndex(0)
