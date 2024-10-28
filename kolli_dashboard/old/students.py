# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from shiny.express import expressify, input, ui, render

import faicons
import pandas as pd
import plot_likert

@expressify
def semester_start_survey_sub_panel():
    with ui.nav_panel("Vorumfrage"):       
        with ui.panel_well(class_="mt-4"):
            "Text im Panel"

        with ui.layout_column_wrap(class_="mt-4"):
            with ui.value_box(
                showcase = faicons.icon_svg("piggy-bank", width="50px"),
                theme    = "bg-gradient-indigo-purple",  
            ):
                "KPI Title"
                "$1 Billion Dollars"
                "Up 30% VS PREVIOUS 30 DAYS"

            with ui.value_box(
                showcase = faicons.icon_svg("piggy-bank", width="50px"),
                theme    = "text-green",  
                showcase_layout = "top right",  
            ):
                "KPI Title"
                "$1 Billion Dollars"
                "Up 30% VS PREVIOUS 30 DAYS"

            with ui.value_box(
                showcase = faicons.icon_svg("piggy-bank", width="50px"),
                theme    = "danger",  
                showcase_layout = "bottom",  
            ):
                "KPI Title"
                "$1 Billion Dollars"
                "Up 30% VS PREVIOUS 30 DAYS"

        with ui.layout_columns(col_widths=(8, 4), class_="mt-4"):
            @render.express()
            def left_side():
                ui.h5("Likert-Skala")

                @render.plot()
                def test_likert_graph():
                    dummy_data = pd.DataFrame({
                        'Dies ist eine ganz lange Frage mit furchtbar viel Text. Die will gar nicht aufhören.': {0: 'Strongly disagree', 1: 'Agree',},
                        'Diese Frage hat jetzt auch nicht gerade wenig Text.': {0: 'Disagree', 1: 'Strongly agree',},
                    })

                    return plot_likert.plot_likert(
                        df              = dummy_data,
                        plot_scale      = plot_likert.scales.agree,
                        plot_percentage = input.number_format() == "percent",
                        bar_labels      = True,
                        width           = 0.15,
                        legend          = 1,
                    )

            @render.express()
            def right_side():
                ui.h5("Datentabelle")

                @render.data_frame
                def test_data_frame():
                    return pd.DataFrame({
                        "Spalte 1": {0: 12121, 1: 2323, 2: 4312},
                        "Spalte 2": {0: 34514, 1: 3143, 2: 3651},
                        "Spalte 3": {0: 53123, 1: 5642, 2: 5421},
                    })

@expressify
def mid_semester_survey_sub_panel():
    with ui.nav_panel("Zwischenumfrage"):
        with ui.div(class_="mt-4"):
            "Zwischenumfrage"

@expressify
def semester_end_survey_sub_panel():
    with ui.nav_panel("Abschlussumfrage"):
        with ui.div(class_="mt-4"):
            "Abschlussumfrage"

@expressify
def students_panel():
    with ui.nav_panel("Studierende"):
        ui.h4("Studentische Evaluation")

        with ui.navset_pill(id="survey"):
            semester_start_survey_sub_panel()
            mid_semester_survey_sub_panel()
            semester_end_survey_sub_panel()