import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def calculate_rel_change(row):
    if row["value_ref"] == 0:
        return float("Nan")
    else:
        return round((row["value_comp"] / row["value_ref"]) - 1, 3)


def calculate_zeroed_cum(row):
    return row["end_value"] - row["value"]


def zeroed_cum_data(df, max_week, scen, model, targ, calc_week):
    df_model = df[df["model_name"] == model]
    if df_model.shape[0] > 0:
        df_mod = df_model.copy()
        if (calc_week is True) or calc_week == "True":
            end_val = max(df_model.value)
            df_mod.loc[:, "end_value"] = end_val
            df_mod["end_value2"] = df_mod.apply(calculate_zeroed_cum, axis=1)
            df_mod = df_mod[["scenario_id", "model_name", "end_value2", "horizon"]]
            df_mod = df_mod.rename({'end_value2': 'end_value', "horizon": "week"}, axis=1)
            df_mod.loc[:, "target"] = str(targ)
            df0 = pd.DataFrame({
                "scenario_id": [scen],
                "model_name": [model],
                "target": [str(targ)],
                "end_value":
                    [float(df_model[df_model["horizon"] == int(max_week)]["value"].iloc[0])],
                "week": [int(0)]
            })
            df_end = pd.concat([df0, df_mod])
        else:
            end_val = df_model[df_model["horizon"] == int(max_week)]["value"]
            end_val = float(end_val.iloc[0])
            df0 = pd.DataFrame({
                "scenario_id": [scen],
                "model_name": [model],
                "target": [str(targ)],
                "end_value": [float(end_val)],
                "week": [int(0)]
            })
            df_end = df0
    else:
        df_end = pd.DataFrame()
    return df_end


def end_cum_value(df, max_week, scen, model, targ):
    df_model = df[df["model_name"] == model]
    if df_model.shape[0] > 0:
        end_val = float(df_model[df_model["horizon"] == int(max_week)]["value"].iloc[0])
        df_end = pd.DataFrame({
            "scenario_id": [scen],
            "model_name": [model],
            "target": [str(targ)],
            "end_value": [float(end_val)]
        })
    else:
        df_end = pd.DataFrame()
    return df_end


def model_cum_data(df, max_week, scen, model, targ):
    df_model = df[df["model_name"] == model]
    df_model = df_model[df_model["horizon"] <= int(max_week)]
    end_val = sum(df_model["value"])
    df_end = pd.DataFrame({
        "scenario_id": [scen],
        "model_name": [model],
        "target": [str(targ)],
        "end_value": [float(end_val)]
    })
    return df_end


def calculate_relative_change(df, comp, comparison_reference, on_vars):
    scen_comp = comparison_reference[comp][0]
    df_comp = df[df["scenario_id"] == scen_comp]
    df_comp = df_comp.rename(columns={
        "scenario_id": "scen_comp", "end_value": "value_comp"})[["scen_comp", "value_comp"] + on_vars]
    scen_ref = comparison_reference[comp][1]
    df_ref = df[df["scenario_id"] == scen_ref]
    df_ref = df_ref.rename(columns={
        "scenario_id": "scen_ref", "end_value": "value_ref"})[["scen_ref", "value_ref"] + on_vars]
    df_rel_change = df_comp.merge(df_ref, on=on_vars)
    df_rel_change["rel_change"] = df_rel_change.apply(calculate_rel_change, axis=1)
    df_rel_change["comparison"] = comp
    return df_rel_change


