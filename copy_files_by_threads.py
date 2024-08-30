import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from pathlib import Path


handled_file_paths = set()
handled_folder_paths = set()
lock = RLock()


def find_files(path_from: Path, path_to: Path):
    for x in path_from.iterdir():
        if x.is_file():
            with lock:
                if x in handled_file_paths:
                    continue
                handled_file_paths.add(x)

            full_path = make_paths(x, path_to)
            copy_file(x, full_path)

        elif x.is_dir():
            find_files(x, path_to)


def make_paths(path_from: Path, path_to: Path) -> Path:
    if not path_from.suffix:
        subdir = path_to / 'no_suffix'
    else:
        subdir = path_to / path_from.suffix.removeprefix('.')

    if subdir not in handled_folder_paths:
        handled_folder_paths.add(subdir)
        subdir.mkdir(parents=True, exist_ok=True)

    full_path = path_to / path_from.suffix.removeprefix('.') / path_from.name
    if full_path.exists():
        full_path = path_to / path_from.suffix.removeprefix('.') / f"{full_path.stem}_copy{full_path.suffix}"
    return full_path


def copy_file(path_from: Path, path_to: Path) -> None:
    shutil.copyfile(path_from, path_to)


if __name__ == '__main__':
    start_time = time.time()
    first_path = None
    second_path = Path('dist')
    thread_count = 6

    if len(sys.argv) < 2 or len(sys.argv) > 4:
        sys.exit('Arguments must me: first_path second_path threads_count / or first_path second_path')
    elif len(sys.argv) == 4 and sys.argv[3].isdigit():
        thread_count = int(sys.argv[3])

    if len(sys.argv) >= 3:
        second_path = Path(sys.argv[2])
    first_path = Path(sys.argv[1])

    with ThreadPoolExecutor(max_workers=thread_count) as executor:
        for _ in range(thread_count):
            executor.submit(find_files, first_path, second_path)

    print(f"{len(handled_file_paths)} files handled in {time.time() - start_time} seconds with {thread_count} threads")
