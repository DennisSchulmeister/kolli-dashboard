# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .utils import src_dir, scale_minus_plus, to_scale_minus_plus, checkbox_to_scale_minus_plus
from shiny  import reactive

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

    # Remove dummy responses
    data = data[data["CASE"] != 242]
    data = data[data["CASE"] != 432]
    data = data[data["CASE"] != 523]
    data = data[data["CASE"] != 553]

    # Repair survey that was accidentally run for the wrong teacher
    filtered_rows = data[(data["QUESTNNR"] == "R1-SILA-1") & (data["STARTED"].dt.date == pd.to_datetime("2024-10-16").date())]
    data.loc[filtered_rows.index, "QUESTNNR"] = "R1-KAWE-1"

    # Make initial pre-survey compatible with the later version
    data["VU03_01"] = data["VU03_01"].clip(upper=4)
    data["VU03_02"] = data["VU03_02"].clip(upper=4)
    data["VU03_03"] = data["VU03_03"].clip(upper=4)
    data["VU03_04"] = data["VU03_04"].clip(upper=4)

    data.loc[data["VU03_01"].notnull(), "V204_02"] = data["VU03_01"]
    data.loc[data["VU01_01"].notnull(), "V202_01"] = data["VU01_01"]
    data.loc[data["VU03_02"].notnull(), "V201_02"] = data["VU03_02"]

    data["V203_01"] = data["V203_01"].fillna(0)
    data["V210_01"] = data.apply(lambda row: "Erwartungen: " + str(row["VU02_01"]) if pd.notnull(row["VU02_01"]) else row["V210_01"], axis=1)

    data.drop(["VU01_01", "VU02_01", "VU03_01", "VU03_02"], axis=1, inplace=True)

    # Question DR06_01 from survey R1-DIRA-PROG1-2-special can be used for the student mid survey, too
    try:
        dira2_special = data[(data["QUESTNNR"] == "R1-DIRA-2-special") & (data["DR06_01"].notnull())].copy()
        dira2_special["QUESTNNR"] = "R1-DIRA-2"
        dira2_special.loc[:,"ZW04_01"] = dira2_special["DR06_01"]
        dira2_special.drop("DR06_01", axis=1)
        data = pd.concat([data, dira2_special], ignore_index=True)
    except KeyError:
        pass

    # Survey S-KAWE-SENG-3 uses slightly different wording for some questions
    for target, source in [
        ("AB09_01", "AB16_01"),
        ("AB09_02", "AB16_02"),
        ("AB09_03", "AB16_03"),
        ("AB09_04", "AB16_04"),
        ("AB09_05", "AB16_05"),
        ("AB09_06", "AB16_06"),
        ("AB09_07", "AB16_07"),
        ("AB14_06", "AB17_06"),
        ("AB14_07", "AB17_07"),
        ("AB14_08", "AB17_08"),
        ("AB14_09", "AB17_09"),
    ]:
        mask = data[source].notnull()
        data.loc[mask, target] = data.loc[mask, source]

    # Replace missing numerical values with minus one
    data["V203_01"] = data["V203_01"].fillna(-1)
    data["AA02_01"] = data["AA02_01"].fillna(-1)

    # Convert plus_minus likert questions to strings
    for label in labels[labels["TYPE"] == "plus_minus"].itertuples():
        try:
            data[label.VAR] = data[label.VAR].apply(to_scale_minus_plus)
        except KeyError:
            pass
    
    for label in labels[labels["TYPE"] == "checkbox_plus_minus"].itertuples():
        try:
            data[label.VAR] = data[label.VAR].apply(checkbox_to_scale_minus_plus)
        except KeyError:
            pass

    # Return final result
    _data = data[data["QUESTNNR"].str.startswith(("R1-", "R2-", "R3-"))]

    return {
        "answers":  data,
        "labels":   labels,
        "max_date": data["STARTED"].max().strftime('%d.%m.%Y'),
        "teachers": _data["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist(),
        "lectures": _data["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist(),
    }

data    = __init__()
version = "1.5.1"

# Reactive values for correlation filters
correlation_filters = {
    "round1_student1": {
        "V201_01": reactive.value([]),
        "V201_02": reactive.value([]),
        "V204_01": reactive.value([]),
        "V204_02": reactive.value([]),
        "V203_01": reactive.value([-1, 11]),
        "VU03_03": reactive.value([]),
        "VU03_04": reactive.value([]),
        "V209_01": reactive.value([]),
        "V209_02": reactive.value([]),
        "V209_03": reactive.value([]),
        "V209_04": reactive.value([]),
        "V209_05": reactive.value([]),
        "V209_06": reactive.value([]),
        "V209_07": reactive.value([]),
        "V209_08": reactive.value([]),
        "V209_09": reactive.value([]),
    },
    "round1_student2": {
        "ZW04_01": reactive.value([]),
        "ZW04_02": reactive.value([]),
        "ZW04_03": reactive.value([]),
        "ZW04_04": reactive.value([]),
        "ZW04_05": reactive.value([]),
        "ZW04_06": reactive.value([]),
        "ZW04_07": reactive.value([]),
        "ZW04_08": reactive.value([]),
    },
    "round1_student3": {
        "AB03_01": reactive.value([]),
        "AB03_02": reactive.value([]),
        "AB03_03": reactive.value([]),
        "AB03_04": reactive.value([]),
        "AB07_01": reactive.value([]),
        "AB07_02": reactive.value([]),
        "AB07_03": reactive.value([]),
        "AB07_04": reactive.value([]),
        "AB07_05": reactive.value([]),
        "AB07_06": reactive.value([]),
        "AB07_07": reactive.value([]),
        "AB07_08": reactive.value([]),
        "AB07_09": reactive.value([]),
        "AB09_01": reactive.value([]),
        "AB09_02": reactive.value([]),
        "AB09_03": reactive.value([]),
        "AB09_04": reactive.value([]),
        "AB09_05": reactive.value([]),
        "AB09_06": reactive.value([]),
        "AB09_07": reactive.value([]),
        "AB14_06": reactive.value([]),
        "AB14_07": reactive.value([]),
        "AB14_08": reactive.value([]),
        "AB14_09": reactive.value([]),
    },
    "round2_student3": {
        "R201_01": reactive.value([]),
        "R201_02": reactive.value([]),
        "R201_03": reactive.value([]),
        "R201_04": reactive.value([]),
        "R201_05": reactive.value([]),
        "R202_02": reactive.value([]),
        "R202_03": reactive.value([]),
        "R202_04": reactive.value([]),
        "R202_05": reactive.value([]),
        "R202_06": reactive.value([]),
        "R204_01": reactive.value([]),
    },
    "round1_student-DIRA2_special": {
        "DR06_01": reactive.value([]),
        "DR06_08": reactive.value([]),
    },
    "round2_student-DESC_general": {
        "AA01_01": reactive.value([]),
        "AA01_02": reactive.value([]),
        "AA01_03": reactive.value([]),
        "AA01_04": reactive.value([]),
        "AA02_01": reactive.value([-1, 11]),
        "AA03_01": reactive.value([]),
        "AA03_02": reactive.value([]),
        "AA03_03": reactive.value([]),
        "AA03_04": reactive.value([]),
    },
    "round2_student-DESC_specific": {
        "AS01_01": reactive.value([]),
        "AS01_02": reactive.value([]),
        "AS01_03": reactive.value([]),
        "AS02_01": reactive.value([]),
        "AS02_02": reactive.value([]),
        "AS02_03": reactive.value([]),
        "AS02_04": reactive.value([]),
        "AS02_05": reactive.value([]),
    },
}

def get_label(var):
    return data["labels"].loc[data["labels"]["VAR"] == var, "LABEL"].values[0]

def plot_likert_chart(input, data, *vars, width=0.15):
    plot_percentage = input.number_format() == "percent"

    df = data[[*vars]]
    df = df.rename(columns={var: get_label(var) for var in vars})

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

    ax = plot_likert.plot_likert(
        df              = df,
        plot_scale      = scale_minus_plus,
        plot_percentage = plot_percentage,
        bar_labels      = True,
        width           = width,
        legend          = 0,
    )

    ax.set_xlabel("Anzahl Antworten")
    return ax

def plot_multiple_choice_bar_chart(input, data, *vars):
    fig, ax = plt.subplots()
    df      = data[[var for var in vars]].astype(int).copy()
    df      = df.rename(columns={var: get_label(var) for var in vars})
    counts  = (df == 2).sum()

    if input.number_format() == "percent":
        ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=df.shape[0]))

    ax.bar(counts.index, counts.values)
    ax.set_ylabel("Anzahl Antworten")
    ax.set_xticklabels(counts.index, rotation=10, ha="right")
    
    return fig