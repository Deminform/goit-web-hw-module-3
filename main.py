import shutil
from pathlib import Path
from typing import Set


def find_files(path: Path) -> Set[Path]:
    filepath_set = set()
    for x in path.iterdir():
        if x.is_dir():
            filepath_set.update(find_files(x))
        elif x.is_file():
            filepath_set.add(x)
    return filepath_set


def make_path(filepath_to: Path, filepath_set: Set[Path]) -> dict:
    filepath_dict = {}
    for file_path in filepath_set:
        if not file_path.suffix:
            subdir = filepath_to / 'no_suffix'
        else:
            subdir = filepath_to / file_path.suffix.removeprefix('.')
        subdir.mkdir(parents=True, exist_ok=True)
        full_path = filepath_to / file_path.suffix.removeprefix('.') / file_path.name
        while full_path in filepath_dict.values():
            full_path = filepath_to / file_path.suffix.removeprefix('.') / f"{full_path.stem}_copy{full_path.suffix}"
        filepath_dict.update({file_path: full_path})
    return filepath_dict


def copy_file(filepath_to: Path, filepath_set: Set[Path]) -> None:
    file_paths = make_path(filepath_to, filepath_set)
    for old_path, new_path in file_paths.items():
        shutil.copyfile(old_path, new_path)


if __name__ == '__main__':
    path_from = Path('images')
    path_to = Path('sorted_files')
    files_set = find_files(path_from)

    copy_file(path_to, files_set)
