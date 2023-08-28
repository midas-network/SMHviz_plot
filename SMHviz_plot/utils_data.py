
import pandas as pd


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
                "end_value": [float(df_model[df_model["horizon"] == int(max_week)]["value"])],
                "week": [int(0)]
            })
            df_end = pd.concat([df0, df_mod])
        else:
            end_val = float(df_model[df_model["horizon"] == int(max_week)]["value"])
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
        end_val = float(df_model[df_model["horizon"] == int(max_week)]["value"])
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


def scen_comparison_data(df, max_week, zeroed, comparison_reference, model_exclusion=None, calc_week=False):
    # Model
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
                if (zeroed is True) or (zeroed == "True"):
                    df_end = zeroed_cum_data(df_targ, max_week, scen, model, targ, calc_week)
                elif zeroed == "Sample":
                    df_end = end_cum_value(df_targ, max_week, scen, model, targ)
                else:
                    df_end = model_cum_data(df_targ, max_week, scen, model, targ)
                df_value.append(df_end)
    df = pd.concat(df_value)
    # Relative change
    df_all = []
    if (zeroed is True) or (zeroed == "True"):
        on_vars = ["target", "model_name", "week"]
    else:
        on_vars = ["target", "model_name"]
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
