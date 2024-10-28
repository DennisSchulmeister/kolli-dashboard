Forschungsprojekt KoLLI: Dashboard
==================================

1. [Übersicht](#übersicht)
1. [Wichtige Kommandos](#wichtige-kommandos)
1. [Deployment](#deployment)
1. [Copyright](#copyright)

Übersicht
---------

TODO

Wichtige Kommandos
------------------

### Kurzversion

 * `poetry run server`: Starten des Webservers ohne Hot-Reloading
 * `poetry run watch`: Starten des Webservers mit Hot-Reloading

### Langversion

Dieses Projekt verwendet [Poetry](https://python-poetry.org/) zur Verwaltung der
Abhängigkeiten, vergleichbar mit [NPM](https://www.npmjs.com/) für Node.js.
Tatsächlich sind viele Konzepte direkt vergleichbar. Die Projektmetadaten finden
sich in der Datei [pyprojekt.toml](./pyprojekt.toml). Die wichtigsten Befehle
hierbei sind:

| **Kommando**         | **Bedeutung**                                                          |
|----------------------|------------------------------------------------------------------------|
| `poetry init`        | Initialisierung eines neuen Projektverzeichnisses (hier schon gemacht) |
| `poetry install`     | Installation aller in der `pyproject.toml` aufgezählten Abhängigkeiten |
| `poetry add xyz`     | Hinzufügen und Installieren einer weiteren Abhängigkeit                |
| `poetry remove xyz`  | Entfernen und Deinstallieren einer Abhängigkeit                        |
| `poetry show --tree` | Anzeige aller direkten und indirekten Abhängigkeiten                   |
| `poetry check`       | Überprüfung der `pyproject.toml` auf offensichtliche Fehler            |
| `poetry shell`       | Start einer neuen Shell mit aktivierter Python-Umgebung                |
| `poetry run xyz`     | Ausführen des übergebenen Konsolenbefehls in der Python-Umgebung       |

### Poetry Skripte

Mit `poetry run` können nicht nur Konsolenbefehle, sondern auch Skripte, die in der `pyproject.toml`
im Abschnitt `[tool.poetry.scripts]` definiert sind, ausgeführt werden. Vergleichbar mit `npm run …`
in Node.js. Allerdings werden hier keine Shell-Befehle eingetragen, sondern Funktionen, die in einem
Python-Modul ausprogrammiert werden. `scripts:server` bedeutet hierbei, dass die Funktion `server()`
im Modul `scripts` ausgeführt werden soll.

Immer, wenn die Skripte in der `pyproject.toml` angepasst wurden, muss `peotry install` ausgeführt
werden, um diese in der Python-Umgebung zu installieren.

Deployment
---------

### ASGI-Server

Das Deployment entspricht einer normalen ASGI-Webanwendung. Für Seiten mit wenig Traffic kann
der in [Shiny](https://shiny.posit.co/py/) enthaltene Webserver mit folgendem Kommando direkt
gestartet werden.

```sh
shiny run kolli_dashboard/app.py
```

Der Befehl muss ggf. in einer Shell mit aktivierter Python-Umgebung ausgeführt werden. Als
Vereinfachung kann auch einfach

```sh
poetry run server
```

verwendet werden, das immer funktionieren sollte.

Soll es eine Nummer professioneller sein, kann eine ASGI-Server wie [Daphne](https://github.com/django/daphne)
installiert und ähnlich einfach genutzt werden. Nach der Installation von Daphne kann die Anwendung
mit folgendem Befehl gestartet werden:

```sh
daphne -p 8000 -b 0.0.0.0 kolli_dashboard:app
```

Die beiden Parameter `-p` und `-b` stehen für die Portnummer und das Netzwerkinterface, an das sich
der Server bindet. Sie müssen ggf. angepasst werden, insbesondere wenn die Anwendung hinter einem
Reverse Proxy wie z.B. [Caddy](https://caddyserver.com/) betrieben werden soll. Denn in diesem Fall
sollte sich der Server nur an das localhost-Interface (127.0.0.1) binden, um nicht aus dem offenen
Netz heraus direkt aufgerufen werden zu können.

### Sticky Sessions

Bei größeren Setups mit lastverteilten Instanzen muss beachtet werden, dass Shiny nur mit sog.
Sticky Sessions funktioniert. Dies bedeutet, dass alle Anfrage einer Benutzersitzung immer von
derselben Instanz beantwortet werden müssen. Siehe [Other Hosting Options](https://shiny.posit.co/py/docs/deploy-on-prem.html#other-hosting-options)
in der Dokumentation.

Copyright
---------

Forschungsprojekt KoLLI: Dashboard <br/>
© 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik <br>
Dennis Schulmeister-Zimolong &lt;[dennis@wpvs.de](mailto:dennis@wpvs.de)&gt; <br>
Lizenziert unter der BSD 3-Clause Lizenz <br>

Webseite: https://kollaborative-lehre.de

_Das Forschungsprojekt KoLLI (Kooperative Lehr-Lern-Innovation) wird von der
Stiftung Innovation in der Hochschullehre gefördert._