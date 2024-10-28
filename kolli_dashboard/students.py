# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .data import data
from shiny import reactive, render, ui

import pandas as pd
import plot_likert

def students_ui():
    return [
        ui.h4("Studentische Evaluation"),
        ui.navset_pill(
            ui.nav_panel("Vorumfrage", ui.div(survey1_ui(), class_="mt-4")),
            ui.nav_panel("Zwischenumfrage", ui.div(survey2_ui(), class_="mt-4")),
            ui.nav_panel("Abschlussumfrage", ui.div(survey3_ui(), class_="mt-4")),
        ),
    ]

def survey1_ui():
    return ui.div(
        ui.layout_column_wrap(
            ui.value_box("Studierende", ui.output_ui("count_students1"), showcase=None, theme=ui.value_box_theme(bg="#f3f7fc", fg="#606060")),
            ui.value_box("Kurse", ui.output_ui("count_courses1"), showcase=None, theme=ui.value_box_theme(bg="#fbfcf3", fg="#606060")),
            ui.value_box("Lehrende", ui.output_ui("count_teachers1"), showcase=None, theme=ui.value_box_theme(bg="#fbfcf3", fg="#60606")),
        ),
        ui.output_ui("no_data1"),
        class_="my-flex-with-gaps",
    )
    
    #[
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
    #]

def survey2_ui():
    return ui.div(
        ui.layout_column_wrap(
            ui.value_box("Studierende", ui.output_ui("count_students2"), showcase=None, theme=ui.value_box_theme(bg="#f3f7fc", fg="#606060")),
            ui.value_box("Kurse", ui.output_ui("count_courses2"), showcase=None, theme=ui.value_box_theme(bg="#fbfcf3", fg="#606060")),
            ui.value_box("Lehrende", ui.output_ui("count_teachers2"), showcase=None, theme=ui.value_box_theme(bg="#fbfcf3", fg="#60606")),
        ),
        ui.output_ui("no_data2"),
        class_="my-flex-with-gaps",
    )

def survey3_ui():
    return ui.div(
        ui.layout_column_wrap(
            ui.value_box("Studierende", ui.output_ui("count_students3"), showcase=None, theme=ui.value_box_theme(bg="#f3f7fc", fg="#606060")),
            ui.value_box("Kurse", ui.output_ui("count_courses3"), showcase=None, theme=ui.value_box_theme(bg="#fbfcf3", fg="#606060")),
            ui.value_box("Lehrende", ui.output_ui("count_teachers3"), showcase=None, theme=ui.value_box_theme(bg="#fbfcf3", fg="#60606")),
        ),
        ui.output_ui("no_data3"),
        class_="my-flex-with-gaps",
    )

def students_server(input, output, session):
    survey1_server(input, output, session)
    survey2_server(input, output, session)
    survey3_server(input, output, session)

def survey1_server(input, output, session):
    @reactive.calc
    def filtered_surveys1():
        teachers   = input.teachers() or data["teachers"]
        questnnrs1 = [f"S-{teacher}-1" for teacher in teachers]
        questnnrs2 = [f"S-{teacher}-1-alt" for teacher in teachers]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        return data["answers"][
            (data["answers"]["QUESTNNR"].isin(questnnrs1 + questnnrs2)) &
            (data["answers"]["STARTED"] >= start_date) &
            (data["answers"]["STARTED"] <= end_date)
        ]

    @render.text
    def count_students1():
        try:
            return filtered_surveys1().shape[0]
        except KeyError:
            return 0

    @render.text
    def count_courses1():
        try:
            return filtered_surveys1()["STARTED"].dt.date.unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def count_teachers1():
        try:
            return filtered_surveys1()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def no_data1():
        if filtered_surveys1().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

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
    @reactive.calc
    def filtered_surveys2():
        teachers   = input.teachers() or data["teachers"]
        questnnrs1 = [f"S-{teacher}-2" for teacher in teachers]
        questnnrs2 = [f"S-{teacher}-2-alt" for teacher in teachers]
        
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        return data["answers"][
            (data["answers"]["QUESTNNR"].isin(questnnrs1 + questnnrs2)) &
            (data["answers"]["STARTED"] >= start_date) &
            (data["answers"]["STARTED"] <= end_date)
        ]

    @render.text
    def count_students2():
        try:
            return filtered_surveys2().shape[0]
        except KeyError:
            return 0

    @render.text
    def count_courses2():
        try:
            return filtered_surveys2()["STARTED"].dt.date.unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def count_teachers2():
        try:
            return filtered_surveys2()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def no_data2():
        if filtered_surveys2().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

def survey3_server(input, output, session):
    @reactive.calc
    def filtered_surveys3():
        teachers   = input.teachers() or data["teachers"]
        questnnrs1 = [f"S-{teacher}-3" for teacher in teachers]
        questnnrs2 = [f"S-{teacher}-3-alt" for teacher in teachers]
        
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        return data["answers"][
            (data["answers"]["QUESTNNR"].isin(questnnrs1 + questnnrs2)) &
            (data["answers"]["STARTED"] >= start_date) &
            (data["answers"]["STARTED"] <= end_date)
        ]
    
    @render.text
    def count_students3():
        try:
            return filtered_surveys3().shape[0]
        except KeyError:
            return 0

    @render.text
    def count_courses3():
        try:
            return filtered_surveys3()["STARTED"].dt.date.unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def count_teachers3():
        try:
            return filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0

    @render.text
    def no_data3():
        if filtered_surveys3().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."