# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from ..ai_llm import ai_conversation, ai_conversation_available, ai_message
from ..data   import calc_likert_statistics, correlation_filters, data, get_label, plot_likert_chart
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

def round1_ui():
    return [
        ui.h4("Runde 1 – Studentische Evaluation"),
        ui.navset_pill(
            ui.nav_panel("Vorumfrage", ui.div(round1_survey1_ui(), class_="mt-4")),
            ui.nav_panel("Zwischenumfrage", ui.div(round1_survey2_ui(), class_="mt-4")),
            ui.nav_panel("Abschlussumfrage", ui.div(round1_survey3_ui(), class_="mt-4")),
        ),
    ]

#------------------------------------------------------------------------------
# Semester Start Survey
#------------------------------------------------------------------------------
def round1_survey1_ui():
    return ui.div(
        ui.p(
            """
            Die studentische Vorumfrage findet am Anfang des Semesters statt, nachdem den Studierenden
            die Inhalte der Lehrveranstaltung und das KoLLI-Konzept vorgestellt wurden. Sie fragt die
            Haltung der Studierenden zur bevorstehenden Partizipation ab, um zu untersuchen, inwiefern
            sich diese im Lauf des Semesters verändert.
            """,
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round1_count_students1"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("round1_count_courses1"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round1_count_teachers1"),
                ui.output_ui("round1_id_teachers1"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round1_count_lectures1"),
                ui.output_ui("round1_id_lectures1"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round1_no_data1"),
        ui.layout_columns(
            ui.h5("Vorwissen und Interesse"),
            ui.output_ui("round1_vorwissen_likert1"),
            ui.div(
                ui.output_data_frame("round1_df_vorwissen1"),
                ui.input_action_button(
                    "btn_round1_ai_summary_vorwissen1",
                    "KI-Zusammenfassung",
                    class_ = f"mt-4 {ai_button_class}"
                ),
            ),

            ui.h5("Mitgestaltung"),
            ui.output_ui("round1_mitgestaltung_likert1"),
            ui.div(
                ui.div(get_label("V203_01"), class_="text-center fw-bold"),
                ui.output_plot("round1_plot_mitgestaltung_hist1"),
            ),

            ui.div(
                ui.h5("Studentisches Engagement"),
                ui.output_ui("round1_engagement_likert1"),
            ),
            ui.div(
                ui.h5("Sonstige Bemerkungen"),
                ui.div(
                    ui.output_data_frame("round1_df_bemerkungen1"),
                    ui.input_action_button(
                        "btn_round1_ai_summary_bemerkungen1",
                        "KI-Zusammenfassung",
                        class_ = f"mt-4 {ai_button_class}"
                    ),
                ),
            ),
            col_widths = (12, 8, 4, 12, 8, 4, 8, 4),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# Semester Mid Survey
#------------------------------------------------------------------------------
def round1_survey2_ui():
    return ui.div(
        ui.p(
            """
            Die studentische Zwischenumfrage findet innerhalb des Semesters statt, nachdem die Studierenden
            erste Erfahrungen mit dem partizipativen Ansatz gesammelt haben. Sie erhebt die Haltung im
            Vergleich zum Semesterbeginn, die momentane Zufriedenheit und den Unterstützungsbedarf der
            Studierenden.
            """,
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round1_count_students2"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("round1_count_courses2"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round1_count_teachers2"),
                ui.output_ui("round1_id_teachers2"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round1_count_lectures2"),
                ui.output_ui("round1_id_lectures2"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round1_no_data2"),
        ui.layout_columns(
            ui.h5("Klarheit und Überforderung"),
            ui.output_ui("round1_klarheit_likert2"),
            ui.div(
                ui.output_data_frame("round1_df_lehr_lern_innovation2"),
                ui.input_action_button(
                    "btn_round1_ai_summary_lehr_lern_innovation2",
                    "KI-Zusammenfassung",
                    class_=f"mt-4 {ai_button_class}"
                ),
            ),

            ui.h5("Zufriedenheit"),
            ui.output_ui("round1_zufriedenheit_likert2"),
            ui.div(
                ui.output_data_frame("round1_df_unterstuetzung2"),
                ui.input_action_button(
                    "btn_round1_ai_summary_unterstuetzung2",
                    "KI-Zusammenfassung",
                    class_=f"mt-4 {ai_button_class}"
                ),
            ),

            col_widths=(12, 8, 4, 12, 8, 4),
        ),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# Semester End Survey
#------------------------------------------------------------------------------
def round1_survey3_ui():
    return ui.div(
        ui.p(
            """
            Die studentische Abschlussumfrage findet als summative Evaluation am Ende des Semesters statt,
            nachdem die Studierenden die Arbeit an den Lehr-Lern-Innovationen abgeschlossen haben.
            Sie erhebt, wie die Studienrenden die Partizipation empfunden haben und welche Verbesserungen
            vorgenommen werden können.
            """,
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("round1_count_students3"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("round1_count_courses3"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("round1_count_teachers3"),
                ui.output_ui("round1_id_teachers3"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
            ui.value_box(
                "Veranstaltungen",
                ui.output_ui("round1_count_lectures3"),
                ui.output_ui("round1_id_lectures3"),
                showcase = icon_lectures,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("round1_no_data3"),

        ui.div(
            ui.h5("Inhalt der Lehrveranstaltung"),
            ui.output_ui("round1_lv_inhalt_likert3"),
        ),

        ui.div(
            ui.h5("Studentisches Engagement"),
            ui.output_ui("round1_engagement_likert3"),
        ),

        ui.div(
            ui.h5("Beurteilung der Partizipation"),
            ui.output_ui("round1_beurteilung_likert3"),
        ),

        ui.div(
            ui.h5("Lernwirksamkeit der Partizipation"),
            ui.output_ui("round1_lernwirksamkeit_likert3"),
        ),

        ui.div(
            ui.h5("Freitextantworten"),
            ui.div(
                ui.div(
                    ui.input_action_button(
                        "btn_round1_ai_summary_freetext3",
                        "KI-Zusammenfassung",
                        class_ = f"{ai_button_class}",
                    ),
                ),
                ui.output_data_frame("round1_df_freetext3"),
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
def round1_server(input, output, session):
    round1_survey1_server(input, output, session)
    round1_survey2_server(input, output, session)
    round1_survey3_server(input, output, session)

#------------------------------------------------------------------------------
# Semester Start Survey
#------------------------------------------------------------------------------
def round1_survey1_server(input, output, session):
    @reactive.calc
    def round1_filtered_surveys1():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = [f"R1-{teacher}-{lecture}-1" for teacher in teachers for lecture in lectures]
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round1_student1"]:
            selected = correlation_filters["round1_student1"][var].get()
            
            if selected:
                if var == "V203_01":
                    conditions.append(data["answers"][var] >= selected[0])
                    conditions.append(data["answers"][var] <= selected[1])
                else:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round1_count_students1():
        try:
            return round1_filtered_surveys1().shape[0]
        except KeyError:
            return 0

    @render.text
    def round1_count_courses1():
        try:
            df = round1_filtered_surveys1()
            return df.groupby(['QUESTNNR', df['STARTED'].dt.date]).ngroups
        except KeyError:
            return 0
    
    @render.text
    def round1_count_teachers1():
        try:
            return round1_filtered_surveys1()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_round1_id_teachers1():
        try:
            return ", ".join(round1_filtered_surveys1()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round1_count_lectures1():
        try:
            return round1_filtered_surveys1()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_id_lectures1():
        try:
            return ", ".join(round1_filtered_surveys1()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""
        
    @render.text
    def round1_no_data1():
        if round1_filtered_surveys1().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."
    
    @render.data_frame
    def round1_df_vorwissen1():
        df = round1_filtered_surveys1()[["V202_01"]].astype(str).copy()
        df = df[df["V202_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"V202_01": get_label("V202_01")})
        return render.DataGrid(df, width="100%", height="400px")

    @render.data_frame
    def round1_df_bemerkungen1():
        df = round1_filtered_surveys1()[["V210_01"]].astype(str).copy()
        df = df[df["V210_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"V210_01": get_label("V210_01")})
        return render.DataGrid(df, width="100%", height="400px")

    @render.plot
    def round1_plot_mitgestaltung_hist1():
        fig, ax = plt.subplots()
        density = False
        df      = round1_filtered_surveys1()["V203_01"].dropna()

        if input.number_format() == "percent":
            density = True
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        ax.hist(df, 11, density=density)
        ax.set_xlabel("Grad der Mitgestaltung")
        ax.set_ylabel("Anzahl Antworten")

        return fig

    @render.ui
    def round1_vorwissen_likert1():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_vorwissen_likert1")
        else:
            return ui.output_plot("round1_plot_vorwissen_likert1")

    @render.plot
    def round1_plot_vorwissen_likert1():
        return plot_likert_chart(input, round1_filtered_surveys1(), "V201_01", "V201_02")

    @render.data_frame
    def round1_stats_vorwissen_likert1():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys1(), "V201_01", "V201_02"),
            width = "100%",
        )
    
    @render.ui
    def round1_mitgestaltung_likert1():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_mitgestaltung_likert1")
        else:
            return ui.output_plot("round1_plot_mitgestaltung_likert1")
        
    @render.plot
    def round1_plot_mitgestaltung_likert1():
        return plot_likert_chart(input, round1_filtered_surveys1(), "V204_01", "V204_02")

    @render.data_frame
    def round1_stats_mitgestaltung_likert1():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys1(), "V204_01", "V204_02"),
            width = "100%",
        )
    
    @render.ui
    def round1_engagement_likert1():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_engagement_likert1")
        else:
            return ui.output_plot("round1_plot_engagement_likert1", height="900px")
        
    @render.plot
    def round1_plot_engagement_likert1():
        return plot_likert_chart(input, round1_filtered_surveys1(),
                                 "VU03_03", "VU03_04",
                                 "V209_01", "V209_02", "V209_03",
                                 "V209_04", "V209_05", "V209_06",
                                 "V209_07", "V209_08", "V209_09",
                                 width = 0.4)

    @render.data_frame
    def round1_stats_engagement_likert1():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys1(),
                                   "VU03_03", "VU03_04",
                                   "V209_01", "V209_02", "V209_03",
                                   "V209_04", "V209_05", "V209_06",
                                   "V209_07", "V209_08", "V209_09",),
            width = "100%",
        )
    
    @reactive.effect
    @reactive.event(input.btn_round1_ai_summary_vorwissen1)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("V202_01")),
            ui.output_ui("round1_ai_summary_vorwissen1"),
                title      = "Zusammenfassung der Antworten",
                easy_close = True,
                size       = "xl",
                footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def round1_ai_summary_vorwissen1():
        df      = round1_filtered_surveys1()
        var     = "V202_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )
    
    @reactive.effect
    @reactive.event(input.btn_round1_ai_summary_bemerkungen1)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("V210_01")),
            ui.output_ui("round1_ai_summary_bemerkungen1"),
                title      = "Zusammenfassung der Antworten",
                easy_close = True,
                size       = "xl",
                footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def round1_ai_summary_bemerkungen1():
        df      = round1_filtered_surveys1()
        var     = "V210_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )
    
#------------------------------------------------------------------------------
# Semester Mid Survey
#------------------------------------------------------------------------------
def round1_survey2_server(input, output, session):
    @reactive.calc
    def round1_filtered_surveys2():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = [f"R1-{teacher}-{lecture}-2" for teacher in teachers for lecture in lectures]
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round1_student2"]:
            selected = correlation_filters["round1_student2"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]

    @render.text
    def round1_count_students2():
        try:
            return round1_filtered_surveys2().shape[0]
        except KeyError:
            return 0

    @render.text
    def round1_count_courses2():
        try:
            df = round1_filtered_surveys2()
            return df.groupby(['QUESTNNR', df['STARTED'].dt.date]).ngroups
        except KeyError:
            return 0
    
    @render.text
    def round1_count_teachers2():
        try:
            return round1_filtered_surveys2()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_id_teachers2():
        try:
            return ", ".join(round1_filtered_surveys2()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""
    
    @render.text
    def round1_count_lectures2():
        try:
            return round1_filtered_surveys2()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_id_lectures2():
        try:
            return ", ".join(round1_filtered_surveys2()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round1_no_data2():
        if round1_filtered_surveys2().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."
    
    @render.data_frame
    def round1_df_lehr_lern_innovation2():
        df = round1_filtered_surveys2()[["ZW06_01"]].astype(str).copy()
        df = df[df["ZW06_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"ZW06_01": get_label("ZW06_01")})
        return render.DataGrid(df, width="100%", height="400px")
    
    @render.data_frame
    def round1_df_unterstuetzung2():
        df = round1_filtered_surveys2()[["ZW05_01"]].astype(str).copy()
        df = df[df["ZW05_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"ZW05_01": get_label("ZW05_01")})
        return render.DataGrid(df, width="100%", height="400px")
    
    @render.ui
    def round1_klarheit_likert2():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_klarheit_likert2")
        else:
            return ui.output_plot("round1_plot_klarheit_likert2")
        
    @render.plot
    def round1_plot_klarheit_likert2():
        return plot_likert_chart(input, round1_filtered_surveys2(), "ZW04_01", "ZW04_02", "ZW04_03", "ZW04_04", width=0.4)
    
    @render.data_frame
    def round1_stats_klarheit_likert2():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys2(), "ZW04_01", "ZW04_02", "ZW04_03", "ZW04_04"),
            width = "100%",
        )

    @render.ui
    def round1_zufriedenheit_likert2():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_zufriedenheit_likert2")
        else:
            return ui.output_plot("round1_plot_zufriedenheit_likert2")
        
    @render.plot
    def round1_plot_zufriedenheit_likert2():
        return plot_likert_chart(input, round1_filtered_surveys2(), "ZW04_05", "ZW04_06", "ZW04_07", "ZW04_08", width=0.4)

    @render.data_frame
    def round1_stats_zufriedenheit_likert2():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys2(), "ZW04_05", "ZW04_06", "ZW04_07", "ZW04_08"),
            width = "100%",
        )

    @reactive.effect
    @reactive.event(input.btn_round1_ai_summary_lehr_lern_innovation2)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("ZW06_01")),
            ui.output_ui("round1_ai_summary_lehr_lern_innovation2"),
                title      = "Zusammenfassung der Antworten",
                easy_close = True,
                size       = "xl",
                footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def round1_ai_summary_lehr_lern_innovation2():
        df      = round1_filtered_surveys2()
        var     = "ZW06_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )

    @reactive.effect
    @reactive.event(input.btn_round1_ai_summary_unterstuetzung2)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("ZW05_01")),
            ui.output_ui("round1_ai_summary_unterstuetzung2"),
                title      = "Zusammenfassung der Antworten",
                easy_close = True,
                size       = "xl",
                footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def round1_ai_summary_unterstuetzung2():
        df      = round1_filtered_surveys2()
        var     = "ZW05_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )

#------------------------------------------------------------------------------
# Semester End Survey
#------------------------------------------------------------------------------
def round1_survey3_server(input, output, session):
    @reactive.calc
    def round1_filtered_surveys3():
        teachers   = input.teachers() or data["teachers"]
        lectures   = input.lectures() or data["lectures"]
        questnnrs  = [f"R1-{teacher}-{lecture}-3" for teacher in teachers for lecture in lectures]
        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        conditions = [
            (data["answers"]["QUESTNNR"].isin(questnnrs)),
            (data["answers"]["STARTED"] >= start_date),
            (data["answers"]["STARTED"] <= end_date),
        ]

        for var in correlation_filters["round1_student3"]:
            selected = correlation_filters["round1_student3"][var].get()
            
            if selected:
                    conditions.append(data["answers"][var].isin(selected))

        return data["answers"][np.logical_and.reduce(conditions)]
    
    @render.text
    def round1_count_students3():
        try:
            return round1_filtered_surveys3().shape[0]
        except KeyError:
            return 0

    @render.text
    def round1_count_courses3():
        try:
            df = round1_filtered_surveys3()
            return df.groupby(['QUESTNNR', df['STARTED'].dt.date]).ngroups
        except KeyError:
            return 0
    
    @render.text
    def round1_count_teachers3():
        try:
            return round1_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_id_teachers3():
        try:
            return ", ".join(round1_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round1_count_lectures3():
        try:
            return round1_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def round1_id_lectures3():
        try:
            return ", ".join(round1_filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[2].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def round1_no_data3():
        if round1_filtered_surveys3().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."
    
    @render.ui
    def round1_lv_inhalt_likert3():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_lv_inhalt_likert3")
        else:
            return ui.output_plot("round1_plot_lv_inhalt_likert3", height="450px")
        
    @render.plot
    def round1_plot_lv_inhalt_likert3(): #450px
        return plot_likert_chart(input, round1_filtered_surveys3(),
                                 "AB03_01", "AB03_02", "AB03_03", "AB03_04", "AB03_05",
                                 width = 0.4)
    
    @render.data_frame
    def round1_stats_lv_inhalt_likert3():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys3(),
                                   "AB03_01", "AB03_02", "AB03_03", "AB03_04", "AB03_05"),
            width = "100%",
        )
    
    @render.ui
    def round1_engagement_likert3():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_engagement_likert3")
        else:
            return ui.output_plot("round1_plot_engagement_likert3", height="800px")
        
    @render.plot
    def round1_plot_engagement_likert3():
        return plot_likert_chart(input, round1_filtered_surveys3(),
                                 "AB07_01", "AB07_02", "AB07_03", "AB07_04",
                                 "AB07_05", "AB07_06", "AB07_07", "AB07_08", "AB07_09",
                                 width = 0.4)
    
    @render.data_frame
    def round1_stats_engagement_likert3():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys3(),
                                   "AB07_01", "AB07_02", "AB07_03", "AB07_04",
                                   "AB07_05", "AB07_06", "AB07_07", "AB07_08", "AB07_09",),
            width = "100%",
        )

    @render.ui
    def round1_beurteilung_likert3():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_beurteilung_likert3")
        else:
            return ui.output_plot("round1_plot_beurteilung_likert3", height="600px")
        
    @render.plot
    def round1_plot_beurteilung_likert3():
        return plot_likert_chart(input, round1_filtered_surveys3(),
                                 "AB09_01", "AB09_02", "AB09_03",
                                 "AB09_04", "AB09_05", "AB09_06", "AB09_07",
                                 width = 0.4)
    
    @render.data_frame
    def round1_stats_beurteilung_likert3():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys3(),
                                   "AB09_01", "AB09_02", "AB09_03",
                                   "AB09_04", "AB09_05", "AB09_06", "AB09_07",),
            width = "100%",
        )

    @render.ui
    def round1_lernwirksamkeit_likert3():
        if input.display_type() == "stat":
            return ui.output_data_frame("round1_stats_lernwirksamkeit_likert3")
        else:
            return ui.output_plot("round1_plot_lernwirksamkeit_likert3", height="400px")
        
    @render.plot
    def round1_plot_lernwirksamkeit_likert3():
        return plot_likert_chart(input, round1_filtered_surveys3(),
                                 "AB14_06", "AB14_07", "AB14_08", "AB14_09",
                                 width = 0.4)

    @render.data_frame
    def round1_stats_lernwirksamkeit_likert3():
        return render.DataGrid(
            calc_likert_statistics(input, round1_filtered_surveys3(),
                                   "AB14_06", "AB14_07", "AB14_08", "AB14_09",),
            width = "100%",
        )
    
    @render.data_frame
    def round1_df_freetext3():
        try:
            df = round1_filtered_surveys3()[["AB01_01", "AB10_01", "AB11_01", "AB15_01", "AB12_01"]].fillna("").astype(str).copy()
            df = df[df[["AB01_01", "AB10_01", "AB11_01", "AB15_01", "AB12_01"]].apply(lambda x: x.str.len() >= 3).any(axis=1)]

            df = df.rename(
                columns={
                    "AB01_01": "Lehr-Lern-Innovation",
                    "AB10_01": "Mehr Unterstützung",
                    "AB11_01": "Über die LV hinausgehende Fähigkeiten",
                    "AB15_01": "Weitere Themen",
                    "AB12_01": "Sonstige Bemerkungen",
                }
            )

            return render.DataTable(df, width="100%")
        except KeyError:
                pass

    @reactive.effect
    @reactive.event(input.btn_round1_ai_summary_freetext3)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Beim ersten Klick auf eine Frage bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.navset_pill(
                ui.nav_panel("Lehr-Lern-Innovation",
                    ui.div(
                        ui.h6(get_label("AB01_01")),
                        ui.output_ui("round1_ai_summary_q1_freetext3"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Unterstützungsbedarf",
                    ui.div(
                        ui.h6(get_label("AB10_01")),
                        ui.output_ui("round1_ai_summary_q2_freetext3"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Fähigkeiten",
                    ui.div(
                        ui.h6(get_label("AB11_01")),
                        ui.output_ui("round1_ai_summary_q3_freetext3"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Weitere Themen",
                    ui.div(
                        ui.h6(get_label("AB15_01")),
                        ui.output_ui("round1_ai_summary_q4_freetext3"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Bemerkungen",
                    ui.div(
                        ui.h6(get_label("AB12_01")),
                        ui.output_ui("round1_ai_summary_q5_freetext3"),
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
    
    def round1_ai_summary_freetext3(var):
        df = round1_filtered_surveys3()
        label = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ai_conversation(ai_message(question))

    @render.ui
    def round1_ai_summary_q1_freetext3():
        return ui.markdown(round1_ai_summary_freetext3("AB01_01"))
    
    @render.ui
    def round1_ai_summary_q2_freetext3():
        return ui.markdown(round1_ai_summary_freetext3("AB10_01"))
    
    @render.ui
    def round1_ai_summary_q3_freetext3():
        return ui.markdown(round1_ai_summary_freetext3("AB11_01"))
    
    @render.ui
    def round1_ai_summary_q4_freetext3():
        return ui.markdown(round1_ai_summary_freetext3("AB15_01"))
    
    @render.ui
    def round1_ai_summary_q5_freetext3():
        return ui.markdown(round1_ai_summary_freetext3("AB12_01"))
