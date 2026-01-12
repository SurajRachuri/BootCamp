import os

def get_files_by_extension(directory, extension=None):
    matching_files = []
    total_size = 0  # in bytes

    for root, dirs, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)

            if extension is None:  # "All" option → accept every file
                matching_files.append(full_path)
                total_size += os.path.getsize(full_path)

            elif file.lower().endswith(extension.lower()):
                matching_files.append(full_path)
                total_size += os.path.getsize(full_path)

    return matching_files, total_size


def format_size(size_bytes):
    # Converts bytes → KB / MB / GB friendly format
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024


if __name__ == "__main__":
    print("Select file type to search:")
    print("1. Text (.txt)")
    print("2. Word Document (.docx)")
    print("3. PDF (.pdf)")
    print("4. Python Files (.py)")
    print("5. ALL Files")

    choice = input("\nEnter your choice (1-5): ").strip()

    ext_map = {
        "1": ".txt",
        "2": ".docx",
        "3": ".pdf",
        "4": ".py",
        "5": None  # Means ALL files
    }

    if choice not in ext_map:
        print("Invalid choice!")
        exit()

    selected_ext = ext_map[choice]
    display_ext = "ALL Files" if selected_ext is None else selected_ext
    print(f"\nYou selected: {display_ext}")

    folder_path = r"C:\Users\9901201\Downloads"

    if not os.path.isdir(folder_path):
        print("Invalid folder path!")
        exit()

    print("\nSearching... Please wait...\n")

    files, total_size = get_files_by_extension(folder_path, selected_ext)

    if files:
        print("Files found:\n")
        for p in files:
            print(p)

        print("\n--------------------------------")
        print(f"Total files: {len(files)}")
        print(f"Total size: {format_size(total_size)}")
        print("--------------------------------")
    else:
        print(f"No files found in {folder_path}")