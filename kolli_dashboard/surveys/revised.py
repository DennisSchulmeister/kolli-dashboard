# Forschungsprojekt KoLLI: Dashboard
# © 2025 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from ..ai_llm import ai_conversation, ai_conversation_available, ai_message
from ..data   import calc_likert_statistics, correlation_filters, data, get_label, plot_likert_chart
from shiny    import reactive, render, ui

import faicons
import pandas as pd
import numpy as np

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

def revised_ui():
    return [
        ui.h4("Runden 2 & 3 – Studentische Evaluation"),
        ui.div(
            ui.p(
                """
                Beginnend mit Runde 2 wurde das Umfragedesign wurde so angepasst, dass nur noch eine summative Abschlussumfrage
                mit den Studierenden am Ende des Semesters durchgeführt wurde. Einzige Ausnahme ist die Vorlesung von DESC, da
                diese zeitlich zu früh lag, und daher mit einer früheren Version des Fragebogens arbeitet. Die Ergebnisse finden
                sich deshalb unter den Spezialumfragen. Die Fragen des neuen Fragebogens sind am Angebot-Nutzen-Wirkungsmodell von
                Helmke ausgerichtet, indem dieses auf die Fragestellung der studentischen Partizipation angewendet wird. Zusätzlich
                wird nach Indikationen zur Wirkung der Partizipation sowie der Gesamtzufriedenheit gefragt, da sich letztere vermutlich
                auch auf alle anderen Antworten abfärbt.
                """,
            ),

            ui.div(
                ui.input_switch("revised_include_r2", "Runde 2", True),
                ui.input_switch("revised_include_r3", "Runde 3", True),
                ui.input_switch("revised_include_kg", "Kontrollgruppe", False),
                class_="my-flex-with-gaps flex-row"
            ),

            ui.layout_column_wrap(
                ui.value_box(
                    "Studierende",
                    ui.output_ui("revised_count_students"),
                    showcase = icon_students,
                    theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
                ),
                ui.value_box(
                    "Lehrende",
                    ui.output_ui("revised_count_teachers"),
                    ui.output_ui("revised_id_teachers"),
                    showcase = icon_teachers,
                    theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
                ),
                ui.value_box(
                    "Veranstaltungen",
                    ui.output_ui("revised_count_lectures"),
                    ui.output_ui("revised_id_lectures"),
                    showcase = icon_lectures,
                    theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
                ),
            ),
            ui.output_ui("revised_no_data"),

            ui.div(
                ui.h5("Umsetzung der Mitgestaltung"),
                ui.output_ui("revised_umsetzung_likert")
            ),

            ui.div(
                ui.h5("Wirkung der Mitgestaltung"),
                ui.output_ui("revised_wirkung_likert")
            ),

            ui.div(
                ui.h5("Sonstiges"),
                ui.output_ui("revised_sonstiges_likert")
            ),

            ui.div(
                ui.h5("Freitextantworten"),
                ui.div(
                    ui.div(
                        ui.input_action_button(
                            "btn_revised_ai_summary_freitext",
                            "KI-Zusammenfassung",
                            class_ = f"{ai_button_class}",
                        ),
                    ),
                    ui.output_data_frame("revised_df_freitext"),
                    class_="my-flex-with-gaps",
                ),
            ),
            class_="my-flex-with-gaps",
        ),
    ]

#==============================================================================
# SERVER
#==============================================================================

