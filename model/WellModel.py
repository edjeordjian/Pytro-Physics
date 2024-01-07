"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import traceback

import lasio
from lasio.reader import StringIO
from os import path
import pandas as pd
import numpy as np

from constants.pytrophysicsConstants import DEFAULT_LITHOLOGIES, STATE_FILE_NAME
from services.tools.file_service import create_file
from services.tools.logger_service import log_error
from services.tools.pandas_service import get_series_in_range
from services.tools.string_service import is_number, remove_characters, re_round_value
from services.tools.json_service import save_json, read_json

from constants import general_constants
from constants.general_constants import (number_of_decimals, METERS_LBL, FEETS_LBL,
                                         las_extention, VIEW_EXTENSION, depth_change_multiplier)
from constants.pytrophysicsConstants import LITHOLOGY_FILE_NAME, IPR_FILE_NAME


class WellModel:
    def __init__(self,
                 name,
                 url,
                 action,
                 well_is_new):
        self.name = name

        self.action = action

        self.las_file = lasio.LASFile()

        #self.las_file.version = []

        #self.las_file.well = []

        self.initial_las_loaded = False

        self.amount_of_updates = 0

        plain_url = url.split("/")

        self.las_file_name = plain_url.pop()

        self.url = f"{'/'.join(plain_url)}"

        if well_is_new:
            las_file = open(self.get_full_url(),
                            "w")

            las_file.write("~Version ---------------------------------------------------\n")

            las_file.write("VERS.              2.0 : CWLS log ASCII Standard -VERSION 2.0\n")

            las_file.write("WRAP.         NO : One Line per Depth Step\n")

            las_file.write("~Curve Information -----------------------------------------\n")

            las_file.write("DEPT.M     : 1 DEPTH\n")

            las_file.close()

        if not path.exists(self.get_lithologies_url()):
            self.lithologies = DEFAULT_LITHOLOGIES

            self.save_lithologies()

        else:
            self.lithologies = self.read_lithologies()
        
        if not path.exists(self.get_ipr_url()):
            self.ipr_curves = []

            self.save_ipr_curves()
        
        else:
            self.ipr_curves = self.read_ipr_curves()

        create_file(self.get_state_url())

        self.las_start = None
        self.las_stop = None
        self.las_step = None


    def get_label_for(self, curve_name, name_to_use=None):
        if name_to_use is None:
            name_to_use = curve_name

        unit = f" [{self.get_unit_of(curve_name)}]"

        if unit == " []":
            unit = ""

        return f"{name_to_use}{unit}"

    def get_unit_of(self, curve_name):
        return str(self.las_file.curvesdict[curve_name].unit)

    def _change_las_depth_unit(self, las, depth_unit):
        depth_label = las.curves[0].mnemonic
        new_df = las.df().reset_index()
        las.curves[0].unit = depth_unit
        las.well[0].unit = depth_unit
        las.well[1].unit = depth_unit
        las.well[2].unit = depth_unit
        new_df[depth_label] = (new_df[depth_label] * depth_change_multiplier[depth_unit])\
            .round(number_of_decimals)

        new_df[depth_label] = new_df[depth_label].map(lambda x: re_round_value(x, number_of_decimals))

        las.set_data_from_df(new_df.set_index(depth_label))
        return las

    def change_depth_unit(self):
        if len(self.las_file.curves) == 0:
            depth_unit = ""

        else:
            depth_unit = FEETS_LBL if (METERS_LBL in str(self.las_file.curves[0].unit).lower()) else METERS_LBL

        self._change_las_depth_unit(self.las_file, depth_unit)

        self.persist_update()

    def get_depth_unit(self, las=None):
        las = self.las_file if las is None else las

        if len(las.curves) == 0:
            return ""

        return METERS_LBL if (METERS_LBL in str(las.curves[0].unit).lower()) else FEETS_LBL

    def fix_depth(self, las, depth_unit):
        if len(las.curves) == 0 or (len(str(las.curves[0].unit)) != 0
                                    and str(las.curves[0].unit).lower() in depth_unit):
            return las

        return self._change_las_depth_unit(las, depth_unit)

    def _fix_input_data(self, df):
        df2 = df.round(decimals=number_of_decimals)

        df2.sort_index(inplace=True)

        self.las_file.set_data_from_df(df2)

    def set_initial_well(self, newLasFile):
        for lasCurve in newLasFile.curves:
            self.las_file.append_curve_item(lasCurve)

        self.las_file.well = newLasFile.well

        self.las_file.version = newLasFile.version

        try:
            self._fix_input_data(self.las_file.df())

        except ValueError:
            log_error(traceback.format_exc())

            print("LAS vacío")

        self.initial_las_loaded = True

    def merge_LAS_aux(self, newLasFile):
        lasMnemonics = list(map(lambda x: x.mnemonic, self.las_file.curves))
        newLasFile.curves[0].mnemonic = self.las_file.curves[0].mnemonic
        for lasCurve in newLasFile.curves[1:]:
            if lasCurve.mnemonic in lasMnemonics:
                lasCurve.mnemonic = lasCurve.mnemonic + general_constants.new_column_suffix
        mergedLasFiles = self.las_file.df().merge(newLasFile.df(), on = self.las_file.curves[0].mnemonic, how = 'outer',  suffixes = ("", general_constants.new_column_suffix))
        mergedLasFiles.sort_index(inplace=True)
        self.las_file.set_data_from_df(mergedLasFiles)
        
        newLas2Mnemonics = list(map(lambda x: x.mnemonic, newLasFile.curves))
        for mnemonic in newLas2Mnemonics[1:]:
            self.las_file.curvesdict[mnemonic].unit = newLasFile.curvesdict[mnemonic].unit
            self.las_file.curvesdict[mnemonic].value = newLasFile.curvesdict[mnemonic].value
            self.las_file.curvesdict[mnemonic].descr = newLasFile.curvesdict[mnemonic].descr
        
        mergedLasFiles.reset_index(inplace=True)

        start = mergedLasFiles[mergedLasFiles.columns[0]][0]
        stop = mergedLasFiles[mergedLasFiles.columns[0]][mergedLasFiles.shape[0] - 1]
        # The LAS 2.0 definition specifies that the depth STEP in case of not being regular should be 0
        step = 0

        mergedLasFiles["depth_aux"] = mergedLasFiles[mergedLasFiles.columns[0]].shift(1)
        steps = mergedLasFiles[mergedLasFiles.columns[0]] - mergedLasFiles["depth_aux"]
        steps = steps.round(number_of_decimals)
        steps = steps.unique()
        steps = steps[~np.isnan(steps)]
        if len(steps) == 1:
            step = steps[0]

        self.las_file.update_start_stop_step(start, stop, step)

    def _merge_file(self, las_file):
        if not self.initial_las_loaded:
            self.set_initial_well(las_file)

        else:
            self.merge_LAS_aux(las_file)

        self.las_start = self.las_file.well["STRT"].value
        self.las_stop = self.las_file.well["STOP"].value
        self.las_step = self.las_file.well["STEP"].value

        fmt = "%." + str(number_of_decimals) + "f"

        self.las_start =  fmt % float(self.las_start)
        self.las_stop =  fmt % float(self.las_stop)
        self.las_step =  fmt % float(self.las_step)

        self.persist_update()

    def merge_LAS(self, las_uri):
        newLasFile = lasio.read(las_uri)

        newLasFile = self.fix_depth(newLasFile, self.get_depth_unit(newLasFile))

        self._merge_file(newLasFile)

    def merge_csv(self, df, column_data, depth_unit):
        las_file = lasio.LASFile()

        for column_name, column_unit in column_data.items():
            las_file.add_curve(column_name, df[column_name], unit=column_unit)

        if len(depth_unit) != 0:
            las_file = self.fix_depth(las_file, depth_unit)

        self._merge_file(las_file)

    def get_action(self):
        return self.action

    def get_DF(self):
        if len(self.las_file.curves) == 0:
            return pd.DataFrame()
        return self.las_file.df()

    def get_raw_data(self):
        if len(self.las_file.curves) == 0:
            return ""
        s = StringIO()
        self.las_file.write(s, STRT=self.las_start, STOP=self.las_stop, STEP=self.las_step)
        s.seek(0)
        new_string = str(s.read())
        return new_string

    def get_curve_names(self):
        if len(self.las_file.curves) == 0:
            return []
        else:
            return list(map(lambda curve: curve.mnemonic, self.las_file.curves))[1::]

    def get_null_value(self):
        try:
            return self.las_file\
                .well\
                .null\
                .value

        except AttributeError:
            return self.las_file\
                .well\
                .NULL\
                .value

    def get_df_curve(self, curveName):
        return self.las_file.df()[curveName].to_numpy()

    def get_depth_curve(self):
        if len(self.las_file.curves) == 0:
            return []

        depth_label = self.get_depth_label()

        return self.las_file.df().reset_index()[depth_label].to_numpy()

    def get_depth_range(self):
        depth_curve = self.get_depth_curve()
        if len(depth_curve) == 0:
            return []
        
        return [min(depth_curve), max(depth_curve)]

    def get_depth_label(self):
        return self.las_file \
            .curves[0] \
            .mnemonic

    def _get_partial_depth_curve(self, minDepth, maxDepth):
        if is_number(minDepth):
            minDepth = max(float(minDepth), min(self.get_depth_curve()))
        else:
            minDepth = min(self.get_depth_curve())

        if is_number(maxDepth):
            maxDepth = min(float(maxDepth), max(self.get_depth_curve()))
        else:
            maxDepth = max(self.get_depth_curve())

        depth_label = self.las_file.curves[0].mnemonic
        depth_curve = self.las_file.df().reset_index()[depth_label]
        depthWithNans = depth_curve.map(lambda x: None if ((x > maxDepth) or (x < minDepth)) else x)
        return depthWithNans

    def get_partial_depth_curve(self, minDepth, maxDepth):
        return self._get_partial_depth_curve(minDepth, maxDepth).to_numpy()

    def get_partial_ranged_df_curve(self, curveName, minDepth, maxDepth, minCurveValue, maxCurveValue):
        if is_number(minCurveValue):
            minCurveValue = max(float(minCurveValue),
                                min(self.get_df_curve(curveName)[~np.isnan(self.get_df_curve(curveName))]))
        elif len(self.get_df_curve(curveName)[~np.isnan(self.get_df_curve(curveName))]) == 0:
            minCurveValue = np.nan
        else:
            minCurveValue = min(self.get_df_curve(curveName)[~np.isnan(self.get_df_curve(curveName))])

        if is_number(maxCurveValue):
            maxCurveValue = min(float(maxCurveValue),
                                max(self.get_df_curve(curveName)[~np.isnan(self.get_df_curve(curveName))]))
        elif len(self.get_df_curve(curveName)[~np.isnan(self.get_df_curve(curveName))]) == 0:
            maxCurveValue = np.nan
        else:
            maxCurveValue = max(self.get_df_curve(curveName)[~np.isnan(self.get_df_curve(curveName))])

        depthWithNans = self._get_partial_depth_curve(minDepth, maxDepth)
        rangedCurve = self.las_file.df()[curveName].map(
            lambda x: np.nan if np.isnan(x) else (
                minCurveValue if x < minCurveValue else (
                    x if x < maxCurveValue else maxCurveValue
                )
            )
        )

        rangedCurveWithNans = depthWithNans.map(rangedCurve)

        return rangedCurveWithNans.to_numpy()

    def get_partial_curve(self,
                          curve_name,
                          min_depth,
                          max_depth,
                          to_list=True):
        depth_label = self.get_depth_label()

        try:
            df_curve = self.get_DF()[curve_name] \
                .copy() \
                .to_frame() \
                .reset_index()

        except KeyError:
            return None

        return get_series_in_range(df_curve, depth_label, curve_name, min_depth,
                                   max_depth, to_list)

    """
    def get_partial_curve_from_well_in_range(self,
                                             curve_name,
                                             min_depth,
                                             max_depth,
                                             to_list=True):
        depth_label = self.get_depth_label()

        try:
            df_curve = self.get_DF()[curve_name] \
                .copy() \
                .to_frame() \
                .reset_index()

        except KeyError:
            return None

        series = np.where(df_curve[depth_label].between(float(min_depth),
                                                        float(max_depth)),
                          df_curve[curve_name],
                          np.nan)

        if to_list:
            return series.tolist()

        return series
    """

    def get_partial_curve_in_range(self,
                                   curve,
                                   min_depth,
                                   max_depth,
                                   to_list=True):
        df_curve = pd.DataFrame({
            'depth': self.get_depth_curve(),

            'curve': curve
        })

        return get_series_in_range(df_curve, 'depth', 'curve', min_depth,
                                   max_depth, to_list)


    def combine_curves(self, dfCurve1, dfCurve2):
        dfCurve1 = pd.Series(dfCurve1)
        dfCurve2 = pd.Series(dfCurve2)
        return dfCurve1.combine(dfCurve2, lambda x, y: x if not np.isnan(x) else y).to_numpy()

    def get_amount_of_updates(self):
        return self.amount_of_updates

    def append_curve(self, curveName, newData, unit: str="",
                     descr: str="", value: str="", force_name=False):
        # Data es un array de numpy, por ejemplo: np.array(DataFrame["nombre_columna"])
        curveName = str(curveName).upper()
        data = np.array(newData)
        dataWithoutNans = data[~np.isnan(data)]
        if len(dataWithoutNans) > 0:
            data=data.round(number_of_decimals)
        
        if curveName in self.las_file.curvesdict.keys():
            if not force_name:
                return False
            else:
                replaced_df = self.las_file.df()
                replaced_df[curveName] = data
                self.las_file.set_data_from_df(replaced_df)
        else:
            self.las_file.append_curve(mnemonic=curveName.upper(),
                                   data=data,
                                   unit=remove_characters(unit, ["[", "]"]),
                                   descr=descr,
                                   value=value)

        self.persist_update()

        return True

    def persist_update(self):
        self.las_file.write(self.get_full_url(), version=2.0, STRT=self.las_start, STOP=self.las_stop, STEP=self.las_step)

        self.amount_of_updates += 1
    
    def delete_curve(self, curveName):
        self.las_file.delete_curve(curveName)
        self.persist_update()

    def replace_curve_values(self, curve_name, old_value, new_value, min_depth, max_depth):
        first_range = pd.Series(dtype="float64")
        last_range = pd.Series(dtype="float64")
        depth_curve = self.get_depth_curve()
        if is_number(min_depth) and float(min_depth) > min(depth_curve):
            first_range = self.las_file.df().loc[min(depth_curve):(float(min_depth) - 10 ** (-1 * number_of_decimals))][curve_name]
            min_depth = max(float(min_depth), min(depth_curve))
        else:
            min_depth = min(depth_curve)

        if is_number(max_depth) and float(max_depth) < max(depth_curve):
            last_range = self.las_file.df().loc[(float(max_depth) + 10 ** (-1 * number_of_decimals)):max(depth_curve)][curve_name]
            max_depth = min(float(max_depth), max(depth_curve))
        else:
            max_depth = max(depth_curve)

        middle_range = self.las_file.df().loc[float(min_depth):float(max_depth)][curve_name].replace(old_value, new_value)

        replaced_curve = list(first_range.to_numpy()) + list(middle_range.to_numpy()) + list(last_range.to_numpy())

        replaced_df = self.las_file.df()
        replaced_df[curve_name] = replaced_curve
        self.las_file.set_data_from_df(replaced_df)
        self.persist_update()

    def get_name(self):
        return self.name

    def set_df(self, newDF):
        self.las_file.set_data_from_df(newDF)
        self.persist_update()

    def save_lithologies(self):
        save_json(self.get_lithologies_url(), self.lithologies)

        self.amount_of_updates += 1

    def read_lithologies(self):
        return read_json(self.get_lithologies_url())

    def get_lithologies(self):
        return self.lithologies

    def set_lithologies(self,
                        lithologies):
        self.lithologies = lithologies

    def save_ipr_curves(self):
        save_json(self.get_ipr_url(), self.ipr_curves)

        self.amount_of_updates += 1

    def read_ipr_curves(self):
        return read_json(self.get_ipr_url())

    def get_ipr_curves(self):
        return self.ipr_curves

    def set_ipr_curves(self,
                        ipr_curves):
        self.ipr_curves = ipr_curves

    def get_url(self):
        return self.url

    def get_full_url(self):
        return f"{self.url}/{self.las_file_name}"

    def get_lithologies_url(self):
        return f"{self.url}/{LITHOLOGY_FILE_NAME}"

    def get_ipr_url(self):
        return f"{self.url}/{IPR_FILE_NAME}_" + str(self.las_file_name).split(".")[0] + ".json"

    def get_state_url(self):
        return f"{self.url}/{STATE_FILE_NAME}{VIEW_EXTENSION}"

    def delete_ipr_curve(self, ipr_curve_name):
        self.ipr_curves = [ipr_curve for ipr_curve in self.ipr_curves if ipr_curve["name"] != ipr_curve_name]
        self.save_ipr_curves()

    def interp_curve_nans_replacing(self, curve_name):
        replaced_df = self.las_file.df()
        
        y = replaced_df[curve_name].to_numpy()
        
        first_not_nan_index = list(y).index(next(filter(lambda x: not np.isnan(x), y)))
        if first_not_nan_index == len(y) - 1:
            return

        reversed_y = np.flip(y)
        last_not_nan_index = list(reversed_y).index(next(filter(lambda x: not np.isnan(x), reversed_y)))
        last_not_nan_index = len(y) - last_not_nan_index - 1

        #y = y[first_not_nan_index:last_not_nan_index + 1]
        
        #https://stackoverflow.com/questions/6518811/interpolate-nan-values-in-a-numpy-array
        nans, x= np.isnan(y), lambda z: z.nonzero()[0]
        y[nans]= np.interp(x(nans), x(~nans), y[~nans])
        
        if first_not_nan_index > 0 and last_not_nan_index + 1 < len(y):
            first_arr = np.zeros(first_not_nan_index)
            first_arr[first_arr==0]=np.nan
            last_arr = np.zeros(len(y) - (last_not_nan_index + 1))
            last_arr[last_arr==0]=np.nan
            replaced_df[curve_name] = np.concatenate((first_arr, y[first_not_nan_index:last_not_nan_index + 1], last_arr))
        elif first_not_nan_index > 0:
            first_arr = np.zeros(first_not_nan_index)
            first_arr[first_arr==0]=np.nan
            replaced_df[curve_name] = np.concatenate((first_arr, y[first_not_nan_index:last_not_nan_index + 1]))
        elif last_not_nan_index + 1 < len(y):
            last_arr = np.zeros(len(y) - (last_not_nan_index + 1))
            last_arr[last_arr==0]=np.nan
            replaced_df[curve_name] = np.concatenate((y[first_not_nan_index:last_not_nan_index + 1], last_arr))
        else:
            replaced_df[curve_name] = y
        
        self.las_file.set_data_from_df(replaced_df)
    
    def interp_curve_nans(self, curve_name, new_curve_name):
        self.append_curve(new_curve_name, 
                            self.las_file.df()[curve_name].to_numpy(), 
                            unit=self.get_unit_of(curve_name))
        self.interp_curve_nans_replacing(new_curve_name)
