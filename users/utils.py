import random
from io import BytesIO

from PIL import Image, ImageDraw

from .constants import (
    COLOR_RED,
    COLOR_LIGHT_BLUE,
    COLOR_GREEN,
    COLOR_PINK,
    SIZE,
    COLOR_TEXT,
)


def generate_avatar(letter):
    img = Image.new(
        "RGB",
        (SIZE, SIZE),
        color=random.choice(
            [COLOR_RED, COLOR_LIGHT_BLUE, COLOR_GREEN, COLOR_PINK]
        ),
    )

    draw = ImageDraw.Draw(img)
    draw.text((SIZE / 2, SIZE / 2), letter.upper(), fill=COLOR_TEXT)

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return buffer.getvalue()
