import json
from pathlib import Path

cwd = Path().cwd()
json_path = cwd / 'data' / 'variables.json'
with open(json_path) as f:
    variables = json.load(f)