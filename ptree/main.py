import os
import pathlib
import argparse
import yaml
from colorama import init, Fore


init(autoreset=True)
final_display_character = "└──"
display_character = "├──"


def count_with_level(root: pathlib.Path) -> tuple[int, int]:
    dirs = files = 0
    stack = [(root, 0)]  # (path, depth)

    while stack:
        path, depth = stack.pop()

        if path != root:
            if path.is_dir() and not (args.prune and empty_dir(path)):
                dirs += 1
            else:
                files += 1

        if not path.is_dir():  # skip iteration if 'path' is a file
            continue

        if int(args.level) and depth >= int(args.level):  # skip directories beyond level (if level > 0)
            continue

        # add children
        children = (
            child for child in path.iterdir()
            if args.all or not child.name.startswith(".")
        )
        stack.extend((child, depth + 1) for child in children)
    return dirs, files

def traverse_dir(dir_path: pathlib.Path, indent_level: int=1) -> None:
    if args.level != 0 and indent_level + 1 > args.level:  # ignoring directory if indicated level reached
        return

    dir_content = list(dir_path.iterdir())
    dir_content.sort(key=lambda item: item.is_file(), reverse=True)

    for content in dir_content:
        if content.name.startswith(".") and not args.all:  # removing hidden files and directories
            continue

        if content.is_dir():
            if args.prune and empty_dir(content):  # skipping if 'prune' set and the directory is empty
                continue

            dir_icon = yaml_icons.get("filetype").get("dir")
            print(f"│{" " * (indent_level * 3)}{display_character if dir_content else final_display_character}" + Fore.BLUE + f" {dir_icon} {content.name}")
            traverse_dir(content, indent_level + 1)
            continue

        if args.directory:  # listing only directories
            continue

        default_file_icon = yaml_icons.get("filetype").get("file")
        file_icon = (yaml_icons.get("name").get(content.name.lower())
                     or yaml_icons.get("extension").get(content.name.split(".")[-1]) or default_file_icon)
        file_size = "" if not args.size else f" [{human_readable_size(content.stat().st_size)}]"
        if content == dir_content[-1]:  # last file in directory
            print(f"│{" " * (indent_level * 3)}{final_display_character}" + file_size + Fore.GREEN + f" {file_icon} {content.name}")
            continue
        print(f"│{" " * (indent_level * 3)}{display_character}" + file_size + Fore.GREEN + f" {file_icon} {content.name}")

def empty_dir(path: pathlib.Path) -> bool:
    return not any(path.iterdir())

def human_readable_size(size: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}PB"

def run() -> None:
    root = pathlib.Path(args.path).resolve()
    print(Fore.BLUE + f"{yaml_icons.get("filetype").get("dir")} {args.path}")

    dir_content = list(root.iterdir())
    dir_content.sort(key=lambda item: item.is_file(), reverse=True)

    dir_icon = yaml_icons.get("filetype").get("dir")
    default_file_icon = yaml_icons.get("filetype").get("file")

    for content in dir_content:
        if content.name.startswith(".") and not args.all:  # removing hidden files and directories
            continue

        if content.is_dir():
            if args.prune and empty_dir(content):  # skipping if 'prune' set and the directory is empty
                continue

            print(f"{display_character if dir_content else final_display_character}" + Fore.BLUE + f" {dir_icon} {content.name}")
            if args.level == 1:  # displaying only the first level of files and directories
                continue
            traverse_dir(content)
            continue

        if args.directory:  # listing only directories
            continue

        file_icon = (yaml_icons.get("name").get(content.name.lower()) or
                     yaml_icons.get("extension").get(content.name.split(".")[-1]) or default_file_icon)
        file_size = "" if not args.size else f" [{human_readable_size(content.stat().st_size)}]"
        if content == dir_content[-1]:  # last file in directory
            print(f"{final_display_character}" + file_size + Fore.GREEN + f" {file_icon} {content.name}")
            continue
        print(f"{display_character}" + file_size + Fore.GREEN + f" {file_icon} {content.name}")

    directory_len, files_len = count_with_level(root)

    if args.directory:
        print(f"\n {dir_icon} {directory_len} directories")
        return

    print(f"\n {dir_icon} {directory_len} directories, {default_file_icon} {files_len} files")

def main() -> None:
    global args, yaml_icons

    parser = argparse.ArgumentParser(description="A colorful directory tree utility")
    parser.add_argument("path", help="Starting directory path", nargs="?", default=".")
    parser.add_argument("--all", help="List all files, by default hidden files are not displayed", action="store_true")
    parser.add_argument("-d", "--directory", help="List directory only", action="store_true")
    parser.add_argument("-l", "--level", help="Max depth to display (0 = no limit)", default=0, type=int)
    parser.add_argument("--prune", help="Prune empty directories from the output", action="store_true")
    parser.add_argument("-s", "--size", help="Print file size in a human readable way", action="store_true")

    yaml_path = os.path.join(os.path.dirname(__file__), "icons-sample.yaml")
    with open(yaml_path, encoding="utf-8") as f:
        yaml_icons = yaml.safe_load(f)

    args = parser.parse_args()
    run()


if __name__ == "__main__":
    main()  # calling the main function
