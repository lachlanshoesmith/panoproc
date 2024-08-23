import sys
import os
import logging
import webbrowser
import threading
import shutil
import json
import argparse
import mozjpeg_lossless_optimization
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request
from pprint import pprint

VERSION = 0.1
URL = 'https://github.com/lachlanshoesmith/panoproc'

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

current_image = -1
images = []
to_write = []


def get_images(path):
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError(f'{path} does not exist')

    if imgs := [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(
            os.path.join(path, f)) and (f.endswith('.png') or f.endswith('.jpg'))]:
        return imgs
    else:
        raise argparse.ArgumentTypeError(
            f'{path} doesn\'t contain any .jpgs or .pngs')


parser = argparse.ArgumentParser(
    prog='panoproc',
    description='Add metadata to (and optionally compress) panoramas, stored in a JSON file.',
)
parser.add_argument('directory', help='directory containing panoramas',
                    type=str)
parser.add_argument('outfile', help='output JSON file',
                    type=argparse.FileType('w'))
parser.add_argument('-s', '--silent', action='store_true', help='silent mode')
parser.add_argument(
    '-o', '--compressed-output', help='output folder for compressed panoramas', type=str)

args = parser.parse_args()
images_folder = args.directory
json_outfile = args.outfile
silent = args.silent
compressed_output_folder = args.compressed_output


def write_to_disk():
    with open(f'{json_outfile}', 'w') as f:
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
        image_filename = os.path.join(images_folder, title)
        if not os.path.exists(image_filename):
            print(
                f'{sys.argv[0]}: hotspot image filename {title} does not exist in {images_folder}')
            return index()

    to_write.append(request.json)
    write_to_disk()
    if not silent:
        print(f'Written...')
        pprint(res)
        print(f'...to {images_folder}\n')

    if at_end():
        done()

    else:
        next_image()
        return index()


def at_end():
    return current_image == len(images) - 1


def compress_image(image):
    if not os.path.exists(compressed_output_folder):
        os.makedirs(compressed_output_folder)

    jpeg_io = BytesIO()

    with Image.open(image, 'r') as input_f:
        input_f.convert('RGB').save(jpeg_io, 'JPEG', quality=70)

    jpeg_io.seek(0)
    input_bytes = jpeg_io.read()

    output_bytes = mozjpeg_lossless_optimization.optimize(input_bytes)

    with open(os.path.join(compressed_output_folder, os.path.basename(image)), 'wb') as output_f:
        output_f.write(output_bytes)

    if not silent:
        print(
            f'Compressed {os.path.basename(image)} -> {os.path.join(compressed_output_folder, os.path.basename(image))}')


def next_image():
    image = images[current_image + 1]
    if not silent:
        print(f'Processing {image}')

    if compressed_output_folder:
        compress_image(image)

    get_image(image, current_image + 1)


@app.route('/')
def index():
    return render_template('index.html', image_name=images[current_image], image_number=current_image + 1, image_count=len(images))


def splash():
    if not silent:
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


def open_website():
    if not silent:
        print('Panoproc is running at http://localhost:5000.')
        open_page = input(
            'Would you like me to try open the webpages [y/n]? ').lower()
        if open_page == 'y':
            webbrowser.open('http://localhost:5000')


def done():
    if not silent:
        print('Done - thanks for using Panoproc :)')
    print('(Press Ctrl+C to close the server)')
    sys.exit(0)


if __name__ == '__main__':
    splash()
    images = get_images(images_folder)

    server = threading.Thread(target=lambda: app.run(
        host='0.0.0.0', port=5000, use_reloader=False))
    server.start()

    open_website()

    if not silent:
        print(f'Ready to process {len(images)} images')

    next_image()
