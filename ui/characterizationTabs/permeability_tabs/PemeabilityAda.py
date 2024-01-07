"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (QLineEdit, QComboBox, QLabel, QHBoxLayout,
                             QCheckBox, QRadioButton)

from constants import permeability_constants

from constants.general_constants import DEFAULT_SCATTERPLOT_CONFIG

from constants.permeability_constants import (K_CORE_CURVE_LABEL, FEATURES_LABEL, PERMEABILITY_ADA_TAB_NAME,
                                              ADA_SCATTER_NAME, ADA_TRACK_NAME, EMPTY_TRAIN_ERROR, KKCORE_LBL,
                                              ADA_N_ESTIMATORS_DEFAULT, ADA_LEARNING_RATE_DEFAULT,
                                              USE_DEFAULT_HYPERPARAMETRS, PICK_HYPERPARAMETERS_LBL,
                                              SEARCH_HYPERPARAMETERS_LBL, K_LBL, K_CORE_LBL, MD_LBL)
from constants.tab_constants import EVERY_TAB

from services.permeability_service import ada_bossting_permeability, get_train_x_y_test

from services.tools.string_service import is_positive_integer, is_number_between
from ui.GraphicWindow import GraphicWindow

from ui.characterizationTabs.QWidgetWithSections import QWidgetWithSections

from ui.popUps.alertWindow import AlertWindow

from ui.popUps.loading_handler import loading_pop_up

from ui.visual_components.MultiComboBox import MultiComboBox

from numpy import log10

from ui.visual_components.combo_handler import if_checked_enable_combo, disable_elements_with_component, \
    update_curve_list_multi_cbo, update_curve_list


