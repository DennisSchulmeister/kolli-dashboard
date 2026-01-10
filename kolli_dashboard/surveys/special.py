# Forschungsprojekt KoLLI: Dashboard
# © 2025 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from ..ai_llm import ai_conversation, ai_conversation_available, ai_message
from ..data   import correlation_filters, data, get_label, plot_likert_chart
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
icon_answers  = faicons.icon_svg("chalkboard-user", width="50px")
icon_yes      = faicons.icon_svg("check",           width="50px")
icon_no       = faicons.icon_svg("xmark",           width="25px")

def special_ui():
    return [
        ui.h4("Runde 2 – Studentische Evaluation"),
        ui.navset_pill(
            ui.nav_panel("Rinde 1: DIRA Lerntagebücher", ui.div(special_dira_r1_special_ui(), class_="mt-4")),
            ui.nav_panel("Runde 2: DESC Allgemein", ui.div(special_desc_r2_general_ui(), class_="mt-4")),
            ui.nav_panel("Runde 2: DESC Lernziele", ui.div(special_desc_r2_objectives_ui(), class_="mt-4")),
            ui.nav_panel("Runde 2: DESC Prüfungsaufgabe", ui.div(special_desc_r2_assessment_ui(), class_="mt-4")),
            ui.nav_panel("Runde 2: DESC Reflexionsfragen", ui.div(special_desc_r2_reflection_ui(), class_="mt-4")),
            ui.nav_panel("Innovativer Lernraum", ui.div(special_learning_roomui(), class_="mt-4")),
        ),
    ]

