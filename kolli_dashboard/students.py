# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from shiny import render, ui

import pandas as pd
import plot_likert

def students_ui():
    return [
        ui.h4("Studentische Evaluation"),
        ui.navset_pill(
            ui.nav_panel("Vorumfrage", survey1_ui()),
            ui.nav_panel("Zwischenumfrage", survey2_ui()),
            ui.nav_panel("Abschlussumfrage", survey3_ui()),
        ),
    ]

def survey1_ui():
    return [
        # ui.output_plot("test_likert"),
        # ui.panel_well(
        #     """
        #     Die studentische Vorumfrage findet am Anfang des Semesters statt, nachdem den Studierenden
        #     die Inhalte der Lehrveranstaltung und das KoLLI-Konzept vorgestellt wurden. Sie fragt die
        #     Haltung der Studierenden zur bevorstehenden Partizipation ab, um zu untersuchen, inwiefern
        #     sich diese im Lauf des Semesters verändert.
        #     """,
        #     class_="mt-4",
        # ),
    ]

def survey2_ui():
    return []

def survey3_ui():
    return []

def students_server(input, output, session):
    survey1_server(input, output, session)
    survey2_server(input, output, session)
    survey3_server(input, output, session)

def survey1_server(input, output, session):
    pass
    # @render.plot
    # def test_likert():
    #     return plot_likert.plot_likert(
    #         df = pd.DataFrame({
    #             'Dies ist eine ganz lange Frage mit furchtbar viel Text. Die will gar nicht aufhören.': {0: 'Strongly disagree', 1: 'Agree',},
    #             'Diese Frage hat jetzt auch nicht gerade wenig Text.': {0: 'Disagree', 1: 'Strongly agree',},
    #         }),
    #         plot_scale      = plot_likert.scales.agree,
    #         plot_percentage = input.number_format() == "percent",
    #         bar_labels      = True,
    #         width           = 0.15,
    #         legend          = 1,
    #     )

def survey2_server(input, output, session):
    pass

def survey3_server(input, output, session):
    pass