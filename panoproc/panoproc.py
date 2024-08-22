import sys
import os
import logging
import webbrowser
import threading
import shutil
import json
from flask import Flask, render_template, request
from pprint import pprint

VERSION = 0.1
URL = 'https://github.com/lachlanshoesmith/panoproc'

argv = sys.argv[1:]

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

current_image = -1
images = []
to_write = []


def write_to_disk():
    with open(f'{argv[1]}', 'w') as f:
        json.dump(to_write, f)


def get_image(image, index):
    global current_image
    current_image = index
    try:
        shutil.copyfile(image, 'panoproc/static/pano.jpg')
    except Exception as e:
        print(e)
        sys.exit(1)


@app.route('/submit', methods=['POST'])
def submit():
    res = request.json
    for hotspot in res['hotspots']:
        title = hotspot['title']
        image_filename = os.path.join(argv[0], title)
        if not os.path.exists(image_filename):
            print(
                f'{sys.argv[0]}: hotspot image filename {title} does not exist in {argv[0]}')
            return index()

    to_write.append(request.json)
    write_to_disk()
    if '-s' not in argv:
        print(f'Written...')
        pprint(res)
        print(f'...to {argv[1]}\n')

    if at_end():
        done()

    else:
        next_image()
        return index()


def at_end():
    return current_image == len(images) - 1


def next_image():
    image = images[current_image + 1]
    if '-s' not in argv:
        print(f'Processing {image}')
    get_image(image, current_image + 1)


@app.route('/')
def index():
    return render_template('index.html', image_name=images[current_image], image_number=current_image + 1, image_count=len(images))


def check_args():
    if len(argv) < 2 or len(argv) > 3 or argv[1] == '-s' or not argv[1].endswith('.json'):
        print(f'usage: {sys.argv[0]} directory outfile.json <-s>')
        sys.exit(1)
    if not os.path.isdir(argv[0]):
        print(f'{sys.argv[0]}: {argv[0]} does not exist')
        sys.exit(1)
    if os.path.exists(argv[1]):
        print(f'{sys.argv[0]}: {argv[1]} already exists')
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
            'Would you like me to try open the webpages [y/n]? ').lower()
        if open_page == 'y':
            webbrowser.open('http://localhost:5000')


def done():
    if '-s' not in argv:
        print('Done - thanks for using Panoproc :)')
    print('(Press Ctrl+C to close the server)')
    sys.exit(0)


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

    if '-s' not in argv:
        print(f'Ready to process {len(images)} images')

    next_image()
