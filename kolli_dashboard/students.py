# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .ai_llm import ai_conversation, ai_conversation_available, ai_message
from .data   import data, get_label, plot_likert_chart
from shiny   import reactive, render, ui

import faicons
import pandas            as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

#==============================================================================
# UI Definition
#==============================================================================

#------------------------------------------------------------------------------
# All Together
#------------------------------------------------------------------------------
ai_button_class = "" if ai_conversation_available() else "d-none"

icon_students = faicons.icon_svg("graduation-cap", width="50px")
icon_courses  = faicons.icon_svg("users", width="50px")
icon_teachers = faicons.icon_svg("chalkboard-user", width="50px")

def students_ui():
    return [
        ui.h4("Studentische Evaluation"),
        ui.navset_pill(
            ui.nav_panel("Vorumfrage", ui.div(survey1_ui(), class_="mt-4")),
            ui.nav_panel("Zwischenumfrage", ui.div(survey2_ui(), class_="mt-4")),
            ui.nav_panel("Abschlussumfrage", ui.div(survey3_ui(), class_="mt-4")),
            ui.nav_menu(
                "Spezifische Umfragen",
                ui.nav_panel("DIRA Lerntagebücher", ui.div(survey_dira2_special_ui(), class_="mt-4")),
            ),
        ),
    ]