class PermeabilityAda(QWidgetWithSections):
    def __init__(self):
        super().__init__(permeability_constants.PERMEABILITY_ADA_TAB_NAME)

        self.init_ui(permeability_constants.PERMEABILITY_ADA_TAB_NAME)

    def init_ui(self,
                name):
        self.hyperparameter_definition_section()

        self.features_section()

        self.hyperparameters_section()

        super().init_ui(name)

        self.scatter_window = None

        self.numeric_inputs.extend([self.n_estimators_textbox, self.learning_rate_textbox])

        self.add_serializable_attributes(self.curve_selectors + [self.depthFullLasRb, self.depthCustomRb,
             self.customMinDepthQle, self.customMaxDepthQle, self.curve_to_save_marker, self.curve_to_save_line,
             self.curve_to_save_color, self.kkcore_checkbox, self.log_checkbox, self.n_estimators_textbox,
             self.loss_cbo, self.learning_rate_textbox, self.use_default_hyperparameters_rb,
             self.pick_hyperparameters_rb, self.search_hyperparameters_rb, self.feature_selector])

    def hyperparameter_definition_section(self):
        self.n_estimators_lbl = QLabel("Estimadores:")

        self.n_estimators_textbox = QLineEdit(ADA_N_ESTIMATORS_DEFAULT)

        self.learning_rate_lbl = QLabel("Learning rate:")

        self.learning_rate_textbox = QLineEdit(ADA_LEARNING_RATE_DEFAULT)

        self.loss_lbl = QLabel("Función de loss:")

        self.loss_cbo = QComboBox()

        self.loss_cbo.addItem('Lineal',
                              'linear')

        self.loss_cbo.addItem('Cuadrático',
                              'square')

        self.loss_cbo.addItem('Exponencial',
                              'exponencial')

        self.hyperparameter_componentes = [self.n_estimators_lbl, self.n_estimators_textbox,
           self.learning_rate_lbl, self.learning_rate_textbox, self.loss_lbl,
           self.loss_cbo]

    def set_hyperparameters_fields(self):
        if self.n_estimators_textbox.text() != ADA_N_ESTIMATORS_DEFAULT:
            self.n_estimators_previous_value = self.n_estimators_textbox.text()

        if self.learning_rate_textbox.text() != ADA_LEARNING_RATE_DEFAULT:
            self.learning_rate_previos_value = self.learning_rate_textbox.text()

        if self.loss_cbo.currentIndex() != 0:
            self.loss_previous_index = self.loss_cbo.currentIndex()

        if self.use_default_hyperparameters_rb.isChecked():
            self.n_estimators_textbox.setText(ADA_N_ESTIMATORS_DEFAULT)

            self.learning_rate_textbox.setText(ADA_LEARNING_RATE_DEFAULT)

            self.loss_cbo.setCurrentIndex(0)

        else:
            self.n_estimators_textbox.setText(self.n_estimators_previous_value)

            self.learning_rate_textbox.setText(self.learning_rate_previos_value)

            self.loss_cbo.setCurrentIndex(self.loss_previous_index)

        if self.pick_hyperparameters_rb.isChecked():
            for element in self.hyperparameter_componentes:
                element.setEnabled(True)

        else:
            for element in self.hyperparameter_componentes:
                element.setEnabled(False)


    def features_section(self):
        self.kcore_lbl = QLabel(K_CORE_CURVE_LABEL)

        self.add_widget_to_layout(self.kcore_lbl)

        self.kcore_cbo = QComboBox()

        self.add_widget_to_layout(self.kcore_cbo)

        self.add_blank_line()

        self.features_lbl = QLabel(FEATURES_LABEL)

        self.add_widget_to_layout(self.features_lbl)

        self.feature_selector = MultiComboBox()

        self.curve_selectors \
            .extend([self.kcore_cbo])

        self.add_widget_to_layout(self.feature_selector)

        self.add_blank_line()

        self.n_estimators_previous_value = ADA_N_ESTIMATORS_DEFAULT

        self.learning_rate_previos_value = ADA_LEARNING_RATE_DEFAULT

        self.loss_previous_index = 0

        self.use_default_hyperparameters_lbl = QLabel(USE_DEFAULT_HYPERPARAMETRS)

        self.use_default_hyperparameters_rb = QRadioButton()

        self.pick_hyperparameters_lbl = QLabel(PICK_HYPERPARAMETERS_LBL)

        self.pick_hyperparameters_rb = QRadioButton()

        self.search_hyperparameters_lbl = QLabel(SEARCH_HYPERPARAMETERS_LBL)

        self.search_hyperparameters_rb = QRadioButton()

        self.pick_hyperparameters_rb.toggled \
            .connect(self.set_hyperparameters_fields)

        self.use_default_hyperparameters_rb.toggled \
            .connect(self.set_hyperparameters_fields)

        self.search_hyperparameters_rb.toggled \
            .connect(self.set_hyperparameters_fields)

        self.use_default_hyperparameters_rb.setChecked(True)

        self.n_estimators_textbox.setText(self.n_estimators_previous_value)

        self.learning_rate_textbox.setText(self.learning_rate_previos_value)

        self.loss_cbo.setCurrentIndex( self.loss_previous_index)

        self.default_hyperparameters_layout = QHBoxLayout()

        self.use_default_hyperparameters_layout = QHBoxLayout()

        self.use_default_hyperparameters_layout.addWidget(self.use_default_hyperparameters_lbl)

        self.use_default_hyperparameters_layout.addWidget(self.use_default_hyperparameters_rb)

        self.pick_hyperparameters_layout = QHBoxLayout()

        self.pick_hyperparameters_layout.addWidget(self.pick_hyperparameters_lbl)

        self.pick_hyperparameters_layout.addWidget(self.pick_hyperparameters_rb)

        self.search_hyperparameters_layout = QHBoxLayout()

        self.search_hyperparameters_layout.addWidget(self.search_hyperparameters_lbl)

        self.search_hyperparameters_layout.addWidget(self.search_hyperparameters_rb)

        self.add_layout_to_layout(self.use_default_hyperparameters_layout)

        self.add_layout_to_layout(self.pick_hyperparameters_layout)

        self.add_layout_to_layout(self.search_hyperparameters_layout)

        self.add_blank_line()

    def hyperparameters_section(self):
        self.hyperparameters_1_labels = QHBoxLayout()

        self.add_widget_to_layout(self.n_estimators_lbl,
                                  next_line=False,
                                  column=0)

        self.add_widget_to_layout(self.learning_rate_lbl,
                                  next_line=False,
                                  column=1)

        self.add_widget_to_layout(self.loss_lbl,
                                  column=2)

        self.add_widget_to_layout(self.n_estimators_textbox,
                                  next_line=False,
                                  alignment=Qt.AlignmentFlag.AlignLeft,
                                  column=0)

        self.add_widget_to_layout(self.learning_rate_textbox,
                                  next_line=False,
                                  alignment=Qt.AlignmentFlag.AlignLeft,
                                  column=1)

        self.add_widget_to_layout(self.loss_cbo,
                                  column=2)

        self.add_blank_line()

        self.kkcore_label = QLabel(KKCORE_LBL)

        self.kkcore_layout = QHBoxLayout()

        self.kkcore_checkbox = QCheckBox()

        self.kkcore_layout.addWidget(self.kkcore_label)

        self.kkcore_layout.addWidget(self.kkcore_checkbox)

        self.add_layout_to_layout(self.kkcore_layout)

        self.kkcore_cbo = QComboBox()

        self.kkcore_checkbox \
            .stateChanged \
            .connect(lambda: if_checked_enable_combo(self.kkcore_cbo,
                                                     self.kkcore_checkbox))

        self.add_widget_to_layout(self.kkcore_cbo,
                                  alignment=Qt.AlignmentFlag.AlignLeft)

        self.kkcore_cbo.setEnabled(False)

        self.curve_selectors.append(self.kkcore_cbo)

        self.add_blank_line()

    def update_tab(self, well=None, force_update=False):
        if well is not None and (self.well is None or self.well.graphicWindow != well.graphicWindow):
            self.scatter_window = GraphicWindow(well.graphicWindow.get_tab_serialization,
                                                well.graphicWindow.set_tabs,
                                                well.graphicWindow.get_depth_unit,
                                                view_id=self.tab_name,
                                                stand_alone=True)

        if not super().update_tab(well, force_update):
            return

        update_curve_list_multi_cbo(self.feature_selector, well)

    def preview(self):
        if not super().preview():
            return

        learning_rate = self.learning_rate_textbox.text()

        if not is_number_between(learning_rate,
                                 0,
                                 1,
                                 closed_range=True):
            return AlertWindow("El learning_rate debe ser un número entre 0 y 1.  (Se usa punto '.' como separador decimal)")

        n_estimators = self.n_estimators_textbox.text()

        if not is_positive_integer(n_estimators):
            return AlertWindow("La cantidad de estimadores debe ser un entero positivo.")

        curve_to_predict = self.kcore_cbo \
            .currentText()

        feature_names = self.feature_selector \
            .currentOptions()

        if curve_to_predict in feature_names:
            return AlertWindow("La curva a predecir no debe ser un feature")

        if len(feature_names) == 0:
            return AlertWindow("Se debe elegir al menos un feature")

        dataset = self.well \
            .wellModel \
            .get_DF() \
            .loc[self.depth_curve_min:self.depth_curve_max] \
            .copy()

        dataset = dataset.reset_index()

        x_train, y_train, x_test = get_train_x_y_test(dataset,
                                                      feature_names,
                                                      curve_to_predict)
        if len(x_train) == 0:
            return AlertWindow(EMPTY_TRAIN_ERROR)

        ml_config = {
            "learning_rate": float(learning_rate),

            "n_estimators":  int(n_estimators),

            'loss': self.loss_cbo.currentData(),

            "x_train": x_train,

            "y_train": log10(y_train),

            "x_test": x_test,

            "fraction": 0.8,

            "search_hyperparameters": self.search_hyperparameters_rb.isChecked(),

            # "iterations": 1000
        }

        loading_pop_up("Cargando",
                       lambda: self.predict(ml_config))

    def predict(self, ml_config):
        y_to_predict, split_20_predicted, predicted_curve, hyperparameters = ada_bossting_permeability(ml_config)

        self.learning_rate_textbox.setText(str(hyperparameters['learning_rate']))

        self.n_estimators_textbox.setText(str(hyperparameters['n_estimators']))

        self.scatter_window.add_scatterplot({
            'tab_name': PERMEABILITY_ADA_TAB_NAME,

            'track_name': ADA_SCATTER_NAME,

            'curve_name': ADA_SCATTER_NAME,

            "x_axis": split_20_predicted,

            "y_axis": y_to_predict,

            "left_label": f"Estimado{self.log_lbl}",

            "bottom_label": f"Real{self.log_lbl}",

            "is_log": True,

            "is_y_log": True,

            "custom_line": True
        })

        self.set_curve_to_save(predicted_curve,
                               data_is_full_size=False,
                               unit=MD_LBL)
        base_dict = {
            'tab_name': PERMEABILITY_ADA_TAB_NAME,

            'track_name': ADA_TRACK_NAME,

            'add_axis': True,

            'y_axis': self.depth_curve,
        }

        x_label = K_LBL

        self.add_curve_with_y_label({**base_dict,
                                     **{
                                        'curve_name': ADA_TRACK_NAME,

                                        'x_axis': self.curve_to_save,

                                        "x_label": x_label,

                                        "y_label": self.get_y_label(),

                                        'color': self.curve_to_save_color.currentText(),

                                        'line_style': self.curve_to_save_line.currentText(),

                                        'line_marker': self.curve_to_save_marker.currentText(),

                                        'line_width': 1,

                                         "is_log": self.log_checkbox.isChecked()
                                    }})

        if self.kkcore_checkbox.isChecked():
            kcore = self.well \
                .wellModel \
                .get_partial_curve(self.kkcore_cbo.currentText(),
                                   self.depth_curve_min,
                                   self.depth_curve_max,
                                   to_list=False)

            self.window.add_curve({** base_dict,
                                      ** DEFAULT_SCATTERPLOT_CONFIG,
                                      ** {
                                          'x_axis': kcore
                                          if self.log_checkbox.isChecked()
                                          else kcore,

                                          'color': 'Rojo',

                                          'line_marker': 'Punto',

                                          'curve_name': f"{PERMEABILITY_ADA_TAB_NAME} "
                                                        f"{permeability_constants.SCATTER_CORE}",

                                          "ephimeral": True,

                                          "cummulative": True,

                                          "x_label": K_CORE_LBL,

                                          "is_log": self.log_checkbox.isChecked()
                                      }})

        self.window.remove_ehphimerals(self.tab_name)

        self.scatter_window.draw_tracks(self.tab_name)

        # For the case where the red points are used to compare
        self.window.draw_tracks(EVERY_TAB)

        self.window.set_ephimeral_to_delete(self.tab_name)
