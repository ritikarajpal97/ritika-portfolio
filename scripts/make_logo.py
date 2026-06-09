"""Generate a 512x512 favicon PNG that mirrors the RR-in-hexagon SVG logo."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

OUT = Path(__file__).resolve().parent.parent / "src" / "images" / "logo.png"

SIZE = 512
NAVY = (10, 25, 47)
GREEN = (100, 255, 218)

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def load_font(size):
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


img = Image.new("RGBA", (SIZE, SIZE), NAVY + (255,))
draw = ImageDraw.Draw(img)

# Regular hexagon (pointy-top), centered, ~80% of canvas.
cx, cy = SIZE / 2, SIZE / 2
r = SIZE * 0.42
points = [
    (cx + r * math.sin(math.radians(60 * i)), cy - r * math.cos(math.radians(60 * i)))
    for i in range(6)
]
draw.polygon(points, outline=GREEN, fill=NAVY, width=24)

font = load_font(200)
text = "RR"
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
# textbbox returns (left, top, right, bottom) with the actual ink box;
# offset by the bbox left/top to center true ink.
draw.text((cx - tw / 2 - bbox[0], cy - th / 2 - bbox[1]), text, font=font, fill=GREEN)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG")
print(f"wrote {OUT} ({SIZE}x{SIZE})")
