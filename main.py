import shutil
from pathlib import Path
from typing import Set


def find_files(path: Path, filepath_set: set) -> None:
    for x in path.iterdir():
        if x.is_dir():
            find_files(x, filepath_set)
        elif x.is_file():
            filepath_set.add(x)


def copy_file(filepath_to: Path, filepath_set: Set[Path]) -> None:
    for path in filepath_set:
        directory_path = Path(filepath_to / path.suffix.removeprefix('.'))
        directory_path.mkdir(parents=True, exist_ok=True)
        full_path = directory_path / path.name
        shutil.copyfile(path, full_path)


if __name__ == '__main__':
    path_from = Path('images')
    path_to = Path('sorted_files')
    files_set = set()

    find_files(path_from, files_set)
    copy_file(path_to, files_set)