#------------------------------------------------------------------------------
# All Together
#------------------------------------------------------------------------------
def revised_server(input, output, session):
    @reactive.calc
    def revised_filtered_surveys3():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = []

        if input.revised_include_r2():
            questnnrs += [f"R2-{teacher}-{lecture}" for teacher in teachers for lecture in lectures]
        if input.revised_include_r3():
            questnnrs += [f"R3-{teacher}-{lecture}" for teacher in teachers for lecture in lectures]
        if input.revised_include_kg():
            questnnrs += [f"KG-R3-{teacher}-{lecture}" for teacher in teachers for lecture in lectures]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["revised"]:
            selected = correlation_filters["revised"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def revised_count_students():
        try:
            return revised_filtered_surveys3().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def revised_count_teachers():
        try:
            return revised_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def revised_id_teachers():
        try:
            return ", ".join(revised_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def revised_count_lectures():
        try:
            return revised_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def revised_id_lectures():
        try:
            return ", ".join(revised_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def revised_no_data():
        if revised_filtered_surveys3().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.ui
    def revised_umsetzung_likert():
        if input.display_type() == "stat":
            return ui.output_data_frame("revised_stats_umsetzung_likert")
        else:
            return ui.output_plot("revised_plot_umsetzung_likert", height="450px")

    @render.data_frame
    def revised_stats_umsetzung_likert():
        return render.DataGrid(
            calc_likert_statistics(input, revised_filtered_surveys3(),
                                   "R201_01", "R201_02", "R201_03", "R201_04", "R201_05"),
            width = "100%",
        )

    @render.plot
    def revised_plot_umsetzung_likert():
        return plot_likert_chart(input, revised_filtered_surveys3(),
                                "R201_01", "R201_02", "R201_03", "R201_04", "R201_05",
                                width = 0.4)
    
    @render.ui
    def revised_wirkung_likert():
        if input.display_type() == "stat":
            return ui.output_data_frame("revised_stats_wirkung_likert")
        else:
            return ui.output_plot("revised_plot_wirkung_likert", height="450px")

    @render.data_frame
    def revised_stats_wirkung_likert():
        return render.DataGrid(
            calc_likert_statistics(input, revised_filtered_surveys3(),
                                   "R202_02", "R202_03", "R202_04", "R202_05", "R202_06"),
            width = "100%",
        )

    @render.plot
    def revised_plot_wirkung_likert():
        return plot_likert_chart(input, revised_filtered_surveys3(),
                                "R202_02", "R202_03", "R202_04", "R202_05", "R202_06",
                                width = 0.4)
    
    @render.ui
    def revised_sonstiges_likert():
        if input.display_type() == "stat":
            return ui.output_data_frame("revised_stats_sonstiges_likert")
        else:
            return ui.output_plot("revised_plot_sonstiges_likert", height="150px")

    @render.data_frame
    def revised_stats_sonstiges_likert():
        return render.DataGrid(
            calc_likert_statistics(input, revised_filtered_surveys3(),
                                   "R204_01"),
            width = "100%",
        )

    @render.plot
    def revised_plot_sonstiges_likert():
        return plot_likert_chart(input, revised_filtered_surveys3(),
                                "R204_01",
                                width = 0.4)

    @render.data_frame
    def revised_df_freitext():
        df = revised_filtered_surveys3()[["R205_01"]].astype(str).copy()
        df = df[df["R205_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"R205_01": get_label("R205_01")})
        return render.DataGrid(df, width="100%", height="400px")
    
    @reactive.effect
    @reactive.event(input.btn_revised_ai_summary_freitext)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Beim ersten Klick auf eine Frage bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.navset_pill(
                ui.nav_panel("Erwähnte Themen",
                    ui.div(
                        ui.h6(get_label("R205_01")),
                        ui.output_ui("revised_ai_summary_freitext_topics"),
                        class_="mt-4",
                    )
                ),
                ui.nav_panel("Interpretation",
                    ui.div(
                        ui.h6(get_label("R205_01")),
                        ui.output_ui("revised_ai_summary_freitext_interpretation"),
                        class_="mt-4",
                    )
                ),
            ),

            title      = "Zusammenfassung der Antworten",
            easy_close = True,
            size       = "xl",
            footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def revised_ai_summary_freitext_topics():
        df      = revised_filtered_surveys3()
        var     = "R205_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = """
                   Stelle dir vor, du schreibst ein wissenschaftliches Paper, in dem über die
                   Forschung zu studentischer Partizipation berichtet wird. Studentische Partizipation
                   heißt hier, dass die Studierenden Einfluss auf die Vorlesung nehmen dürfen, indem
                   sie bei relevanten Fragestellungen in die Entscheidung oder Umsetzung eingebunden
                   werden.
                   """ \
                   f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                   f"{answers}\n\n" \
                   """
                   Bitte extrahiere die Themen, die in den Antworten vorkommen, aber interpretiere
                   die Antworten nicht! Stattdessen erstelle eine Tabelle, die jedes Thema mit einem
                   kurzen Stichwort nennt, die Anzahl der Erwähnungen und ein repräsentatives
                   Beispiel nennt. Beachte aber, dass die Umfrage in unterschiedlichen Vorlesungen
                   durchgeführt wurde, die Kategorien aber möglichst allgemeingültig sein sollten.
                   Fasse daher Kategorien zu einem allgemeinen Oberbegriff zusammen, wenn sie sonst
                   spezifisch für eine Vorlesung wären.
                   
                   Erstelle unterhalb der Tabelle zu Kontrollzwecken eine Auflistung aller Themen
                   und der Aussagen dazu. Du darfst die Aussagen Abkürzen aber nicht umformulieren!
                   """
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )

    @render.ui
    def revised_ai_summary_freitext_interpretation():
        df      = revised_filtered_surveys3()
        var     = "R205_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = """
                   Stelle dir vor, du schreibst ein wissenschaftliches Paper, in dem über die
                   Forschung zu studentischer Partizipation berichtet wird. Studentische Partizipation
                   heißt hier, dass die Studierenden Einfluss auf die Vorlesung nehmen dürfen, indem
                   sie bei relevanten Fragestellungen in die Entscheidung oder Umsetzung eingebunden
                   werden.
                   """ \
                   f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                   f"{answers}\n\n" \
                   """
                   Bitte fasse die Antworten zusammen und interpretiere sie als Textvorschlag
                   für die Findings in diesem Paper. Welche Erkenntnisse lassen sich aus den
                   Antworten ziehen?
                   """
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )