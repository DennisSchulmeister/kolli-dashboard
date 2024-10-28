# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .info_popup   import info_popup_navbar_button
from .sidebar      import sidebar
from .students     import students_panel
from .teachers     import teachers_panel
from .utils        import get_src_dir

from shiny.express import ui

ui.page_opts(
    title      = "Forschungsprojekt KoLLI: Evaluationsergebnisse",
    lang       = "de",
    id         = "group",
    fillable   = False,
    full_width = True,
    theme      = ui.Theme(preset="cerulean").add_mixins(navbar_light_bg="#303030"),
)

ui.head_content(ui.include_css(str(get_src_dir() / "www" / "style.css")))

sidebar()

ui.nav_spacer()

students_panel()
teachers_panel()
info_popup_navbar_button("info")