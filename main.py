import os
import traceback
import warnings

import pandas as pd
import config as app_config

import pyautogui
from PyQt6.QtWidgets import (QMainWindow, QWidget, QFileDialog,
                             QHBoxLayout, QVBoxLayout, QPushButton, QMenu,
                             QTabWidget, QApplication)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTimer
from pathlib import Path
import sys

from constants.messages_constants import CANNOT_USE_STATE_IN_READ_MODE_LBL
from constants.pytrophysicsConstants import (READ_MODE_WELL_NAME, READ_MODE_BASE_PATH, READ_MODE_WELL_PARTIAL_URL,
                                             APP_NAME, STATE_FILE_NAME)
from model.Well import Well
from services.tools.file_service import delete_directory_content, clean_file
from services.tools.list_service import flat_map, get_uniques
from services.tools.logger_service import log_error
from ui.popUps.AboutWindow import AboutWindow
from ui.popUps.InfoWindow import InfoWindow
from ui.popUps.YesOrNoQuestion import YesOrNoQuestion
from ui.visual_components.UnitDefiner.UnitDefiner import UnitDefiner

# The windows for each option of the side menu
from ui.filesTabs.filesWindow import FilesWindow
from ui.editor.curvesWindow import CurvesWindow
from ui.characterizationTabs.characterizationWindow import CharacterizationWindow

# The window to input the well name
from ui.popUps.LoadingWindow import LoadingWindow
from ui.popUps.newWellNameWindow import NewWellNameWindow
from ui.popUps.alertWindow import AlertWindow

import constants.media_constants as media_constants

from constants.general_constants import (las_extention, csv_extention, loading_pop_up_timeout_ms, 
                                         initial_loading_pop_up, FONT_SIZE, txt_extention, 
                                         VIEW_EXTENSION, NO_INTERNET_CONNECTION, END_BETA_TEXT)

from ui.visual_components.ScrollableWellWrapper import ScrollableWellWrapper

from ui.visual_components.data_menu_handler import deserialize_qt_attributes, save_state, load_state

import multiprocessing

