import os
import pathlib
import argparse
import yaml
from colorama import init, Fore


init(autoreset=True)
final_display_character = "└──"
display_character = "├──"


def traverse_dir(dir_path: pathlib.Path, indent_level: int=1) -> None:
    dir_content = list(dir_path.iterdir())
    dir_content.sort(key=lambda item: item.is_file(), reverse=True)

    for content in dir_content:
        if content.name.startswith(".") and not args.all:  # removing hidden files and directories
            continue

        if content.is_dir():
            dir_icon = yaml_icons.get("filetype").get("dir")
            print(f"│{" " * (indent_level * 3)}{display_character if dir_content else final_display_character}" + Fore.BLUE + f"  {dir_icon} {content.name}")
            traverse_dir(content, indent_level + 1)
            continue

        if args.directory:  # listing only directories
            continue

        default_file_icon = yaml_icons.get("filetype").get("file")
        file_icon = (yaml_icons.get("name").get(content.name.lower())
                     or yaml_icons.get("extension").get(content.name.split(".")[-1]) or default_file_icon)
        if content == dir_content[-1]:  # last file in directory
            print(f"│{" " * (indent_level * 3)}{final_display_character}" + Fore.GREEN + f" {file_icon} {content.name}")
            continue
        print(f"│{" " * (indent_level * 3)}{display_character}" + Fore.GREEN + f" {file_icon} {content.name}")

def is_hidden(path, root) -> bool:
    try:
        relative = path.relative_to(root)
        return any(part.startswith('.') for part in relative.parts)
    except ValueError:
        return False

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
            print(
                f"{display_character if dir_content else final_display_character}" + Fore.BLUE + f"  {dir_icon} {content.name}")
            traverse_dir(content)
            continue

        if args.directory:  # listing only directories
            continue

        file_icon = (yaml_icons.get("name").get(content.name.lower()) or
                     yaml_icons.get("extension").get(content.name.split(".")[-1]) or default_file_icon)
        if content == dir_content[-1]:  # last file in directory
            print(f"{final_display_character}" + Fore.GREEN + f" {file_icon} {content.name}")
            continue
        print(f"{display_character}" + Fore.GREEN + f" {file_icon} {content.name}")

    if args.all:
        all_paths = list(root.rglob("*"))
    else:
        all_paths = [p for p in root.rglob("*") if not is_hidden(p, root)]

    directory_len = sum(1 for d in all_paths if d.is_dir())
    files_len = sum(1 for f in all_paths if f.is_file())

    if args.directory:
        print(f"\n {dir_icon} {directory_len} directories")
        return

    print(f"\n {dir_icon} {directory_len} directories, {default_file_icon} {files_len} files")

def main() -> None:
    global args, yaml_icons

    parser = argparse.ArgumentParser(description="A colorful directory tree utility")
    parser.add_argument("path", help="Starting directory path")
    parser.add_argument("--all", help="List all files, by default hidden files are not displayed", action="store_true")
    parser.add_argument("-d", "--directory", help="List directory only", action="store_true")

    yaml_path = os.path.join(os.path.dirname(__file__), "icons-sample.yaml")
    with open(yaml_path, encoding="utf-8") as f:
        yaml_icons = yaml.safe_load(f)

    args = parser.parse_args()
    run()


if __name__ == "__main__":
    main()  # calling the main function
