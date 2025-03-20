import os
from pathlib import Path

# Find the project root by looking for a known file or folder (like .git or pyproject.toml)
root_dir = Path(__file__).resolve().parents[
    next(i for i, p in enumerate(Path(__file__).resolve().parents) if (p / ".git").exists() or (p / "pyproject.toml").exists())
]


def get_root_path(folder):
    return f'{root_dir}/{folder}'

def extract_file_name(path):
    return os.path.splitext(os.path.basename(path))[0]


def list_csv_names(path):
    files = os.listdir(path)
    return sorted([extract_file_name(f) for f in files if f.endswith('.csv')])
