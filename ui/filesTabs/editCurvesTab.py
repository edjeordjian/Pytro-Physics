"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

    # Funcionalidades tentativas: 
    # - Agregar Curva Nueva (inicialmente llena de Nans o valor fijo)
    # - Combinar Curvas (opcion: borrando las iniciales)
    # - Borrar Curva
    # - Reemplazar Nulos por valor fijo (opcion unica curva o toda la tabla) -> Todo el LAS o rango custom de profundidad
    # - Reemplazar valor fijo por nulos (opcion unica curva o toda la tabla) -> Todo el LAS o rango custom de profundidad
    # - Sumar a toda la columna un offset (opcion unica curva o toda la tabla) -> Todo el LAS o rango custom de profundidad
    # - Multiplicar toda la columna por un valor (opcion unica curva o toda la tabla) -> Todo el LAS o rango custom de profundidad
    # - Dividir a toda la columna por un valor (opcion unica curva o toda la tabla) -> Todo el LAS o rango custom de profundidad
    # - Elevar a toda la columna por un valor (opcion unica curva o toda la tabla) -> Todo el LAS o rango custom de profundidad
    # - Aplicar Logaritmo a toda la columna (opcion unica curva o toda la tabla) -> Todo el LAS o rango custom de profundidad

from PyQt6.QtWidgets import (QLabel,
                             QHBoxLayout, QVBoxLayout, QGridLayout,
                             QRadioButton, QGroupBox,
                             QPushButton, QComboBox, QCheckBox, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

import numpy as np
from constants.messages_constants import MISSING_WELL
from constants.media_constants import APP_ICON_ROUTE
from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
from ui.popUps.alertWindow import AlertWindow
from ui.popUps.informationWindow import InformationWindow
from ui.style.button_styles import PREVIEW_BUTTON_STYLE, SAVE_BUTTON_STYLE, QLE_NAME_STYLE

from services.crossplot_service import getMN
from services.tools.string_service import is_number


class EditCurvesTab(QWidgetWithWell):
    def __init__(self):
        super().__init__("Editar Curvas")        
        self.savedCurveName = ""
        self.graphWindow = None

        self.initUI()

    def initUI(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.gridLayout)

        ########################################################################
        
        row = 0
        
        self.addCurveGroup = QGroupBox("Agregar Curva")
        self.addCurveLayout = QVBoxLayout()

        self.addCurveNameLbl = QLabel("Nombre Curva:")
        self.addCurveNameQle = QLineEdit(self)
        self.addCurveNameQle.setStyleSheet(QLE_NAME_STYLE)
        self.addCurveNameQle.setPlaceholderText("Ingrese nombre de la curva")
        self.addCurveNameLayout = QHBoxLayout()
        self.addCurveNameLayout.addWidget(self.addCurveNameLbl)
        self.addCurveNameLayout.addWidget(self.addCurveNameQle)

        self.addCurveDefaultValueLbl = QLabel("Valor (Numerico):")
        self.addCurveDefaultValueQle = QLineEdit(self)
        self.addCurveDefaultValueQle.setPlaceholderText("Ingrese valor de la curva")
        self.addCurveDefaultValueQle.setStyleSheet(QLE_NAME_STYLE)
        self.addCurveDefaultNanValueCb = QCheckBox("Llenar de Nulos")
        self.addCurveDefaultNanValueCb.stateChanged.connect(self.addCurveDefaultNan)
        self.addCurveValueLayout = QHBoxLayout()
        self.addCurveValueLayout.addWidget(self.addCurveDefaultValueLbl)
        self.addCurveValueLayout.addWidget(self.addCurveDefaultValueQle)
        self.addCurveValueLayout.addWidget(self.addCurveDefaultNanValueCb)

        self.addCurveBtn = QPushButton("Agregar Curva")
        self.addCurveBtn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.addCurveBtn.clicked.connect(
            lambda checked: self.addCurve()
        )

        self.addCurveLayout.addLayout(self.addCurveNameLayout)
        self.addCurveLayout.addLayout(self.addCurveValueLayout)
        self.addCurveLayout.addWidget(QLabel(""))
        self.addCurveLayout.addWidget(self.addCurveBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.addCurveGroup.setLayout(self.addCurveLayout)

        self.gridLayout.addWidget(self.addCurveGroup, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1
        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1

        self.deleteCurveGroup = QGroupBox("Borrar Curva")
        self.deleteCurveLayout = QVBoxLayout()

        self.deleteCurveLbl = QLabel("Nombre Curva:")
        self.deleteCurveCbo = QComboBox(self)
        self.deleteCurveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.deleteCurveCbo)
        self.confirmDeleteCurveCb = QCheckBox("Confirmar borrado manualmente")
        self.confirmDeleteCurveCb.setChecked(True)

        self.deleteCurveNameLayout = QHBoxLayout()
        self.deleteCurveNameLayout.addWidget(self.deleteCurveLbl)
        self.deleteCurveNameLayout.addWidget(self.deleteCurveCbo)
        self.deleteCurveNameLayout.addWidget(self.confirmDeleteCurveCb)

        self.deleteCurveBtn = QPushButton("Borrar Curva")
        self.deleteCurveBtn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.deleteCurveBtn.clicked.connect(
            lambda checked: self.deleteCurve()
        )        

        self.deleteCurveLayout.addLayout(self.deleteCurveNameLayout)
        self.deleteCurveLayout.addWidget(QLabel(""))
        self.deleteCurveLayout.addWidget(self.deleteCurveBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.deleteCurveGroup.setLayout(self.deleteCurveLayout)

        self.gridLayout.addWidget(self.deleteCurveGroup, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1
        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1

        self.combineCurvesGroup = QGroupBox("Combinar Curvas")
        self.combineCurvesLayout = QVBoxLayout()

        self.explanationLbl = QLabel("Para cada paso de profundidad toma el valor de curva 1, o en \ncaso de que este sea nulo toma el valor de curva 2")

        self.combineCurve1Lbl = QLabel("Nombre Curva 1:")
        self.combineCurve1Cbo = QComboBox(self)
        self.combineCurve1Cbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.combineCurve1Cbo)

        self.combineCurve1NameLayout = QHBoxLayout()
        self.combineCurve1NameLayout.addWidget(self.combineCurve1Lbl)
        self.combineCurve1NameLayout.addWidget(self.combineCurve1Cbo)

        self.combineCurve2Lbl = QLabel("Nombre Curva 2:")
        self.combineCurve2Cbo = QComboBox(self)
        self.combineCurve2Cbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.combineCurve2Cbo)

        self.combineCurve2NameLayout = QHBoxLayout()
        self.combineCurve2NameLayout.addWidget(self.combineCurve2Lbl)
        self.combineCurve2NameLayout.addWidget(self.combineCurve2Cbo)

        self.combineCurveNameLbl = QLabel("Nombre: ")
        self.combineCurveNameQle = QLineEdit(self)
        self.combineCurveNameQle.setStyleSheet(QLE_NAME_STYLE)
        self.combineCurveNameQle.setPlaceholderText("Ingrese nombre de la curva")
        self.combineCurveDeleteOriginalCurvesCb = QCheckBox("Borrar Curvas Originales")
        self.combineCurveNameLayout = QHBoxLayout()
        self.combineCurveNameLayout.addWidget(self.combineCurveNameLbl)
        self.combineCurveNameLayout.addWidget(self.combineCurveNameQle)
        self.combineCurveNameLayout.addWidget(self.combineCurveDeleteOriginalCurvesCb)

        self.combineCurvesBtn = QPushButton("Combinar Curvas")
        self.combineCurvesBtn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.combineCurvesBtn.clicked.connect(
            lambda checked: self.combineCurves()
        )        

        self.combineCurvesLayout.addWidget(self.explanationLbl)
        self.combineCurvesLayout.addLayout(self.combineCurve1NameLayout)
        self.combineCurvesLayout.addLayout(self.combineCurve2NameLayout)
        self.combineCurvesLayout.addLayout(self.combineCurveNameLayout)
        self.combineCurvesLayout.addWidget(QLabel(""))
        self.combineCurvesLayout.addWidget(self.combineCurvesBtn, alignment=Qt.AlignmentFlag.AlignCenter)
        self.combineCurvesGroup.setLayout(self.combineCurvesLayout)

        self.gridLayout.addWidget(self.combineCurvesGroup, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1
        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1

        self.replaceGroup = QGroupBox("Reemplazar Valores")
        self.replaceLayout = QVBoxLayout()

        self.replaceCurveLbl = QLabel("Nombre Curva:")
        self.replaceCurveCbo = QComboBox(self)
        self.replaceCurveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.replaceCurveCbo)
        self.replaceAllCurvesCb = QCheckBox("Reemplazar en todas las curvas")
        self.replaceAllCurvesCb.stateChanged.connect(self.replaceAllCurves)
        
        self.replaceCurveLayout = QHBoxLayout()
        self.replaceCurveLayout.addWidget(self.replaceCurveLbl)
        self.replaceCurveLayout.addWidget(self.replaceCurveCbo)
        self.replaceCurveLayout.addWidget(self.replaceAllCurvesCb)

        self.replaceValue1Lbl = QLabel("Valor 1 (Numerico):")
        self.replaceValue1Qle = QLineEdit(self)
        self.replaceValue1Qle.setStyleSheet(QLE_NAME_STYLE)
        self.replaceValue1Qle.setPlaceholderText("Ingrese valor a borrar")
        self.replaceValue1NanCb = QCheckBox("Nulos")
        self.replaceValue1NanCb.stateChanged.connect(self.replaceValue1Nan)
        self.replaceValue1Layout = QHBoxLayout()
        self.replaceValue1Layout.addWidget(self.replaceValue1Lbl)
        self.replaceValue1Layout.addWidget(self.replaceValue1Qle)
        self.replaceValue1Layout.addWidget(self.replaceValue1NanCb)

        self.replaceValue2Lbl = QLabel("Valor 2 (Numerico):")
        self.replaceValue2Qle = QLineEdit(self)
        self.replaceValue2Qle.setStyleSheet(QLE_NAME_STYLE)
        self.replaceValue2Qle.setPlaceholderText("Ingrese valor nuevo")
        self.replaceValue2NanCb = QCheckBox("Nulos")
        self.replaceValue2NanCb.stateChanged.connect(self.replaceValue2Nan)
        self.replaceValue2Layout = QHBoxLayout()
        self.replaceValue2Layout.addWidget(self.replaceValue2Lbl)
        self.replaceValue2Layout.addWidget(self.replaceValue2Qle)
        self.replaceValue2Layout.addWidget(self.replaceValue2NanCb)

        self.replaceValuesBtn = QPushButton("Reemplazar valor 1 por valor 2")
        self.replaceValuesBtn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.replaceValuesBtn.clicked.connect(
            lambda checked: self.replaceValues()
        ) 

        self.depthGrpBox = QGroupBox("Profundidad")
        self.depthLayout = QVBoxLayout()

        self.depthFullLasRb = QRadioButton("Todo el LAS")
        self.depthFullLasRb.setChecked(True)
        self.depthFullLasRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthFullLasRb)

        self.depthCustomRb = QRadioButton("personalizado")
        self.depthCustomRb.toggled.connect(self.on_selected)
        self.depthLayout.addWidget(self.depthCustomRb)

        self.depthGrpBox.setLayout(self.depthLayout)

        self.customMinDepthLbl = QLabel("Profundidad mín.: ")
        self.customMinDepthQle = QLineEdit(self)
        self.customMinDepthQle.setStyleSheet(QLE_NAME_STYLE)
        self.customMinDepthLayout = QHBoxLayout()
        self.customMinDepthLayout.addWidget(self.customMinDepthLbl)
        self.customMinDepthLayout.addWidget(self.customMinDepthQle)
        self.customMinDepthQle.setEnabled(False)

        self.customMaxDepthLbl = QLabel("Profundidad máx.:")
        self.customMaxDepthQle = QLineEdit(self)
        self.customMaxDepthQle.setStyleSheet(QLE_NAME_STYLE)
        self.customMaxDepthLayout = QHBoxLayout()
        self.customMaxDepthLayout.addWidget(self.customMaxDepthLbl)
        self.customMaxDepthLayout.addWidget(self.customMaxDepthQle)
        self.customMaxDepthQle.setEnabled(False)

        self.customDepthLayout = QVBoxLayout()
        self.customDepthLayout.addLayout(self.customMinDepthLayout)
        self.customDepthLayout.addLayout(self.customMaxDepthLayout)

        self.depthLayout = QHBoxLayout()
        self.depthLayout.addWidget(self.depthGrpBox)
        self.depthLayout.addLayout(self.customDepthLayout)

        self.replaceLayout.addLayout(self.replaceCurveLayout)
        self.replaceLayout.addLayout(self.replaceValue1Layout)
        self.replaceLayout.addLayout(self.replaceValue2Layout)
        self.replaceLayout.addLayout(self.depthLayout)
        self.replaceLayout.addWidget(QLabel(""))
        self.replaceLayout.addWidget(self.replaceValuesBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.replaceGroup.setLayout(self.replaceLayout)

        self.gridLayout.addWidget(self.replaceGroup, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
    
        ########################################################################

        row += 1
        self.gridLayout.addWidget(QLabel(""), row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)

        ########################################################################

        row += 1

        self.interpGroup = QGroupBox("Interpolar valores nulos")
        self.interpLayout = QVBoxLayout()

        self.interpCopyingRb = QRadioButton("Crear nueva curva interpolando nulos")
        self.interpCopyingRb.setChecked(True)
        self.interpCopyingRb.toggled.connect(self.on_selected_interp)
        self.interpLayout.addWidget(self.interpCopyingRb)

        self.interpReplacingOneRb = QRadioButton("Reemplazar curva original interpolando nulos")
        self.interpReplacingOneRb.setChecked(False)
        self.interpReplacingOneRb.toggled.connect(self.on_selected_interp)
        self.interpLayout.addWidget(self.interpReplacingOneRb)

        self.interpReplacingAllRb = QRadioButton("Reemplazar todas las curvas originales interpolando nulos")
        self.interpReplacingAllRb.setChecked(False)
        self.interpReplacingAllRb.toggled.connect(self.on_selected_interp)
        self.interpLayout.addWidget(self.interpReplacingAllRb)

        self.interpCurveLbl = QLabel("Curva original:")
        self.interpCurveCbo = QComboBox(self)
        self.interpCurveCbo.setPlaceholderText('Elige Curva')
        self.curve_selectors.append(self.interpCurveCbo)
        
        self.interpCurveLayout = QHBoxLayout()
        self.interpCurveLayout.addWidget(self.interpCurveLbl)
        self.interpCurveLayout.addWidget(self.interpCurveCbo)

        self.interpCurveNameLbl = QLabel("Nuevo nombre:")
        self.interpCurveNameQle = QLineEdit(self)
        self.interpCurveNameQle.setStyleSheet(QLE_NAME_STYLE)
        self.interpCurveNameQle.setPlaceholderText("Ingrese nombre de la curva")
        self.interpCurveNameLayout = QHBoxLayout()
        self.interpCurveNameLayout.addWidget(self.interpCurveNameLbl)
        self.interpCurveNameLayout.addWidget(self.interpCurveNameQle)

        self.interpValuesBtn = QPushButton("Interpolar valores nulos")
        self.interpValuesBtn.setStyleSheet(SAVE_BUTTON_STYLE)
        self.interpValuesBtn.clicked.connect(
            lambda checked: self.interpValues()
        ) 

        self.interpLayout.addLayout(self.interpCurveLayout)
        self.interpLayout.addLayout(self.interpCurveNameLayout)
        self.interpLayout.addWidget(QLabel(""))
        self.interpLayout.addWidget(self.interpValuesBtn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.interpGroup.setLayout(self.interpLayout)

        self.gridLayout.addWidget(self.interpGroup, row, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignLeft)
    
        ########################################################################


    # method or slot for the toggled signal
    def on_selected(self):
        radio_button = self.sender()
        
        if radio_button.isChecked():
            print("You have selected : " + radio_button.text())
        #    self.label.setText("You have selected : " + radio_button.text())

        self.customMinDepthQle.setEnabled(self.depthCustomRb.isChecked())
        self.customMaxDepthQle.setEnabled(self.depthCustomRb.isChecked())


    def on_selected_interp(self):
        self.interpCurveLbl.setEnabled(self.interpCopyingRb.isChecked() or self.interpReplacingOneRb.isChecked())
        self.interpCurveCbo.setEnabled(self.interpCopyingRb.isChecked() or self.interpReplacingOneRb.isChecked())
        self.interpCurveNameLbl.setEnabled(self.interpCopyingRb.isChecked())
        self.interpCurveNameQle.setEnabled(self.interpCopyingRb.isChecked())


    def setSavedCurveName(self, text):
        self.savedCurveName = text


    def addCurveDefaultNan(self, state):
        self.addCurveDefaultValueLbl.setEnabled(state == 0)
        self.addCurveDefaultValueQle.setEnabled(state == 0)


    def replaceAllCurves(self, state):
        self.replaceCurveLbl.setEnabled(state == 0)
        self.replaceCurveCbo.setEnabled(state == 0)


    def replaceValue1Nan(self, state):
        self.replaceValue1Lbl.setEnabled(state == 0)
        self.replaceValue1Qle.setEnabled(state == 0)


    def replaceValue2Nan(self, state):
        self.replaceValue2Lbl.setEnabled(state == 0)
        self.replaceValue2Qle.setEnabled(state == 0)


    def saveCurve(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(self.well.wellModel.get_depth_curve()))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(self.well.wellModel.get_depth_curve()))

        config_aux = getMN(self.well.wellModel.get_partial_ranged_df_curve(self.phiNCbo.currentText(), minDepth, maxDepth, "", ""),
                           self.well.wellModel.get_partial_ranged_df_curve(self.dTCbo.currentText(), minDepth, maxDepth, "", ""),
                           self.well.wellModel.get_partial_ranged_df_curve(self.rhoCbo.currentText(), minDepth, maxDepth, "", "")
                           )

        if self.saveAsMRb.isChecked():
            curve = config_aux["m"]
        else:
            curve = config_aux["n"]

        self.well.wellModel.append_curve(self.savedCurveName, curve)

        InformationWindow("Curva guardada")


    def addCurve(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return
        
        if str(self.addCurveNameQle.text()) == "":
            AlertWindow("El nombre de la curva no puede ser vacio")
            return

        if str(self.addCurveNameQle.text()).upper() in set(self.well.wellModel.get_curve_names()):
            AlertWindow("Ya existe una curva con ese nombre")
            return
        
        if not is_number(self.addCurveDefaultValueQle.text()) and not self.addCurveDefaultNanValueCb.isChecked():
            AlertWindow("El valor ingresado no es un numero valido (Se usa punto '.' como separador decimal)")
            return

        newCurve = list(np.zeros(len(self.well.wellModel.get_depth_curve())))
        if is_number(self.addCurveDefaultValueQle.text()) and not self.addCurveDefaultNanValueCb.isChecked():
            newCurve = list(map(lambda x: x + float(self.addCurveDefaultValueQle.text()), newCurve))
        else:
            newCurve = list(map(lambda x: x + np.nan, newCurve))

        self.well.wellModel.append_curve(str(self.addCurveNameQle.text()).upper(), newCurve)

        print("Curva " + str(self.addCurveNameQle.text()).upper() + " Guardada")
        InformationWindow("Curva " + str(self.addCurveNameQle.text()).upper() + " Guardada")
        self.addCurveNameQle.setText("")
        self.update_tab(self.well)


    def deleteCurve(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return
        
        if self.confirmDeleteCurveCb.isChecked():
            self.confirmMsg = QMessageBox()
            self.confirmMsg.setIcon(QMessageBox.Icon.Question)
            self.confirmMsg.setText("¿Estas seguro de borrar la curva: " + str(self.deleteCurveCbo.currentText()) + "?")
            self.confirmMsg.setWindowTitle("Confirmar borrado")
            self.confirmMsg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            buttonY = self.confirmMsg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('Si')
            buttonN = self.confirmMsg.button(QMessageBox.StandardButton.Cancel)
            buttonN.setText('Cancelar')
            self.confirmMsg.setWindowIcon(QIcon(APP_ICON_ROUTE))
            self.confirmMsg.exec()
            if self.confirmMsg.clickedButton() == buttonY:
                self._delete_curve_confirmed()
            else: 
                InformationWindow("No se borro la Curva " + str(self.deleteCurveCbo.currentText()))
        else:
            self._delete_curve_confirmed()

    def _delete_curve_confirmed(self):
        self.well.wellModel.delete_curve(self.deleteCurveCbo.currentText())
        print("Curva " + str(self.deleteCurveCbo.currentText()) + " Borrada")
        InformationWindow("Curva " + str(self.deleteCurveCbo.currentText()) + " Borrada")
        self.update_tab(self.well)


    def combineCurves(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return

        if str(self.combineCurveNameQle.text()) == "":
            AlertWindow("El nombre de la curva no puede ser vacio")
            return

        if str(self.combineCurveNameQle.text()).upper() in set(self.well.wellModel.get_curve_names()):
            AlertWindow("Ya existe una curva con ese nombre")
            return

        curve1 = self.well.wellModel.get_df_curve(self.combineCurve1Cbo.currentText())
        curve2 = self.well.wellModel.get_df_curve(self.combineCurve2Cbo.currentText())

        if self.combineCurveDeleteOriginalCurvesCb.isChecked():
            self.confirmMsg = QMessageBox()
            self.confirmMsg.setIcon(QMessageBox.Icon.Question)
            self.confirmMsg.setText("¿Estas seguro de borrar las curvas: " + str(self.combineCurve1Cbo.currentText()) + " y " + str(self.combineCurve2Cbo.currentText()) + "?")
            self.confirmMsg.setWindowTitle("Confirmar borrado")
            self.confirmMsg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel)
            buttonY = self.confirmMsg.button(QMessageBox.StandardButton.Yes)
            buttonY.setText('Si')
            buttonN = self.confirmMsg.button(QMessageBox.StandardButton.Cancel)
            buttonN.setText('Cancelar')
            self.confirmMsg.exec()
            if self.confirmMsg.clickedButton() == buttonY:
                self.well.wellModel.delete_curve(self.combineCurve1Cbo.currentText())
                if self.combineCurve1Cbo.currentText() != self.combineCurve2Cbo.currentText():
                    self.well.wellModel.delete_curve(self.combineCurve2Cbo.currentText())
            else: 
                InformationWindow("No se borraron las curvas: " + str(self.combineCurve1Cbo.currentText()) + " y " + str(self.combineCurve2Cbo.currentText()))
                return

        combinedCurve = self.well.wellModel.combine_curves(curve1, curve2)
        self.well.wellModel.append_curve(str(self.combineCurveNameQle.text()).upper(), combinedCurve)

        print("Curvas " + str(self.combineCurve1Cbo.currentText()) + " y " + str(self.combineCurve2Cbo.currentText()) +  " combinadas en " + str(self.combineCurveNameQle.text()).upper())
        InformationWindow("Curvas " + str(self.combineCurve1Cbo.currentText()) + " y " + str(self.combineCurve2Cbo.currentText()) +  " combinadas en " + str(self.combineCurveNameQle.text()).upper())
        self.combineCurveNameQle.setText("")
        self.update_tab(self.well)


    def replaceValues(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return

        if not is_number(self.replaceValue1Qle.text()) and not self.replaceValue1NanCb.isChecked():
            AlertWindow("El valor 1 no es un numero valido (Se usa punto '.' como separador decimal)")
            return
        
        if not is_number(self.replaceValue2Qle.text()) and not self.replaceValue2NanCb.isChecked():
            AlertWindow("El valor 2 no es un numero valido (Se usa punto '.' como separador decimal)")
            return

        oldValue = float(self.replaceValue1Qle.text()) if not self.replaceValue1NanCb.isChecked() else np.nan
        newValue = float(self.replaceValue2Qle.text()) if not self.replaceValue2NanCb.isChecked() else np.nan

        minDepth = self.customMinDepthQle.text() if self.customMinDepthQle.isEnabled() else str(min(self.well.wellModel.get_depth_curve()))
        maxDepth = self.customMaxDepthQle.text() if self.customMaxDepthQle.isEnabled() else str(max(self.well.wellModel.get_depth_curve()))

        curveNames = [self.replaceCurveCbo.currentText()]
        if self.replaceAllCurvesCb.isChecked():
            curveNames = self.well.wellModel.get_curve_names()
        
        for curveName in curveNames:
            self.well.wellModel.replace_curve_values(curveName, oldValue, newValue, minDepth, maxDepth)

        print("Valores reemplazados")
        InformationWindow("Valores reemplazados")


    def interpValues(self):
        if not self.well:
            AlertWindow(MISSING_WELL)
            return

        if self.interpCopyingRb.isChecked():
            if str(self.interpCurveNameQle.text()) == "":
                AlertWindow("El nombre de la curva no puede ser vacio")
                return
            if str(self.interpCurveNameQle.text()).upper() in set(self.well.wellModel.get_curve_names()):
                AlertWindow("Ya existe una curva con ese nombre")
                return

            self.well.wellModel.interp_curve_nans(self.interpCurveCbo.currentText(), str(self.interpCurveNameQle.text()).upper())

        else:
            curveNames = [self.interpCurveCbo.currentText()]
            if self.interpReplacingOneRb.isChecked():
                curveNames = self.well.wellModel.get_curve_names()
            for curveName in curveNames:
                self.well.wellModel.interp_curve_nans_replacing(curveName)

        print("Valores interpolados")
        InformationWindow("Valores interpolados")


    def update_tab(self, well):
        if not super().update_tab(well):
            return

        self.deleteCurveCbo.setCurrentIndex(0)
        self.combineCurve1Cbo.setCurrentIndex(0)
        self.combineCurve2Cbo.setCurrentIndex(0)
        self.replaceCurveCbo.setCurrentIndex(0)
        self.interpCurveCbo.setCurrentIndex(0)
