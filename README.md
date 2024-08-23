# panoproc 🖼️
add location and pannellum-tour-related metadata to panoramas.

## installation

1. assure you have `poetry` [installed](https://python-poetry.org/docs/#installing-with-pipx) and a recent version of python3 installed (^3.10).
2. in the cloned repo, run `poetry install`.
3. run `poetry run python panoproc/panoproc.py folder_with_panoramas/ output.json`

## usage

`usage: panoproc [-h] [-s] [-o COMPRESSED_OUTPUT] directory outfile`

* `-s` is a silent mode.
* `-o` compresses panoramas with [mozjpeg](https://github.com/mozilla/mozjpeg), and it saves them in the directory specified as `COMPRESSED_OUTPUT`.

> ⚠️ note that the browser-opening functionality (powered by the `webbrowser` module) will not work under wsl.

## credits

cat.jpg by [yerlin matu](https://unsplash.com/@yerlinmatu) on [unsplash](https://unsplash.com/photos/shallow-focus-photography-of-white-and-brown-cat-GtwiBmtJvaU)
