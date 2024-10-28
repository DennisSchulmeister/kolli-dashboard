# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .data import data, version
from shiny import reactive, ui

import faicons

def infobox_ui():
    return ui.input_action_link("open_info_popup", "", icon=faicons.icon_svg("circle-info"))

def infobox_server(input, output, session):
    @reactive.effect
    @reactive.event(input.open_info_popup)
    def _():
        m = ui.modal(
            ui.markdown(
                f"""
                **© 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik** <br>
                **Dennis Schulmeister-Zimolong &lt;[dennis@wpvs.de](mailto:dennis@wpvs.de)&gt;** <br>
                Lizenziert unter der BSD 3-Clause Lizenz

                _Das Forschungsprojekt KoLLI (Kooperative Lehr-Lern-Innovation) wird von der Stiftung Innovation
                in der Hochschullehre gefördert._
                """
            ),
            title      = "Forschungsprojekt KoLLI - Evaluationsergebnisse",
            easy_close = True,
            size       = "l",
            footer     = ui.markdown(
                f"""
                **Version:** {version} <span class="text-secondary">|</span>
                **Stand:** {data["max_date"]}     <span class="text-secondary">|</span>
                [Quellcode](https://github.com/DennisSchulmeister/kolli-dashboard)
                """
            ),
        )

        ui.modal_show(m)