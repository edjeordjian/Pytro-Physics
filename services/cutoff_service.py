"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

import pandas as pd


def _get_cutoff_curve(main_curve, depth_curve, cutoff_value, values_below_cutoff):
    df = pd.DataFrame(data=main_curve, index=depth_curve, columns=["main_curve"])

    if values_below_cutoff:
        df["main_curve_aux"] = True if cutoff_value == np.nan else df["main_curve"] > cutoff_value 

    else:
        df["main_curve_aux"] = True if cutoff_value == np.nan else df["main_curve"] < cutoff_value 

    df["main_curve_aux"] = df["main_curve_aux"].replace(True, np.nan)
    df["main_curve_aux"] = df["main_curve_aux"].replace(False, 1)
    df["main_curve"] = df["main_curve"] * df["main_curve_aux"]
    #print("=====================")
    #print("=====================")
    #print(df)

    return df["main_curve"].to_numpy()


def _get_cutoff_using_thc(main_curve, depth_curve, thc_value, increasing, values_below_cutoff):
    df = pd.DataFrame(data=main_curve, index=depth_curve, columns=["main_curve"])
    main_curve = df.dropna(inplace=False)
    main_curve = main_curve.sort_values(by="main_curve", ascending=increasing)
    main_curve["amount"] = main_curve.reset_index().index + 1
    main_curve["max"] = main_curve.groupby(["main_curve"])["amount"].transform("max")
    main_curve["max"] = (100 * main_curve["max"]) / len(main_curve.index)

    if values_below_cutoff:
        cutoff_value = main_curve.loc[main_curve["max"] >= thc_value]
    else:
        cutoff_value = main_curve.loc[main_curve["max"] <= thc_value]
    
    cutoff_value = cutoff_value.reset_index().iloc[0 if values_below_cutoff else (len(cutoff_value.index) - 1)]["main_curve"] if len(cutoff_value[cutoff_value.columns[0]]) > 0 else np.nan
    
    joined = df.join(main_curve[["max"]], rsuffix='_r')
    if values_below_cutoff:
        joined["main_curve_aux"] = True if cutoff_value == np.nan else joined["main_curve"] > cutoff_value 
    else:
        joined["main_curve_aux"] = True if cutoff_value == np.nan else joined["main_curve"] < cutoff_value 
        
    joined["main_curve_aux"] = joined["main_curve_aux"].replace(True, np.nan)
    joined["main_curve_aux"] = joined["main_curve_aux"].replace(False, 1)
    joined["main_curve"] = joined["main_curve"] * joined["main_curve_aux"]
    #print("=====================")
    #print("=====================")
    #print(joined)

    config = {
        'x_axis': main_curve.groupby("main_curve").agg({"max":"max"}).reset_index()["main_curve"].to_numpy(),
        'y_axis': main_curve.groupby("main_curve").agg({"max":"max"})["max"].to_numpy(),
        'cutoff_value': cutoff_value,
        'thc_value': thc_value,
        'main_curve': joined["main_curve"].to_numpy()
    }

    return config


def _get_cutoff_using_cutoff(vshale_curve, depth_curve, cutoff_value, increasing, values_below_cutoff):

    df = pd.DataFrame(data=vshale_curve, index=depth_curve, columns=["main_curve"])
    main_curve = df.dropna(inplace=False)
    main_curve = main_curve.sort_values(by="main_curve", ascending=increasing)
    main_curve["amount"] = main_curve.reset_index().index + 1
    main_curve["max"] = main_curve.groupby(["main_curve"])["amount"].transform("max")
    main_curve["max"] = (100 * main_curve["max"]) / len(main_curve.index)

    joined = df.join(main_curve[["max"]], rsuffix='_r')

    if values_below_cutoff:
        thc_value = main_curve.loc[main_curve["main_curve"] >= cutoff_value]
        joined["main_curve_aux"] = True if cutoff_value == np.nan else joined["main_curve"] > cutoff_value 

    else:
        thc_value = main_curve.loc[main_curve["main_curve"] <= cutoff_value]
        joined["main_curve_aux"] = True if cutoff_value == np.nan else joined["main_curve"] < cutoff_value 

    thc_value = thc_value.reset_index().iloc[0]["max"] if len(thc_value[thc_value.columns[0]]) > 0 else np.nan
    
    joined["main_curve_aux"] = joined["main_curve_aux"].replace(True, np.nan)
    joined["main_curve_aux"] = joined["main_curve_aux"].replace(False, 1)
    joined["main_curve"] = joined["main_curve"] * joined["main_curve_aux"]
    #print("=====================")
    #print("=====================")
    #print(joined)

    config = {
        'x_axis': main_curve.groupby("main_curve").agg({"max":"max"}).reset_index()["main_curve"].to_numpy(),
        'y_axis': main_curve.groupby("main_curve").agg({"max":"max"})["max"].to_numpy(),
        'cutoff_value': cutoff_value,
        'thc_value': thc_value,
        'main_curve': joined["main_curve"].to_numpy()
    }

    return config


