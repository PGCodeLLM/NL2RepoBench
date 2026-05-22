import csv
import json
import subprocess
import tempfile
import os
import time

# Mapping from your previous task list to the owner/repo format
REPO_MAPPING = {
    "aiofiles": "Tinche/aiofiles", "arguably": "treykeown/arguably", "arxiv-mcp-server": "blazickjp/arxiv-mcp-server",
    "asteval": "newville/asteval", "autojump": "wting/autojump", "Autopep8": "hhatto/autopep8",
    "autorccar": "hamuchiwa/AutoRCCar", "binaryalert": "airbnb/binaryalert", "bleach": "mozilla/bleach",
    "boltons": "mahmoud/boltons", "boto": "boto/boto", "Box": "cdgriffith/Box", "Cachier": "shaypal5/cachier",
    "cerberus": "pyeve/cerberus", "Cherry": "Windsooon/cherry", "cookiecutter": "cookiecutter/cookiecutter",
    "coverage_shield": "matthias-k/coverage-shield", "databases": "encode/databases", "DBUtils": "WebwareForPython/DBUtils",
    "decouple": "henriquebastos/python-decouple", "deepdiff": "seperman/deepdiff", "DESlib": "scikit-learn-contrib/DESlib",
    "DictDataBase": "mkrd/DictDataBase", "docopt-ng": "jazzband/docopt-ng", "emoji": "carpedm20/emoji",
    "fastapi-users": "fastapi-users/fastapi-users", "flask-restful": "flask-restful/flask-restful", "flasky": "miguelgrinberg/flasky",
    "freezegun": "spulec/freezegun", "frontmatter": "eyeseast/python-frontmatter", "ftfy": "rspeer/python-ftfy",
    "funcy": "Suor/funcy", "fuzzywuzzy": "seatgeek/fuzzywuzzy", "gitingest": "cyclotruc/gitingest",
    "google-images-download": "hardikvasa/google-images-download", "graphneuralnetwork": "pyg-team/pytorch_geometric",
    "humanize": "python-humanize/humanize", "icecream": "gruns/icecream", "ipytest": "chmp/ipytest",
    "jinja": "pallets/jinja", "jsonlines": "wbolster/jsonlines", "jusText": "miso-belica/jusText",
    "markdownify": "matthewwithanm/python-markdownify", "markupsafe": "pallets/markupsafe", "math-verify": "huggingface/Math-Verify",
    "mechanicalsoup": "MechanicalSoup/MechanicalSoup", "mootdx": "bopo/mootdx", "More-Itertools": "more-itertools/more-itertools",
    "paillier": "data61/python-paillier", "pandarallel": "nalepae/pandarallel", "parse": "r1chardj0n3s/parse",
    "pathlib2": "mcmtroffaes/pathlib2", "pdfplumber-stable": "jsvine/pdfplumber", "plac": "micheles/plac",
    "pss": "eliben/pss", "PyAutoGUI": "asweigart/pyautogui", "pyjwt": "jpadilla/pyjwt", "pylama": "klen/pylama",
    "pyperclip": "asweigart/pyperclip", "pypinyin": "mozillazg/python-pinyin", "pyquery": "gawel/pyquery",
    "pysondb-v2": "pysondb/pysondb", "pytest-cov": "pytest-dev/pytest-cov", "pytestify": "dannysepler/pytestify",
    "python-dotenv": "theskumar/python-dotenv", "python-fsutil": "fabiocaccamo/python-fsutil", "python-jose": "mpdavis/python-jose",
    "python-pathspec": "cpburnz/python-pathspec", "python-patterns": "faif/python-patterns", "python-pytest-cases": "smarie/python-pytest-cases",
    "python-slugify": "un33k/python-slugify", "PythonProjectTemplate": "jacebrowning/template-python", "pytorch-grad-cam": "jacobgil/pytorch-grad-cam",
    "pytz": "stub42/pytz", "records": "kennethreitz/records", "requests-html": "psf/requests-html", "retrying": "rholder/retrying",
    "Rich-Click": "ewels/rich-click", "schedule-master": "dbader/schedule", "schema": "keleshev/schema",
    "six": "benjaminp/six", "sklearn": "scikit-learn/scikit-learn", "sortedcontainers": "grantjenks/python-sortedcontainers",
    "sqlparse": "andialbrecht/sqlparse", "Stable-Baselines3": "DLR-RM/stable-baselines3", "stamina": "hynek/stamina",
    "structlog": "hynek/structlog", "Synthetic": "dssg/synthetic", "tablib": "jazzband/tablib", "tenacity": "jd/tenacity",
    "tinydb": "msiemens/tinydb", "tqdm": "tqdm/tqdm", "trimming": "TrimTeam/PyTrim", "tsfresh": "blue-yonder/tsfresh",
    "typing_extensions": "python/typing_extensions", "uiautomator": "xiaocong/uiautomator", "unidecode": "avian2/unidecode",
    "unittest-parametrize": "martinpko/unittest-parametrize", "Verifiers": "PrimeIntellect-ai/verifiers", "voluptuous": "alecthomas/voluptuous",
    "wifiphisher": "wifiphisher/wifiphisher", "wsgidav": "mar10/wsgidav", "xlrd": "python-excel/xlrd", "ydata-profiling": "ydataai/ydata-profiling"
}