def scen_comparison_data(df, max_week, end_method, comparison_reference, model_exclusion=None, calc_week=False,
                         on_vars=None):
    # Model
    if on_vars is None:
        on_vars = ["target", "model_name"]
    model_list = list(df["model_name"].drop_duplicates())
    if model_exclusion is not None:
        for j in model_exclusion:
            if j in model_list:
                model_list.remove(j)
    df = df[df["model_name"].isin(model_list)]
    # Get end_values
    df_endvalue = df.copy()
    df_value = []
    for scen in df_endvalue["scenario_id"].drop_duplicates():
        df_scen = df_endvalue[df_endvalue["scenario_id"] == scen]
        for targ in df_endvalue["target"].drop_duplicates():
            df_targ = df_scen[df_scen["target"] == targ]
            for model in df_endvalue["model_name"].drop_duplicates():
                if end_method == zeroed_cum_data:
                    df_end = end_method(df_targ, max_week, scen, model, targ, calc_week)
                else:
                    df_end = end_method(df_targ, max_week, scen, model, targ)
                df_value.append(df_end)
    df = pd.concat(df_value)
    # Relative change
    df_all = []
    for comparison in comparison_reference:
        if isinstance(comparison, dict):
            for i in comparison.keys():
                df_rel_change = calculate_relative_change(df, i, comparison, on_vars)
                df_all.append(df_rel_change)
        else:
            i = comparison
            df_rel_change = calculate_relative_change(df, i, comparison_reference, on_vars)
            df_all.append(df_rel_change)
    df_all = pd.concat(df_all)
    # Remove NaN value
    df_all = df_all[~df_all["rel_change"].isna()]
    return df_all


def flatten_list(clist):
    """ Flatten a list

    Flatten a complex list

    :parameter clist: complex list of different level (i.e. list of list)
    :type clist: list
    :return: a flatten list
    """
    flat_list = [item for sublist in clist for item in sublist]
    return flat_list


def sample_df(df, scenario, pathogen, k=1000):
    """Sample DataFrame per scenario

    For a specific DataFrame, containing trajectories information in the SMH standard format:

    -  Create a "sample_id" variable corresponding to `<model_name>_<output_type_id>_<scenario_id>`
    -  For each team_model:
         - create a `"list_sample"`: list of all the possible `"sample_id"` associated with the team_model.
           For example: `"modelA_1_scenC"`, `"modelA_2_scenC"`, etc.
         - create a `"`list_weight"` : list of all each weight associated with each `"sample_id"`.
           Calculated as: 1/total number of trajectories of the location, target, scenario, model_team.
           For example: 1/100, 1/100, etc.
    - Concatenate all the list for each team_model together. For example: `list_sample = "modelA_1_scenC",
      "modelA_2_scenC", …, "modelA_100_scenC", "modelB_1_scenC", "modelB_2_scenC", …,  modelB_90_scenC", etc.` and
      `list_weight = 1/100, 1/100, …, 1/100, 1/90, 1/90, …, 1/90, etc.`
    - Transform the list_weight to sum to 1 by dividing by the number of `model_team` and `scenario` for the `location`,
      `target`. For example (if we have 2 model team for US, Incident Hospitalization, Flu):
         `list_weight = (1/100)/2, (1/100)/2, …, (1/100)/2, (1/90)/2, (1/90)/2, …, (1/90)/2`.
         `list_weight = list_weight/number of scenario inputted` (length of the parameter `scenario`)
    - Sample the `list_sample` k times (by default, 1000) with the associated weight and with replacement,
      by applying: `sample = np.random.choice(list_sample, p=weight_sample_fin, size=k, replace=True)`
    - Shuffle the list to avoid having the list ordered by `scenario`, `model`, `trajectories id`.
    - Select all the individual trajectories data frame input from the complete `"sample"` list. If a sample_id is
      sampled multiple times, it will be repeated multiple times in the output data frame.
    - Recode the sample_id to a numeric corresponding to 0 to number of sample - 1 (by default k-1: 999)
    - Return the output as a data frame with three columns: date, value_<pathogen name>, sample_id

    :parameter df: DataFrame in the SMH standard format containing all the trajectories associated with a specific
      round and pathogen
    :type df: pd.DataFrame
    :parameter scenario: list of scenario to filter the inputted the data frame with. If list is empty, an empty
      DataFrame will be return
    :type scenario: list
    :parameter pathogen: name of the pathogen associated with the data
    :type pathogen: str
    :parameter k: number of samples to draw, by default 1000
    :type k: int
    :return: A DataFrame with three columns: date, value_<pathogen name>, sample_id
    """
    pathogen = pathogen.lower()
    if len(scenario) > 0:
        df_scen = df[df["scenario_id"].isin(scenario)].copy()
        df_scen["sample_id"] = (df_scen["model_name"].astype(str) + "_" + df_scen["type_id"].astype(str) + "_" +
                                df_scen["scenario_id"].astype(str))
        df_scen["pathogen"] = pathogen
        list_sample = list()
        weight_sample = list()
        for model in list(df_scen["model_name"].drop_duplicates()):
            df_model = df_scen[df_scen["model_name"] == model]
            len_df = len(df_model[(df_model["scenario_id"] == scenario[0]) &
                                  (df_model["horizon"] == min(df_model["horizon"]))])
            list_sample.append(list(df_model["sample_id"].unique()))
            weight_list = [1 / int(len_df)] * int(len(list(df_model["sample_id"].unique())))
            weight_sample.append(weight_list)
        list_sample = flatten_list(list_sample)
        weight_sample_fin = flatten_list(weight_sample) / np.array(len(list(df_scen["model_name"].drop_duplicates())))
        weight_sample_fin = weight_sample_fin / np.array(len(scenario))
        all_sample_sel = np.random.choice(list_sample, p=weight_sample_fin, size=k, replace=True)
        all_sample_sel = list(np.random.permutation(all_sample_sel))
        df_sample_sel = df_scen.reset_index().set_index("sample_id").loc[all_sample_sel]
        all_sample = df_sample_sel.reset_index().drop(columns="index")
        all_sample["sample_id_n"] = list(np.repeat(list(range(k)), len(df_scen['horizon'].drop_duplicates())))
        all_sample = all_sample[["value", "target_end_date", "sample_id_n"]]
        all_sample = all_sample.rename(columns={"value": "value" + "_" + pathogen})
    else:
        all_sample = pd.DataFrame(columns=["value" + "_" + pathogen, "target_end_date", "sample_id_n"])
    return all_sample


