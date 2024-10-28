# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from .data         import data, version
from shiny         import reactive
from shiny.express import module, input, ui

import faicons

@module
def info_popup_navbar_button(input, output, session):
    with ui.nav_control():
        ui.input_action_link("open_info_popup", "", icon=faicons.icon_svg("circle-info"))
    
    @reactive.effect
    @reactive.event(input.open_info_popup)
    def _():
        m = ui.modal(
            ui.markdown(
                f"""
                **© 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik** <br>
                **Dennis Schulmeister-Zimolong &lt;[dennis@wpvs.de](mailto:dennis@wpvs.de)&gt;** <br>

                **Version:** {version} <span class="text-secondary">|</span>
                **Stand:** {data["max_date"]}     <span class="text-secondary">|</span>
                [Quellcode](https://github.com/DennisSchulmeister/kolli-dashboard)

                ----
                ##### Lizenziert unter der BSD 3-Clause Lizenz

                Die Weitergabe und Verwendung in Quell- und Binärform, mit oder ohne Änderungen, ist gestattet,
                sofern die folgenden Bedingungen erfüllt sind:

                 1. Bei der Weitergabe des Quellcodes müssen der obige Urheberrechtsvermerk, diese Liste der
                    Bedingungen und der folgende Haftungsausschluss beibehalten werden.

                 2. Weiterverteilungen in binärer Form müssen den obigen Copyright-Hinweis, diese Liste der
                    Bedingungen und den folgenden Haftungsausschluss in der Dokumentation und/oder anderen
                    mit der Verteilung gelieferten Materialien wiedergeben.

                 3. Weder der Name des Urheberrechtsinhabers noch die Namen der Mitwirkenden dürfen ohne
                    ausdrückliche vorherige schriftliche Genehmigung verwendet werden, um von dieser Software
                    abgeleitete Produkte zu unterstützen oder zu bewerben.

                DIESE SOFTWARE WIRD VON DEN URHEBERRECHTSINHABERN UND MITWIRKENDEN IN DER VORLIEGENDEN FORM
                ZUR VERFÜGUNG GESTELLT, UND JEGLICHE AUSDRÜCKLICHE ODER STILLSCHWEIGENDE GARANTIE, EINSCHLIESSLICH,
                ABER NICHT BESCHRÄNKT AUF DIE STILLSCHWEIGENDE GARANTIE DER MARKTGÄNGIGKEIT UND EIGNUNG FÜR EINEN
                BESTIMMTEN ZWECK, WIRD ABGELEHNT. IN KEINEM FALL HAFTEN DER URHEBERRECHTSINHABER ODER DIE MITWIRKENDEN
                FÜR DIREKTE, INDIREKTE, ZUFÄLLIGE, BESONDERE, BEISPIELHAFTE SCHÄDEN ODER FOLGESCHÄDEN (EINSCHLIESSLICH,
                ABER NICHT BESCHRÄNKT AUF DIE BESCHAFFUNG VON ERSATZGÜTERN ODER -DIENSTLEISTUNGEN, NUTZUNGS-, DATEN-
                ODER GEWINNVERLUSTE ODER GESCHÄFTSUNTERBRECHUNGEN), WIE AUCH IMMER DIESE VERURSACHT WURDEN UND AUF
                WELCHER HAFTUNGSTHEORIE SIE BERUHEN, SEI ES DURCH VERTRAG, VERSCHULDENSUNABHÄNGIGE HAFTUNG ODER UNERLAUBTE
                HANDLUNG (EINSCHLIESSLICH FAHRLÄSSIGKEIT ODER ANDERWEITIG), DIE IN IRGENDEINER WEISE AUS DER NUTZUNG DIESER
                SOFTWARE ENTSTEHEN, AUCH WENN AUF DIE MÖGLICHKEIT SOLCHER SCHÄDEN HINGEWIESEN WURDE.

                ----

                ##### Projektförderung
                
                Das Forschungsprojekt KoLLI (Kooperative Lehr-Lern-Innovation) wird von der
                Stiftung Innovation in der Hochschullehre gefördert.
                """
            ),
            title      = "Forschungsprojekt KoLLI - Evaluationsergebnisse",
            easy_close = True,
            footer     = None,
            size       = "l",
        )

        ui.modal_show(m)
