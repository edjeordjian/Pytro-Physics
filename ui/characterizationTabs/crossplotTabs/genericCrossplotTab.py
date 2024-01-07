"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox, QPushButton, QComboBox,
                             QCheckBox, QLineEdit)
from PyQt6.QtCore import Qt
import numpy as np

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS
from constants.messages_constants import MISSING_WELL
from constants.pytrophysicsConstants import SEE_WINDOW_LBL
from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone
from ui.popUps.alertWindow import AlertWindow
from ui.style.StyleCombos import (color_combo_box, marker_combo_box, colormap_combo_box)
from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE
from services.tools.string_service import is_positive_integer
from services.tools.pandas_service import set_nan_in_array_if_another_is_nan


class GenericCrossplotTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Crossplot general")

        self.initUI()

        self.numeric_inputs.extend([self.customMaxDepthQle, self.customMinDepthQle])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.forceInvertXCb, self.forceLogXCb,
             self.xAxisQle, self.titleQle, self.forceInvertYCb, self.forceLogYCb,
             self.yAxisQle, self.groupsQle, self.groups])

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0

        self.titleLbl = QLabel("Titulo del Crossplot: ")
        self.titleQle = QLineEdit(self)
        self.titleQle.setStyleSheet(QLE_NAME_STYLE)
        #self.titleQle.textChanged[str].connect(self.setTitleName)
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addWidget(self.titleLbl)
        self.titleLayout.addWidget(self.titleQle, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.gridLayout.addLayout(self.titleLayout, row, 0, 1, 1)

        ########################################################################

        row += 1

        self.xAxisLbl = QLabel("Titulo del Eje X: ")
        self.xAxisQle = QLineEdit(self)
        self.xAxisQle.setStyleSheet(QLE_NAME_STYLE)
        #self.xAxisQle.textChanged[str].connect(self.setYAxisTitleName)
        self.xAxisLayout = QHBoxLayout()
        self.xAxisLayout.addWidget(self.xAxisLbl)
        self.xAxisLayout.addWidget(self.xAxisQle, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.gridLayout.addLayout(self.xAxisLayout, row, 0, 1, 1)

        ########################################################################

        self.forceLogXCb = QCheckBox("Log Eje X")
        #self.forceLogXCb.stateChanged.connect(self.forceLogX)

        self.forceInvertXCb = QCheckBox("Invertir Eje X")
        #self.forceInvertXCb.stateChanged.connect(self.forceInvertX)
        
        self.xAxisCbLayout = QHBoxLayout()
        self.xAxisCbLayout.addWidget(self.forceInvertXCb)
        self.xAxisCbLayout.addWidget(self.forceLogXCb)

        self.gridLayout.addLayout(self.xAxisCbLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

        self.yAxisLbl = QLabel("Titulo del Eje Y: ")
        self.yAxisQle = QLineEdit(self)
        self.yAxisQle.setStyleSheet(QLE_NAME_STYLE)
        #self.yAxisQle.textChanged[str].connect(self.setYAxisTitleName)
        self.yAxisLayout = QHBoxLayout()
        self.yAxisLayout.addWidget(self.yAxisLbl)
        self.yAxisLayout.addWidget(self.yAxisQle, alignment=Qt.AlignmentFlag.AlignLeft)
        
        self.gridLayout.addLayout(self.yAxisLayout, row, 0, 1, 1)

        ########################################################################

        self.forceLogYCb = QCheckBox("Log Eje Y")
        #self.forceLogYCb.stateChanged.connect(self.forceLogY)

        self.forceInvertYCb = QCheckBox("Invertir Eje Y")
        #self.forceInvertYCb.stateChanged.connect(self.forceInvertY)
        
        self.yAxisCbLayout = QHBoxLayout()
        self.yAxisCbLayout.addWidget(self.forceInvertYCb)
        self.yAxisCbLayout.addWidget(self.forceLogYCb)

        self.gridLayout.addLayout(self.yAxisCbLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

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

        self.groupsLbl = QLabel("Cantidad de crossplots    ")
        self.groupsQle = QLineEdit(self)
        self.groupsQle.setStyleSheet(QLE_NAME_STYLE)
        self.groupsLayout = QHBoxLayout()
        self.groupsQle.textChanged[str].connect(self.enableGroupAmount)
        self.groupsQle.setPlaceholderText("1")
        self.groupsLayout.addWidget(self.groupsLbl)
        self.groupsLayout.addWidget(self.groupsQle, alignment=Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addLayout(self.groupsLayout, row, 0, 1, 1)

        ########################################################################

        row += 1
        groupAmount = 4

        self.groups = []
        for i in range(groupAmount):
            group = {
                "Enabled": i == 0,
                "Grid GroupBox": QGroupBox("Scatterplot " + str(i + 1)),
                "Scatter Title Label": QLabel("Nombre del Scatter"),
                "Scatter Title QLE": QLineEdit(self),
                "X Axis Label": QLabel("Eje X"),
                "X Axis CBO": QComboBox(self),
                "Y Axis Label": QLabel("Eje Y"),
                "Y Axis CBO": QComboBox(self),
                "Marker Label": QLabel("Simbolo"),
                "Marker CBO": marker_combo_box(),
                "Use Z Axis CB": QCheckBox("Usar Eje Z"),
                "Color Label": QLabel("Color"),
                "Color CBO": color_combo_box(),
                "Z Axis Label": QLabel("Eje Z"),
                "Z Axis CBO": QComboBox(self),
                "Force Depth Z axis CB": QCheckBox("Eje Z = Profundidad"),
                "Z Axis Colormap Label": QLabel("Colores Eje Z"),
                "Z Axis Colormap CBO": colormap_combo_box(),
                "Send To Front CB": QCheckBox("Enviar al Frente"),
                "Grid Layout": QGridLayout(self),
            }
            
            group["Marker CBO"].removeItem(0)
            group["Marker CBO"].setCurrentIndex(0)
            
            group["X Axis CBO"].setPlaceholderText('Elige Curva')
            group["Y Axis CBO"].setPlaceholderText('Elige Curva')
            group["Z Axis CBO"].setPlaceholderText('Elige Curva')

            group["Grid Layout"].addWidget(group["Scatter Title Label"], 1, 1)
            group["Grid Layout"].addWidget(group["Scatter Title QLE"], 1, 2)
            group["Grid Layout"].addWidget(group["X Axis Label"], 2, 1)
            group["Grid Layout"].addWidget(group["X Axis CBO"], 2, 2)
            group["Grid Layout"].addWidget(group["Y Axis Label"], 3, 1)
            group["Grid Layout"].addWidget(group["Y Axis CBO"], 3, 2)
            group["Grid Layout"].addWidget(group["Marker Label"], 4, 1)
            group["Grid Layout"].addWidget(group["Marker CBO"], 4, 2)
            group["Grid Layout"].addWidget(group["Color Label"], 5, 1)
            group["Grid Layout"].addWidget(group["Color CBO"], 5, 2)
            group["Grid Layout"].addWidget(group["Use Z Axis CB"], 6, 1)
            group["Grid Layout"].addWidget(group["Z Axis Label"], 7, 1)
            group["Grid Layout"].addWidget(group["Z Axis CBO"], 7, 2)
            group["Grid Layout"].addWidget(group["Force Depth Z axis CB"], 8, 1)
            group["Grid Layout"].addWidget(group["Z Axis Colormap Label"], 9, 1)
            group["Grid Layout"].addWidget(group["Z Axis Colormap CBO"], 9, 2)
            group["Grid Layout"].addWidget(group["Send To Front CB"], 10, 1)
            
            group["Use Z Axis CB"].stateChanged.connect(self.updateCheckBoxes)
            group["Force Depth Z axis CB"].stateChanged.connect(self.updateCheckBoxes)
            
            self.curve_selectors.append(group["X Axis CBO"])
            self.curve_selectors.append(group["Y Axis CBO"])
            self.curve_selectors.append(group["Z Axis CBO"])

            if i == 0:
                group["Scatter Title QLE"].setEnabled(True)
                group["X Axis CBO"].setEnabled(True)
                group["Y Axis CBO"].setEnabled(True)
                group["Marker CBO"].setEnabled(True)
                group["Use Z Axis CB"].setEnabled(True)
                group["Color Label"].setEnabled(not group["Use Z Axis CB"].isChecked())
                group["Color CBO"].setEnabled(not group["Use Z Axis CB"].isChecked())
                group["Z Axis Label"].setEnabled(group["Use Z Axis CB"].isChecked() and not group["Force Depth Z axis CB"].isChecked())
                group["Z Axis CBO"].setEnabled(group["Use Z Axis CB"].isChecked() and not group["Force Depth Z axis CB"].isChecked())
                group["Force Depth Z axis CB"].setEnabled(group["Use Z Axis CB"].isChecked())
                group["Z Axis Colormap Label"].setEnabled(group["Use Z Axis CB"].isChecked())
                group["Z Axis Colormap CBO"].setEnabled(group["Use Z Axis CB"].isChecked())
            else:
                group["Grid GroupBox"].setEnabled(False)

                group["Grid GroupBox"].setVisible(False)
            
            group["Grid GroupBox"].setLayout(group["Grid Layout"])

            #print("Se agrega layout en fila: ", row + int(i/2), " y columna: ", i % 2 )
            self.gridLayout.addWidget(group["Grid GroupBox"], row + int(i/2), i % 2)

            self.groups.append(group)

        ########################################################################

        row += int(groupAmount/2) + 1

        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2)

        row += 1

        self.previewBtn = QPushButton(CROSSPLOTS_CONSTANTS.PREVIEW_BUTTON)

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

        ########################################################################


    # method or slot for the toggled signal
    def on_selected(self):
        radio_button = self.sender()
        
        if radio_button.isChecked():
            print("You have selected : " + radio_button.text())
        #    self.label.setText("You have selected : " + radio_button.text())

        self.customMinDepthQle.setEnabled(self.depthCustomRb.isChecked())
        self.customMaxDepthQle.setEnabled(self.depthCustomRb.isChecked())

    def updateCheckBoxes(self, state):
        for group in self.groups:
            if group["Enabled"]:
                group["Color Label"].setEnabled(not group["Use Z Axis CB"].isChecked())
                group["Color CBO"].setEnabled(not group["Use Z Axis CB"].isChecked())
                group["Z Axis Label"].setEnabled(group["Use Z Axis CB"].isChecked() and not group["Force Depth Z axis CB"].isChecked())
                group["Z Axis CBO"].setEnabled(group["Use Z Axis CB"].isChecked() and not group["Force Depth Z axis CB"].isChecked())
                group["Force Depth Z axis CB"].setEnabled(group["Use Z Axis CB"].isChecked())
                group["Z Axis Colormap Label"].setEnabled(group["Use Z Axis CB"].isChecked())
                group["Z Axis Colormap CBO"].setEnabled(group["Use Z Axis CB"].isChecked())


    def enableGroupAmount(self, text):
        for group in self.groups[1::]:
            group["Enabled"] = False
            group["Grid GroupBox"].setEnabled(False)
            group["Grid GroupBox"].setVisible(False)
        
        if (is_positive_integer(text) and int(text) > 0):
            for i in range(1, min(len(self.groups), int(text))):
                self.groups[i]["Enabled"] = True
                self.groups[i]["Grid GroupBox"].setEnabled(True)
                self.groups[i]["Grid GroupBox"].setVisible(True)
                self.groups[i]["Scatter Title QLE"].setEnabled(True)
                self.groups[i]["X Axis CBO"].setEnabled(True)
                self.groups[i]["Y Axis CBO"].setEnabled(True)
                self.groups[i]["Marker CBO"].setEnabled(True)
                self.groups[i]["Use Z Axis CB"].setEnabled(True)
                self.groups[i]["Color Label"].setEnabled(not self.groups[i]["Use Z Axis CB"].isChecked())
                self.groups[i]["Color CBO"].setEnabled(not self.groups[i]["Use Z Axis CB"].isChecked())
                self.groups[i]["Z Axis Label"].setEnabled(self.groups[i]["Use Z Axis CB"].isChecked() and not self.groups[i]["Force Depth Z axis CB"].isChecked())
                self.groups[i]["Z Axis CBO"].setEnabled(self.groups[i]["Use Z Axis CB"].isChecked() and not self.groups[i]["Force Depth Z axis CB"].isChecked())
                self.groups[i]["Force Depth Z axis CB"].setEnabled(self.groups[i]["Use Z Axis CB"].isChecked())
                self.groups[i]["Z Axis Colormap Label"].setEnabled(self.groups[i]["Use Z Axis CB"].isChecked())
                self.groups[i]["Z Axis Colormap CBO"].setEnabled(self.groups[i]["Use Z Axis CB"].isChecked())


    def preview(self):
        if not super().preview():
            return

        self.init_window()

        depth_curve = self.well.wellModel.get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        config = {
            'title': self.titleQle.text(),
            'x_axis_title': self.xAxisQle.text(),
            'y_axis_title': self.yAxisQle.text(),
            'flex_size': 6,
            'invert_x': self.forceInvertXCb.isChecked(),
            'invert_y': self.forceInvertYCb.isChecked(),
            'log_x': self.forceLogXCb.isChecked(),
            'log_y': self.forceLogYCb.isChecked(),
            'scatter_groups': [],
            'line_groups': []
        }

        for group in self.groups:
            if group["Enabled"]:
                x_axis = self.well.wellModel.get_partial_ranged_df_curve(group["X Axis CBO"].currentText(), minDepth, maxDepth, "", "")
                if self.forceLogXCb.isChecked():
                    x_axis = np.log10(x_axis)
                y_axis = self.well.wellModel.get_partial_ranged_df_curve(group["Y Axis CBO"].currentText(), minDepth, maxDepth, "", "")
                if self.forceLogYCb.isChecked():
                    y_axis = np.log10(y_axis)

                x_axis, y_axis = set_nan_in_array_if_another_is_nan(x_axis, y_axis)        
                z_axis = x_axis
                if group["Use Z Axis CB"].isChecked():
                    if group["Force Depth Z axis CB"].isChecked():
                        z_axis = self.well.wellModel.get_partial_depth_curve(minDepth, maxDepth)
                    else:
                        z_axis = self.well.wellModel.get_partial_ranged_df_curve(group["Z Axis CBO"].currentText(), minDepth, maxDepth, "", "")

                    x_axis, z_axis = set_nan_in_array_if_another_is_nan(x_axis, z_axis)
                    y_axis, z_axis = set_nan_in_array_if_another_is_nan(y_axis, z_axis)

                scatter_config = {
                        'x_axis': x_axis,
                        'y_axis': y_axis,
                        'scatter_name': group["Scatter Title QLE"].text(),
                        'marker': group["Marker CBO"].currentText(),
                        'fixed_color': group["Color CBO"].currentText(),
                        'has_z_axis': group["Use Z Axis CB"].isChecked(),
                        'front': group["Send To Front CB"].isChecked(),
                }

                if scatter_config['has_z_axis']:
                    scatter_config['z_axis'] = z_axis
                    scatter_config['z_axis_colormap'] = group["Z Axis Colormap CBO"].currentText()
                    scatter_config['z_axis_title'] = "Profundidad" if group["Force Depth Z axis CB"].isChecked() else group["Z Axis CBO"].currentText()

                config['scatter_groups'].append(scatter_config)            

        front_groups = list(filter(lambda scatter_config: scatter_config["front"], config['scatter_groups']))
        back_groups = list(filter(lambda scatter_config: not scatter_config["front"], config['scatter_groups']))

        config['scatter_groups'] = back_groups + front_groups

        self.window \
            .add_color_crossplot(config)

        self.window.draw_tracks(config["title"])

    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return
