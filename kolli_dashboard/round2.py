# Forschungsprojekt KoLLI: Dashboard
# © 2025 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .ai_llm import ai_conversation, ai_conversation_available, ai_message
from .data   import correlation_filters, data, get_label, plot_likert_chart
from shiny   import reactive, render, ui

import faicons
import pandas            as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy             as np

#==============================================================================
# UI Definition
#==============================================================================

#------------------------------------------------------------------------------
# All Together
#------------------------------------------------------------------------------
ai_button_class = "" if ai_conversation_available() else "d-none"

icon_students = faicons.icon_svg("graduation-cap",    width="50px")
icon_courses  = faicons.icon_svg("users",             width="50px")
icon_teachers = faicons.icon_svg("chalkboard-user",   width="50px")
icon_lectures = faicons.icon_svg("person-chalkboard", width="50px")

def round2_ui():
    return [
        ui.h4("Runde 2 – Studentische Evaluation"),
        ui.navset_pill(
            ui.nav_panel("Abschlussumfrage", ui.div(round2_survey3_ui(), class_="mt-4")),
            ui.nav_menu(
                "Spezifische Umfragen",
                ui.nav_panel("DESC Allgemein", ui.div(round2_desc_general_ui(), class_="mt-4")),
                ui.nav_panel("DESC Lernziele", ui.div(round2_desc_objectives_ui(), class_="mt-4")),
                ui.nav_panel("DESC Prüfungsaufgabe", ui.div(round2_desc_assessment_ui(), class_="mt-4")),
                ui.nav_panel("DESC Reflexionsfragen", ui.div(round2_desc_reflection_ui(), class_="mt-4")),
            ),
        ),
    ]