# Define what file extensions actually count as source code
CODE_EXTENSIONS = {
    '.py', '.pyx', '.c', '.h', '.cpp', '.hpp', '.cc', '.js', 
    '.ts', '.java', '.go', '.rs', '.rb', '.sh'
}

def count_lines_in_directory(directory):
    """
    Walks through the directory and counts lines of actual code.
    Filters by code file extensions and ignores blank lines and basic comments.
    """
    total_lines = 0
    for root, dirs, files in os.walk(directory):
        # Prevent diving into the .git folder
        if '.git' in dirs:
            dirs.remove('.git')
            
        for file in files:
            # 1. Only process files with recognized source code extensions
            ext = os.path.splitext(file)[1].lower()
            if ext not in CODE_EXTENSIONS:
                continue
                
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    for line in f:
                        stripped_line = line.strip()
                        
                        # 2. Skip empty lines
                        if not stripped_line:
                            continue
                            
                        # 3. Skip basic single-line comments 
                        # (Handles Python '#', and C/JS/Go/Rust '//' or '/*')
                        if stripped_line.startswith(('#', '//', '/*', '*')):
                            continue
                            
                        total_lines += 1
                        
            except UnicodeDecodeError:
                # Skip binary files silently
                pass
            except Exception as e:
                # Catch any other file permission errors and skip
                pass
                
    return total_lines

def get_real_loc(full_repo_name):
    """
    Performs a shallow git clone to a temporary directory,
    counts the actual lines of code, and cleans up.
    """
    repo_url = f"https://github.com/{full_repo_name}.git"
    
    # Create a temporary directory that automatically deletes itself when done
    with tempfile.TemporaryDirectory() as temp_dir:
        try:
            # --depth 1 pulls only the most recent commit, saving massive amounts of time and bandwidth
            subprocess.run(
                ['git', 'clone', '--depth', '1', repo_url, temp_dir],
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL, 
                check=True
            )
            return count_lines_in_directory(temp_dir)
        except subprocess.CalledProcessError:
            print(f"  [Error] Failed to clone {full_repo_name}.")
            return None

def main():
    csv_file = "task_difficulty.csv"
    output_file = "repo_lines.json"
    results = []

    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found. Please ensure the path is correct.")
        return

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue
            
            task_name = row[0].strip()
            difficulty = row[1].strip()

            full_repo_name = REPO_MAPPING.get(task_name)
            if not full_repo_name:
                print(f"Skipping {task_name}: No mapped repository found.")
                continue

            repo_name = full_repo_name.split("/")[-1]
            
            print(f"Cloning & Counting LOC for: {full_repo_name}...")
            
            # Use our new shallow clone method
            loc = get_real_loc(full_repo_name)

            if loc is not None:
                results.append({
                    "full-repo-name": full_repo_name,
                    "repo-name": repo_name,
                    "lines_of_code": loc,
                    "difficulty": difficulty
                })
                print(f"  -> {loc:,} lines")

    with open(output_file, "w", encoding="utf-8") as json_out:
        json.dump(results, json_out, indent=4)
        
    print(f"\nSuccessfully generated {output_file} with {len(results)} repositories.")

if __name__ == "__main__":
    main()