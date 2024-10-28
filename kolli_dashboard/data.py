# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .utils import get_src_dir
import pandas as pd

def __init__():
    """
    Read in data files when the module is first imported. Returns a dictionary
    with the following properties:
    
     * `data`: A dataframe with the survey results
     * `labels`: A dataframe with the question labels
     * `max_date`: A string with the formatted date of the last survey
     * `teachers`: A list of the teacher IDs
    """
    src_dir = get_src_dir()
    data    = pd.read_csv(str(src_dir / "data" / "data.csv"),   encoding="utf-16", sep="\t", quotechar='"', decimal=".")
    labels  = pd.read_csv(str(src_dir / "data" / "labels.csv"), encoding="utf-16", sep="\t", quotechar='"', decimal=".")

    data["STARTED"] = pd.to_datetime(data["STARTED"])
    data = data[data["CASE"] != 242]

    filtered_rows = data[(data["QUESTNNR"] == "S-SILA-1") & (data["STARTED"].dt.date == pd.to_datetime("2024-10-16").date())]
    data.loc[filtered_rows.index, "QUESTNNR"] = "S-KAWE-1"

    return {
        "answers":  data,
        "labels":   labels,
        "max_date": data["STARTED"].max().strftime('%d.%m.%Y'),
        "teachers": data["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist(),
    }

data    = __init__()
version = "1.0.0"


