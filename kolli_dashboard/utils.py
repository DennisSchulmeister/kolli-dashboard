# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path

src_dir = Path(__file__).resolve().parent

scale_minus_plus = ["--", "-", "±", "+", "++"]

def to_scale_minus_plus(nr):
    try:
        nr = int(nr)
    except ValueError:
        nr = -1

    if nr == 1:
        return "--"
    elif nr == 2:
        return "-"
    elif nr == 3:
        return "+"
    elif nr == 4:
        return "++"
    else:
        return "±"

def checkbox_to_scale_minus_plus(nr):
    try:
        nr = int(nr)
    except ValueError:
        nr = -1

    if nr == 1:
        return "--"
    elif nr == 2:
        return "++"
    else:
        return "±"