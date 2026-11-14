
from pathlib import Path
import shutil

# File categories and their extensions
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".webm"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xlsx"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css"]
}


def get_category(extension):
    """Find the category for a file extension."""
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    """Prevent overwriting files with the same name."""
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}{destination.suffix}"
        )
        new_path = destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


def organize_files(folder_path):
    folder = Path(folder_path).expanduser()

    if not folder.exists() or not folder.is_dir():
        print("Error: Invalid folder path!")
        return

    organized_count = 0

    print("\nStarting file organization...\n")

    for file in folder.iterdir():

        if not file.is_file():
            continue

        category = get_category(file.suffix)

        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)

        destination = category_folder / file.name
        destination = get_unique_path(destination)

        try:
            shutil.move(str(file), str(destination))

            print(f"[OK] {file.name} -> {category}/")
            organized_count += 1

        except (OSError, shutil.Error) as error:
            print(f"[ERROR] {file.name}: {error}")

    print("\n" + "=" * 45)
    print("FILE ORGANIZATION COMPLETED")
    print(f"Total files organized: {organized_count}")
    print("=" * 45)


def main():
    print("=" * 45)
    print("       AUTOMATIC FILE ORGANIZER")
    print("=" * 45)

    folder_path = input(
        "\nEnter the folder path to organize: "
    ).strip().strip('"')

    if not folder_path:
        print("No folder path provided!")
        return

    confirm = input(
        "Files will be moved into category folders. Continue? (y/n): "
    ).strip().lower()

    if confirm == "y":
        organize_files(folder_path)
    else:
        print("Operation cancelled.")


if __name__ == "__main__":
    main()
