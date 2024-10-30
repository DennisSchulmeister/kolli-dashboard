# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .data  import correlation_filters, data, get_label, version
from .utils import scale_minus_plus
from shiny  import ui, reactive

def sidebar_ui():
    return ui.sidebar(
        ui.div(
            ui.h5("Filterkriterien"),
            ui.input_selectize("teachers", "Lehrperson", multiple=True, choices=data["teachers"]),
            ui.input_date_range("date_range", "Zeitraum", start="2024-09-01", end="2026-04-30"),
            ui.input_action_button(
                "btn_correlation_filter",
                "Filter für Korrelationsanalyse",
            ),
        ),

        ui.div(
            ui.h5("Darstellung"),
            ui.input_selectize("number_format", "Zahlenformat", selected="absolut", choices={"absolute": "Anzahl", "percent":  "Prozent"}),
        ),

        ui.div(class_="flex-grow-1"),

        ui.div(
            ui.hr(),
            ui.div(
                ui.markdown(
                    """
                    KoLLI ist ein an der DHBW Karlsruhe entwickelter Prozessleitfaden, der Lehrende dabei
                    unterstützt, Lehr-Lern-Innovationen mit Studierenden partizipativ zu gestalten.
                    Diese Anwendung zeigt die Evaluationsergebnisse des dazugehörigen Forschungsprojekts.
                    Das Projekt wird von der Stiftung Innovation in der Hochschullehre gefördert.
                    Die Projektlaufzeit ist von April 2024 bis April 2026.
                    """
                ),
                style  = "text-align: justify; hyphens: auto; font-size:75%;",
            ),
            ui.div(
                ui.div(
                    ui.strong("Version:"), f" {version}",
                    ui.span(" | ", class_="text-secondary"),
                    ui.strong("Stand:"), f" {data['max_date']}"
                ),
                ui.img(src="dhbw-logo.svg", height="60px", class_="mt-2"),
                class_="text-center",
            ),
        ),

        width = "20em"
    )

all_correlation_plus_minus_selectize = []

def ui_correlation_plus_minus(input, var, survey):
    name = f"correlation_{var}"

    if not name in all_correlation_plus_minus_selectize:
        @reactive.effect
        @reactive.event(input[name])
        def _():
            correlation_filters[survey][var].set([*input[name]()])
    
    all_correlation_plus_minus_selectize.append(name)

    return ui.input_selectize(
        name,
        get_label(var),
        multiple = True,
        choices  = scale_minus_plus,
        selected = correlation_filters[survey][var](),
        width    = "100%"
    ),

