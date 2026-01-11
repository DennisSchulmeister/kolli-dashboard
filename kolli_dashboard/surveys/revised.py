# Forschungsprojekt KoLLI: Dashboard
# © 2025 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

import asyncio

from ..ai_llm import (
    ai_conversation_available,
    ai_conversation_json,
    ai_message,
    cancel_ai_stream,
    start_ai_stream,
    start_ai_task,
)

from ..data import (
    calc_likert_statistics,
    correlation_filters,
    data,
    get_label,
    plot_likert_chart
)

from shiny import reactive, render, ui

import faicons
import pandas as pd
import numpy as np
import html

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
                Beginnend mit Runde 2 wurde das Umfragedesign so angepasst, dass nur noch eine summative Abschlussumfrage
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
    revised_ai_summary_freitext_topics_md = reactive.Value("")
    revised_ai_summary_freitext_summary_md = reactive.Value("")

    @reactive.calc
    def revised_filtered_surveys3():
        cancel_ai_stream("revised_topics")
        cancel_ai_stream("revised_interpretation")
        revised_ai_summary_freitext_topics_md.set("")
        revised_ai_summary_freitext_summary_md.set("")

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
            ui.navset_pill(
                ui.nav_panel("Zusammenfassung",
                    ui.div(
                        ui.output_ui("revised_ai_summary_freitext_summary"),
                        class_="mt-4",
                    )
                ),
                ui.nav_panel("Kategorisierung",
                    ui.div(
                        ui.output_ui("revised_ai_summary_freitext_topics"),
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
        return ui.markdown(revised_ai_summary_freitext_topics_md.get() or "")

    @reactive.effect
    @reactive.event(input.btn_revised_ai_summary_freitext)
    def _revised_ai_summary_freitext_topics_stream():
        if revised_ai_summary_freitext_topics_md.get():
            return

        df    = revised_filtered_surveys3()
        var   = "R205_01"
        label = get_label(var)

        # Filter usable answers once, then build a stable mapping
        # QUESTNNR -> [answers] (keeps original row order).
        answers_df = df[["QUESTNNR", var]].dropna(subset=[var])
        answers_df = answers_df.assign(
            _questnnr=answers_df["QUESTNNR"].astype(str),
            _answer=answers_df[var].astype(str).str.strip(),
        )
        answers_df = answers_df[answers_df["_answer"].str.len() > 3]

        questnnr_to_answers: dict[str, list[str]] = (
            answers_df.groupby("_questnnr", sort=False)["_answer"].apply(list).to_dict()
        )

        # Stable, unique answer list (first occurrence order in df).
        raw_answers: list[str] = answers_df["_answer"].drop_duplicates().tolist()

        # For each answer text, show all questionnaire IDs it appears in.
        answer_to_questnnrs: dict[str, list[str]] = {}
        for questnnr, answers in questnnr_to_answers.items():
            for answer_text in dict.fromkeys(answers):
                answer_to_questnnrs.setdefault(answer_text, []).append(questnnr)

        raw_answer_questnnrs: list[str] = [
            ", ".join(sorted(set(answer_to_questnnrs.get(a, [])))) for a in raw_answers
        ]

        if not raw_answers:
            revised_ai_summary_freitext_topics_md.set("Es liegen keine verwertbaren Freitextantworten vor.")
            return

        def _render_progress_md(
            *,
            step:     str = "",
            topics:   list[str]      | None = None,
            counts:   dict[str, int] | None = None,
            examples: dict[str, str] | None = None,
            matches:  dict[str, list[int]] | None = None,
        ) -> str:
            topics   = topics or []
            counts   = counts or {}
            examples = examples or {}

            lines: list[str] = []

            if step:
                lines += [
                    f"<span class='text-secondary'>{step}</span> <br>",
                    "",
                ]

            if topics:
                lines += [
                    "<table class='table'>"
                    "    <thead>"
                    "        </tr>"
                    "            <th scope='col'>Kategorie</th>"
                    "            <th scope='col'>Anzahl</th>"
                    "            <th scope='col'>Beispiel</th>"
                    "        </tr>"
                    "    </thead>"
                    "    <tbody class='table-group-divider'>"
                ]

                for topic in topics:
                    n           = counts.get(topic) or 0
                    example     = examples.get(topic, "")
                    example_str = "" if not example else example

                    lines += [
                        "<tr>",
                        f"    <td>{topic}</td>",
                        f"    <td>{n}</td>",
                        f"    <td>{html.escape(example_str)}</td>",
                        "</tr>",
                    ]
                
                lines += [
                    "    </tbody>",
                    "</table>"
                ]
            
            if matches:
                for topic in topics:
                    count = counts.get(topic, 0)
                    if not count:
                        continue

                    lines += [
                        "<table class='table'>"
                        "    <thead>"
                        "        </tr>"
                        f"           <th scope='col'>{topic} (N={count})</th>"
                        "            <th scope='col'>Fragebogen</th>"
                        "        </tr>"
                        "    </thead>"
                        "    <tbody class='table-group-divider'>"
                    ]

                    for n in matches.get(topic, []):
                        answer_text = raw_answers[n - 1]
                        questnnr = raw_answer_questnnrs[n - 1]
                        lines += [
                            "<tr>",
                            f"    <td>{html.escape(answer_text)}</td>",
                            f"    <td>{html.escape(questnnr)}</td>",
                            "</tr>",
                        ]

                    lines += [
                        "    </tbody>",
                        "</table>"
                    ]

            result = "\n".join(lines)
            return result

        async def _run():
            try:
                # Step 1: Extract topics
                revised_ai_summary_freitext_topics_md.set(
                    _render_progress_md(step="Schritt 1/3: Extrahiere Themen …")
                )
                await reactive.flush()

                numbered_answers = "\n".join([f"{i+1}. {a}" for i, a in enumerate(raw_answers)])
                topics = ["Positive Eindrücke", "Verbesserungsvorschläge", "Sonstige Bemerkungen"]

#                 topic_result = await ai_conversation_json(
#                     ai_message(
#                         "Stelle dir vor, du schreibst ein wissenschaftliches Paper zur Forschung "
#                         "über studentische Partizipation (Studierende nehmen Einfluss auf die Vorlesung, "
#                         "indem sie bei relevanten Fragestellungen in Entscheidung oder Umsetzung eingebunden werden).\n\n"
#                         f"Auf die Frage '{label}' liegen folgende Freitextantworten vor (nummeriert):\n\n"
#                         f"{numbered_answers}\n\n"
#                         "Aufgabe: Extrahiere eine Liste von Themen, die in den Antworten vorkommen.\n"
#                         "Wichtig: Verwende generische, allgemein gültige Themen (nicht kurs-/dozenten-spezifisch). "
#                         "Fasse kurs-/veranstaltungsspezifische Formulierungen zu allgemeinen Oberbegriffen zusammen.\n"
#                         "Gib möglichst wenig Themen zurück (lieber zusammenfassen als zu granular werden).\n"
#                         "Verwende kurze Bezeichnungen (ca. 3 Wörter) für die Themen.\n"
#                         "Antworte ausschließlich als JSON gemäß Schema."
#                     ),
#                     json_schema = {
#                         "name": "topics_schema",
#                         "schema": {
#                             "type": "object",
#                             "properties": {
#                                 "topics": {
#                                     "type": "array",
#                                     "items": {
#                                         "type": "string",
#                                     },
#                                 }
#                             },
#                             "required": ["topics"],
#                             "additionalProperties": False,
#                         },
#                     },
#                 )
# 
#                 topics: list[str] = []
# 
#                 if isinstance(topic_result, dict):
#                     topics = topic_result.get("topics") or [] # type: ignore
# 
#                 if not topics:
#                     revised_ai_summary_freitext_topics_md.set("Keine Themen erkannt!")
#                     await reactive.flush()
#                     await asyncio.sleep(0)
#                     return

                # Step 2: Find answers for each topic
                counts: dict[str, int] = {}
                examples: dict[str, str] = {}
                matches_by_topic: dict[str, list[int]] = {}

                revised_ai_summary_freitext_topics_md.set(
                    _render_progress_md(
                        step   = "Ordne Antworten zu",
                        topics = topics,
                    )
                )
                await reactive.flush()
                await asyncio.sleep(0)

                for answer_idx, answer_text in enumerate(raw_answers, start=1):
                    step_md = _render_progress_md(
                        step     = f"Ordne Antwort {answer_idx}/{len(raw_answers)} zu",
                        topics   = topics,
                        counts   = counts,
                        examples = examples,
                    )
                    revised_ai_summary_freitext_topics_md.set(step_md)
                    await reactive.flush()
                    await asyncio.sleep(0)

                    classify_result = await ai_conversation_json(
                        ai_message(
                            "Du bekommst eine einzelne Freitextantwort und eine Liste von Kategorien.\n"
                            "Aufgabe: Wähle die Kategorien aus, die wirklich (explizit) inhaltlich zur Antwort passen.\n"
                            "Wichtig: Sei konservativ – wenn du unsicher bist, wähle die SONSTIGE Kategorie.\n"
                            "Wichtig: Mehrfachzuordnung ist erlaubt, aber nur wenn klar mehrere Themen angesprochen werden. "
                            "Vermeide Überinterpretation.\n"
                            "Wichtig: Verwende ausschließlich Kategorien aus der gegebenen Liste.\n"
                            "Gib nur Kategorienamen zurück, keine Paraphrasen oder Zitate.\n"
                            "Optional: Wähle eine 'primary' Kategorie aus deinen gewählten Kategorien, die am repräsentativsten ist; "
                            "falls keine Kategorie passt, setze categories=[] und primary=null.\n\n"
                            f"Kategorien: {', '.join(topics)}\n\n"
                            f"Antwort:\n{answer_text}\n\n"
                            "Antworte ausschließlich als JSON gemäß Schema."
                        ),
                        json_schema = {
                            "name": "answer_classification_schema",
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "categories": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "primary": {"type": ["string", "null"]},
                                },
                                "required": ["categories", "primary"],
                                "additionalProperties": False,
                            },
                        },
                    )

                    selected: list[str] = []
                    primary: str | None = None

                    if not (isinstance(classify_result, dict) and classify_result.get("_error")):
                        if isinstance(classify_result, dict):
                            raw_selected = classify_result.get("categories")
                            if isinstance(raw_selected, list):
                                for t in raw_selected:
                                    if isinstance(t, str) and t in topics:
                                        selected.append(t)

                            raw_primary = classify_result.get("primary")
                            if isinstance(raw_primary, str) and raw_primary in topics:
                                primary = raw_primary

                    # De-duplicate & stabilize order.
                    selected = list(dict.fromkeys(selected))
                    if primary is not None and primary not in selected:
                        primary = None

                    for topic in selected:
                        matches_by_topic.setdefault(topic, []).append(answer_idx)
                        counts[topic] = len(matches_by_topic[topic])

                        # Prefer an explicitly chosen representative example.
                        if not examples.get(topic) or (primary == topic):
                            examples[topic] = answer_text

                    revised_ai_summary_freitext_topics_md.set(
                        _render_progress_md(
                            step     = f"Ordne Antwort {answer_idx}/{len(raw_answers)} zu",
                            topics   = topics,
                            counts   = counts,
                            examples = examples,
                            matches  = matches_by_topic,
                        )
                    )
                    await reactive.flush()
                    await asyncio.sleep(0)

                # Stabilize topic match ordering.
                for topic in topics:
                    if topic in matches_by_topic:
                        matches_by_topic[topic] = sorted(set(matches_by_topic[topic]))

                # Sort topics by count desc, then name.
                topics_sorted = sorted(topics, key=lambda t: (-counts.get(t, 0), t.lower()))

                revised_ai_summary_freitext_topics_md.set(
                    _render_progress_md(
                        step     = "Erstelle Tabelle …",
                        topics   = topics_sorted,
                        counts   = counts,
                        examples = examples,
                    )
                )
                await reactive.flush()
                await asyncio.sleep(0)

                # Final assembly (table + nested list of verbatim answers)
                revised_ai_summary_freitext_topics_md.set(
                    _render_progress_md(
                        topics   = topics,
                        counts   = counts,
                        examples = examples,
                        matches  = matches_by_topic,
                    )
                )
                await reactive.flush()
                await asyncio.sleep(0)
            except asyncio.CancelledError:
                raise
            except Exception as error:
                revised_ai_summary_freitext_topics_md.set(f"Fehler bei der Themen-Generierung: {error}")
                await reactive.flush()
                await asyncio.sleep(0)

        start_ai_task(coro=_run(), task_name="revised_topics")

    @render.ui
    def revised_ai_summary_freitext_summary():
        return ui.markdown(revised_ai_summary_freitext_summary_md.get() or "")

    @reactive.effect
    @reactive.event(input.btn_revised_ai_summary_freitext)
    def _revised_ai_summary_freitext_summary_stream():
        df      = revised_filtered_surveys3()
        var     = "R205_01"
        label   = get_label(var)
        answers = " - " + "\n - ".join(df[var].dropna().astype(str).unique().tolist())

        question = f"Auf die Frage '{label}' haben die Studierenden folgendes geantwortet.\n\n" \
                   f"{answers}\n\n" \
                   """
                   Bitte fasse die Antworten zusammen. Unterscheide dabei explizit zwischen
                   Studentischer Partizipation (Studierende nehmen Einfluss auf die Vorlesung,
                   indem sie bei relevanten Fragestellungen in Entscheidung oder Umsetzung eingebunden
                   werden) als zusätzliche Ebene der Mitbestimmung zu den ohnehin vorhandenene Lern-
                   bzw. Lehraktivitäten. Bedenke dabei auch, dass es sich um Eindrücke der Studierenden
                   handelt, die durch die persönliche Brille verzerrt sein können.

                   Wichtig: Antworte als Fließtext und vermeide lange Aufzählungen.
                   Wichtig: Füge Überschriten und Zwischenüberschriften ein, um deine Antwort zu strukturieren.
                   Wichtig: Nutze eine saubere Markdown-Formatierung für deine Antwort.
                   """

        if not revised_ai_summary_freitext_summary_md.get():
            start_ai_stream(
                question=question,
                target_md=revised_ai_summary_freitext_summary_md,
                task_name="revised_interpretation",
            )