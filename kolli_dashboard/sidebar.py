# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .data         import data, version
from shiny.express import expressify, ui

@expressify
def sidebar():
    with ui.sidebar(width="20em"):
        ui.h5("Allgemeine Filter")

        ui.input_selectize(
            id       = "teacher",
            label    = "Lehrperson",
            multiple = True,
            choices  = data["teachers"],
        )

        ui.input_date_range("time_range", "Zeitraum", start="2024-09-01", end="2026-04-30")

        with ui.panel_conditional("input.group === 'Studierende'"):
            with ui.panel_conditional("input.survey === 'Vorumfrage'"):
                ui.h5("Studentische Vorumfrage", style="margin-top: 0.5em;")
                ui.p("Hier sollen mal Filter erscheinen")

    #         with ui.panel_conditional("input.survey === 'Zwischenumfrage'"):
    #             ui.h5("Studentische Zwischenumfrage", style="margin-top: 0.5em;")
    #             ui.p("Noch keine Filter vorhanden")
    # 
    #         with ui.panel_conditional("input.survey === 'Abschlussumfrage'"):
    #             ui.h5("Studentische Abschlussumfrage", style="margin-top: 0.5em;")
    #             ui.p("Noch keine Filter vorhanden")

        ui.h5("Optionen", style="margin-top: 0.5em;")

        ui.input_selectize(
            id       = "number_format",
            label    = "Darstellung",
            selected = "absolut",
            choices  = {
                "absolute": "Anzahl",
                "percent":  "Prozent",
            }
        )

        ui.div(class_="flex-grow-1")
        ui.hr()

        ui.markdown(
            """
            Kollaborative Lehr-Lern-Innovationen sind ...
            """
        )

        with ui.div(class_="text-center"):
            with ui.div():
                ui.strong("Version:")
                f" {version}"
            
                ui.span(" | ", class_="text-secondary")

                ui.strong("Stand:")
                f" {data["max_date"]}"

            ui.tags.img(src="dhbw-logo.svg", height="60px", class_="mt-2")