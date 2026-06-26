import shutil
import sys
from pathlib import Path

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


def main():
    planned_moves = []
    dirs_to_create = set()

    working_directory = Path(
        input("Specify a working directory that you want to organize: ").strip()
    ).expanduser()

    if not working_directory.exists():
        print(f"{working_directory} does not exist.")
        sys.exit(1)

    if not working_directory.is_dir():
        print(f"{working_directory} is not a directory.")
        sys.exit(1)

    for item in sorted(working_directory.iterdir()):
        if not item.is_file():
            continue

        category = CATEGORIES.get(item.suffix.lower(), "Other")
        target_dir = working_directory / category
        if confirm_prompt(f"Move {item.name} --> {target_dir}?"):
            planned_moves.append((item, target_dir))

    for source, destination_dir in planned_moves:
        if not destination_dir.exists():
            dirs_to_create.add(destination_dir)

    print("Creating directories to move files to...")
    for directory in dirs_to_create:
        if DRY_RUN:
            print(f"Would create {directory}")
        else:
            directory.mkdir(parents=True, exist_ok=True)

    print("Directories created...")
    print("Moving files...")

    summary = []

    for source, destination_dir in planned_moves:
        if DRY_RUN:
            summary.append(f"Would move {source.name} to {destination_dir}")
        else:
            summary.append(f"Will move {source.name} to {destination_dir}")

    print("\n".join(summary))

    if DRY_RUN:
        print("DRY_RUN: Stopping the script.")
        sys.exit(1)

    if confirm_prompt("Proceed with moving files:"):
        for source, destination_dir in planned_moves:
            shutil.move(source, destination_dir / source.name)


if __name__ == "__main__":
    main()
