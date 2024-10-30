# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .utils import src_dir, scale_minus_plus, to_scale_minus_plus
import pandas as pd
import plot_likert

def __init__():
    """
    Read in data files when the module is first imported. Returns a dictionary
    with the following properties:
    
     * `data`: A dataframe with the survey results
     * `labels`: A dataframe with the question labels
     * `max_date`: A string with the formatted date of the last survey
     * `teachers`: A list of the teacher IDs
    """
    # Read data files
    data    = pd.read_csv(str(src_dir / "data" / "data.csv"),   encoding="utf-16", sep="\t", quotechar='"', decimal=".")
    labels  = pd.read_csv(str(src_dir / "data" / "labels.csv"), encoding="utf-16", sep="\t", quotechar='"', decimal=".")

    data["STARTED"] = pd.to_datetime(data["STARTED"])

    # Repair survey that was accidentally run for the wrong teacher
    data = data[data["CASE"] != 242]
    filtered_rows = data[(data["QUESTNNR"] == "S-SILA-1") & (data["STARTED"].dt.date == pd.to_datetime("2024-10-16").date())]
    data.loc[filtered_rows.index, "QUESTNNR"] = "S-KAWE-1"

    # Make initial pre-survey compatible with the later version
    data["VU03_01"] = data["VU03_01"].clip(upper=4)
    data["VU03_02"] = data["VU03_02"].clip(upper=4)
    data["VU03_03"] = data["VU03_03"].clip(upper=4)
    data["VU03_04"] = data["VU03_04"].clip(upper=4)

    data.loc[data["VU03_01"].notnull(), "V204_02"] = data["VU03_01"]
    data.loc[data["VU01_01"].notnull(), "V202_01"] = data["VU01_01"]
    data.loc[data["VU03_02"].notnull(), "V201_02"] = data["VU03_02"]

    data["V210_01"] = data.apply(lambda row: "Erwartungen: " + str(row["VU02_01"]) if pd.notnull(row["VU02_01"]) else row["V210_01"], axis=1)

    data.drop(["VU01_01", "VU02_01", "VU03_01", "VU03_02"], axis=1, inplace=True)

    # Question DR06_01 from survey S-DIRA-2-spezial can be used for the student mid survey, too
    try:
        dira2_special = data[(data["QUESTNNR"] == "S-DIRA-2-spezial") & (data["DR06_01"].notnull())].copy()
        dira2_special["QUESTNNR"] = "S-DIRA-2"
        data = data.append(dira2_special, ignore_index=True)
    except KeyError:
        pass

    # Return final result
    return {
        "answers":  data,
        "labels":   labels,
        "max_date": data["STARTED"].max().strftime('%d.%m.%Y'),
        "teachers": data["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist(),
    }

data    = __init__()
version = "1.1.0"

def get_label(var):
    return data["labels"].loc[data["labels"]["VAR"] == var, "LABEL"].values[0]

def plot_likert_chart(input, data, *vars, width=0.15):
    plot_percentage = input.number_format() == "percent"

    df = data[[*vars]]

    for var in vars:
        df[var] = df[var].apply(to_scale_minus_plus)
        df = df.rename(columns={var: get_label(var)})

    # Bug in plot-likert? Crashes with percentages if there a no answers for one question
    df1 = df.copy()
    df1.dropna(axis=1, how="all", inplace=True)

    if df1.shape[1]:
        df = df1
    else:
        plot_percentage = False

    # See: https://gist.github.com/nmalkin/9a31437d3be18d637d0b63e54926c491
    if plot_percentage:
        plot_likert.__internal__.BAR_LABEL_FORMAT = "%.1f"
    else:
        plot_likert.__internal__.BAR_LABEL_FORMAT = "%.0f"

    return plot_likert.plot_likert(
        df              = df,
        plot_scale      = scale_minus_plus,
        plot_percentage = plot_percentage,
        bar_labels      = True,
        width           = width,
        legend          = 0,
    )