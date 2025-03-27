# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .ai_llm import ai_conversation, ai_conversation_available, ai_message
from .data   import data, get_label, plot_likert_chart, plot_multiple_choice_bar_chart
from shiny   import reactive, render, ui

import faicons
import pandas            as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy             as np

#==============================================================================
# UI Definition
#==============================================================================
ai_button_class = "" if ai_conversation_available() else "d-none"

icon_answers = faicons.icon_svg("chalkboard-user", width="50px")
icon_yes     = faicons.icon_svg("check",           width="50px")
icon_no      = faicons.icon_svg("xmark",           width="25px")

def learning_room_ui():
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

def learning_room_server(input, output, session):
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
    