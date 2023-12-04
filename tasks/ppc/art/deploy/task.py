#!/usr/bin/env python3
from os.path import dirname, join
from PIL import Image
import random

from rubik.cube import Cube


IMAGE_W, IMAGE_H = 291, 15
IMAGE_LEN = IMAGE_W * IMAGE_H
BG_COLORS = "BGORY"

MOVES = "L Li R Ri U Ui D Di F Fi B Bi M Mi E Ei S Si X Xi Y Yi Z Zi".split()


def nsplit(it, n):
    return [it[i : i + n] for i in range(0, len(it), n)]


def load_text_mask() -> list[str | None]:
    img = Image.open(join(dirname(__file__), "text.png"))
    assert img.size == (IMAGE_W, IMAGE_H)
    return list(map({(0, 0, 0, 0): None, (255, 255, 255, 255): "W"}.get, img.getdata()))


def generate_random_bg() -> str:
    return "".join(random.choices(BG_COLORS, k=IMAGE_LEN))


def split_into_faces(linear_picture: str) -> list[tuple[int, int, str]]:
    lines = [nsplit(l, 3) for l in nsplit(linear_picture, IMAGE_W)]

    faces = []
    for y, three_lines in enumerate(nsplit(lines, 3)):
        for x, what in enumerate(zip(*three_lines)):
            faces.append((x, y, "\n".join(what)))

    return faces


def challenge_round(x: int, y: int, face: str):
    # Shuffle the cube
    initial_cube = Cube("OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR")
    initial_cube.sequence(" ".join(random.choices(MOVES, k=21)))

    print("Out of my bag, I pull out a cube...")
    print(initial_cube)
    print(f"And here's a 3x3 section at ({x}, {y})")
    print(face)

    while True:
        while True:
            raw_moves = input("moves> ")
            if all(move in MOVES for move in raw_moves.split()):
                break
            print("These don't look like real moves, y'know? Let's try again.")
        moves = " ".join(raw_moves.split())

        cube = Cube(initial_cube)
        cube.sequence(moves)

        cube_str = str(cube)
        cube_front_face = "\n".join(
            (cube_str[28 : 28 + 3], cube_str[44 : 44 + 3], cube_str[60 : 60 + 3])
        )

        if cube_front_face == face:
            break

        print("Sorry, this doesn't look right. Let's try again.")

    print("Great! Moving on...")


if __name__ == "__main__":
    picture = "".join(
        [fg or bg for fg, bg in zip(load_text_mask(), generate_random_bg())]
    )

    print(f"Greetings! Let's cube a {IMAGE_W // 3}x{IMAGE_H // 3} picture!")
    print()
    print("I'll provide you with a random cube from my bag and a 3x3 section")
    print("of our picture. Your task is to help me assemble the cube so that")
    print("this section becomes its front face.")
    print()
    print("Let's get started!")
    print()

    faces = split_into_faces(picture)
    random.shuffle(faces)

    for x, y, face in faces:
        challenge_round(x, y, face)

    print("...we're done. Thanks! Bye.")
