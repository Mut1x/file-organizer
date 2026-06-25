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


skipped_dirs = set()

downloads = Path.home() / "Downloads"

for item in downloads.iterdir():
    if item.is_file():
        category = CATEGORIES.get(item.suffix.lower(), "Other")
        target_dir = downloads / category

        if confirm_prompt(f"Create directory {target_dir}?"):
            print(f"Creating {target_dir}...")
            # target_dir.mkdir(parents=True, exist_ok=True)
        else:
            skipped_dirs.add(target_dir)
            print("Skipping...")

        if target_dir in skipped_dirs:
            print(f"Skipping {str(item)} since {target_dir} was not created")
        else:
            if confirm_prompt(f"Move {item.name} --> {target_dir}?"):
                print(f"moving {str(item)} ->{str(target_dir / item)}...")
                # shutil.move(str(item), str(target_dir / item.name))
            else:
                print("Skipping...")
