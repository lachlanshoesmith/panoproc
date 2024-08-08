import sys
import os
import webview

VERSION = 0.1
URL = 'https://github.com/lachlanshoesmith/panoproc'

argv = sys.argv[1:]


def check_args():
    if len(argv) == 0 or len(argv) > 2:
        print(f'usage: {sys.argv[0]} directory <-s>')
        sys.exit(1)
    if not os.path.isdir(argv[0]):
        print(f'{sys.argv[0]}: {argv[0]} does not exist')
        sys.exit(1)


def splash():
    if '-s' not in argv:
        print(f'''
  _____        _   _  ____  _____  _____   ____   _____
 |  __ \ /\   | \ | |/ __ \|  __ \|  __ \ / __ \ / ____|
 | |__) /  \  |  \| | |  | | |__) | |__) | |  | | |
 |  ___/ /\ \ | . ` | |  | |  ___/|  _  /| |  | | |
 | |  / ____ \| |\  | |__| | |    | | \ \| |__| | |____
 |_| /_/    \_\_| \_|\____/|_|    |_|  \_\\____/ \_____|

by Lachlan Shoesmith, v{VERSION}
{URL}
''')


def get_images(path):
    return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(
        os.path.join(path, f)) and (f.endswith('.png') or f.endswith('.jpg'))]


def open_editor(images):
    webview.create_window('panoproc', 'https://google.com')
    webview.start()


if __name__ == '__main__':
    check_args()
    splash()
    images = get_images(argv[0])
    if not images:
        print(f'{sys.argv[0]}: {argv[0]} contains no .jpg and .png images')
        sys.exit(1)
    open_editor(images)
