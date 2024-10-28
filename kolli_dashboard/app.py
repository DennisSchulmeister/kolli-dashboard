# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .infobox  import infobox_ui, infobox_server
from .sidebar  import sidebar_ui, sidebar_server
from .students import students_ui, students_server
from .teachers import teachers_ui, teachers_server
from .utils    import get_src_dir
from shiny     import App, ui

app_ui = ui.page_navbar(
    ui.head_content(ui.include_css(str(get_src_dir() / "www" / "style.css"))),
    ui.nav_spacer(),
    ui.nav_panel("Studierende", students_ui(), value="students"),
    ui.nav_panel("Lehrende", teachers_ui(), value="teachers"),
    ui.nav_control(infobox_ui()),

    title   = "Forschungsprojekt KoLLI: Evaluationsergebnisse",
    id      = "group",
    lang    = "de",
    theme   = ui.Theme(preset="cerulean").add_mixins(navbar_light_bg="#303030"),
    sidebar = sidebar_ui(),
)

def server(input, output, session):
    sidebar_server(input, output, session)
    students_server(input, output, session)
    teachers_server(input, output, session)
    infobox_server(input, output, session)

app = App(app_ui, server)