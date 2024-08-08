import sys
import pygame
from os import listdir
from os.path import isdir, isfile, join

VERSION = 0.1
URL = 'https://github.com/lachlanshoesmith/panoproc'

argv = sys.argv[1:]


def check_args():
    if len(argv) == 0 or len(argv) > 2:
        print(f'usage: {sys.argv[0]} directory <-s>')
        sys.exit(1)
    if not isdir(argv[0]):
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
    return [f for f in listdir(path) if isfile(join(path, f) and (f.endswith('.png') or f.endswith('.jpg')))]


def open_editor(images):
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('panoproc')

    clock = pygame.time.Clock()
    running = True

    print(images)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill('purple')
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    print('thanks for using panoproc :)')
    sys.exit(0)


if __name__ == '__main__':
    check_args()
    splash()
    images = get_images(argv[0])
    if not images:
        print(f'{sys.argv[0]}: {argv[0]} contains no .jpg and .png images')
        sys.exit(1)
    open_editor(images)
