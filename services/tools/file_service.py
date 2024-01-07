"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from pathlib import Path

from os import path, stat


# https://stackoverflow.com/questions/13118029/deleting-folders-in-python-recursively
def delete_directory_content(directory):
    directory = Path(directory)

    for item in directory.iterdir():
        if item.is_dir():
            delete_directory_content(item)

        else:
            item.unlink()

    # Can me used to delete the folder itself
    # directory.rmdir()


def create_file(url):
    if path.exists(url):
        return

    file = open(url,
                "w")

    file.write("")

    file.close()


def clean_file(url):
    if not path.exists(url):
        return

    with open(url, "w") as file:
        file.write("")


def file_is_empty(url):
    return stat(url).st_size == 0
