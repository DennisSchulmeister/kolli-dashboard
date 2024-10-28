# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from shiny import run_app

def server():
    """
    Lokaler Webserver ohne Hot Reloading. Geeignet für kleine Deployments.
    """
    run_app(
        app            = "kolli_dashboard.app:app",
        host           = "127.0.0.1",
        port           = 8000,
        reload         = False,
        launch_browser = False,
    )

def watch():
    """
    Lokaler Webserver mit Hot Reloading. Geeignet für die Entwicklung.
    """
    run_app(
        app            = "kolli_dashboard.app:app",
        host           = "127.0.0.1",
        port           = 8000,
        reload         = True,
        launch_browser = True,
    )