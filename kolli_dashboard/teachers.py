# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from shiny.express import expressify, ui

@expressify
def teachers_panel():
    with ui.nav_panel("Lehrende"):
        ui.h4("Befragung der Lehrenden")
        "Bisher wurden noch keine Umfragen mit Lehrenden durchgeführt."