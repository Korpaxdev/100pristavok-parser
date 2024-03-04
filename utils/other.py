import shutil
from pathlib import Path
from typing import Callable


def create_dir_if_not_exists(dir_path: Path):
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def convert_to_path(path: str | Path):
    if isinstance(path, Path):
        return path
    return Path(path)


def run_callback_with_ignore_errors(callback: Callable, **kwargs):
    try:
        return callback(**kwargs)
    except Exception as e:
        message = getattr(e, "message") if hasattr(e, "message") else e
        print(message)
        return None


def remove_dir_if_exists(dir_path: Path | str):
    dir_path = convert_to_path(dir_path)
    if dir_path.exists():
        return shutil.rmtree(dir_path)


def str_to_int(value: str) -> int:
    return int(value.strip().replace(" ", ""))
