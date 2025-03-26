# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from dotenv import load_dotenv
load_dotenv()

from .infobox   import infobox_ui, infobox_server
from .sidebar   import sidebar_ui, sidebar_server
from .students1 import students1_ui, students1_server
from .others    import learning_room_ui, learning_room_server
from .utils     import src_dir
from shiny      import App, ui

app_ui = ui.page_navbar(
    ui.head_content(ui.include_css(str(src_dir / "www" / "style.css"))),
    ui.nav_spacer(),
    ui.nav_panel("Runde 1", students1_ui(), value="students1"),
    ui.nav_panel("Innovativer Lernraum", learning_room_ui(), value="learning_room"),
    ui.nav_control(infobox_ui()),

    title   = "Forschungsprojekt KoLLI: Evaluationsergebnisse",
    id      = "group",
    lang    = "de",
    theme   = ui.Theme(preset="cerulean").add_mixins(navbar_light_bg="#303030"),
    sidebar = sidebar_ui(),
)

def server(input, output, session):
    sidebar_server(input, output, session)
    students1_server(input, output, session)
    learning_room_server(input, output, session)
    infobox_server(input, output, session)

app = App(app_ui, server, static_assets=str(src_dir / "www"))