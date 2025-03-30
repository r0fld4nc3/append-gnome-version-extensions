import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path

parser = argparse.ArgumentParser(
    description="Iterate through GNOME extensions directory and add supported GNOME version."
)

LOOK_FOR_FILE = "metadata.json"


def create_backup(filepath: Path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = filepath.with_name(f"{filepath.stem}_backup_{timestamp}{filepath.suffix}")

    try:
        shutil.copy2(filepath, backup_file)
        print(f"Created backup: {backup_file}")
    except Exception as e:
        print(f"[ERROR] Failed to create backup for {filepath}: {e}")

    return backup_file


def process_files(directory: Path, version_number):
    subdirs = [d for d in directory.iterdir() if d.is_dir()]

    subdirs.insert(0, directory)

    for sub_dir in subdirs:
        for item in sub_dir.iterdir():
            if item.is_file() and item.name.lower() == LOOK_FOR_FILE:
                print()
                try:
                    with open(item, "r") as f:
                        data = json.load(f)
                except Exception as e:
                    print(f"[ERROR] Unable to parse file {item}: {e}")
                    continue

                shell_version = data.get("shell-version")

                if not shell_version:
                    print(f"Does not have 'shell-version': {item}")
                    continue

                if version_number not in shell_version:
                    shell_version.append(version_number)
                else:
                    # Don't need to do anything else
                    print(f"Skipping {item}: Version already present.")
                    continue

                data["shell-version"] = shell_version

                backup_file: Path = create_backup(item)
                if not backup_file.exists():
                    print(f"[ERROR] Skipping update for {item} due to backup failure")
                    continue

                # Write file
                print(f"Update file: {item}")
                try:
                    with open(item, "w") as f:
                        json.dump(data, f, indent=2)

                    # If we're here. it was successful
                    try:
                        print(f"Unlink backup: {backup_file}")
                        backup_file.unlink()
                    except Exception as e:
                        print(f"[ERROR] Unable to unlink backup file: {backup_file}")

                except Exception as e:
                    print(f"[ERROR] Unable to write to file {item}: {e}")

                break


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    # Root Directory
    parser.add_argument(
        "root_dir",
        type=Path,
        default=None,
        nargs="?",
        help="Path to the system location (default: current working directory).",
    )
    # Version Number
    parser.add_argument(
        "--version-number",
        "-vn",
        type=str,
        default=None,
        help="The version number to add (must be a numeric value)",
    )

    args = parser.parse_args()

    return args


def main():
    args = parse_args(parser)

    home = Path.home()
    path_gnome_extensions = home / ".local/share/gnome-shell/extensions/"

    root = args.root_dir
    version_number = args.version_number

    # Ensure version number is numeric
    if not str(version_number).isnumeric():
        print(f"Version Number {version_number} is not a valid numeric string value.")
        return False

    # Use path_gnome_extensions as default if root_dir is None
    root = Path(args.root_dir) if args.root_dir is not None else path_gnome_extensions

    if not root.is_dir():
        print(f"Root is not dir. Getting current parent structure.")
        root = root.parent

    print(f"Chosen root: {root}")

    process_files(root, version_number)

    print("Finished.")
    return True


if __name__ == "__main__":
    main()
