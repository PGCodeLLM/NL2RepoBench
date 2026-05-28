#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
HARBOR="$SCRIPT_DIR/harbor"

# Map of task-name (lowercase) -> full-repo-name
declare -A REPO_MAP=(
    [autorccar]="hamuchiwa/AutoRCCar"
    [requests-html]="psf/requests-html"
    [markupsafe]="pallets/markupsafe"
    [fuzzywuzzy]="seatgeek/fuzzywuzzy"
    [decouple]="henriquebastos/python-decouple"
    [google-images-download]="hardikvasa/google-images-download"
    [frontmatter]="eyeseast/python-frontmatter"
    [pandarallel]="nalepae/pandarallel"
    [python-slugify]="un33k/python-slugify"
    [cherry]="Windsooon/cherry"
    [aiofiles]="Tinche/aiofiles"
    [python-fsutil]="fabiocaccamo/python-fsutil"
    [python-patterns]="faif/python-patterns"
    [pylama]="klen/pylama"
    [pytest-cov]="pytest-dev/pytest-cov"
    [databases]="encode/databases"
    [uiautomator]="xiaocong/uiautomator"
    [pyautogui]="asweigart/pyautogui"
    [binaryalert]="airbnb/binaryalert"
    [tinydb]="msiemens/tinydb"
    [deepdiff]="seperman/deepdiff"
    [boltons]="mahmoud/boltons"
    [wifiphisher]="wifiphisher/wifiphisher"
    [cachier]="shaypal5/cachier"
    [pyjwt]="jpadilla/pyjwt"
    [dbutils]="WebwareForPython/DBUtils"
    [sortedcontainers]="grantjenks/python-sortedcontainers"
    [python-pytest-cases]="smarie/python-pytest-cases"
    [fastapi-users]="fastapi-users/fastapi-users"
    [autopep8]="hhatto/autopep8"
)

for task in "${!REPO_MAP[@]}"; do
    repo_dir="$HARBOR/$task/solution/repo"
    mkdir -p "$repo_dir"

    if [ -d "$repo_dir/.git" ]; then
        echo "[SKIP] $task already cloned"
    else
        echo "[CLONE] ${REPO_MAP[$task]} -> $repo_dir"
        echo "git clone git@github.com:${REPO_MAP[$task]}.git -> $repo_dir"
        git clone "git@github.com:${REPO_MAP[$task]}.git" "$repo_dir"
    fi
done

echo "Done."