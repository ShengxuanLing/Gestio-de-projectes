# -*- coding: utf-8 -*-
"""Sincroniza Status / Start / End del Projects board con docs/tablero.csv.

Usa `gh project item-edit` por nombre de campo (evita el problema de los
option-id GraphQL). Ejecutar:  python docs/sync_board.py
"""

import csv
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE, "docs", "tablero.csv")
REPO = "ShengxuanLing/Trabajo_Gesti-projectes"
PROJECT = "1"
OWNER = "ShengxuanLing"

MAP = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "I": 9, "J": 10, "K": 11, "L": 12, "M": 13, "N": 14, "O": 15, "P": 16,
}


def edit(issue_no, field, kind, value):
    url = "https://github.com/%s/issues/%d" % (REPO, issue_no)
    cmd = [
        "gh", "project", "item-edit", PROJECT,
        "--owner", OWNER, "--url", url,
        "--field", field, "--" + kind, value,
    ]
    return subprocess.run(cmd, capture_output=True, text=True)


def main():
    with open(CSV_PATH, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    ok = fail = 0
    for row in rows:
        act = row["Title"].split(" - ", 1)[0]
        issue_no = MAP.get(act)
        if not issue_no:
            print("skip", act); continue

        for field, kind, value in (
            ("Status", "value", row["Status"]),
            ("Start", "date", row["Start"]),
            ("End", "date", row["End"]),
        ):
            r = edit(issue_no, field, kind, value)
            if r.returncode != 0:
                print("ERR %s (#%d) %s=%s: %s"
                      % (act, issue_no, field, value, r.stderr.strip()))
                fail += 1
                break
        else:
            ok += 1
            print("ok  %s (#%d) %s %s -> %s"
                  % (act, issue_no, row["Status"], row["Start"], row["End"]))

    print("--- done ok=%d fail=%d ---" % (ok, fail))
    sys.exit(0 if fail == 0 else 1)


if __name__ == "__main__":
    main()
