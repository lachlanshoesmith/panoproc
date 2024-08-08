import sys
import os
import logging
import webbrowser
import threading
from flask import Flask

VERSION = 0.1
URL = 'https://github.com/lachlanshoesmith/panoproc'

argv = sys.argv[1:]

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None


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


def open_website():
    if '-s' not in argv:
        print('Panoproc is running at http://localhost:5000.')
        open_page = input(
            'Would you like me to try open this for you [y/n]? ').lower()
        if open_page.startswith('y'):
            webbrowser.open('http://localhost:5000')


if __name__ == '__main__':
    check_args()
    splash()
    images = get_images(argv[0])
    if not images:
        print(f'{sys.argv[0]}: {argv[0]} contains no .jpg and .png images')
        sys.exit(1)

    server = threading.Thread(target=lambda: app.run(
        host='0.0.0.0', port=5000, use_reloader=False))
    server.start()

    open_website()

    print(f'Ready to process {len(images)} images')
    print('Done - thanks for using Panoproc :)')
    print('(Use Ctrl+C to close the server)')