def sidebar_server(input, output, session):
    @reactive.effect
    @reactive.event(input.btn_correlation_filter)
    def _():    
        m = ui.modal(
            ui.panel_well(
                """
                Hier können die angezeigten Umfrageergebnisse weiter eingeschränkt werden,
                um nur Ergebnisse mit bestimmten Antworten zu sehen. Auf diese Weise können
                Zusammenhänge zwischen den Fragen untersucht werden. Die Filter wirken sich
                nur auf den jeweiligen Umfragetyp aus.
                """,
                class_="mb-4",
            ),
            ui.navset_pill(
                ui.nav_panel(
                    "Studentische Vorumfrage",
                    ui.div(
                        ui.navset_card_tab(
                            ui.nav_panel(
                                "Vorwissen und Interesse",
                                ui_correlation_plus_minus(input, "V201_01", "student1"),
                                ui_correlation_plus_minus(input, "V201_02", "student1"),
                            ),
                            ui.nav_panel(
                                "Mitgestaltung",
                                ui_correlation_plus_minus(input, "V204_01", "student1"),
                                ui_correlation_plus_minus(input, "V204_02", "student1"),
                                ui.input_slider(
                                    "correlation_V203_01",
                                    get_label("V203_01"),
                                    min   = 0,
                                    max   = 11,
                                    value = correlation_filters["student1"]["V203_01"].get(),
                                    ticks = True,
                                    width = "100%",
                                ),
                            ),
                            ui.nav_panel(
                                "Student Engagement",
                                ui_correlation_plus_minus(input, "VU03_03", "student1"),
                                ui_correlation_plus_minus(input, "VU03_04", "student1"),
                                ui_correlation_plus_minus(input, "V209_01", "student1"),
                                ui_correlation_plus_minus(input, "V209_02", "student1"),
                                ui_correlation_plus_minus(input, "V209_03", "student1"),
                                ui_correlation_plus_minus(input, "V209_04", "student1"),
                                ui_correlation_plus_minus(input, "V209_05", "student1"),
                                ui_correlation_plus_minus(input, "V209_06", "student1"),
                                ui_correlation_plus_minus(input, "V209_07", "student1"),
                                ui_correlation_plus_minus(input, "V209_08", "student1"),
                                ui_correlation_plus_minus(input, "V209_09", "student1"),
                            ),
                        ),
                        class_="mt-4",
                    ),
                ),
                ui.nav_panel(
                    "Studentische Zwischenumfrage",
                    ui.div(
                        ui.navset_card_tab(
                            ui.nav_panel(
                                "Klarheit und Überforderung",
                                ui_correlation_plus_minus(input, "ZW04_01", "student2"),
                                ui_correlation_plus_minus(input, "ZW04_02", "student2"),
                                ui_correlation_plus_minus(input, "ZW04_03", "student2"),
                                ui_correlation_plus_minus(input, "ZW04_04", "student2"),
                            ),
                            ui.nav_panel(
                                "Zufriedenheit",
                                ui_correlation_plus_minus(input, "ZW04_05", "student2"),
                                ui_correlation_plus_minus(input, "ZW04_06", "student2"),
                                ui_correlation_plus_minus(input, "ZW04_07", "student2"),
                                ui_correlation_plus_minus(input, "ZW04_08", "student2"),
                            ),
                        ),
                        class_="mt-4",
                    ),
                ),
                # ui.nav_panel(
                #     "Studentische Abschlussumfrage",
                #     ui.div(
                #         ui.navset_card_tab(
                #             ui.nav_panel(
                #                 "Klarheit und Überforderung",
                #                 ui_correlation_plus_minus(input, "ZW04_01", "student3"),
                #                 ui_correlation_plus_minus(input, "ZW04_02", "student3"),
                #                 ui_correlation_plus_minus(input, "ZW04_03", "student3"),
                #                 ui_correlation_plus_minus(input, "ZW04_04", "student3"),
                #             ),
                #             ui.nav_panel(
                #                 "Zufriedenheit",
                #                 ui_correlation_plus_minus(input, "ZW04_05", "student3"),
                #                 ui_correlation_plus_minus(input, "ZW04_06", "student3"),
                #                 ui_correlation_plus_minus(input, "ZW04_07", "student3"),
                #                 ui_correlation_plus_minus(input, "ZW04_08", "student3"),
                #             ),
                #         ),
                #         class_="mt-4",
                #     ),
                # ),
                ui.nav_menu(
                    "Spezifische Umfragen",
                    ui.nav_panel(
                        "DIRA Lerntagebücher",
                        ui.div(
                            ui.h4("DIRA Lerntagebücher / Zwischenumfrage", class_="my-survey-title mb-4"),
                            ui_correlation_plus_minus(input, "DR06_01", "student-DIRA2_special"),
                            ui_correlation_plus_minus(input, "DR06_08", "student-DIRA2_special"),
                            class_="mt-4",
                        ),
                    ),
                ),
            ),
            title      = "Filter für Korrelationsanalyse",
            easy_close = True,
            size       = "xl",
            footer     = ui.input_action_button("btn_reset_correlation_filter", "Filter zurücksetzen"),
        )

        ui.modal_show(m)
    
    @reactive.effect
    @reactive.event(input.correlation_V203_01)
    def _():
        correlation_filters["student1"]["V203_01"].set(input.correlation_V203_01())

    @reactive.effect
    @reactive.event(input.btn_reset_correlation_filter)
    def _():
        ui.update_slider("correlation_V203_01", value=[0, 11])

        for selectize in all_correlation_plus_minus_selectize:
            ui.update_selectize(selectize, selected=[])