#!/usr/bin/env bash
# Sincroniza Status / Start / End del Projects board con docs/tablero.csv.
# Usa gh project item-edit (por nombre de campo) para evitar el problema de
# los option-id GraphQL.
set -euo pipefail
cd "$(dirname "$0")/.."
OWNER=ShengxuanLing
REPO=ShengxuanLing/Trabajo_Gesti-projectes
PROJECT=1

# id de la WBS A-P -> numero de issue
declare -A MAP=(
  [A]=1 [B]=2 [C]=3 [D]=4 [E]=5 [F]=6 [G]=7 [H]=8
  [I]=9 [J]=10 [K]=11 [L]=12 [M]=13 [N]=14 [O]=15 [P]=16
)

ok=0; fail=0
while IFS=, read -r title status start end _ rest; do
  # primera columna: "A - Mapear consumo ..."
  id="${title%% - *}"
  issue=${MAP[$id]:-}
  [ -n "$issue" ] || { echo "skip $id (no issue)"; continue; }
  url="https://github.com/$REPO/issues/$issue"

  # Status
  if gh project item-edit "$PROJECT" --owner "$OWNER" --url "$url" \
       --field "Status" --value "$status" >/dev/null 2>&1; then
    :
  else
    echo "ERR status $id (#$issue) $status"; fail=$((fail+1)); continue
  fi

  # Start
  if gh project item-edit "$PROJECT" --owner "$OWNER" --url "$url" \
       --field "Start" --date "$start" >/dev/null 2>&1; then
    :
  else
    echo "ERR start $id (#$issue) $start"; fail=$((fail+1)); continue
  fi

  # End
  if gh project item-edit "$PROJECT" --owner "$OWNER" --url "$url" \
       --field "End" --date "$end" >/dev/null 2>&1; then
    :
  else
    echo "ERR end $id (#$issue) $end"; fail=$((fail+1)); continue
  fi

  ok=$((ok+1))
  echo "ok  $id (#$issue) $status  $start -> $end"
done < <(tail -n +2 docs/tablero.csv)

echo "--- done ok=$ok fail=$fail ---"
