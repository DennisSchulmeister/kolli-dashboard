# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from shiny import ui

def learning_room_ui():
    return [
        ui.h4("Innovativer Lernraum"),
        "Hier erscheint demnächst die Umfrage zum innovativen Lernraum.",
    ]

def learning_room_server(input, output, session):
    pass