""" converter """

import json
from base64 import b64decode
from pathlib import Path

import click

DATA_DIR = Path(__file__).parent / "responses"


@click.command()
@click.option("--filename", prompt="Enter file name", help="Input file name")
def main(filename: str) -> None:
    "main func"

    filepath = DATA_DIR / filename

    while not filepath.exists() or not filepath.is_file():
        filename = input("Not a file or path doesn't exist! Enter filename: ")
        filepath = DATA_DIR / filename

    imagepath = Path(__file__).parent / "images" / filepath.stem
    imagepath.mkdir(parents=True, exist_ok=True)

    with filepath.open("r", encoding="utf-8") as file:
        response = json.load(file)

    for index, image_dict in enumerate(response["data"]):
        image_data = b64decode(image_dict["b64_json"])
        image_file = imagepath / f"{filepath.stem}-{index}.png"

        with image_file.open("wb") as image:
            image.write(image_data)


if __name__ == "__main__":
    main()
