# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .data import data, version
from shiny import ui

def sidebar_ui():
    return ui.sidebar(
        ui.div(
            ui.h5("Filterkriterien"),
            ui.input_selectize("teachers", "Lehrperson", multiple=True, choices=data["teachers"]),
            ui.input_date_range("date_range", "Zeitraum", start="2024-09-01", end="2026-04-30"),
        ),

        ui.div(
            ui.h5("Darstellung"),
            ui.input_selectize("number_format", "Zahlenformat", selected="absolut", choices={"absolute": "Anzahl", "percent":  "Prozent"}),
        ),

        ui.div(class_="flex-grow-1"),

        ui.div(
            ui.hr(),
            ui.div(
                ui.markdown(
                    """
                    Kollaborative Lehr-Lern-Innovationen werden von Lehrenden und Studierenden partizipativ gestaltet,
                    indem die Ideenfindung, Umsetzung, Implementierung und Evaluation von Lehr-Lern-Innovationen zum
                    Gegenstand der Lehrveranstaltung selbst wird. Die Arbeit an den Lehr-Lern-Innovationen wird
                    dementsprechend didaktisch in der Lehrveranstaltung verankert und mit ihren primären Lernzielen
                    verknüpft.
                    
                    KoLLI ist ein an der DHBW Karlsruhe entwickelter Prozessleitfaden, der Lehrende hierbei unterstützt.
                    Diese Anwendung zeigt die Evaluationsergebnisse des dazugehörigen Forschungsprojekts.
                    """
                ),
                style  = "text-align: justify; hyphens: auto; font-size:75%;",
            ),
            ui.div(
                ui.div(
                    ui.strong("Version:"), f" {version}",
                    ui.span(" | ", class_="text-secondary"),
                    ui.strong("Stand:"), f" {data["max_date"]}"
                ),
                ui.tags.img(src="dhbw-logo.svg", height="60px", class_="mt-2"),
                class_="text-center",
            ),
        ),

        width = "20em"
    )

def sidebar_server(input, output, session):
    pass