def get_cutoff_general(curves_list, cutoff_list, values_below_cutoff_list, main_curve, depth_curve):
    data = {}
    for i in range(len(curves_list)):
        data[str(i)] = curves_list[i]
    df = pd.DataFrame(data, index=depth_curve)
    df["NaN"] = False
    for i in range(len(curves_list)):
        df[df.columns[i]] = _get_cutoff_curve(curves_list[i], depth_curve, cutoff_list[i], values_below_cutoff_list[i])
        df[df.columns[i]] = df[df.columns[i]].isna()
        # df["NaN"] = (df["NaN"] + df[df.columns[i]] > 0)
        df["NaN"] = df["NaN"] | df[df.columns[i]]
    
    df["NaN"] = df["NaN"].replace(True, np.nan)
    df["NaN"] = df["NaN"].replace(False, 1)

    df["main_curve"] = main_curve
    df["main_curve"] = df["main_curve"] * df["NaN"]
    return df["main_curve"].to_numpy()


def get_cutoff_general_using_thc(curves_list, cutoff_list, values_below_cutoff_list, main_curve, depth_curve, thc_value, increasing, values_below_cutoff):
    # Recibe una lista de curvas con valores de cutoff para los cuales se debe adaptar
    config = _get_cutoff_using_thc(
        get_cutoff_general(curves_list, cutoff_list, values_below_cutoff_list, main_curve, depth_curve),
        depth_curve, 
        thc_value, 
        increasing,
        values_below_cutoff
    )

    config["main_curve"][np.isnan(config["main_curve"])] = 0
    config["main_curve"] = np.array(list(map(lambda x: 1 if x > 0 else 0, config["main_curve"])))

    return config


def get_cutoff_general_using_cutoff(curves_list, cutoff_list, values_below_cutoff_list, main_curve, depth_curve, cutoff_value, increasing, values_below_cutoff):
    config = _get_cutoff_using_cutoff(
        get_cutoff_general(curves_list, cutoff_list, values_below_cutoff_list, main_curve, depth_curve),
        depth_curve, 
        cutoff_value, 
        increasing,
        values_below_cutoff
    )
    
    config["main_curve"][np.isnan(config["main_curve"])] = 0
    config["main_curve"] = np.array(list(map(lambda x: 1 if x > 0 else 0, config["main_curve"])))

    return config


def get_thickness_rectangles(pay_flag_curve, depth_curve):
    df = pd.DataFrame(data=pay_flag_curve, index=depth_curve, columns=["main_curve"])
    first_value = df.iloc[0, 0]
    df["aux"] = df["main_curve"].shift(1, fill_value=first_value)
    df["result"] = df["main_curve"] == df["aux"]
    result = df.loc[df["result"] == False]
    result = result.reset_index()["index"].to_numpy()
    
    rectangles = []
    
    if len(result) == 0:
        return [{
            "x": [0, 1],
            "y": [min(depth_curve), max(depth_curve)],
            "value": first_value
        }]

    rectangles.append({
        "x": [0, 1],
        "y": [min(depth_curve), result[0]],
        "value": first_value
    })
    first_value = (first_value + 1) % 2

    for i in range(len(result) - 1):
        rectangles.append({
            "x": [0, 1],
            "y": [result[i], result[i+1]],
            "value": first_value
        })
        first_value = (first_value + 1) % 2

    rectangles.append({
        "x": [0, 1],
        "y": [result[len(result) - 1], max(depth_curve)],
        "value": first_value
    })

    return rectangles


def get_cutoff_rectangles(main_curve, pay_flag_curve, depth_curve):
    rectangles = get_thickness_rectangles(pay_flag_curve, depth_curve)
    min_val = min(main_curve[~np.isnan(main_curve)])
    max_val = max(main_curve[~np.isnan(main_curve)])

    for i in range(len(rectangles)):
        rectangles[i]["x"] = [min_val, max_val]

    return rectangles