#------------------------------------------------------------------------------
# DIRA2 Learning Diaries
#------------------------------------------------------------------------------
def special_dira_r1_special_ui():
    return ui.div(
        ui.h4("DIRA Lerntagebücher / Zwischenumfrage", class_="my-survey-title"),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round1_count_students_dira2_special"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("round1_count_courses_dira2_special"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round1_count_teachers_dira2_special"),
                ui.output_ui("round1_id_teachers_dira2_special"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round1_count_lectures_dira2_special"),
                ui.output_ui("round1_id_lectures_dira2_special"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round1_no_data_dira2_special"),
        ui.output_plot("round1_plot_likert_dira2_special"),
        ui.div(
            ui.input_action_button(
                "btn_round1_ai_summary_dira2_special",
                "KI-Zusammenfassung",
                class_ = f"{ai_button_class}",
            ),
        ),
        ui.output_data_frame("round1_df_freetext_dira2_special"),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Participation in General
#------------------------------------------------------------------------------
def special_desc_r2_general_ui():
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
                ui.output_ui("special_count_students_desc_general"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("special_count_teachers_desc_general"),
                ui.output_ui("special_id_teachers_desc_general"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("special_count_lectures_desc_general"),
                ui.output_ui("special_id_lectures_desc_general"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("special_no_data_desc_general"),

        ui.layout_columns(
            ui.h5("Lernen und Lehren allgemein"),
            ui.output_plot("special_plot_haltung_likert_desc_general"),
            ui.div(
                ui.div(get_label("AA02_01"), class_="text-center fw-bold"),
                ui.output_plot("special_plot_haltung_hist_desc_general"),
            ),

            ui.h5("Mitbestimmung in der Vorlesung"),
            ui.output_plot("special_plot_mitbestimmung_likert_desc_general"),
            ui.output_data_frame("special_df_freitext_desc_general"),
            
            col_widths = (12, 8, 4, 12, 8, 4),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Learning Objectives
#------------------------------------------------------------------------------
def special_desc_r2_objectives_ui():
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
                ui.output_ui("special_count_students_desc_objectives"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("special_count_teachers_desc_objectives"),
                ui.output_ui("special_id_teachers_desc_objectives"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("special_count_lectures_desc_objectives"),
                ui.output_ui("special_id_lectures_desc_objectives"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("special_no_data_desc_objectives"),

        ui.layout_columns(
            ui.h5("Allgemeiner Nutzen"),
            ui.output_plot("special_plot_nutzen_likert_desc_objectives", height="330px"),

            ui.h5("Tatsächliche Umsetzung"),
            ui.output_plot("special_plot_umsetzung_likert_desc_objectives", height="500px"),

            ui.div(
                ui.h5("Freitextantworten"),
                ui.output_data_frame("special_df_freitext_desc_objectives"),
            ),
            col_widths = (12, 12, 12, 12, 12),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Assessment Criteria
#------------------------------------------------------------------------------
def special_desc_r2_assessment_ui():
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
                ui.output_ui("special_count_students_desc_assessment"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("special_count_teachers_desc_assessment"),
                ui.output_ui("special_id_teachers_desc_assessment"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("special_count_lectures_desc_assessment"),
                ui.output_ui("special_id_lectures_desc_assessment"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("special_no_data_desc_assessment"),

        ui.layout_columns(
            ui.h5("Allgemeiner Nutzen"),
            ui.output_plot("special_plot_nutzen_likert_desc_assessment", height="330px"),

            ui.h5("Tatsächliche Umsetzung"),
            ui.output_plot("special_plot_umsetzung_likert_desc_assessment", height="500px"),

            ui.div(
                ui.h5("Freitextantworten"),
                ui.output_data_frame("special_df_freitext_desc_assessment"),
            ),
            col_widths = (12, 12, 12, 12, 12),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DESCH2 Reflection Questions
#------------------------------------------------------------------------------
def special_desc_r2_reflection_ui():
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
                ui.output_ui("special_count_students_desc_reflection"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("special_count_teachers_desc_reflection"),
                ui.output_ui("special_id_teachers_desc_reflection"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("special_count_lectures_desc_reflection"),
                ui.output_ui("special_id_lectures_desc_reflection"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("special_no_data_desc_reflection"),

        ui.layout_columns(
            ui.h5("Allgemeiner Nutzen"),
            ui.output_plot("special_plot_nutzen_likert_desc_reflection", height="330px"),

            ui.h5("Tatsächliche Umsetzung"),
            ui.output_plot("special_plot_umsetzung_likert_desc_reflection", height="500px"),

            ui.div(
                ui.h5("Freitextantworten"),
                ui.output_data_frame("special_df_freitext_desc_reflection"),
            ),
            col_widths = (12, 12, 12, 12, 12),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# Innovative Learning Room
#------------------------------------------------------------------------------
def special_learning_roomui():
    return ui.div(
        ui.h4("Innovativer Lernraum"),
        ui.p(
            """
            An der DHBW Karlsruhe gibt es einen innovativen Lernraum (A473), der durch seine Ausstattung flexible und
            kreative Arbeitsmöglichkeiten bietet. Das Konzept wurde im Studiengang Wirtschaftsinformatik gemeinsam mit
            Studierenden entworfen. In dieser Umfrage, die im Januar und Februar 2025 unter Lehrenden durchgeführt wurde,
            sollten Ideen, Erfahrungen und Wünsche erhoben werden, um weitere Lernräume einzurichten.
            """
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Teilnehmer",
                ui.output_ui("count_answers_lr1"),
                showcase = icon_answers,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Raum A473 bekannt",
                ui.output_ui("count_knowing_lr1"),
                showcase = icon_yes,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Raum A473 nicht bekannt",
                ui.output_ui("count_not_knowing_lr1"),
                showcase = icon_no,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("no_data_lr1"),

        ui.layout_columns(
            ui.h5("Raumnutzung"),

            ui.h6(get_label("IL03")),
            ui.output_plot("plot_usage_likert_lr1", height="400px"),
            ui.output_data_frame("df_usage_freetext_lr1"),
            
            ui.h6(get_label("IL05")),
            ui.output_plot("plot_imagination_likert_lr1", height="400px"),
            ui.output_data_frame("df_imagination_freetext_lr1"),
            
            col_widths = (12, 12, 8, 4, 12, 8, 4),
        ),

        ui.layout_columns(
            ui.h5("Raumgestaltung"),

            ui.h6(get_label("IL06")),
            ui.output_plot("plot_aspects_likert_lr1", height="350px"),
            ui.output_data_frame("df_aspects_freetext_lr1"),

            ui.h6(get_label("IL08")),
            ui.output_plot("plot_colors_likert_lr1", height="280px"),
            ui.output_data_frame("df_colors_freetext_lr1"),

            ui.h6(get_label("IL09")),
            ui.output_plot("plot_accessibility_likert_lr1", height="350px"),
            ui.output_data_frame("df_accessibility_freetext_lr1"),

            col_widths = (12, 12, 8, 4, 12, 8, 4, 12, 8, 4),
        ),

        ui.layout_columns(
            ui.h5("Raumausstattung"),

            ui.h6(get_label("IL10")),
            ui.output_plot("plot_digital_tools_likert_lr1", height="480px"),
            ui.output_data_frame("df_digital_tools_freetext_lr1"),

            ui.h6(get_label("IL12")),
            ui.output_plot("plot_digital_ressources_likert_lr1", height="280px"),
            ui.output_data_frame("df_digital_ressources_freetext_lr1"),

            ui.h6(get_label("IL13")),
            ui.output_plot("plot_other_equipment_likert_lr1", height="880px"),
            ui.output_data_frame("df_other_equipment_freetext_lr1"),

            col_widths = (12, 12, 8, 4, 12, 8, 4, 12, 8, 4),
        ),

        ui.div(
            ui.h5("Sonstiges"),
            ui.div(
                ui.div(
                    ui.input_action_button(
                        "btn_ai_summary_others_lr1",
                        "KI-Zusammenfassung",
                        class_ = f"{ai_button_class}",
                    ),
                ),
                ui.output_data_frame("df_others_lr1"),
                class_="my-flex-with-gaps",
            ),
        ),

        class_="my-flex-with-gaps",
    )

#==============================================================================
# SERVER
#==============================================================================

#------------------------------------------------------------------------------
# All Together
#------------------------------------------------------------------------------
def special_server(input, output, session):
    special_dira_r1_special_server(input, output, session)
    special_desc_r2_general_server(input, output, session)
    special_desc_r2_objectives_server(input, output, session)
    special_desc_r2_assessment_server(input, output, session)
    special_desc_r2_reflection_server(input, output, session)
    special_learning_roomserver(input, output, session)

#------------------------------------------------------------------------------
# DIRA2 Learning Diaries
#------------------------------------------------------------------------------
def special_dira_r1_special_server(input, output, session):
    @reactive.calc
    def round1_filtered_surveys_dira2_special():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = []

        if "DIRA" in teachers and "PROG1" in lectures:
            questnnrs = ["R1-DIRA-PROG1-2-special"]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["special_DIRA_r1"]:
            selected = correlation_filters["special_DIRA_r1"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round1_count_students_dira2_special():
        try:
            return round1_filtered_surveys_dira2_special().shape[0]
        except KeyError:
            return 0

    @render.text
    def round1_count_courses_dira2_special():
        try:
            return round1_filtered_surveys_dira2_special()["STARTED"].dt.date.unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_count_teachers_dira2_special():
        try:
            return round1_filtered_surveys_dira2_special()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_id_teachers_dira2_special():
        try:
            return ", ".join(round1_filtered_surveys_dira2_special()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""
    
    @render.text
    def round1_count_lectures_dira2_special():
        try:
            return round1_filtered_surveys_dira2_special()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_id_lectures_dira2_special():
        try:
            return ", ".join(round1_filtered_surveys_dira2_special()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""
        
    @render.text
    def round1_no_data_dira2_special():
        if round1_filtered_surveys_dira2_special().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."
    
    @render.data_frame
    def round1_df_freetext_dira2_special():
        try:
            df = round1_filtered_surveys_dira2_special()[["DR01_01", "DR02_01", "DR03_01", "DR04_01", "DR05_01"]].astype(str).copy()
            df = df[df[["DR01_01", "DR02_01", "DR03_01", "DR04_01", "DR05_01"]].apply(lambda x: x.str.len() >= 3).any(axis=1)]

            df = df.rename(
                columns={
                    "DR01_01": get_label("DR01_01"),
                    "DR02_01": get_label("DR02_01"),
                    "DR03_01": get_label("DR03_01"),
                    "DR04_01": get_label("DR04_01"),
                    "DR05_01": get_label("DR05_01"),
                }
            )

            return render.DataTable(df, width="100%")
        except KeyError:
                pass
    
    @render.plot
    def round1_plot_likert_dira2_special():
        return plot_likert_chart(input, round1_filtered_surveys_dira2_special(), "DR06_01", "DR06_08")
    
    @reactive.effect
    @reactive.event(input.btn_round1_ai_summary_dira2_special)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Beim ersten Klick auf eine Frage bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.navset_pill(
                ui.nav_panel("Frage 1",
                    ui.div(
                        ui.h6(get_label("DR01_01")),
                        ui.output_ui("round1_ai_summary_q1_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 2",
                    ui.div(
                        ui.h6(get_label("DR02_01")),
                        ui.output_ui("round1_ai_summary_q2_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 3",
                    ui.div(
                        ui.h6(get_label("DR03_01")),
                        ui.output_ui("round1_ai_summary_q3_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 4",
                    ui.div(
                        ui.h6(get_label("DR04_01")),
                        ui.output_ui("round1_ai_summary_q4_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 5",
                    ui.div(
                        ui.h6(get_label("DR05_01")),
                        ui.output_ui("round1_ai_summary_q5_dira2_special"),
                        class_="mt-4",
                    ),
                ),
            ),
            title      = "Zusammenfassung der Antworten",
            easy_close = True,
            size       = "xl",
            footer     = None,
        )

        ui.modal_show(m)
    
    def round1_ai_summary_dira2_special(var):
        df = round1_filtered_surveys_dira2_special()
        label = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ai_conversation(ai_message(question))

    @render.ui
    def round1_ai_summary_q1_dira2_special():
        return ui.markdown(round1_ai_summary_dira2_special("DR01_01"))
    
    @render.ui
    def round1_ai_summary_q2_dira2_special():
        return ui.markdown(round1_ai_summary_dira2_special("DR02_01"))
    
    @render.ui
    def round1_ai_summary_q3_dira2_special():
        return ui.markdown(round1_ai_summary_dira2_special("DR03_01"))
    
    @render.ui
    def round1_ai_summary_q4_dira2_special():
        return ui.markdown(round1_ai_summary_dira2_special("DR04_01"))
    
    @render.ui
    def round1_ai_summary_q5_dira2_special():
        return ui.markdown(round1_ai_summary_dira2_special("DR05_01"))

#------------------------------------------------------------------------------
# DESCH2 Participation in General
#------------------------------------------------------------------------------
def special_desc_r2_general_server(input, output, session):
    @reactive.calc
    def special_filtered_surveys_desc_general():
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

        for var in correlation_filters["special_DESC_r2_general"]:
            selected = correlation_filters["special_DESC_r2_general"][var].get()
            
            if selected:
                if var == "AA02_01":
                    conditions.append(data["answers"][var] >= selected[0])
                    conditions.append(data["answers"][var] <= selected[1])
                else:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def special_count_students_desc_general():
        try:
            return special_filtered_surveys_desc_general().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_count_teachers_desc_general():
        try:
            return special_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_teachers_desc_general():
        try:
            return ", ".join(special_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_count_lectures_desc_general():
        try:
            return special_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_lectures_desc_general():
        try:
            return ", ".join(special_filtered_surveys_desc_general()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_no_data_desc_general():
        if special_filtered_surveys_desc_general().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def special_plot_haltung_likert_desc_general():
        return plot_likert_chart(input, special_filtered_surveys_desc_general(),
                                 "AA01_01", "AA01_02", "AA01_03", "AA01_04",
                                 width = 0.4)

    @render.plot
    def special_plot_haltung_hist_desc_general():
        fig, ax = plt.subplots()
        density = False
        df      = special_filtered_surveys_desc_general()["AA02_01"].dropna()

        if input.number_format() == "percent":
            density = True
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        ax.hist(df, 11, density=density)
        ax.set_xlabel("Grad der Mitgestaltung")
        ax.set_ylabel("Anzahl Antworten")

        return fig
    
    @render.plot
    def special_plot_mitbestimmung_likert_desc_general():
        return plot_likert_chart(input, special_filtered_surveys_desc_general(),
                                 "AA03_01", "AA03_02", "AA03_03", "AA03_04",
                                 width = 0.4)
    
    @render.data_frame
    def special_df_freitext_desc_general():
        df = special_filtered_surveys_desc_general()[["AA04_01"]].astype(str).copy()
        df = df[df["AA04_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"AA04_01": get_label("AA04_01")})
        return render.DataGrid(df, width="100%", height="400px")

#------------------------------------------------------------------------------
# DESCH2 Learning Objectives
#------------------------------------------------------------------------------
def special_desc_r2_objectives_server(input, output, session):
    @reactive.calc
    def special_filtered_surveys_desc_objectives():
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

        for var in correlation_filters["special_DESC_r2_specific"]:
            selected = correlation_filters["special_DESC_r2_specific"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def special_count_students_desc_objectives():
        try:
            return special_filtered_surveys_desc_objectives().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_count_teachers_desc_objectives():
        try:
            return special_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_teachers_desc_objectives():
        try:
            return ", ".join(special_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_count_lectures_desc_objectives():
        try:
            return special_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_lectures_desc_objectives():
        try:
            return ", ".join(special_filtered_surveys_desc_objectives()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_no_data_desc_objectives():
        if special_filtered_surveys_desc_objectives().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def special_plot_nutzen_likert_desc_objectives():
        return plot_likert_chart(input, special_filtered_surveys_desc_objectives(),
                                 "AS01_01", "AS01_02", "AS01_03",
                                 width = 0.4)

    @render.plot
    def special_plot_umsetzung_likert_desc_objectives():
        return plot_likert_chart(input, special_filtered_surveys_desc_objectives(),
                                 "AS02_01", "AS02_02", "AS02_03", "AS02_04", "AS02_05",
                                 width = 0.4)

    @render.data_frame
    def special_df_freitext_desc_objectives():
        try:
            df = special_filtered_surveys_desc_objectives()[["AS03_01", "AS04_01"]].fillna("").astype(str).copy()
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
def special_desc_r2_assessment_server(input, output, session):
    @reactive.calc
    def special_filtered_surveys_desc_assessment():
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

        for var in correlation_filters["special_DESC_r2_specific"]:
            selected = correlation_filters["special_DESC_r2_specific"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def special_count_students_desc_assessment():
        try:
            return special_filtered_surveys_desc_assessment().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_count_teachers_desc_assessment():
        try:
            return special_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_teachers_desc_assessment():
        try:
            return ", ".join(special_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_count_lectures_desc_assessment():
        try:
            return special_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_lectures_desc_assessment():
        try:
            return ", ".join(special_filtered_surveys_desc_assessment()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_no_data_desc_assessment():
        if special_filtered_surveys_desc_assessment().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def special_plot_nutzen_likert_desc_assessment():
        return plot_likert_chart(input, special_filtered_surveys_desc_assessment(),
                                 "AS01_01", "AS01_02", "AS01_03",
                                 width = 0.4)

    @render.plot
    def special_plot_umsetzung_likert_desc_assessment():
        return plot_likert_chart(input, special_filtered_surveys_desc_assessment(),
                                 "AS02_01", "AS02_02", "AS02_03", "AS02_04", "AS02_05",
                                 width = 0.4)
    
    @render.data_frame
    def special_df_freitext_desc_assessment():
        try:
            df = special_filtered_surveys_desc_assessment()[["AS03_01", "AS04_01"]].fillna("").astype(str).copy()
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
def special_desc_r2_reflection_server(input, output, session):
    @reactive.calc
    def special_filtered_surveys_desc_reflection():
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

        for var in correlation_filters["special_DESC_r2_specific"]:
            selected = correlation_filters["special_DESC_r2_specific"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def special_count_students_desc_reflection():
        try:
            return special_filtered_surveys_desc_reflection().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_count_teachers_desc_reflection():
        try:
            return special_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_teachers_desc_reflection():
        try:
            return ", ".join(special_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_count_lectures_desc_reflection():
        try:
            return special_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def special_id_lectures_desc_reflection():
        try:
            return ", ".join(special_filtered_surveys_desc_reflection()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def special_no_data_desc_reflection():
        if special_filtered_surveys_desc_reflection().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def special_plot_nutzen_likert_desc_reflection():
        return plot_likert_chart(input, special_filtered_surveys_desc_reflection(),
                                 "AS01_01", "AS01_02", "AS01_03",
                                 width = 0.4)

    @render.plot
    def special_plot_umsetzung_likert_desc_reflection():
        return plot_likert_chart(input, special_filtered_surveys_desc_reflection(),
                                 "AS02_01", "AS02_02", "AS02_03", "AS02_04", "AS02_05",
                                 width = 0.4)
    
    @render.data_frame
    def special_df_freitext_desc_reflection():
        try:
            df = special_filtered_surveys_desc_reflection()[["AS03_01", "AS04_01"]].fillna("").astype(str).copy()
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
# Innovative Learning Room
#------------------------------------------------------------------------------
def special_learning_roomserver(input, output, session):
    @reactive.calc
    def filtered_surveys_lr1():
        questnnrs  = ["LERNRAUM-1"]
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        return data["answers"][np.logical_and.reduce(conditions)]
    
    @render.text
    def count_answers_lr1():
        try:
            return filtered_surveys_lr1().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def count_knowing_lr1():
        try:
            return filtered_surveys_lr1()["IL02"].value_counts().get(1, 0)
        except KeyError:
            return 0
    
    @render.text
    def count_not_knowing_lr1():
        try:
            return filtered_surveys_lr1()["IL02"].value_counts().get(2, 0)
        except KeyError:
            return 0

    @render.text
    def no_data_lr1():
        if filtered_surveys_lr1().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def plot_usage_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), "IL03_01", "IL03_02", "IL03_03", "IL03_04", "IL03_05", width=0.5)

    @render.data_frame
    def df_usage_freetext_lr1():
        df = filtered_surveys_lr1()[["IL04_06"]].astype(str).copy()
        df = df[df["IL04_06"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL04_06": get_label("IL04_06")})
        return render.DataGrid(df, width="100%")
    
    @render.plot
    def plot_imagination_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), "IL05_01", "IL05_02", "IL05_03", "IL05_04", "IL05_05", width=0.5)

    @render.data_frame
    def df_imagination_freetext_lr1():
        df = filtered_surveys_lr1()[["IL16_06"]].astype(str).copy()
        df = df[df["IL16_06"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL16_06": get_label("IL16_06")})
        return render.DataGrid(df, width="100%")
    
    @render.plot
    def plot_aspects_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), "IL06_01", "IL06_02", "IL06_03", "IL06_04", width=0.5)

    @render.data_frame
    def df_aspects_freetext_lr1():
        df = filtered_surveys_lr1()[["IL07_01"]].astype(str).copy()
        df = df[df["IL07_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL07_01": get_label("IL07_01")})
        return render.DataGrid(df, width="100%")
    
    @render.plot
    def plot_colors_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), "IL08_01", "IL08_02", "IL08_03", width=0.5)

    @render.data_frame
    def df_colors_freetext_lr1():
        df = filtered_surveys_lr1()[["IL15_06"]].astype(str).copy()
        df = df[df["IL15_06"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL15_06": get_label("IL15_06")})
        return render.DataGrid(df, width="100%")
        
    @render.plot
    def plot_accessibility_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), "IL09_01", "IL09_02", "IL09_03", "IL09_04", width=0.5)

    @render.data_frame
    def df_accessibility_freetext_lr1():
        df = filtered_surveys_lr1()[["IL17_06"]].astype(str).copy()
        df = df[df["IL17_06"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL17_06": get_label("IL17_06")})
        return render.DataGrid(df, width="100%")
    

    @render.plot
    def plot_digital_tools_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), "IL10_01", "IL10_02", "IL10_03", "IL10_04", "IL10_05", "IL10_06", width=0.5)

    @render.data_frame
    def df_digital_tools_freetext_lr1():
        df = filtered_surveys_lr1()[["IL11_01"]].astype(str).copy()
        df = df[df["IL11_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL11_01": get_label("IL11_01")})
        return render.DataGrid(df, width="100%")

    @render.plot
    def plot_digital_ressources_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), "IL12_01", "IL12_02", "IL12_03", width=0.5)

    @render.data_frame
    def df_digital_ressources_freetext_lr1():
        df = filtered_surveys_lr1()[["IL18_06"]].astype(str).copy()
        df = df[df["IL18_06"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL18_06": get_label("IL18_06")})
        return render.DataGrid(df, width="100%")
    
    @render.plot
    def plot_other_equipment_likert_lr1():
        return plot_likert_chart(input, filtered_surveys_lr1(), 
                                 "IL13_01", "IL13_02", "IL13_03", "IL13_04", "IL13_05", "IL13_06",
                                 "IL13_07", "IL13_08", "IL13_09", "IL13_10", "IL13_11",
                                 width=0.5)

    @render.data_frame
    def df_other_equipment_freetext_lr1():
        df = pd.DataFrame({"IL19_06": []})  # Missing in data export?!
        df = df.rename(columns={"IL19_06": get_label("IL19_06")})
        return render.DataGrid(df, width="100%")

    @render.data_frame
    def df_others_lr1():
        df = filtered_surveys_lr1()[["IL14_01"]].astype(str).copy()
        df = df[df["IL14_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"IL14_01": get_label("IL14_01")})
        return render.DataGrid(df, width="100%")

    @reactive.effect
    @reactive.event(input.btn_ai_summary_others_lr1)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("IL14_01")),
            ui.output_ui("ai_summary_others_lr1"),
            title      = "Zusammenfassung der Antworten",
            easy_close = True,
            size       = "xl",
            footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def ai_summary_others_lr1():
        df      = filtered_surveys_lr1()
        var     = "IL14_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Lehrenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )
    