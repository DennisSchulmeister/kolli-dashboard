#! /usr/bin/env python3

# Forschungsprojekt KoLLI: Dashboard
# © 2025 DHBW Karlsruhe / Studiengang Wirtschaftsinformatik
# Dennis Schulmeister-Zimolong <dennis@wpvs.de>
#
# This source code is licensed under the BSD 3-Clause License found in the
# LICENSE file in the root directory of this source tree.

#==============================================================================
# Small script to filter out the e-mail addresses from the data file.
# The e-mail addresses will be printed on the console.
#==============================================================================

import csv, sys

input_path = "kolli_dashboard/data/data.csv"
columns_to_remove = ["AA05_01", "R206_01"]

# Read the file
with open(input_path, "r", encoding="utf-16") as f:
    reader = csv.DictReader(f, delimiter="\t")
    rows = list(reader)
    fieldnames = reader.fieldnames

# Find indices of columns to remove
if not fieldnames:
    sys.exit(-1)

remove_indices = [fieldnames.index(col) for col in columns_to_remove if col in fieldnames]

# Print and remove the columns
for row in rows:
    questionnaire = row.get("QUESTNNR", "").strip()

    for col in columns_to_remove:
        email = row.get(col, "").strip()

        if email != "":
            print(questionnaire, "\t", email)

# Write back the filtered data
new_fieldnames = [fn for fn in fieldnames if fn not in columns_to_remove]

with open(input_path, "w", encoding="utf-16", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=new_fieldnames, delimiter="\t")
    writer.writeheader()

    for row in rows:
        filtered_row = {k: v for k, v in row.items() if k in new_fieldnames}
        writer.writerow(filtered_row)