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

def control_group_ui():
    return [
        ui.h4("Kontrollgruppe"),
        ui.navset_pill(
            ui.nav_panel("Abschlussumfrage", ui.div(control_group_survey3_ui(), class_="mt-4")),
        ),
    ]

#------------------------------------------------------------------------------
# Semester End Survey
#------------------------------------------------------------------------------
def control_group_survey3_ui():
    return ui.div(
        ui.p(
            """
            Das Umfragedesign entspricht dem von Runde 2.
            """,
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("control_group_count_students3"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("control_group_count_teachers3"),
                ui.output_ui("control_group_id_teachers3"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("control_group_count_lectures3"),
                ui.output_ui("control_group_id_lectures3"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("control_group_no_data3"),

        ui.div(
            ui.h5("Umsetzung der Mitgestaltung"),
            ui.output_plot("control_group_plot_umsetzung_likert", height="450px"),
        ),

        ui.div(
            ui.h5("Wirkung der Mitgestaltung"),
            ui.output_plot("control_group_plot_wirkung_likert", height="450px"),
        ),

        ui.div(
            ui.h5("Sonstiges"),
            ui.output_plot("control_group_plot_sonstiges_likert", height="150px"),
        ),

        ui.div(
            ui.h5("Freitextantworten"),
            ui.div(
                ui.div(
                    ui.input_action_button(
                        "btn_control_group_ai_summary_freitext",
                        "KI-Zusammenfassung",
                        class_ = f"{ai_button_class}",
                    ),
                ),
                ui.output_data_frame("control_group_df_freitext"),
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
def control_group_server(input, output, session):
    control_group_survey3_server(input, output, session)

#------------------------------------------------------------------------------
# Semester End Survey
#------------------------------------------------------------------------------
def control_group_survey3_server(input, output, session):
    @reactive.calc
    def control_group_filtered_surveys3():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = [f"KG-R3-{teacher}-{lecture}" for teacher in teachers for lecture in lectures]
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["control_group_student3"]:
            selected = correlation_filters["control_group_student3"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def control_group_count_students3():
        try:
            return control_group_filtered_surveys3().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def control_group_count_teachers3():
        try:
            return control_group_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def control_group_id_teachers3():
        try:
            return ", ".join(control_group_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def control_group_count_lectures3():
        try:
            return control_group_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def control_group_id_lectures3():
        try:
            return ", ".join(control_group_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def control_group_no_data3():
        if control_group_filtered_surveys3().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

    @render.plot
    def control_group_plot_umsetzung_likert():
        return plot_likert_chart(input, control_group_filtered_surveys3(),
                                 "R201_01", "R201_02", "R201_03", "R201_04", "R201_05",
                                 width = 0.4)
    
    @render.plot
    def control_group_plot_wirkung_likert():
        return plot_likert_chart(input, control_group_filtered_surveys3(),
                                 "R202_02", "R202_03", "R202_04", "R202_05", "R202_06",
                                 width = 0.4)
    
    @render.plot
    def control_group_plot_sonstiges_likert():
        return plot_likert_chart(input, control_group_filtered_surveys3(),
                                 "R204_01",
                                 width = 0.4)
    
    @render.data_frame
    def control_group_df_freitext():
        df = control_group_filtered_surveys3()[["R205_01"]].astype(str).copy()
        df = df[df["R205_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"R205_01": get_label("R205_01")})
        return render.DataGrid(df, width="100%", height="400px")
    
    @reactive.effect
    @reactive.event(input.btn_control_group_ai_summary_freitext)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("R205_01")),
            ui.output_ui("control_group_ai_summary_freitext"),
                title      = "Zusammenfassung der Antworten",
                easy_close = True,
                size       = "xl",
                footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def control_group_ai_summary_freitext():
        df      = control_group_filtered_surveys3()
        var     = "R205_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )
