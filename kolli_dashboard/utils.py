# Forschungsprojekt KoLLI: Dashboard
# © 2024 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

from pathlib import Path

def get_src_dir():
    """
    Get string with the source directory path. Use it like so to address files
    in the source tree: `get_src_dir() / "file.ext"`
    """
    return Path(__file__).resolve().parent