import requests, datetime


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # -----------------
        # Add buttons to the side bar of the main window
        self.btn_1 = QPushButton('Archivos', self)
        self.btn_2 = QPushButton('Curvas de profundidad', self)
        self.btn_3 = QPushButton('Caracterizacion', self)
        #self.btn_4 = QPushButton('...', self)

        self.btn_1.clicked.connect(self.button1)
        self.btn_2.clicked.connect(self.button2)
        self.btn_3.clicked.connect(self.button3)
        #self.btn_4.clicked.connect(self.button4)

        self.characterization_window = CharacterizationWindow()

        # Add hidden tabs that will be associated with the buttons
        # The tabs contained in the array will be the Widgets
        self.tabs = []
        self.tabs.append(FilesWindow())
        self.tabs.append(ScrollableWellWrapper(CurvesWindow()))
        self.tabs.append(self.characterization_window)

        self.wells = {}

        self.selected_well = ""

        self.current_tab_index = 0

        self.initUI()

    def initUI(self):
        # -----------------
        # Top status bar of the main window
        self.statusBar()

        # Open file button that is linked to an open file dialog, this will be added to the file menu in the status bar
        open_las = QAction(QIcon('media/open.png'), 'Open', self)
        open_las.setText('Agregar LAS')
        open_las.setShortcut('Ctrl+O')
        open_las.setStatusTip('Agregar archivo .las')
        open_las.triggered.connect(lambda x: self.open_file_dialog(".las"))

        open_csv = QAction(QIcon('media/open.png'), 'Open', self)
        open_csv.setText('Agregar CSV')
        open_csv.setStatusTip('Agregar archivo .csv')
        open_csv.triggered.connect(lambda x: self.open_file_dialog(".csv"))

        open_txt = QAction(QIcon('media/open.png'), 'Open', self)
        open_txt.setText('Agregar TXT')
        open_txt.setStatusTip('Agregar archivo .txt')
        open_txt.triggered.connect(lambda x: self.open_file_dialog(".txt"))

        # File menu in the status bar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(open_las)
        fileMenu.addAction(open_csv)
        fileMenu.addAction(open_txt)
        # If not set, the default text in the button is "File"
        fileMenu.setTitle('Archivo')

        newWellAction = QAction('Nuevo', self)
        newWellAction.triggered.connect(self.showAddWellWindow)
        newWellAction.setShortcut('Ctrl+N')

        load_well_action = QAction('Cargar', self)
        load_well_action.triggered.connect(lambda: self.load_well())
        load_well_action.setShortcut('Ctrl+L')

        self.selectWellMenu = QMenu('Seleccionar', self)

        # Well menu in the menubar
        wellMenu = menubar.addMenu("&Pozo")
        wellMenu.addAction(newWellAction)
        wellMenu.addAction(load_well_action)
        wellMenu.addMenu(self.selectWellMenu)
        wellMenu.setTitle("Pozo")

        self.state_sub_menu(menubar)

        self.about_window = AboutWindow()

        self.about_sub_menu(menubar)

        # Buttons of the side menu
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.btn_1)
        left_layout.addWidget(self.btn_2)
        left_layout.addWidget(self.btn_3)
        #left_layout.addWidget(self.btn_4)
        left_layout.addStretch(5)
        left_layout.setSpacing(20)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # Right widget will contain the tabs of each section
        self.right_widget = QTabWidget()
        self.right_widget.tabBar().setObjectName("mainTab")
        self.right_widget.currentChanged.connect(self.updateTab)

        # Hidden tabs, associated with the side menu buttons
        self.right_widget.addTab(self.tabs[0], 'Archivos')
        self.right_widget.addTab(self.tabs[1], 'Curvas')
        self.right_widget.addTab(self.tabs[2], 'Caracterizacion')
        #self.right_widget.addTab(self.tabs[3], '...')

        self.right_widget.setCurrentIndex(0)
        # Make tabs invisible:
        self.right_widget.setStyleSheet('''QTabBar::tab{width: 0; \
            height: 0; margin: 0; padding: 0; border: none;}''')

        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget)
        main_layout.addWidget(self.right_widget)
        main_layout.setStretch(0, 40)
        main_layout.setStretch(1, 200)
        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        self.setWindowIcon(QIcon(media_constants.APP_ICON_ROUTE))

        self.setGeometry(0,
                         0,
                         app_config.window_width,
                         app_config.window_height)
        self.setWindowTitle(APP_NAME)

        if os.path.exists(READ_MODE_BASE_PATH):
            delete_directory_content(READ_MODE_BASE_PATH)

        directory_path = os.path.dirname(os.path.realpath(__file__))

        self.addWell(f"{directory_path}{READ_MODE_WELL_PARTIAL_URL}", READ_MODE_WELL_NAME, True)

        self.show()

    def get_graphic_windows(self):
        characterization_windows = []

        characterization_windows.append(self.wells[self.selected_well].graphicWindow)

        cutoff_every_tabs = self.characterization_window.tabs[7].tabs

        cutoff_tabs = [cutoff_every_tabs[0], cutoff_every_tabs[1], cutoff_every_tabs[2].tabs[0],
                       cutoff_every_tabs[3]]

        crossplot_tabs = self.characterization_window.tabs[8].tabs

        histogram_tabs = [self.characterization_window.tabs[9]]

        ipr_tabs = self.characterization_window.tabs[10].tabs

        stand_alone_tabs = cutoff_tabs + crossplot_tabs + histogram_tabs + ipr_tabs

        for tab in stand_alone_tabs:
            characterization_windows.append(tab.window)

        return characterization_windows

    def state_sub_menu(self, menu_bar):
        save_state_action = QAction('Guardar', self)

        save_state_action.triggered.connect(self.save_state_wrapper)

        clean_state_Action = QAction('Limpiar', self)

        clean_state_Action.triggered.connect(self.clear_state_wrapper)

        state_menu = menu_bar.addMenu("&estado")

        state_menu.addAction(save_state_action)

        state_menu.addAction(clean_state_Action)

        state_menu.setTitle("Estado")

    def save_state_wrapper(self):
        if len(self.wells) == 1:
            return InfoWindow(CANNOT_USE_STATE_IN_READ_MODE_LBL)

        save_state(self.get_graphic_windows(),
                   self.get_state_full_path())

    def clear_state_wrapper(self):
        if len(self.wells) == 1:
            return InfoWindow(CANNOT_USE_STATE_IN_READ_MODE_LBL)

        YesOrNoQuestion("¿Seguro que desea borrar el estado del pozo actual?",
                        lambda: clean_file(self.get_state_full_path()),
                        lambda: ())

    def about_sub_menu(self, menu_bar):
        about_action = QAction('Acerca de', self)

        about_action.triggered.connect(lambda: self.about_window.show())

        state_menu = menu_bar.addMenu("&ayuda")

        state_menu.addAction(about_action)

        state_menu.setTitle("Ayuda")


    def updateTab(self, tabIndex):
        print("Elegida pestaña: ", tabIndex)
        self.current_tab_index = tabIndex
        if self.selected_well in self.wells.keys():
            self.tabs[tabIndex].update_tab(self.wells[self.selected_well])

    def load_well(self, file_uri=None, loading_pop_up=True):
        if file_uri is None:
            file_uri = QFileDialog.getOpenFileName(self, 'Abrir pozo', "", "Archivo LAS (*.las)")[0]

        if len(file_uri) == 0:
            AlertWindow("Se debe especificar un archivo")
            return

        file_name = file_uri.split("/")[-1]

        if las_extention not in file_name:
            AlertWindow("Formato inválido: debe ser '.las'")
            return

        well_name = file_name.replace(las_extention, "")

        if self.wellExists(well_name):
            AlertWindow("Ya existe un pozo con ese nombre, elige otro")
            return

        if loading_pop_up:
            self.pop_up = LoadingWindow('Cargando archivo')

            QTimer.singleShot(loading_pop_up_timeout_ms,
                              lambda: (self.open_well(file_uri, well_name),
                                      load_state(self.get_graphic_windows(), self.get_state_full_path())))

        else:
            self.open_well(file_uri, well_name)

    def open_well(self, file_uri, well_name):
        try:
            self.addWell(file_uri,
                         well_name,
                         False)

            self.wells[well_name].wellModel.merge_LAS(file_uri)

            self.update_windows()

            self.pop_up.close()

        except Exception:
            log_error(traceback.format_exc())

            AlertWindow("Error al abrir el pozo.")

            self.pop_up.close()

    def open_file_dialog(self, extention):
        if self.selected_well == "":
            AlertWindow("No hay ningún pozo seleccionado.")
            return

        homeDir = str(Path.home())

        merge_file = {
            las_extention: self.load_las,
            csv_extention: self.load_csv,
            txt_extention: self.load_csv
        }

        file_kind = extention.upper()\
            .replace(".", "")

        # https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QFileDialog.html
        fname = QFileDialog.getOpenFileName(self,
                                            'Abrir archivo',
                                            homeDir, "Archivo " + file_kind + " (*" + extention + ")")

        file_name = fname[0]

        print(fname)

        print("Pozo seleccionado: ", self.selected_well)

        if (file_name and len(file_name) > 4 and file_name.endswith(extention, len(file_name) - 4)):
            print("Abierto archivo " + extention)

            self.pop_up = LoadingWindow('Cargando archivo...')

            QTimer.singleShot(loading_pop_up_timeout_ms, lambda: self.load_file(merge_file, extention, file_name))

    def load_file(self, merge_file, extention, file_name):
        try:
            merge_file[extention](file_name)

        except Exception as ex:
            log_error(str(ex))

            AlertWindow("Error al intentar abrir el archivo.")

            self.pop_up.close()

    def end_successfull_load_file(self):
        self.update_windows()

        self.pop_up.close()

    def load_las(self, file_name):
        self.wells[self.selected_well].wellModel.merge_LAS(file_name)

        self.end_successfull_load_file()

    def load_csv(self, file_name):
        df = pd.read_csv(file_name)

        # CSV files must be 'in english':
        # • ',' is the separator
        # • decimal numbers are written with '.'
        if len(df.columns) == 0 or len(df.columns[0].split(";")) > 1:
            df = pd.read_csv(file_name, sep=";")

        merge_fn = self.wells[self.selected_well] \
            .wellModel \
            .merge_csv

        UnitDefiner(df, merge_fn, self.end_successfull_load_file)

    def button1(self):
        self.right_widget.setCurrentIndex(0)

    def button2(self):
        self.right_widget.setCurrentIndex(1)

    def button3(self):
        self.right_widget.setCurrentIndex(2)

    def button4(self):
        self.right_widget.setCurrentIndex(3)

    def showAddWellWindow(self):
        wellName = ""

        self.nameWindow = NewWellNameWindow(wellName,
                                            self.addWell,
                                            self.wellExists)

        self.toggle_window(self.nameWindow)

    def get_state_full_path(self):
        return f"{self.wells[self.selected_well].wellModel.url}/{STATE_FILE_NAME}{VIEW_EXTENSION}"

    def addWell(self, wellURL, wellName, well_is_new):
        wellAction = QAction(wellName, self)

        self.selectWellMenu.addAction(wellAction)

        self.wells[wellName] = Well(wellName, wellURL, wellAction, well_is_new,
                                    self.get_tabs_serialization, self.set_tabs, self.update_windows)

        self._update_windows_on_add_well(wellAction,
                                         wellName)

        #if not well_is_new:
        wellAction.triggered.connect(
            lambda: self._update_windows_on_add_well(wellAction,
                                                     wellName)
        )

    def _update_windows_on_add_well(self, wellAction, wellName):
        self.set_selected_well(wellName),

        wellAction.setIcon(QIcon(media_constants.checked_icon)),

        #self.update_windows()

    def set_selected_well(self, wellName):
        if self.selected_well in self.wells.keys():
            self.wells[self.selected_well].wellModel.get_action().setIcon(QIcon(media_constants.unchecked_icon))

        self.selected_well = wellName

        app_config.current_well = self.selected_well

        self.updateTab(self.current_tab_index)

    def update_windows(self):
        for tab in self.tabs:
            tab.update_tab(self.wells.get(self.selected_well, None))

    def wellExists(self, wellName):
        return wellName in self.wells.keys()

    def toggle_window(self, window):
        if window.isVisible():
            window.hide()

        else:
            window.show()

    def get_tabs_serialization(self):
        # for tab in self.tabs[2]
        return [widget.get_view_serialization() for widget in self.get_tabs_in_use()]

    def get_tabs_in_use(self, tab_to_update_names=None):
        tabs = []

        self.get_tabs(self.tabs[2]
                      .get_tabs(),
                      tabs)

        if tab_to_update_names is None:
            return list(
                filter(lambda tab: tab.is_ever_updated(), tabs)
            )

        else:
            return list(
                filter(lambda tab: tab.tab_name in tab_to_update_names,
                       get_uniques(tabs))
            )

    def set_tabs(self, tab_state):
        tabs_to_update_names = list(flat_map(lambda x: list(x.keys()), tab_state))

        tabs_to_update = self.get_tabs_in_use(tabs_to_update_names)

        for i in range(len(tab_state)):
            # widget tab name == tab_state
            deserialize_qt_attributes(tabs_to_update[i], list(tab_state[i].values())[0])

            tabs_to_update[i].update_tab(force_update=True)

    def get_tabs(self, tabs_list, tabs_to_update):
        for tab in tabs_list:
            try:
                tab.tab_name

                tabs_to_update.append(tab)

            except Exception:
                self.get_tabs(tab.get_tabs(), tabs_to_update)

    def unset_update_in_tabs(self):
        tabs = []

        self.get_tabs(self.tabs[2]
                      .get_tabs(),
                      tabs)

        for tab in tabs:
            tab.set_ever_updated(False)


