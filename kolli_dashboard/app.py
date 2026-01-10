# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from dotenv import load_dotenv
load_dotenv()

from .infobox         import infobox_ui, infobox_server
from .sidebar         import sidebar_ui, sidebar_server
from .surveys.round1  import round1_ui, round1_server
from .surveys.revised import revised_ui, revised_server
from .surveys.special import special_ui, special_server
from .utils           import src_dir
from shiny            import App, ui

app_ui = ui.page_navbar(
    ui.head_content(
        ui.include_css(str(src_dir / "www" / "style.css")),
        ui.HTML('<link rel="icon" href="favicon.svg"/>'),
    ),
    ui.nav_spacer(),
    ui.nav_panel("Runden 2 & 3", revised_ui(), value="round3"),
    ui.nav_panel("Runde 1", round1_ui(), value="round1"),
    ui.nav_panel("Spezialumfragen", special_ui(), value="round2"),
    ui.nav_control(infobox_ui()),

    title   = "Forschungsprojekt KoLLI: Evaluationsergebnisse",
    id      = "group",
    lang    = "de",
    theme   = ui.Theme(preset="cerulean").add_mixins(navbar_light_bg="#303030"),
    sidebar = sidebar_ui(),
)

def server(input, output, session):
    sidebar_server(input, output, session)
    revised_server(input, output, session)
    round1_server(input, output, session)
    special_server(input, output, session)
    infobox_server(input, output, session)

app = App(app_ui, server, static_assets=str(src_dir / "www"))