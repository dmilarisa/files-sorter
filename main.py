import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging

"""
First, parse a folder to get a structure - store in the list all directories which we'll need to parse further
For this purpose we're using library argparse which helps dealing with command line

"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source dir", required=True)
parser.add_argument("--output", "-o", help="Output dir", default="dist")

print(parser.parse_args())
args = vars(parser.parse_args())
print(args)

source = Path(args.get("source"))
output = Path(args.get("output"))

folders = []


def grabs_folders(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folders(el)


# Next function makes dirs with name like files extensions and then copies corresponding files to these dirs
def copy_file(path: Path) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / ext
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / el.name)
            except OSError as err:
                logging.error(err)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(threadName)s %(message)s')

    folders.append(source)
    grabs_folders(source)
    print(folders)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]
    print(f"You can delete {source} now, all files are copied to 'dist' dir")
