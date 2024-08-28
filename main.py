import shutil
from pathlib import Path
from typing import Set
from threading import Semaphore, Thread


def find_files(path: Path) -> Set[Path]:
    filepath_set = set()
    for x in path.iterdir():
        if x.is_dir():
            filepath_set.update(find_files(x))
        elif x.is_file():
            filepath_set.add(x)
    return filepath_set


def make_paths(filepath_to: Path, filepath_set: Set[Path]) -> dict:
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


def get_path(paths: dict):
    return paths.popitem()


def copy_file(paths: dict, condition) -> None:
    copy_paths_dict = paths.copy()
    old_path, new_path = get_path(copy_paths_dict)
    with condition:
        shutil.copyfile(old_path, new_path)


if __name__ == '__main__':
    path_from = Path('images')
    path_to = Path('sorted_files')
    files_set = find_files(path_from)
    files_old_and_new_paths = make_paths(path_to, files_set)

    pool = Semaphore(4)
    for _ in range(10):
        thread = Thread(target=copy_file, args=(files_old_and_new_paths, pool))
        thread.start()
