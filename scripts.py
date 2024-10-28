# Forschungsprojekt KoLLI: Dashboard
# © 2024 Dennis Schulmeister-Zimolong <dennis@wpvs.de>
# Lizenziert unter der BSD 3-Clause Lizenz

from shiny import run_app

def server():
    """
    Lokaler Webserver ohne Hot Reloading. Geeignet für kleine Deployments.
    """
    run_app(
        app            = "kolli_dashboard/app.py",
        host           = "127.0.0.1",
        port           = 8000,
        reload         = False,
        launch_browser = False
    )

def watch():
    """
    Lokaler Webserver mit Hot Reloading. Geeignet für die Entwicklung.
    """
    run_app(
        app            = "kolli_dashboard/app.py",
        host           = "127.0.0.1",
        port           = 8000,
        reload         = True,
        launch_browser = True
    )