#------------------------------------------------------------------------------
# Semester End Survey
#------------------------------------------------------------------------------
def round2_survey3_ui():
    return ui.div(
        ui.p(
            """
            Das Umfragedesign wurde so angepasst, dass nur noch eine summative Abschlussumfrage
            mit den Studierenden am Ende des Semesters durchgeführt wurde. Die Fragen sind dabei am
            Angebot-Nutzen-Wirkungsmodell der Lehre ausgerichtet, indem dieses auf die Fragestellung
            der studentischen Partizipation angewendet wird.
            """,
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round2_count_students3"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round2_count_teachers3"),
                ui.output_ui("round2_id_teachers3"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round2_count_lectures3"),
                ui.output_ui("round2_id_lectures3"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round2_no_data3"),

        ui.div(
            ui.h5("Umsetzung der Mitgestaltung"),
            ui.output_plot("round2_plot_umsetzung_likert", height="450px"),
        ),

        ui.div(
            ui.h5("Wirkung der Mitgestaltung"),
            ui.output_plot("round2_plot_wirkung_likert", height="450px"),
        ),

        ui.div(
            ui.h5("Sonstiges"),
            ui.output_plot("round2_plot_sonstiges_likert", height="150px"),
        ),

        ui.div(
            ui.h5("Freitextantworten"),
            ui.div(
                ui.div(
                    ui.input_action_button(
                        "btn_round2_ai_summary_freitext",
                        "KI-Zusammenfassung",
                        class_ = f"{ai_button_class}",
                    ),
                ),
                ui.output_data_frame("round2_df_freitext"),
                class_="my-flex-with-gaps",
            ),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Participation in General
#------------------------------------------------------------------------------
def round2_desc_general_ui():
    return ui.div(
        ui.h4("Partizipation Allgemein", class_="my-survey-title"),
        ui.p(
            """
            Die folgenden Fragen zielen allgemein auf die Möglichkeit ab, das Lernen und Lehren in der Vorlesung
            mitzubestimmen. Hier geht es nur um die allgemeine Möglichkeit. Zu den einzelnen Möglichkeiten gibt es
            eigene, kurze Umfragen, um diese besser vergleichen zu können. 
            """
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round2_count_students_desc_general"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round2_count_teachers_desc_general"),
                ui.output_ui("round2_id_teachers_desc_general"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round2_count_lectures_desc_general"),
                ui.output_ui("round2_id_lectures_desc_general"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round2_no_data_desc_general"),

        ui.layout_columns(
            ui.h5("Lernen und Lehren allgemein"),
            ui.output_plot("round2_plot_haltung_likert_desc_general"),
            ui.div(
                ui.div(get_label("AA02_01"), class_="text-center fw-bold"),
                ui.output_plot("round2_plot_haltung_hist_desc_general"),
            ),

            ui.h5("Mitbestimmung in der Vorlesung"),
            ui.output_plot("round2_plot_mitbestimmung_likert_desc_general"),
            ui.output_data_frame("round2_df_freitext_desc_general"),
            
            col_widths = (12, 8, 4, 12, 8, 4),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Learning Objectives
#------------------------------------------------------------------------------
def round2_desc_objectives_ui():
    return ui.div(
        ui.h4("Umfrage zu den Lernzielen", class_="my-survey-title"),
        ui.p(
            """
            In der ersten Vorlesungsstunde hatten die Studierenden die Möglichkeit, eine Umfrage zu ihren Erwartungen
            an die Vorlesung und zu ihren persönlichen Lernzielen auszufüllen. In dieser Umfrage wollten wir wissen,
            inwiefern sie diese Möglichkeit genutzt haben und welche Eindrücke sie hierzu haben.
            """
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round2_count_students_desc_objectives"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round2_count_teachers_desc_objectives"),
                ui.output_ui("round2_id_teachers_desc_objectives"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round2_count_lectures_desc_objectives"),
                ui.output_ui("round2_id_lectures_desc_objectives"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round2_no_data_desc_objectives"),

        ui.layout_columns(
            ui.h5("Allgemeiner Nutzen"),
            ui.output_plot("round2_plot_nutzen_likert_desc_objectives", height="330px"),

            ui.h5("Tatsächliche Umsetzung"),
            ui.output_plot("round2_plot_umsetzung_likert_desc_objectives", height="500px"),

            ui.div(
                ui.h5("Freitextantworten"),
                ui.output_data_frame("round2_df_freitext_desc_objectives"),
            ),
            col_widths = (12, 12, 12, 12, 12),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Assessment Criteria
#------------------------------------------------------------------------------
def round2_desc_assessment_ui():
    return ui.div(
        ui.h4("Umfrage zur Prüfungsaufgabe", class_="my-survey-title"),
        ui.p(
            """
            Am Anfang des Semesters konnten die Studierende am Ende des Aufgabenblatts eine Umfrage zur Portfolioaufgabe
            ausfüllen. Unter anderem ging es darin auch warum, wie diese bewertet werden soll. In dieser Umfrage wollten
            wir wissen, inwiefern sie diese Möglichkeit genutzt haben und welche Eindrücke sie hierzu haben.
            """
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round2_count_students_desc_assessment"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round2_count_teachers_desc_assessment"),
                ui.output_ui("round2_id_teachers_desc_assessment"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round2_count_lectures_desc_assessment"),
                ui.output_ui("round2_id_lectures_desc_assessment"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round2_no_data_desc_assessment"),

        ui.layout_columns(
            ui.h5("Allgemeiner Nutzen"),
            ui.output_plot("round2_plot_nutzen_likert_desc_assessment", height="330px"),

            ui.h5("Tatsächliche Umsetzung"),
            ui.output_plot("round2_plot_umsetzung_likert_desc_assessment", height="500px"),

            ui.div(
                ui.h5("Freitextantworten"),
                ui.output_data_frame("round2_df_freitext_desc_assessment"),
            ),
            col_widths = (12, 12, 12, 12, 12),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Reflection Questions
#------------------------------------------------------------------------------
def round2_desc_reflection_ui():
    return ui.div(
        ui.h4("Reflexionsfragen nach jeder Vorlesungen", class_="my-survey-title"),
        ui.p(
            """
            Am Ende jeder Vorlesung hatten die Studierenden jeweils ein paar Minuten Zeit, um eine kurze Umfrage zur Vorlesung
            auszufüllen. Diese beinhaltete sowohl Reflexionsfragen als auch Wünsche für die nächste Vorlesung. In dieser Umfrage
            wollten wir wissen, inwiefern sie diese Möglichkeit genutzt haben und welche Eindrücke sie hierzu haben.
            """
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round2_count_students_desc_reflection"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round2_count_teachers_desc_reflection"),
                ui.output_ui("round2_id_teachers_desc_reflection"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round2_count_lectures_desc_reflection"),
                ui.output_ui("round2_id_lectures_desc_reflection"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round2_no_data_desc_reflection"),

        ui.layout_columns(
            ui.h5("Allgemeiner Nutzen"),
            ui.output_plot("round2_plot_nutzen_likert_desc_reflection", height="330px"),

            ui.h5("Tatsächliche Umsetzung"),
            ui.output_plot("round2_plot_umsetzung_likert_desc_reflection", height="500px"),

            ui.div(
                ui.h5("Freitextantworten"),
                ui.output_data_frame("round2_df_freitext_desc_reflection"),
            ),
            col_widths = (12, 12, 12, 12, 12),
        ),
        class_="my-flex-with-gaps",
    )

#==============================================================================
# SERVER
#==============================================================================

#------------------------------------------------------------------------------
# All Together
#------------------------------------------------------------------------------
def round2_server(input, output, session):
    round2_survey3_server(input, output, session)
    round2_desc_general_server(input, output, session)
    round2_desc_objectives_server(input, output, session)
    round2_desc_assessment_server(input, output, session)
    round2_desc_reflection_server(input, output, session)

#------------------------------------------------------------------------------
# Semester End Survey
#------------------------------------------------------------------------------
def round2_survey3_server(input, output, session):
    @reactive.calc
    def round2_filtered_surveys3():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = [f"R2-{teacher}-{lecture}" for teacher in teachers for lecture in lectures]
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round2_student3"]:
            selected = correlation_filters["round2_student3"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round2_count_students3():
        try:
            return round2_filtered_surveys3().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_count_teachers3():
        try:
            return round2_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_teachers3():
        try:
            return ", ".join(round2_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_count_lectures3():
        try:
            return round2_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_lectures3():
        try:
            return ", ".join(round2_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_no_data3():
        if round2_filtered_surveys3().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def round2_plot_umsetzung_likert():
        return plot_likert_chart(input, round2_filtered_surveys3(),
                                 "R201_01", "R201_02", "R201_03", "R201_04", "R201_05",
                                 width = 0.4)
    
    @render.plot
    def round2_plot_wirkung_likert():
        return plot_likert_chart(input, round2_filtered_surveys3(),
                                 "R202_02", "R202_03", "R202_04", "R202_05", "R202_06",
                                 width = 0.4)
    
    @render.plot
    def round2_plot_sonstiges_likert():
        return plot_likert_chart(input, round2_filtered_surveys3(),
                                 "R204_01",
                                 width = 0.4)
    
    @render.data_frame
    def round2_df_freitext():
        df = round2_filtered_surveys3()[["R205_01"]].astype(str).copy()
        df = df[df["R205_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"R205_01": get_label("R205_01")})
        return render.DataGrid(df, width="100%", height="400px")
    
    @reactive.effect
    @reactive.event(input.btn_round2_ai_summary_freitext)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("R205_01")),
            ui.output_ui("round2_ai_summary_freitext"),
                title      = "Zusammenfassung der Antworten",
                easy_close = True,
                size       = "xl",
                footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def round2_ai_summary_freitext():
        df      = round2_filtered_surveys3()
        var     = "R205_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )

#------------------------------------------------------------------------------
# DESCH2 Participation in General
#------------------------------------------------------------------------------
def round2_desc_general_server(input, output, session):
    @reactive.calc
    def round2_filtered_surveys_desc_general():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = []

        if "DESC" in teachers and "VERTSYS" in lectures:
            questnnrs = ["R2-DESC-VERTSYS-Allgemein"]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round2_student-DESC_general"]:
            selected = correlation_filters["round2_student-DESC_general"][var].get()
            
            if selected:
                if var == "AA02_01":
                    conditions.append(data["answers"][var] >= selected[0])
                    conditions.append(data["answers"][var] <= selected[1])
                else:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round2_count_students_desc_general():
        try:
            return round2_filtered_surveys_desc_general().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_count_teachers_desc_general():
        try:
            return round2_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_teachers_desc_general():
        try:
            return ", ".join(round2_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_count_lectures_desc_general():
        try:
            return round2_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_lectures_desc_general():
        try:
            return ", ".join(round2_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_no_data_desc_general():
        if round2_filtered_surveys_desc_general().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def round2_plot_haltung_likert_desc_general():
        return plot_likert_chart(input, round2_filtered_surveys_desc_general(),
                                 "AA01_01", "AA01_02", "AA01_03", "AA01_04",
                                 width = 0.4)

    @render.plot
    def round2_plot_haltung_hist_desc_general():
        fig, ax = plt.subplots()
        density = False
        df      = round2_filtered_surveys_desc_general()["AA02_01"].dropna()

        if input.number_format() == "percent":
            density = True
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        ax.hist(df, 11, density=density)
        ax.set_xlabel("Grad der Mitgestaltung")
        ax.set_ylabel("Anzahl Antworten")

        return fig
    
    @render.plot
    def round2_plot_mitbestimmung_likert_desc_general():
        return plot_likert_chart(input, round2_filtered_surveys_desc_general(),
                                 "AA03_01", "AA03_02", "AA03_03", "AA03_04",
                                 width = 0.4)
    
    @render.data_frame
    def round2_df_freitext_desc_general():
        df = round2_filtered_surveys_desc_general()[["AA04_01"]].astype(str).copy()
        df = df[df["AA04_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"AA04_01": get_label("AA04_01")})
        return render.DataGrid(df, width="100%", height="400px")

#------------------------------------------------------------------------------
# DESCH2 Learning Objectives
#------------------------------------------------------------------------------
def round2_desc_objectives_server(input, output, session):
    @reactive.calc
    def round2_filtered_surveys_desc_objectives():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = []

        if "DESC" in teachers and "VERTSYS" in lectures:
            questnnrs = ["R2-DESC-VERTSYS-Lernziele"]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round2_student-DESC_specific"]:
            selected = correlation_filters["round2_student-DESC_specific"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round2_count_students_desc_objectives():
        try:
            return round2_filtered_surveys_desc_objectives().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_count_teachers_desc_objectives():
        try:
            return round2_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_teachers_desc_objectives():
        try:
            return ", ".join(round2_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_count_lectures_desc_objectives():
        try:
            return round2_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_lectures_desc_objectives():
        try:
            return ", ".join(round2_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_no_data_desc_objectives():
        if round2_filtered_surveys_desc_objectives().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def round2_plot_nutzen_likert_desc_objectives():
        return plot_likert_chart(input, round2_filtered_surveys_desc_objectives(),
                                 "AS01_01", "AS01_02", "AS01_03",
                                 width = 0.4)

    @render.plot
    def round2_plot_umsetzung_likert_desc_objectives():
        return plot_likert_chart(input, round2_filtered_surveys_desc_objectives(),
                                 "AS02_01", "AS02_02", "AS02_03", "AS02_04", "AS02_05",
                                 width = 0.4)

    @render.data_frame
    def round2_df_freitext_desc_objectives():
        try:
            df = round2_filtered_surveys_desc_objectives()[["AS03_01", "AS04_01"]].fillna("").astype(str).copy()
            df = df[df[["AS03_01", "AS04_01"]].apply(lambda x: x.str.len() >= 3).any(axis=1)]

            df = df.rename(
                columns={
                    "AS03_01": get_label("AS03_01"),
                    "AS04_01": get_label("AS04_01"),
                }
            )

            return render.DataTable(df, width="100%")
        except KeyError:
                pass

#------------------------------------------------------------------------------
# DESCH2 Assessment Criteria
#------------------------------------------------------------------------------
def round2_desc_assessment_server(input, output, session):
    @reactive.calc
    def round2_filtered_surveys_desc_assessment():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = []

        if "DESC" in teachers and "VERTSYS" in lectures:
            questnnrs = ["R2-DESC-VERTSYS-Pruefungsaufgabe"]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round2_student-DESC_specific"]:
            selected = correlation_filters["round2_student-DESC_specific"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round2_count_students_desc_assessment():
        try:
            return round2_filtered_surveys_desc_assessment().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_count_teachers_desc_assessment():
        try:
            return round2_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_teachers_desc_assessment():
        try:
            return ", ".join(round2_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_count_lectures_desc_assessment():
        try:
            return round2_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_lectures_desc_assessment():
        try:
            return ", ".join(round2_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_no_data_desc_assessment():
        if round2_filtered_surveys_desc_assessment().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def round2_plot_nutzen_likert_desc_assessment():
        return plot_likert_chart(input, round2_filtered_surveys_desc_assessment(),
                                 "AS01_01", "AS01_02", "AS01_03",
                                 width = 0.4)

    @render.plot
    def round2_plot_umsetzung_likert_desc_assessment():
        return plot_likert_chart(input, round2_filtered_surveys_desc_assessment(),
                                 "AS02_01", "AS02_02", "AS02_03", "AS02_04", "AS02_05",
                                 width = 0.4)
    
    @render.data_frame
    def round2_df_freitext_desc_assessment():
        try:
            df = round2_filtered_surveys_desc_assessment()[["AS03_01", "AS04_01"]].fillna("").astype(str).copy()
            df = df[df[["AS03_01", "AS04_01"]].apply(lambda x: x.str.len() >= 3).any(axis=1)]

            df = df.rename(
                columns={
                    "AS03_01": get_label("AS03_01"),
                    "AS04_01": get_label("AS04_01"),
                }
            )

            return render.DataTable(df, width="100%")
        except KeyError:
                pass

#------------------------------------------------------------------------------
# DESCH2 Reflection Questions
#------------------------------------------------------------------------------
def round2_desc_reflection_server(input, output, session):
    @reactive.calc
    def round2_filtered_surveys_desc_reflection():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = []

        if "DESC" in teachers and "VERTSYS" in lectures:
            questnnrs = ["R2-DESC-VERTSYS-Reflexion"]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round2_student-DESC_specific"]:
            selected = correlation_filters["round2_student-DESC_specific"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round2_count_students_desc_reflection():
        try:
            return round2_filtered_surveys_desc_reflection().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_count_teachers_desc_reflection():
        try:
            return round2_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_teachers_desc_reflection():
        try:
            return ", ".join(round2_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_count_lectures_desc_reflection():
        try:
            return round2_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round2_id_lectures_desc_reflection():
        try:
            return ", ".join(round2_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round2_no_data_desc_reflection():
        if round2_filtered_surveys_desc_reflection().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def round2_plot_nutzen_likert_desc_reflection():
        return plot_likert_chart(input, round2_filtered_surveys_desc_reflection(),
                                 "AS01_01", "AS01_02", "AS01_03",
                                 width = 0.4)

    @render.plot
    def round2_plot_umsetzung_likert_desc_reflection():
        return plot_likert_chart(input, round2_filtered_surveys_desc_reflection(),
                                 "AS02_01", "AS02_02", "AS02_03", "AS02_04", "AS02_05",
                                 width = 0.4)
    
    @render.data_frame
    def round2_df_freitext_desc_reflection():
        try:
            df = round2_filtered_surveys_desc_reflection()[["AS03_01", "AS04_01"]].fillna("").astype(str).copy()
            df = df[df[["AS03_01", "AS04_01"]].apply(lambda x: x.str.len() >= 3).any(axis=1)]

            df = df.rename(
                columns={
                    "AS03_01": get_label("AS03_01"),
                    "AS04_01": get_label("AS04_01"),
                }
            )

            return render.DataTable(df, width="100%")
        except KeyError:
                pass
