# panoproc 🖼️

a level editor for the [yellowshirt](https://github.com/devsoc-unsw/trainee-woodelf-24t2) project.
more generally, panoproc lets you add location and pannellum-tour-related metadata to panoramas, which is then stored in a specified json file.

## installation

1. assure you have `poetry` [installed](https://python-poetry.org/docs/#installing-with-pipx) and a recent version of python3 installed (^3.10).
2. in the cloned repo, run `poetry install`.
3. run `poetry run python panoproc/panoproc.py folder_with_panoramas/ output.json`

## usage

### cli

`usage: panoproc [-h] [-s] [-o COMPRESSED_OUTPUT] directory outfile`

* `-s` is a silent mode.
* `-o` compresses panoramas with [mozjpeg](https://github.com/mozilla/mozjpeg), and it saves them in the directory specified as `COMPRESSED_OUTPUT`.

> ⚠️ note that the browser-opening functionality (powered by the `webbrowser` module) will not work under wsl.

### gui

once the cli has started successfully, the gui will be accessible on port `5000`.

the gui is composed of several elements:
* the **panorama viewer** is useful for not only visualising the image you're working with, but to identify where you might want to place 'hotspots' - clickable buttons that sit above the panorama at a certain angle in a certain spot. these buttons may be clicked to transition between different images, as if you're on a self-guided tour.
* the **basic metadata** section holds the known geographical data about the image.
	* note that this will be N/A by default, regardless of any actual metadata embedded into the image.
* below the **last clicked** heading sits information about the angle and place where a user last clicked in the panorama. once you are happy with the location of a hotspot...
	1. click in said location,
	2. type in the name of the image you're linking to, and
	3. press add!
* the **clickable spots** table holds a list of the hotspots.
* the **map** lets you choose where exactly the image was taken.
* the **submit and load next image** button does what it says.

once you have been through all of the images, a message will be printed to the cli and you can exit the program when you're ready.

## credits

* [pannellum](https://github.com/mpetroff/pannellum/) by matthew petroff
* [mazemap](https://api.mazemap.com/js/v2.1.2/docs/)
* cat.jpg by [yerlin matu](https://unsplash.com/@yerlinmatu) on [unsplash](https://unsplash.com/photos/shallow-focus-photography-of-white-and-brown-cat-GtwiBmtJvaU)
