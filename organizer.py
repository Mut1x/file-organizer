import shutil
from pathlib import Path


def confirm_prompt(prompt: str) -> bool:
    while True:
        response = input(f"{prompt} (y/n)").strip().lower()

        if response in ("y", "yes"):
            return True
        if response in ("n", "no"):
            return False

        print("Please enter y or n.")


DRY_RUN = False

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

files_to_move = list()
dirs_to_create = set()

working_directory = Path(
    input("Specify a working directory that you want to organize: ").strip()
)

if not working_directory.exists():
    print(f"{working_directory} does not exist.")
    exit(1)

if not working_directory.is_dir():
    print(f"{working_directory} is not a directory.")
    exit(1)

for item in working_directory.iterdir():
    if not item.is_file():
        continue

    category = CATEGORIES.get(item.suffix.lower(), "Other")
    target_dir = working_directory / category
    if confirm_prompt(f"Move {item.name} --> {target_dir}?"):
        files_to_move.append({"file": item, "destination_dir": target_dir})

for file in files_to_move:
    if not file["destination_dir"].exists():
        dirs_to_create.add(file["destination_dir"])


print("Creating directories to move files to...")
for dir in dirs_to_create:
    if DRY_RUN:
        print(f"Would create {dir}")
    else:
        dir.mkdir(parents=True, exist_ok=True)

print("Directories created...")
print("Moving files...")

summary = ""

for file in files_to_move:
    if DRY_RUN:
        summary += f"Would move {file['file'].name} to {file['destination_dir']}\n"
    else:
        summary += f"Will move {file['file'].name} to {file['destination_dir']}\n"

print(summary)

if DRY_RUN:
    exit("DRY_RUN: Stopping the script.")

if confirm_prompt("Proceed with moving files:"):
    for file in files_to_move:
        shutil.move(file["file"], file["destination_dir"])
