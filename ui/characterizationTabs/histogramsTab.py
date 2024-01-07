"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox, QSlider, QPushButton,
                             QComboBox, QCheckBox, QLineEdit)

from PyQt6.QtCore import Qt

import numpy as np

import constants.CROSSPLOTS_CONSTANTS as CROSSPLOTS_CONSTANTS

from constants.messages_constants import MISSING_WELL

from constants.pytrophysicsConstants import SEE_WINDOW_LBL
from constants.tab_constants import HISTOGRAM_TAB_NAME

from ui.characterizationTabs.QWidgetStandAlone import QWidgetStandAlone

from ui.popUps.alertWindow import AlertWindow

from ui.style.StyleCombos import color_combo_box

from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE

from services.tools.string_service import is_number, is_positive_integer

from services.histogram_service import (normal_mean, normal_sigma, log_normal_mean, log_normal_sigma,
                                        triangular_min, triangular_mode, triangular_max, 
                                        exponential_beta, uniform_min, uniform_max)


class HistogramsTab(QWidgetStandAlone):
    def __init__(self):
        super().__init__("Histogramas")

        self.distributions = {
            "Ninguna": {
                "params": [],
                "function": None
            },
            "Normal": {
                "params": ["Media", "Sigma"],
                "param_functions": [normal_mean, normal_sigma],
                "function": np.random.normal
            },
            "Log Normal": {
                "params": ["Media", "Sigma"],
                "param_functions": [log_normal_mean, log_normal_sigma],
                "function": np.random.lognormal
            },
            "Triangular": {
                "params": ["Limite inferior", "Moda", "Limite superior"],
                "param_functions": [triangular_min, triangular_mode, triangular_max],
                "function": np.random.triangular
            },
            "Exponencial": {
                "params": ["Beta (1/Lambda)"],
                "param_functions": [exponential_beta],
                "function": np.random.exponential
            },
            "Uniforme": {
                "params": ["Limite inferior", "Limite superior"],
                "param_functions": [uniform_min, uniform_max],
                "function": np.random.uniform
            }
        }

        """
            "Weibull": {
                "params": ["Alpha"],
                "function": np.random.weibull
            },
            "Rayleigh": {
                "params": ["Chi"],
                "function": np.random.rayleigh
            },
            "Pareto": {
                "params": ["Alpha"],
                "function": np.random.pareto
            },
            "Chi cuadrado": {
                "params": ["Grados de Libertad"],
                "function": np.random.chisquare
            },
            "Beta": {
                "params": ["Alpha", "Beta"],
                "function": np.random.beta
            },
        """

        self.initUI()

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.forceInvertXCb, self.forceLogXCb,
             self.xAxisQle, self.titleQle, self.forceInvertYCb, self.yAxisQle,
             self.groupsQle, self.groups, self.bucketsQle])

    def initUI(self):
        self.setLayout(self.gridLayout)

        row = 0

        self.titleLbl = QLabel("Titulo del Histograma: ")
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

        #self.forceLogYCb = QCheckBox("Log Eje Y")
        #self.forceLogYCb.stateChanged.connect(self.forceLogY)

        self.forceInvertYCb = QCheckBox("Invertir Eje Y")
        #self.forceInvertYCb.stateChanged.connect(self.forceInvertY)
        
        self.yAxisCbLayout = QHBoxLayout()
        self.yAxisCbLayout.addWidget(self.forceInvertYCb)
        #self.yAxisCbLayout.addWidget(self.forceLogYCb)

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
        self.customMinDepthQle.textChanged[str].connect(self.selectDistributionGroups)

        self.customMaxDepthLbl = QLabel("Profundidad máx.:")
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle)
        self.customMaxDepthQle.setEnabled(False)
        self.customMaxDepthQle.textChanged[str].connect(self.selectDistributionGroups)

        self.customDepthLayout = QVBoxLayout()
        self.customDepthLayout.addLayout(self.customMinDepthLayout)
        self.customDepthLayout.addLayout(self.customMaxDepthLayout)
        self.gridLayout.addLayout(self.customDepthLayout, row, 1, 1, 1)

        ########################################################################

        row += 1

        self.bucketsLbl = QLabel("Cantidad de Buckets")
        self.bucketsQle = QLineEdit(self)
        self.bucketsQle.setStyleSheet(QLE_NAME_STYLE)
        self.bucketsLayout = QHBoxLayout()
        self.bucketsQle.setPlaceholderText("40")
        self.bucketsLayout.addWidget(self.bucketsLbl)
        self.bucketsLayout.addWidget(self.bucketsQle, alignment=Qt.AlignmentFlag.AlignLeft)
        self.gridLayout.addLayout(self.bucketsLayout, row, 0, 1, 1)

        ########################################################################

        row += 1

        self.groupsLbl = QLabel("Cantidad de Histogramas")
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
                "Grid GroupBox": QGroupBox("Histograma " + str(i + 1)),
                "Histogram Title Label": QLabel("Nombre del Histograma"),
                "Histogram Title QLE": QLineEdit(self),
                "X Axis Label": QLabel("Eje X"),
                "X Axis CBO": QComboBox(self),
                "Color Label": QLabel("Color"),
                "Color CBO": color_combo_box(),
                "Alpha Label": QLabel("Opacidad"),
                "Alpha Slider": QSlider(Qt.Orientation.Horizontal, self),
                "Accum Curve CB": QCheckBox("Mostrar Curva Acumulada"),
                "Accum Curve Slider": QSlider(Qt.Orientation.Horizontal, self),
                "Send To Front CB": QCheckBox("Enviar al Frente"),
                "Distribution Type Label": QLabel("Agregar Distribucion"),
                "Distribution Type CBO": QComboBox(self),
                "Distribution Param 1 Label": QLabel("-"),
                "Distribution Param 1 QLE": QLineEdit(self),
                "Distribution Param 2 Label": QLabel("-"),
                "Distribution Param 2 QLE": QLineEdit(self),
                "Distribution Param 3 Label": QLabel("-"),
                "Distribution Param 3 QLE": QLineEdit(self),
                "Distribution Color Label": QLabel("Color"),
                "Distribution Color CBO": color_combo_box(),
                "Distribution Alpha Label": QLabel("Opacidad"),
                "Distribution Alpha Slider": QSlider(Qt.Orientation.Horizontal, self),
                "Distribution Accum Curve CB": QCheckBox("Mostrar Curva Acumulada"),
                "Distribution Accum Curve Slider": QSlider(Qt.Orientation.Horizontal, self),
                "Distribution Send To Front CB": QCheckBox("Enviar distribucion al Frente"),
                "Grid Layout": QGridLayout(self)
            }

            group["X Axis CBO"].setPlaceholderText('Elige Curva')
            
            # Slider Values = [0, ..., 99]
            group["Alpha Slider"].setValue(99)
            group["Accum Curve Slider"].setValue(99)

            group["Accum Curve CB"].stateChanged.connect(self.updateCheckBoxes)
            group["Accum Curve Slider"].setEnabled(False)

            group["Distribution Type CBO"].textActivated[str].connect(self.selectDistributionGroups)
            for key in self.distributions.keys():
                group["Distribution Type CBO"].addItem(key)
            group["Distribution Type CBO"].setCurrentIndex(0)
            group["Distribution Param 1 Label"].setEnabled(False)
            group["Distribution Param 1 QLE"].setEnabled(False)
            group["Distribution Param 2 Label"].setEnabled(False)
            group["Distribution Param 2 QLE"].setEnabled(False)
            group["Distribution Param 3 Label"].setEnabled(False)
            group["Distribution Param 3 QLE"].setEnabled(False)
            group["Distribution Color Label"].setEnabled(False)
            group["Distribution Color CBO"].setEnabled(False)
            group["Distribution Alpha Label"].setEnabled(False)
            group["Distribution Alpha Slider"].setEnabled(False)
            group["Distribution Accum Curve CB"].setEnabled(False)
            group["Distribution Accum Curve Slider"].setEnabled(False)
            group["Distribution Send To Front CB"].setEnabled(False)
            
            group["Distribution Accum Curve CB"].stateChanged.connect(self.updateCheckBoxes)
            
            group["Distribution Alpha Slider"].setValue(99)
            group["Distribution Accum Curve Slider"].setValue(99)

            group["Grid Layout"].addWidget(group["Histogram Title Label"], 1, 1)
            group["Grid Layout"].addWidget(group["Histogram Title QLE"], 1, 2)
            group["Grid Layout"].addWidget(group["X Axis Label"], 2, 1)
            group["Grid Layout"].addWidget(group["X Axis CBO"], 2, 2)
            group["Grid Layout"].addWidget(group["Color Label"], 3, 1)
            group["Grid Layout"].addWidget(group["Color CBO"], 3, 2)
            group["Grid Layout"].addWidget(group["Alpha Label"], 4, 1)
            group["Grid Layout"].addWidget(group["Alpha Slider"], 4, 2)
            group["Grid Layout"].addWidget(group["Accum Curve CB"], 5, 1)
            group["Grid Layout"].addWidget(group["Accum Curve Slider"], 5, 2)
            group["Grid Layout"].addWidget(group["Send To Front CB"], 6, 1)
            group["Grid Layout"].addWidget(group["Distribution Type Label"], 7, 1)
            group["Grid Layout"].addWidget(group["Distribution Type CBO"], 7, 2)
            group["Grid Layout"].addWidget(group["Distribution Param 1 Label"], 8, 1)
            group["Grid Layout"].addWidget(group["Distribution Param 1 QLE"], 8, 2)
            group["Grid Layout"].addWidget(group["Distribution Param 2 Label"], 9, 1)
            group["Grid Layout"].addWidget(group["Distribution Param 2 QLE"], 9, 2)
            group["Grid Layout"].addWidget(group["Distribution Param 3 Label"], 10, 1)
            group["Grid Layout"].addWidget(group["Distribution Param 3 QLE"], 10, 2)
            group["Grid Layout"].addWidget(group["Distribution Color Label"], 11, 1)
            group["Grid Layout"].addWidget(group["Distribution Color CBO"], 11, 2)
            group["Grid Layout"].addWidget(group["Distribution Alpha Label"], 12, 1)
            group["Grid Layout"].addWidget(group["Distribution Alpha Slider"], 12, 2)
            group["Grid Layout"].addWidget(group["Distribution Accum Curve CB"], 13, 1)
            group["Grid Layout"].addWidget(group["Distribution Accum Curve Slider"], 13, 2)
            group["Grid Layout"].addWidget(group["Distribution Send To Front CB"], 14, 1)
            
            self.curve_selectors.append(group["X Axis CBO"])

            if i > 0:
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


    def selectDistributionGroups(self, dist):
        depth_curve = self.well \
            .wellModel \
            .get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        for group in self.groups:
            if group["Enabled"]:
                group["Distribution Color Label"].setEnabled(len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0)
                group["Distribution Color CBO"].setEnabled(len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0)
                group["Distribution Alpha Label"].setEnabled(len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0)
                group["Distribution Alpha Slider"].setEnabled(len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0)
                group["Distribution Send To Front CB"].setEnabled(len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0)
                group["Distribution Accum Curve CB"].setEnabled(len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0)
                group["Distribution Accum Curve Slider"].setEnabled((len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0) and
                                                                     group["Distribution Accum Curve CB"].isChecked())
                
                group["Distribution Param 1 Label"].setEnabled(False)
                group["Distribution Param 1 Label"].setText("-")
                group["Distribution Param 1 QLE"].setEnabled(False)
                group["Distribution Param 1 QLE"].setPlaceholderText("")
                group["Distribution Param 2 Label"].setEnabled(False)
                group["Distribution Param 2 Label"].setText("-")
                group["Distribution Param 2 QLE"].setEnabled(False)
                group["Distribution Param 2 QLE"].setPlaceholderText("")
                group["Distribution Param 3 Label"].setEnabled(False)
                group["Distribution Param 3 Label"].setText("-")
                group["Distribution Param 3 QLE"].setEnabled(False)
                group["Distribution Param 3 QLE"].setPlaceholderText("")

                if group["X Axis CBO"].count() > 0:
                    x_axis = self.well.wellModel.get_partial_ranged_df_curve(group["X Axis CBO"].currentText(), minDepth, maxDepth, "", "")

                    for i in range(len(self.distributions[group["Distribution Type CBO"].currentText()]["params"])):
                        group[f"Distribution Param {i+1} Label"].setEnabled(True)
                        group[f"Distribution Param {i+1} Label"].setText(self.distributions[group["Distribution Type CBO"].currentText()]["params"][i])
                        group[f"Distribution Param {i+1} QLE"].setEnabled(True)
                        param_value = self.distributions[group["Distribution Type CBO"].currentText()]["param_functions"][i](x_axis)
                        group[f"Distribution Param {i+1} QLE"].setPlaceholderText("" if param_value is None else str(param_value))


    # method or slot for the toggled signal
    def on_selected(self):
        radio_button = self.sender()
        
        if radio_button.isChecked():
            print("You have selected : " + radio_button.text())
        #    self.label.setText("You have selected : " + radio_button.text())

        self.customMinDepthQle.setEnabled(self.depthCustomRb.isChecked())
        self.customMaxDepthQle.setEnabled(self.depthCustomRb.isChecked())
        self.selectDistributionGroups(None)


    def updateCheckBoxes(self):
        for group in self.groups:
            if group["Enabled"]:
                group["Accum Curve Slider"].setEnabled(group["Accum Curve CB"].isChecked())
                group["Distribution Accum Curve Slider"].setEnabled((len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0) and
                                                                     group["Distribution Accum Curve CB"].isChecked())


    def enableGroupAmount(self, text):
        for i in range(1, len(self.groups)):
            self.groups[i]["Enabled"] = False

            self.groups[i]["Grid GroupBox"].setEnabled(False)

            self.groups[i]["Grid GroupBox"].setVisible(False)
        
        if (is_positive_integer(text) and int(text) > 0):
            for i in range(min(len(self.groups), int(text))):
                self.groups[i]["Enabled"] = True

                self.groups[i]["Grid GroupBox"].setEnabled(True)

                self.groups[i]["Grid GroupBox"].setVisible(True)

    def _obtainGroupsConfig(self, config, minDepth, maxDepth):
        front_groups = list(filter(lambda group: group["Send To Front CB"].isChecked(), self.groups))
        back_groups = list(filter(lambda group: not group["Send To Front CB"].isChecked(), self.groups))

        for group in (back_groups + front_groups):
            if group["Enabled"]:
                x_axis = self.well.wellModel.get_partial_ranged_df_curve(group["X Axis CBO"].currentText(), minDepth, maxDepth, "", "")
                if len(x_axis[~np.isnan(x_axis)]) != 0:
                    histogram_config = {
                        'values': x_axis,
                        'histogram_name': group["Histogram Title QLE"].text(),
                        'color': group["Color CBO"].currentText(),
                        'alpha': group["Alpha Slider"].value() * (255/99),
                        'show_accum': group["Accum Curve CB"].isChecked(),
                        'alpha_accum': group["Accum Curve Slider"].value() * (255/100),
                        'front': group["Send To Front CB"].isChecked()
                    }

                    config['histogram_groups'].append(histogram_config)   
        return config 


    def _auxObtainDistConfig(self, group):
        histogram_config = None

        qle = QLineEdit()

        qle.placeholderText()

        np.random.seed(0)

        try:
            if len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) > 0:
                #size = len(self.well.wellModel.get_partial_depth_curve(minDepth, maxDepth))
                size = 500000
                if group["Distribution Param 1 QLE"].text() == "":
                    first_param = float(group["Distribution Param 1 QLE"].placeholderText())
                else:
                    first_param = float(group["Distribution Param 1 QLE"].text())
                if len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) == 1:
                    x_axis = self.distributions[group["Distribution Type CBO"].currentText()]["function"](first_param, size)
                elif len(self.distributions[group["Distribution Type CBO"].currentText()]["params"]) == 2:
                    if group["Distribution Param 2 QLE"].text() == "":
                        second_param = float(group["Distribution Param 2 QLE"].placeholderText())
                    else:
                        second_param = float(group["Distribution Param 2 QLE"].text())
                    x_axis = self.distributions[group["Distribution Type CBO"].currentText()]["function"](first_param, second_param, size)
                else:
                    if group["Distribution Param 2 QLE"].text() == "":
                        second_param = float(group["Distribution Param 2 QLE"].placeholderText())
                    else:
                        second_param = float(group["Distribution Param 2 QLE"].text())
                    if group["Distribution Param 3 QLE"].text() == "":
                        third_param = float(group["Distribution Param 3 QLE"].placeholderText())
                    else:
                        third_param = float(group["Distribution Param 3 QLE"].text())
                    x_axis = self.distributions[group["Distribution Type CBO"].currentText()]["function"](first_param, second_param, third_param, size)
                
                if self.forceLogXCb.isChecked():
                    x_axis = np.log10(x_axis)

                hist_name = group["Grid GroupBox"].title()

                histogram_config = {
                    'values': x_axis,
                    'histogram_name': group["Distribution Type CBO"].currentText() + f"({hist_name})",
                    'color': group["Distribution Color CBO"].currentText(),
                    'alpha': group["Distribution Alpha Slider"].value() * (255/99),
                    'show_accum': group["Distribution Accum Curve CB"].isChecked(),
                    'alpha_accum': group["Distribution Accum Curve Slider"].value() * (255/100),
                    'front': group["Distribution Send To Front CB"].isChecked()
                }

        except ValueError:
            AlertWindow("Parametro invalido ingresado para la distribucion elegida")

        np.random.seed()

        return histogram_config

    def _obtainDistConfig(self, config):

        front_groups = list(filter(lambda group: group["Distribution Send To Front CB"].isChecked(), self.groups))
        back_groups = list(filter(lambda group: not group["Distribution Send To Front CB"].isChecked(), self.groups))

        for group in (back_groups + front_groups):
            if group["Enabled"]:
                histogram_config = self._auxObtainDistConfig(group)
                if histogram_config is not None:
                    config['histogram_groups'].append(histogram_config)   
        
        return config


    def preview(self):
        if not super().preview():
            return

        depth_curve = self.well \
            .wellModel \
            .get_depth_curve()

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(depth_curve))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(depth_curve))

        config = {
            'title': self.titleQle.text(),
            'tab_name': HISTOGRAM_TAB_NAME,
            'x_axis_title': self.xAxisQle.text(),
            'y_axis_title': self.yAxisQle.text(),
            'flex_size': 6,
            'invert_x': self.forceInvertXCb.isChecked(),
            'invert_y': self.forceInvertYCb.isChecked(),
            'log_x': self.forceLogXCb.isChecked(),
            'buckets': self.bucketsQle.text(),
            'histogram_groups': [],
            'ephimeral': True
        }

        config = self._obtainGroupsConfig(config, minDepth, maxDepth)
        config = self._obtainDistConfig(config)

        front_groups = list(filter(lambda hist_config: hist_config["front"], config['histogram_groups']))
        back_groups = list(filter(lambda hist_config: not hist_config["front"], config['histogram_groups']))

        config['histogram_groups'] = back_groups + front_groups

        if len(config["histogram_groups"]) == 0:
            AlertWindow("No se ha ingresado ningún histograma")
            return

        self.window.add_histogram(config)

        self.window.draw_tracks(HISTOGRAM_TAB_NAME)

    def update_tab(self, well=None, force_update=False):
        if not super().update_tab(well, force_update=force_update):
            return