def q1(x):
    """Calculate the quantile 0.025

    Calculate the quantile 0.025 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.025)


def q2(x):
    """Calculate the quantile 0.05

    Calculate the quantile 0.05 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.05)


def q3(x):
    """Calculate the quantile 0.1

    Calculate the quantile 0.1 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.1)


def q4(x):
    """Calculate the quantile 0.25

    Calculate the quantile 0.25 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.25)


def q5(x):
    """Calculate the quantile 0.75

    Calculate the quantile 0.75 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.75)


def q6(x):
    """Calculate the quantile 0.9

    Calculate the quantile 0.9 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.9)


def q7(x):
    """Calculate the quantile 0.95

    Calculate the quantile 0.95 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.95)


def q8(x):
    """Calculate the quantile 0.975

    Calculate the quantile 0.975 on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.975)


def median(x):
    """Calculate the quantile 0.5 (or median)

    Calculate the quantile 0.5 (or median) on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.quantile(0.5)


def mean(x):
    """Calculate the mean

    Calculate the mean on a specific pandas Series

    :parameter x: A pandas Series of value
    :type x: pd.Series
    :return: float
    """
    return x.mean()


def calc_value(pathogen_information, write_sample, write_quantiles):
    """Process Data for Combined Multi-pathogen plot (internal function_

     From a dictionary containing each DataFrame associated to a specific pathogen:

     - `"value"`: Sum of all the "value_" columns ("value_<pathogen>" set to NA for pathogen with empty DataFrame
       (not selected))

     Each quantile is noted as: q1, q2, q3, q4, q5, q6, q7, q8, corresponding to: 0.025, 0.05, 0.1, 0.25, 0.75, 0.9,
     0.95, 0.975, respectively. The median and mean are noted as "med" and "mean", respectively.

     The input `pathogen_information` should be in a specific format:

     - `pathogen_information = {<pathogenA>: {"dataframe":<DataFrame>}, <pathogenB>: {"dataframe":<DataFrame>}, etc.}`
     - `<DataFrame>` is a data frame in the output format of the `sample_df()` function with 3 columns:
       "target_end_date", "sample_id_n" and "value_<pathogen>".
     - For more information, please consult the `sample_df()` function documentation

     :parameter pathogen_information: A dictionary containing multiple dictionary containing a DataFrame (result of
      sampling process, key: "dataframe") and named with the associated specific pathogen (keys).
     :type pathogen_information: dict
     :parameter write_sample: If not None, write the associated samples in a csv files to the
     path and filename inputted
     :type write_sample: None | str
     :parameter write_quantiles: If not None, write the quantiles associated with the `"value"`
      columns in a csv or parquet files to the path and filename inputted
     :type write_quantiles: None | str
    """
    all_sample = pd.DataFrame()
    f = {'value': [median, q1, q2, q3, q4, q5, q6, q7, q8]}
    for patho in pathogen_information:
        # Preparation
        pathogen_name = patho.lower()
        f.update({"value_" + pathogen_name: [median, q1, q2, q3, q4, q5, q6, q7, q8]})
        # Merge all pathogen in one dataframe
        if len(all_sample) > 0:
            if len(pathogen_information[patho]["dataframe"]) > 0:
                all_sample = pd.merge(all_sample, pathogen_information[patho]["dataframe"],
                                      on=["target_end_date", "sample_id_n"])
            else:
                all_sample = all_sample.copy()
                all_sample["value_" + pathogen_name] = pd.NA
        else:
            all_sample = pathogen_information[patho]["dataframe"]
    for col in f.keys():
        if col not in all_sample.columns:
            all_sample[col] = pd.NA
    # Calculate sum of all pathogen
    all_sample["value"] = all_sample[[col for col in all_sample.columns if col.startswith('value_')]].sum(axis=1)
    # Calculate the quantiles for each "value" columns
    all_quantile = all_sample.groupby(["target_end_date"]).agg(f)
    all_quantile.columns = all_quantile.columns.get_level_values(0) + "-" + all_quantile.columns.get_level_values(1)
    if write_sample is not None:
        if write_sample.endswith(".csv"):
            all_sample.to_csv(write_sample)
        else:
            table = pa.Table.from_pandas(all_sample)
            pq.write_table(table, write_sample, compression="GZIP", compression_level=9)
    if write_quantiles is not None:
        if write_quantiles.endswith(".csv"):
            all_quantile.to_csv(write_quantiles)
        else:
            table = pa.Table.from_pandas(all_quantile)
            pq.write_table(table, write_quantiles, compression="GZIP", compression_level=9)
    return all_quantile, all_sample


def calc_proportion(all_sample, primary=None,
                    calc_mean=False,  write_proportion=None):
    """Process Data for Combined Multi-pathogen plot (internal function)

    From a DataFrame containing samples for specific pathogens:

    - Proportion of each pathogen :
        - If two pathogens calculate proportion for primary pathogen:
            - primary pathogen: `"proportion_<primary_pathogen>" = "value_<primary_pathogen>" / "value"`
        - If three pathogens calculate proportion for primary pathogen and secondary pathogen:
            - primary pathogen: `"proportion_<primary_pathogen>" = "value_<primary_pathogen>" / "value"`
            - primary + secondary pathogen: `"proportion__<primary_pathogen>_<secondary_pathogen>"` =
                (`"value_<primary_pathogen>" + "value_<secondary_pathogen>"`) / `"value"`
    - Calculate the median, and 50% quantiles for each "value" and "proportion" columns (and the mean
      if `calc_mean` set to `True`) except:
        - For proportion with two pathogens:
            - secondary pathogen: `"proportion_<other_pathogen>_median"` = 1 - `"proportion_<primary_pathogen>_median"
        - For proportion with three pathogens:
            - last pathogen: `"proportion_<other_pathogen>_median"` =
                `1 - "proportion_<primary_pathogen>_<secondary_pathogen>_median"`

    Each quantile is noted as: q1, q2, q3, q4, q5, q6, q7, q8, corresponding to: 0.025, 0.05, 0.1, 0.25, 0.75, 0.9,
    0.95, 0.975, respectively. The median and mean are noted as "med" and "mean", respectively.
    :parameter all_sample: A DataFrame containing the second result of `calc_value` function (
     sampling process output)
    :type all_sample: pd.DataFrame
    :parameter primary Name of the pathogen(s) to treat as "primary"/"secondary" for proportion calculation.
    If `None` the first pathogen(s) in the `pathogen_information`
    :type primary: None | list
    :parameter calc_mean: Boolean indicating if the mean should be calculated too (in addition to the other quantiles)
    :type calc_mean: bool
    :parameter write_proportion: If not None, write the quantiles associated with the `"proportion"`
     columns in a csv files to the path and filename inputted
    :type write_proportion: None | str
    """
    # Calculate proportion of each pathogen
    f2 = {}
    ## Prep column selection
    all_sample = all_sample.round({"value": 5})
    all_sample = all_sample.dropna(axis=1, how='all')
    list_patho = list(all_sample.filter(regex='^value_').columns)
    list_patho = [s.replace('value_', '') for s in list_patho]
    if primary is None:
        if len(list_patho) == 2:
            primary = list_patho[0]
        if len(list_patho) == 3:
            primary = list_patho[:2]
    else:
        if len(list_patho) == 2 and len(primary) != 1:
            raise ValueError("Primary should be of length 1")
        if len(list_patho) == 3 and len(primary) != 2:
            raise ValueError("Primary should be of length 2")
    other = []
    for patho in list_patho:
        if patho.lower() not in primary:
            other.append(patho.lower())
    ## Calculate proportion
    if (all_sample["value"] == 0).any():
        all_sample = all_sample[all_sample["value"] > 0]
    all_sample["proportion_" + primary[0]] = all_sample["value_" + primary[0]] / all_sample["value"]
    if calc_mean is True:
        f2.update({"proportion_" + primary[0]: [median, mean, q4, q5]})
    else:
        f2.update({"proportion_" + primary[0]: [median, q4, q5]})
    if len(primary) > 1:
        all_sample["proportion_" + primary[0] + "_" + primary[1]] = (
                (all_sample["value_" + primary[0]] + all_sample["value_" + primary[1]]) /
                all_sample["value"])
        if calc_mean:
            f2.update({"proportion_" + primary[0] + "_" + primary[1]: [median, mean]})
        else:
            f2.update({"proportion_" + primary[0] + "_" + primary[1]: [median]})
    # Calculate the quantiles for each "proportion" columns
    detail_quantile = all_sample.groupby(["target_end_date"]).agg(f2)
    detail_quantile.columns = (detail_quantile.columns.get_level_values(0) + "-" +
                               detail_quantile.columns.get_level_values(1))
    if len(primary) > 1:
        detail_quantile["proportion_" + other[0] + "-median"] = (
                1 - detail_quantile["proportion_" + primary[0] + "_" + primary[1] + "-median"])
        detail_quantile["proportion_" + primary[1] + "-median"] = (
                1 - detail_quantile["proportion_" + other[0] + "-median"] -
                detail_quantile["proportion_" + primary[0] + "-median"])
    else:
        detail_quantile["proportion_" + other[0] + "-median"] = (
                1 - detail_quantile["proportion_" + primary[0] + "-median"])
    if write_proportion is not None:
        detail_quantile.to_csv(write_proportion)
    return detail_quantile


def prep_multipat_plot_comb(pathogen_information, primary=None, calc_mean=False,
                            calc_prop=True, write_sample=None, write_quantiles=None,
                            write_proportion=None):
    """Process Data for Combined Multi-pathogen plot

    From a dictionary containing each DataFrame associated to a specific pathogen:

    - `"value"`: Sum of all the "value_" columns ("value_<pathogen>" set to NA for pathogen with empty DataFrame
      (not selected))
    - Proportion of each pathogen :
        - If two pathogens calculate proportion for primary pathogen:
            - primary pathogen: `"proportion_<primary_pathogen>" = "value_<primary_pathogen>" / "value"`
        - If three pathogens calculate proportion for primary pathogen and secondary pathogen:
            - primary pathogen: `"proportion_<primary_pathogen>" = "value_<primary_pathogen>" / "value"`
            - primary + secondary pathogen: `"proportion__<primary_pathogen>_<secondary_pathogen>"` =
                (`"value_<primary_pathogen>" + "value_<secondary_pathogen>"`) / `"value"`
    - Calculate the median, and 50% quantiles for each "value" and "proportion" columns (and the mean
      if `calc_mean` set to `True`) except:
        - For proportion with two pathogens:
            - secondary pathogen: `"proportion_<other_pathogen>_median"` = 1 - `"proportion_<primary_pathogen>_median"
        - For proportion with three pathogens:
            - last pathogen: `"proportion_<other_pathogen>_median"` =
                `1 - "proportion_<primary_pathogen>_<secondary_pathogen>_median"`

    Each quantile is noted as: q1, q2, q3, q4, q5, q6, q7, q8, corresponding to: 0.025, 0.05, 0.1, 0.25, 0.75, 0.9,
    0.95, 0.975, respectively. The median and mean are noted as "med" and "mean", respectively.

    The input `pathogen_information` should be in a specific format:

    - `pathogen_information = {<pathogenA>: {"dataframe":<DataFrame>}, <pathogenB>: {"dataframe":<DataFrame>}, etc.}`
    - `<DataFrame>` is a data frame in the output format of the `sample_df()` function with 3 columns:
      "target_end_date", "sample_id_n" and "value_<pathogen>".
    - For more information, please consult the `sample_df()` function documentation

    :parameter pathogen_information: A dictionary containing multiple dictionary containing a DataFrame (result of
     sampling process, key: "dataframe") and named with the associated specific pathogen (keys).
    :type pathogen_information: dict
    :parameter primary Name of the pathogen(s) to treat as "primary"/"secondary" for proportion calculation.
    If `None` the first pathogen(s) in the `pathogen_information`
    :type primary: None | list
    :parameter calc_mean: Boolean indicating if the mean should be calculated too (in addition to the other quantiles)
    :type calc_mean: bool
    :parameter calc_prop: Boolean indicating if the proportion and associated quantiles are
    calculated
    :type calc_prop: bool
    :parameter write_sample: If not None, write the associated samples in a csv pr parquet files to the
    path and filename inputted
    :type write_sample: None | str
    :parameter write_quantiles: If not None, write the quantiles associated with the `"value"`
     columns in a csv  or parquet files to the path and filename inputted
    :type write_quantiles: None | str
    :parameter write_proportion: If not None, write the quantiles associated with the `"proportion"`
     columns in a csv files to the path and filename inputted
    :type write_proportion: None | str
    :return: A dictionary with 2 objects: (1) "all":  median, 95%, 90%, 80%, and 50% quantiles for each "value" and
     "value_<pathogen>-<quantile>"columns and (2) "detail": median, 95%, 90%, 80%, and 50% quantiles for each
     "proportion_<pathogen>-<quantile>" columns.
    """
    all_quantile, all_sample = calc_value(pathogen_information, write_sample, write_quantiles)
    if calc_prop:
        detail_quantile = calc_proportion(all_sample, primary=primary,
                                          calc_mean=calc_mean,  write_proportion=write_proportion)
    else:
        detail_quantile = None
    return {"all": all_quantile, "detail": detail_quantile}