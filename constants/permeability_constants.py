"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

PERMEABILITY_TAB_NAME = "Permeabilidad"

K_PHI_LBL = "K PHI"

K_CORE_LBL = "K Core"

PHI_CORE_LBL = "PHI Core"

MD_LBL = "[mD]"

K_LBL = "K [mD]"

PERMEABILITY_XGBOOST_TAB_NAME = "XGboost"

PERMEABILITY_RANDOM_FOREST_TAB_NAME = "Random Forest"

PERMEABILITY_ADA_TAB_NAME = "Decision Tree con Ada"

PERMEABILITY_TIXIER = "Tixier"

PERMEABILITY_COATES = "Coates"

PERMEABILITY_TIMUR = "Timur"

RESISTIVITY_HYDROCARBON_LBL = "Resistividad (sat. con hidrocarburo)"

RESISTIVITY_SWIRR_LBL = "Resistividad"

SW_LBL = "Sat. de agua irreducible."

RESISTIVITY_LBL = "Resistividad"

PERMEABILITY_COATES_DUMANOIR = "Coates y Dumanoir"

XGBOOST_TRACK_NAME = f"{PERMEABILITY_TAB_NAME} - {PERMEABILITY_XGBOOST_TAB_NAME}"

RANDOM_FOREST_TRACK_NAME = f"{PERMEABILITY_TAB_NAME} - {PERMEABILITY_RANDOM_FOREST_TAB_NAME}"

ADA_TRACK_NAME = f"{PERMEABILITY_TAB_NAME} - {PERMEABILITY_ADA_TAB_NAME}"

TIXIER_TRACK_NAME = f"{PERMEABILITY_TAB_NAME} - {PERMEABILITY_TIXIER}"

SCATTER_CORE = "core scatter"

COATES_TRACK_NAME = f"{PERMEABILITY_TAB_NAME} - {PERMEABILITY_COATES}"

TIMUR_TRACK_NAME = f"{PERMEABILITY_TAB_NAME} - {PERMEABILITY_TIMUR}"

COATES_AND_DUMANOIR_TRACK_NAME = f"{PERMEABILITY_TAB_NAME} - {PERMEABILITY_COATES_DUMANOIR}"

LOG_LABEL = "Ver en escala logarítmica"

K_CORE_CURVE_LABEL = "Curva de valores core"

USE_DEFAULT_HYPERPARAMETRS = "Usar hiperparámetros por defecto"

SEARCH_HYPERPARAMETERS_LBL = "Buscar hiperparámetros"

PICK_HYPERPARAMETERS_LBL = "Elegir hiperparámetros"

FEATURES_LABEL = "Features a utilizar"

XGBOOST_SCATTER_NAME = "Predicciones XGboost"

RANDOM_FOREST_SCATTER_NAME = "Predicciones Random Forest"

ADA_SCATTER_NAME = "Predicciones Ada"

CONSTANT_LBL = "Constante de proporcionalidad"

KKCORE_LBL = "Mostrar valores para comparar"

INVALID_CONSTANT = "Las constantes a definir deben ser números positivos.  (Se usa punto '.' como separador decimal)"

INVALID_NUMERIC_CONSTANT = "Las constantes a definir deben ser números.  (Se usa punto '.' como separador decimal)"

EMPTY_TRAIN_ERROR = "En la región indicada, no hay valores de curva para entrenar el modelo."

DEFAULT_TIMUR_CONSTANT = "0.136"

DEFAULT_TIXIER_CONSTANT = "1000"

DEFAULT_COATES_CONSTANT = "100"

CONSTANT_1_C_COATES_DUM = "Cte. 1 de factor C"

CONSTANT_2_C_COATES_DUM = "Cte. 2 de factor C"

CONSTANT_3_C_COATES_DUM = "Cte. 3 de factor C"

CONSTANT_1_W_COATES_DUM = "Cte. 1 de factor W"

CONSTANT_2_W_COATES_DUM = "Cte. 2 de factor W"

CONSTANT_3_W_COATES_DUM = "Cte. 3 de factor W"

RSHALE_LBL = "Rshale"

A_CONSTANT_LBL = "a"

A_DEFAULT_VALUE = "1"

ERROR_MSG_COATES_DUM_CONSTANTS = "Las constantes de los factores deben ser números."

CONSTANT_1_C_DEFAULT = "23"

CONSTANT_2_C_DEFAULT = "465"

CONSTANT_3_C_DEFAULT = "188"

CONSTANT_1_W_DEFAULT = "3.75"

CONSTANT_2_W_DEFAULT = "0.2"

CONSTANT_3_W_DEFAULT = "2.2"

XGBOOST_MAX_DEPTH_DEFAULT = "4"

XGBOOST_GAMMA_DEFAULT = "5"

XGBOOST_N_ESTIMATORS_DEFAULT = "500"

XGBOOST_LEARNING_RATE_DEFAULT = "0.4"

XGBOOST_MIN_CHILD_WEIGHT = "1"

RF_MAX_DEPTH_DEFAULT = "100"

RF_MIN_SAMPLE_DEFAULT = "0.01"

RF_N_ESTIMATORS = "50"

RF_MIN_WEIGHT = "0.0"

RF_MIN_SAMPLES_LEAF = "1"

ADA_N_ESTIMATORS_DEFAULT = "500"

ADA_LEARNING_RATE_DEFAULT = "1.0"
