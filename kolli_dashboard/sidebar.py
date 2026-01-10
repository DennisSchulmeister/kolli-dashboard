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
            ui.input_selectize("lectures", "Veranstaltung", multiple=True, choices=data["lectures"]),
            ui.input_date_range("date_range", "Zeitraum", start="2024-09-01", end="2026-04-30"),
            ui.input_action_button(
                "btn_correlation_filter",
                "Filter für Korrelationsanalyse",
            ),
        ),

        ui.div(
            ui.input_selectize("number_format", "Zahlenformat", selected="absolut", choices={
                "absolute": "Anzahl",
                "percent":  "Prozent",
                "stats":    "Statistik",
            }),
        ),

        ui.div(class_="flex-grow-1"),

        ui.div(
            ui.hr(),
            ui.div(
                ui.markdown(
                    """
                    KoLLI ist ein an der DHBW Karlsruhe entwickeltes Konzept, das Lehrende dabei
                    unterstützt, Studierende gezielt in die Verbesserung der Lehre einzubeziehen.
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
                    "Runden 2 und 3",
                    ui.div(
                        ui.navset_card_tab(
                            ui.nav_panel(
                                "Umsetzung der Mitgestaltung",
                                ui_correlation_plus_minus(input, "R201_01", "revised"),
                                ui_correlation_plus_minus(input, "R201_02", "revised"),
                                ui_correlation_plus_minus(input, "R201_03", "revised"),
                                ui_correlation_plus_minus(input, "R201_04", "revised"),
                                ui_correlation_plus_minus(input, "R201_05", "revised"),
                            ),
                            ui.nav_panel(
                                "Wirkung der Mitgestaltung",
                                ui_correlation_plus_minus(input, "R202_02", "revised"),
                                ui_correlation_plus_minus(input, "R202_03", "revised"),
                                ui_correlation_plus_minus(input, "R202_04", "revised"),
                                ui_correlation_plus_minus(input, "R202_05", "revised"),
                                ui_correlation_plus_minus(input, "R202_06", "revised"),
                            ),
                            ui.nav_panel(
                                "Sonstiges",
                                ui_correlation_plus_minus(input, "R204_01", "revised"),
                            ),
                        ),
                        class_="mt-4",
                    ),
                ),
                ui.nav_menu(
                    "Runde 1",
                    ui.nav_panel(
                        "Studentische Vorumfrage",
                        ui.div(
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Vorwissen und Interesse",
                                    ui_correlation_plus_minus(input, "V201_01", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V201_02", "round1_student1"),
                                ),
                                ui.nav_panel(
                                    "Mitgestaltung",
                                    ui_correlation_plus_minus(input, "V204_01", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V204_02", "round1_student1"),
                                    ui.input_slider(
                                        "correlation_V203_01",
                                        get_label("V203_01"),
                                        min   = -1,
                                        max   = 11,
                                        value = correlation_filters["round1_student1"]["V203_01"].get(),
                                        ticks = True,
                                        width = "100%",
                                    ),
                                ),
                                ui.nav_panel(
                                    "Studentisches Engagement",
                                    ui_correlation_plus_minus(input, "VU03_03", "round1_student1"),
                                    ui_correlation_plus_minus(input, "VU03_04", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_01", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_02", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_03", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_04", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_05", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_06", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_07", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_08", "round1_student1"),
                                    ui_correlation_plus_minus(input, "V209_09", "round1_student1"),
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
                                    ui_correlation_plus_minus(input, "ZW04_01", "round1_student2"),
                                    ui_correlation_plus_minus(input, "ZW04_02", "round1_student2"),
                                    ui_correlation_plus_minus(input, "ZW04_03", "round1_student2"),
                                    ui_correlation_plus_minus(input, "ZW04_04", "round1_student2"),
                                ),
                                ui.nav_panel(
                                    "Zufriedenheit",
                                    ui_correlation_plus_minus(input, "ZW04_05", "round1_student2"),
                                    ui_correlation_plus_minus(input, "ZW04_06", "round1_student2"),
                                    ui_correlation_plus_minus(input, "ZW04_07", "round1_student2"),
                                    ui_correlation_plus_minus(input, "ZW04_08", "round1_student2"),
                                ),
                            ),
                            class_="mt-4",
                        ),
                    ),
                    ui.nav_panel(
                        "Studentische Abschlussumfrage",
                        ui.div(
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Inhalt der Lehrveranstaltung",
                                    ui_correlation_plus_minus(input, "AB03_01", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB03_02", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB03_03", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB03_04", "round1_student3"),
                                ),
                                ui.nav_panel(
                                    "Studentisches Engagement",
                                    ui_correlation_plus_minus(input, "AB07_01", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_02", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_03", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_04", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_05", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_06", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_07", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_08", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB07_09", "round1_student3"),
                                ),
                                ui.nav_panel(
                                    "Beurteilung der Partizipation",
                                    ui_correlation_plus_minus(input, "AB09_01", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB09_02", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB09_03", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB09_04", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB09_05", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB09_06", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB09_07", "round1_student3"),
                                ),
                                ui.nav_panel(
                                    "Beurteilung der Lernwirksamkeit",
                                    ui_correlation_plus_minus(input, "AB14_06", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB14_07", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB14_08", "round1_student3"),
                                    ui_correlation_plus_minus(input, "AB14_09", "round1_student3"),
                                ),
                            ),
                            class_="mt-4",
                        ),
                    ),
                ),
                ui.nav_menu(
                    "Spezialumfragen",
                    ui.nav_panel(
                        "DIRA Lerntagebücher",
                        ui.div(
                            ui.h4("DIRA Lerntagebücher", class_="my-survey-title mb-4"),
                            ui_correlation_plus_minus(input, "DR06_01", "special_DIRA_r1"),
                            ui_correlation_plus_minus(input, "DR06_08", "special_DIRA_r1"),
                            class_="mt-4",
                        ),
                    ),
                                        ui.nav_panel(
                        "DESC Partizipation Allgemein",
                        ui.div(
                            ui.h4("DESC Partizipation Allgemein", class_="my-survey-title mb-4"),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Lernen und Lehren allgemein",
                                    ui_correlation_plus_minus(input, "AA01_01", "special_DESC_r2_general"),
                                    ui_correlation_plus_minus(input, "AA01_02", "special_DESC_r2_general"),
                                    ui_correlation_plus_minus(input, "AA01_03", "special_DESC_r2_general"),
                                    ui_correlation_plus_minus(input, "AA01_04", "special_DESC_r2_general"),
                                    ui.input_slider(
                                        "correlation_AA02_01",
                                        get_label("AA02_01"),
                                        min   = -1,
                                        max   = 11,
                                        value = correlation_filters["special_DESC_r2_general"]["AA02_01"].get(),
                                        ticks = True,
                                        width = "100%",
                                    ),
                                ),
                                ui.nav_panel(
                                    "Mitbestimmung in der Vorlesung",
                                    ui_correlation_plus_minus(input, "AA03_01", "special_DESC_r2_general"),
                                    ui_correlation_plus_minus(input, "AA03_02", "special_DESC_r2_general"),
                                    ui_correlation_plus_minus(input, "AA03_03", "special_DESC_r2_general"),
                                    ui_correlation_plus_minus(input, "AA03_04", "special_DESC_r2_general"),
                                ),
                            ),
                            class_="mt-4",
                        )
                    ),
                    ui.nav_panel(
                        "DESC Spezifische Interventionen",
                        ui.div(
                            ui.h4("DESC Spezifische Interventionen", class_="my-survey-title mb-4"),
                            ui.navset_card_tab(
                                ui.nav_panel(
                                    "Allgemeiner Nutzen",
                                    ui_correlation_plus_minus(input, "AS01_01", "special_DESC_r2_specific"),
                                    ui_correlation_plus_minus(input, "AS01_02", "special_DESC_r2_specific"),
                                    ui_correlation_plus_minus(input, "AS01_03", "special_DESC_r2_specific"),
                                ),
                                ui.nav_panel(
                                    "Tatsächliche Umsetzung",
                                    ui_correlation_plus_minus(input, "AS02_01", "special_DESC_r2_specific"),
                                    ui_correlation_plus_minus(input, "AS02_02", "special_DESC_r2_specific"),
                                    ui_correlation_plus_minus(input, "AS02_03", "special_DESC_r2_specific"),
                                    ui_correlation_plus_minus(input, "AS02_04", "special_DESC_r2_specific"),
                                    ui_correlation_plus_minus(input, "AS02_05", "special_DESC_r2_specific"),
                                ),
                            ),
                            class_="mt-4",
                        )
                    ),
                )
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
        correlation_filters["round1_student1"]["V203_01"].set(input.correlation_V203_01())

    @reactive.effect
    @reactive.event(input.correlation_AA02_01)
    def _():
        correlation_filters["special_DESC_r2_general"]["AA02_01"].set(input.correlation_AA02_01())

    @reactive.effect
    @reactive.event(input.btn_reset_correlation_filter)
    def _():
        ui.update_slider("correlation_V203_01", value=[-1, 11])
        ui.update_slider("correlation_AA02_01", value=[-1, 11])

        for selectize in all_correlation_plus_minus_selectize:
            ui.update_selectize(selectize, selected=[])