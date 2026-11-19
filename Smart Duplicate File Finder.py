
import os
import hashlib
import shutil
from pathlib import Path
from collections import defaultdict


def calculate_hash(file_path):
    """Calculate SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(65536):
                sha256.update(chunk)

        return sha256.hexdigest()

    except (OSError, PermissionError) as error:
        print(f"Cannot read {file_path}: {error}")
        return None


def format_size(size):
    """Convert bytes into readable units."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def find_duplicates(folder):
    """Find duplicate files inside a folder."""
    hashes = defaultdict(list)

    print("\nScanning files... Please wait.\n")

    for root, dirs, files in os.walk(folder):
        # Avoid scanning previously moved duplicates
        dirs[:] = [
            d for d in dirs
            if d != "Duplicate_Files"
        ]

        for filename in files:
            file_path = Path(root) / filename

            try:
                if not file_path.is_file():
                    continue

                file_hash = calculate_hash(file_path)

                if file_hash:
                    hashes[file_hash].append(file_path)

            except OSError as error:
                print(f"Skipping {file_path}: {error}")

    return {
        file_hash: paths
        for file_hash, paths in hashes.items()
        if len(paths) > 1
    }


def display_duplicates(duplicates):
    """Display duplicate files and wasted space."""
    if not duplicates:
        print("No duplicate files found!")
        return

    wasted_space = 0

    print("\n========== DUPLICATE REPORT ==========")

    for index, files in enumerate(
        duplicates.values(), start=1
    ):
        print(f"\nDuplicate Group {index}")

        for file in files:
            print(f"  {file}")

        size = files[0].stat().st_size
        wasted_space += size * (len(files) - 1)

    print("\n======================================")
    print(f"Duplicate Groups: {len(duplicates)}")
    print(f"Wasted Space: {format_size(wasted_space)}")


def move_duplicates(duplicates, folder):
    """Move extra copies into a separate folder."""
    destination = Path(folder) / "Duplicate_Files"
    destination.mkdir(exist_ok=True)

    moved_count = 0

    for files in duplicates.values():
        # Keep the first file in its original location
        for file in files[1:]:
            target = destination / file.name

            counter = 1

            while target.exists():
                target = destination / (
                    f"{file.stem}_{counter}{file.suffix}"
                )
                counter += 1

            try:
                shutil.move(str(file), str(target))
                moved_count += 1

            except OSError as error:
                print(f"Could not move {file}: {error}")

    print(f"\nSuccessfully moved {moved_count} files!")
    print(f"Location: {destination}")


def main():
    print("=" * 45)
    print("       SMART DUPLICATE FILE FINDER")
    print("=" * 45)

    folder = input("\nEnter folder path: ").strip().strip('"')

    if not os.path.isdir(folder):
        print("Invalid folder path!")
        return

    duplicates = find_duplicates(folder)

    display_duplicates(duplicates)

    if duplicates:
        choice = input(
            "\nMove duplicates to a separate folder? (y/n): "
        ).strip().lower()

        if choice == "y":
            confirm = input(
                "Confirm moving duplicate files? (yes/no): "
            ).strip().lower()

            if confirm == "yes":
                move_duplicates(duplicates, folder)
            else:
                print("Operation cancelled.")
        else:
            print("No files were moved.")

    print("\nThank you for using Duplicate File Finder!")


if __name__ == "__main__":
    main()