#------------------------------------------------------------------------------
# Semester Start Survey
#------------------------------------------------------------------------------
def survey1_ui():
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
                ui.output_ui("count_students1"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("count_courses1"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("count_teachers1"),
                ui.output_ui("id_teachers1"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("no_data1"),
        ui.layout_columns(
            ui.h5("Vorwissen und Interesse"),
            ui.output_plot("plot_vorwissen_likert1"),
            ui.div(
                ui.output_data_frame("df_vorwissen1"),
                ui.input_action_button(
                    "btn_ai_summary_vorwissen1",
                    "KI-Zusammenfassung",
                    class_ = f"mt-4 {ai_button_class}"
                ),
            ),

            ui.h5("Mitgestaltung"),
            ui.output_plot("plot_mitgestaltung_likert1"),
            ui.div(
                ui.div(get_label("V203_01"), class_="text-center fw-bold"),
                ui.output_plot("plot_mitgestaltung_hist1"),
            ),

            ui.div(
                ui.h5("Student Engagement"),
                ui.output_plot("plot_engagement_likert1", height="900px"),
            ),
            ui.div(
                ui.h5("Sonstige Bemerkungen"),
                ui.div(
                    ui.output_data_frame("df_bemerkungen1"),
                    ui.input_action_button(
                        "btn_ai_summary_bemerkungen1",
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
def survey2_ui():
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
                ui.output_ui("count_students2"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("count_courses2"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("count_teachers2"),
                ui.output_ui("id_teachers2"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("no_data2"),
        ui.layout_columns(
            ui.h5("Klarheit und Überforderung"),
            ui.output_plot("plot_klarheit_likert2"),
            ui.div(
                ui.output_data_frame("df_lehr_lern_innovation2"),
                ui.input_action_button(
                    "btn_ai_summary_lehr_lern_innovation2",
                    "KI-Zusammenfassung",
                    class_=f"mt-4 {ai_button_class}"
                ),
            ),

            ui.h5("Zufriedenheit"),
            ui.output_plot("plot_zufriedenheit_likert2"),
            ui.div(
                ui.output_data_frame("df_unterstuetzung2"),
                ui.input_action_button(
                    "btn_ai_summary_unterstuetzung2",
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
def survey3_ui():
    return ui.div(
        ui.p(
            """
            Die studentische Abschlussumfrage findet als sumative Evaluation am Ende des Semesters statt,
            nachdem die Studierenden die Arbeit an den Lehr-Lern-Innovationen abgeschlossen haben.
            Sie erhebt, wie die Studienrenden die Partizipation empfunden haben und welche Verbesserungen
            vorgenommen werden können.
            """,
        ),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("count_students3"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("count_courses3"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("count_teachers3"),
                ui.output_ui("id_teachers3"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("no_data3"),
        class_="my-flex-with-gaps",
    )

#------------------------------------------------------------------------------
# DIRA2 Learning Diaries
#------------------------------------------------------------------------------
def survey_dira2_special_ui():
    return ui.div(
        ui.h4("DIRA Lerntagebücher / Zwischenumfrage", class_="my-survey-title"),
        ui.layout_column_wrap(
            ui.value_box(
                "Studierende",
                ui.output_ui("count_students_dira2_special"),
                showcase = icon_students,
                theme    = ui.value_box_theme(bg="#f3f7fc", fg="#606060")
            ),
            ui.value_box(
                "Kurse",
                ui.output_ui("count_courses_dira2_special"),
                showcase = icon_courses,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#606060")
            ),
            ui.value_box(
                "Lehrende",
                ui.output_ui("count_teachers_dira2_special"),
                ui.output_ui("id_teachers_dira2_special"),
                showcase = icon_teachers,
                theme    = ui.value_box_theme(bg="#fbfcf3", fg="#60606")
            ),
        ),
        ui.output_ui("no_data_dira2_special"),
        ui.output_plot("plot_likert_dira2_special"),
        ui.div(
            ui.input_action_button(
                "btn_ai_summary_dira2_special",
                "KI-Zusammenfassung",
                class_ = f"{ai_button_class}"
            ),
        ),
        ui.output_data_frame("df_freetext_dira2_special"),
        class_="my-flex-with-gaps",
    )

#==============================================================================
# SERVER
#==============================================================================

#------------------------------------------------------------------------------
# All Together
#------------------------------------------------------------------------------
def students_server(input, output, session):
    survey1_server(input, output, session)
    survey2_server(input, output, session)
    survey3_server(input, output, session)
    survey_dira2_special_server(input, output, session)

#------------------------------------------------------------------------------
# Semester Start Survey
#------------------------------------------------------------------------------
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
            df = filtered_surveys1()
            return df.groupby(['QUESTNNR', df['STARTED'].dt.date]).ngroups
        except KeyError:
            return 0
    
    @render.text
    def count_teachers1():
        try:
            return filtered_surveys1()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def id_teachers1():
        try:
            return ", ".join(filtered_surveys1()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""
    
    @render.text
    def no_data1():
        if filtered_surveys1().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."
    
    @render.data_frame
    def df_vorwissen1():
        df = filtered_surveys1()[["V202_01"]].astype(str).copy()
        df = df[df["V202_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"V202_01": get_label("V202_01")})
        return render.DataGrid(df, width="100%", height="400px")

    @render.data_frame
    def df_bemerkungen1():
        df = filtered_surveys1()[["V210_01"]].astype(str).copy()
        df = df[df["V210_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"V210_01": get_label("V210_01")})
        return render.DataGrid(df, width="100%", height="400px")

    @render.plot
    def plot_mitgestaltung_hist1():
        fig, ax = plt.subplots()
        density = False
        df      = filtered_surveys1()["V203_01"].dropna()

        if input.number_format() == "percent":
            density = True
            ax.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))

        ax.hist(df, 11, density=density)
        ax.set_xlabel("Grad der Mitgestaltung")
        ax.set_ylabel("Anzahl Antworten")

        return fig

    @render.plot
    def plot_vorwissen_likert1():
        return plot_likert_chart(input, filtered_surveys1(), "V201_01", "V201_02")

    @render.plot
    def plot_mitgestaltung_likert1():
        return plot_likert_chart(input, filtered_surveys1(), "V204_01", "V204_02")

    @render.plot
    def plot_engagement_likert1():
        return plot_likert_chart(input, filtered_surveys1(),
                                 "VU03_03", "VU03_04",
                                 "V209_01", "V209_02", "V209_03",
                                 "V209_04", "V209_05", "V209_06",
                                 "V209_07", "V209_08", "V209_09",
                                 width = 0.4)

    @reactive.effect
    @reactive.event(input.btn_ai_summary_vorwissen1)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("V202_01")),
            ui.output_ui("ai_summary_vorwissen1"),
            title      = "Zusammenfassung der Antworten",
            easy_close = True,
            size       = "xl",
            footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def ai_summary_vorwissen1():
        df      = filtered_surveys1()
        var     = "V202_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )
    
    @reactive.effect
    @reactive.event(input.btn_ai_summary_bemerkungen1)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("V210_01")),
            ui.output_ui("ai_summary_bemerkungen1"),
            title      = "Zusammenfassung der Antworten",
            easy_close = True,
            size       = "xl",
            footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def ai_summary_bemerkungen1():
        df      = filtered_surveys1()
        var     = "V210_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )
    
#------------------------------------------------------------------------------
# Semester Mid Survey
#------------------------------------------------------------------------------
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
            df = filtered_surveys2()
            return df.groupby(['QUESTNNR', df['STARTED'].dt.date]).ngroups
        except KeyError:
            return 0
    
    @render.text
    def count_teachers2():
        try:
            return filtered_surveys2()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def id_teachers2():
        try:
            return ", ".join(filtered_surveys2()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""
    
    @render.text
    def no_data2():
        if filtered_surveys2().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."
    
    @render.data_frame
    def df_lehr_lern_innovation2():
        df = filtered_surveys2()[["ZW06_01"]].astype(str).copy()
        df = df[df["ZW06_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"ZW06_01": get_label("ZW06_01")})
        return render.DataGrid(df, width="100%", height="400px")
    
    @render.data_frame
    def df_unterstuetzung2():
        df = filtered_surveys2()[["ZW05_01"]].astype(str).copy()
        df = df[df["ZW05_01"].apply(lambda x: len(x.strip()) > 3)]
        df = df.rename(columns={"ZW05_01": get_label("ZW05_01")})
        return render.DataGrid(df, width="100%", height="400px")
    
    @render.plot
    def plot_klarheit_likert2():
        return plot_likert_chart(input, filtered_surveys2(), "ZW04_01", "ZW04_02", "ZW04_03", "ZW04_04", width=0.4)
    
    @render.plot
    def plot_zufriedenheit_likert2():
        return plot_likert_chart(input, filtered_surveys2(), "ZW04_05", "ZW04_06", "ZW04_07", "ZW04_08", width=0.4)

    @reactive.effect
    @reactive.event(input.btn_ai_summary_lehr_lern_innovation2)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("ZW06_01")),
            ui.output_ui("ai_summary_lehr_lern_innovation2"),
            title      = "Zusammenfassung der Antworten",
            easy_close = True,
            size       = "xl",
            footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def ai_summary_lehr_lern_innovation2():
        df      = filtered_surveys2()
        var     = "ZW06_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )

    @reactive.effect
    @reactive.event(input.btn_ai_summary_unterstuetzung2)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Bitte warten, bis die Antwort erscheint.",
                class_="mb-4",
            ),
            ui.h6(get_label("ZW05_01")),
            ui.output_ui("ai_summary_unterstuetzung2"),
            title      = "Zusammenfassung der Antworten",
            easy_close = True,
            size       = "xl",
            footer     = None,
        )

        ui.modal_show(m)

    @render.ui
    def ai_summary_unterstuetzung2():
        df      = filtered_surveys2()
        var     = "ZW05_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ui.markdown(
            ai_conversation(ai_message(question))
        )

#------------------------------------------------------------------------------
# Semester End Survey
#------------------------------------------------------------------------------
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
            df = filtered_surveys3()
            return df.groupby(['QUESTNNR', df['STARTED'].dt.date]).ngroups
        except KeyError:
            return 0
    
    @render.text
    def count_teachers3():
        try:
            return filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def id_teachers3():
        try:
            return ", ".join(filtered_surveys3()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""

    @render.text
    def no_data3():
        if filtered_surveys3().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."

#------------------------------------------------------------------------------
# DIRA2 Learning Diaries
#------------------------------------------------------------------------------
def survey_dira2_special_server(input, output, session):
    @reactive.calc
    def filtered_surveys_dira2_special():
        teachers   = input.teachers() or data["teachers"]
        questnnrs  = []

        if "DIRA" in teachers:
            questnnrs = ["S-DIRA-2-special"]

        start_date = pd.to_datetime(input.date_range()[0])
        end_date   = pd.to_datetime(input.date_range()[1])

        return data["answers"][
            (data["answers"]["QUESTNNR"].isin(questnnrs)) &
            (data["answers"]["STARTED"] >= start_date) &
            (data["answers"]["STARTED"] <= end_date)
        ]

    @render.text
    def count_students_dira2_special():
        try:
            return filtered_surveys_dira2_special().shape[0]
        except KeyError:
            return 0

    @render.text
    def count_courses_dira2_special():
        try:
            return filtered_surveys_dira2_special()["STARTED"].dt.date.unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def count_teachers_dira2_special():
        try:
            return filtered_surveys_dira2_special()["QUESTNNR"].str.split("-", expand=True)[1].unique().shape[0]
        except KeyError:
            return 0
    
    @render.text
    def id_teachers_dira2_special():
        try:
            return ", ".join(filtered_surveys_dira2_special()["QUESTNNR"].str.split("-", expand=True)[1].unique().tolist())
        except KeyError:
            return ""
    
    @render.text
    def no_data_dira2_special():
        if filtered_surveys_dira2_special().shape[0] == 0:
            return "Es liegen keine Umfrageergebnisse für die gewählten Filterkriterien vor."
    
    @render.data_frame
    def df_freetext_dira2_special():
        try:
            df = filtered_surveys_dira2_special()[["DR01_01", "DR02_01", "DR03_01", "DR04_01", "DR05_01"]].astype(str).copy()
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
    def plot_likert_dira2_special():
        return plot_likert_chart(input, filtered_surveys_dira2_special(), "DR06_01", "DR06_08")
    
    @reactive.effect
    @reactive.event(input.btn_ai_summary_dira2_special)
    def _():
        m = ui.modal(
            ui.panel_well(
                "Beim ersten Klick auf eine Frage bitte warten, bis die Antwort erscheint. " \
                "Die KI ist nicht so schnell im Lesen ...",
                class_="mb-4",
            ),
            ui.navset_pill(
                ui.nav_panel("Frage 1",
                    ui.div(
                        ui.h6(get_label("DR01_01")),
                        ui.output_ui("ai_summary_q1_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 2",
                    ui.div(
                        ui.h6(get_label("DR02_01")),
                        ui.output_ui("ai_summary_q2_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 3",
                    ui.div(
                        ui.h6(get_label("DR03_01")),
                        ui.output_ui("ai_summary_q3_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 4",
                    ui.div(
                        ui.h6(get_label("DR04_01")),
                        ui.output_ui("ai_summary_q4_dira2_special"),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel("Frage 5",
                    ui.div(
                        ui.h6(get_label("DR05_01")),
                        ui.output_ui("ai_summary_q5_dira2_special"),
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
    
    def ai_summary_dira2_special(var):
        df = filtered_surveys_dira2_special()
        label = get_label(var)
        answers = " - " + "\n - ".join(df[var].astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                    f"{answers}\n\n" \
                    f"Bitte fasse die Antworten zusammen."
    
        return ai_conversation(ai_message(question))

    @render.ui
    def ai_summary_q1_dira2_special():
        return ui.markdown(ai_summary_dira2_special("DR01_01"))
    
    @render.ui
    def ai_summary_q2_dira2_special():
        return ui.markdown(ai_summary_dira2_special("DR02_01"))
    
    @render.ui
    def ai_summary_q3_dira2_special():
        return ui.markdown(ai_summary_dira2_special("DR03_01"))
    
    @render.ui
    def ai_summary_q4_dira2_special():
        return ui.markdown(ai_summary_dira2_special("DR04_01"))
    
    @render.ui
    def ai_summary_q5_dira2_special():
        return ui.markdown(ai_summary_dira2_special("DR05_01"))