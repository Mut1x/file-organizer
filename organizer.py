import shutil
import sys
from pathlib import Path
from typing import Iterable, NoReturn

DRY_RUN = True

CATEGORIES = {
    ".pdf": "Documents",
    ".dmg": "Programs",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".txt": "Text",
    ".md": "Text",
    ".epub": "Documents/Books",
}


def confirm_prompt(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} (y/n)").strip().lower()

        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False

        print("Please enter y or n.")


def abort_and_print_message(message: str) -> NoReturn:
    print(message)
    sys.exit(1)


def plan_moves(working_directory: Path) -> list[tuple[Path, Path]]:
    if not working_directory.exists():
        abort_and_print_message(f"{working_directory} does not exist.")

    if not working_directory.is_dir():
        abort_and_print_message(f"{working_directory} is not a directory.")

    planned_moves = []
    for item in sorted(working_directory.iterdir()):
        if not item.is_file():
            continue

        category = CATEGORIES.get(item.suffix.lower(), "Other")
        target_dir = working_directory / category
        planned_moves.append((item, target_dir))

    return planned_moves


def collect_directories_to_create(
    planned_moves: Iterable[tuple[Path, Path]],
) -> set[Path]:
    dirs_to_create = set()
    for source, destination_dir in planned_moves:
        if not destination_dir.exists():
            dirs_to_create.add(destination_dir)

    return dirs_to_create


def get_summary_moves(planned_moves: Iterable[tuple[Path, Path]], dry_run: bool) -> str:
    summary = []

    for source, destination_dir in planned_moves:
        if dry_run:
            summary.append(f"Would move {source.name} to {destination_dir}")
        else:
            summary.append(f"Will move {source.name} to {destination_dir}")

    return "\n".join(summary)


def get_summary_dirs(dirs_to_create: set[Path], dry_run: bool) -> str:
    summary = []

    for dir_to_create in dirs_to_create:
        if dry_run:
            summary.append(f"Would create {dir_to_create}")
        else:
            summary.append(f"Will create {dir_to_create}")

    return "\n".join(summary)


def main():
    working_directory = Path(
        input("Specify a working directory that you want to organize: ").strip()
    ).expanduser()

    planned_moves = plan_moves(working_directory)
    dirs_to_create = collect_directories_to_create(planned_moves)

    print(get_summary_dirs(dirs_to_create, DRY_RUN))
    print(get_summary_moves(planned_moves, DRY_RUN))

    if DRY_RUN:
        abort_and_print_message("DRY RUN: Stopping the script.")

    if confirm_prompt("Proceed with moving files and creating directories:"):
        for directory in dirs_to_create:
            directory.mkdir(parents=True, exist_ok=True)
        for source, destination_dir in planned_moves:
            shutil.move(source, destination_dir / source.name)


if __name__ == "__main__":
    main()
