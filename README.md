# File Organizer

A short Pyhton script that organizes file into category subfolders, depending on the file extension.
It runs in a safe non-executing dry-run mode by default, showing what would happen without doing anything.

## Features
- Organizes files into folders according to extension (Documents, Images, Music, etc.)
- **Dry run by default** - Nothing is actually moved unless you pass `--execute`
- Asks for y/n confirmation before moving files or creating folders
- Only processes files directly in target directory (no recursion into subfolders)

## Requirements
- Pyhton 3.9+
- No extenral dependencies, it only uses `pathlib`, `argparse`, and `shutil` from standard library

## Usage

**Dry run** (default — shows what would happen, does not make changes):
```bash
python3 organize.py ~/Downloads
```

**Actually move files** (prints the plan, then asks for confirmation):
```bash
python3 organize.py ~/Downloads --execute
```

## Categories

| Extension(s) | Destination folder |
|---|---|
| `.pdf` | `Documents` |
| `.dmg` | `Programs` |
| `.jpg`, `.jpeg`, `.png` | `Images` |
| `.txt`, `.md` | `Text` |
| `.mp3`, `.flac`, `.aac` | `Music` |
| `.epub` | `Documents/Books` |
| anything else | `Other` |

Destination folders are created (if they don't already exist) under the target directory.

## How it works

1. Scans the top level of the given directory for files (ignores subdirectories).
2. Looks up the extension of each file in the category table to see where to put it.
3. Prints a summary of the folders that would be created and files that would be moved.
4. **Without `--execute`:** stops, this is the dry run.
5. **With `--execute`:** prompts `Proceed with moving files and creating directories: (y/n)` It creates the folders needed on `y` and moves the files with `shutil.move`.


## Notes

- File names are case-insensitively matched by extension (`.JPG` is treated the same as `.jpg`).
- If a file of the same name already exists in the destination, behavior follows Python's `shutil.move` defaults (it will generally overwrite a file at the destination).
- The directory argument supports `~` (e.g. `~/Downloads` expands to your home directory).