def main():
    # "RuntimeWarning: invalid value encountered in greater"
    # occurs when trying to draw markers in a curve with nans
    warnings.filterwarnings("ignore", category=RuntimeWarning)

    app = QApplication(sys.argv)

    app.setStyleSheet("QLabel{font-size: " + str(FONT_SIZE) + "pt;}\
                      QLineEdit{font-size: " + str(FONT_SIZE) + "pt;}\
                      QTextEdit{font-size: " + str(FONT_SIZE) + "pt;}\
                      QComboBox{font-size: " + str(FONT_SIZE) + "pt;}\
                      QGroupBox{font-size: " + str(FONT_SIZE) + "pt;}\
                      QCheckBox{font-size: " + str(FONT_SIZE) + "pt;}\
                      QRadioButton{font-size: " + str(FONT_SIZE) + "pt;}\
                      QPushButton{font-size: " + str(FONT_SIZE) + "pt;}\
                      QAction{font-size: " + str(FONT_SIZE) + "pt;}\
                      QMenu{font-size: " + str(FONT_SIZE) + "pt;}\
                      QMenuBar{font-size: " + str(FONT_SIZE) + "pt;}\
                      QTableView{font-size: " + str(FONT_SIZE) + "pt;}")

    app_config.screen_width, app_config.screen_height = pyautogui.size()

    app_config.window_width = int(app_config.screen_width / 2)

    app_config.window_height = int(app_config.screen_height - app_config.screen_height * 0.07)

    target_date = datetime.datetime(2023, 8, 1)

    system_date = datetime.datetime.now()

    check_date = False

    if check_date:
        try:
            response = requests.get("http://worldtimeapi.org/api/timezone/America/Argentina/Buenos_Aires") \
                               .json()

            internet_datetime = datetime.datetime.fromisoformat(response["datetime"])

        except:
            internet_datetime = None

        if internet_datetime is None:
            AlertWindow(NO_INTERNET_CONNECTION)

            sys.exit()

        elif system_date.date() >= target_date.date() or \
                internet_datetime.date() >= target_date.date():
            AlertWindow(END_BETA_TEXT)

            sys.exit()

    if initial_loading_pop_up:
        ex = LoadingWindow("Cargando Pytrophysics...")

        QTimer.singleShot(loading_pop_up_timeout_ms,
                              lambda: (MainWindow(),
                                        ex.close()))

    else:
        ex = MainWindow()

    sys.exit(app.exec())


# https://stackoverflow.com/questions/20602727/pyinstaller-generate-exe-file-folder-in-onefile-mode/20677118#20677118
# https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile/13790741#13790741
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    # Multiprocessing does not work well with PyInstaller
    multiprocessing.freeze_support()

    main()
