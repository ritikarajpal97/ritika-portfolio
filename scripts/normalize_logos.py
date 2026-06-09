"""Replace the wordmark-bearing logos with their tighter brand-mark versions
so they read clearly at the small in-tab display size.

- Microsoft: generated fresh as the 4-color square (no 'Microsoft' wordmark).
- UrbanClap: cropped to just the dark UC monogram tile (no 'UrbanClap' text).
- Accenture / AWS / Fraud.Net: left alone — they're already tight wordmarks
  whose recognition depends on the lettering.
"""
from PIL import Image, ImageDraw, ImageChops
from pathlib import Path
import os

DIR = Path(__file__).resolve().parent.parent / "static" / "companies"


def atomic_save(im: Image.Image, path: Path):
    tmp = path.with_suffix(path.suffix + ".tmp")
    im.save(tmp, "PNG")
    os.replace(tmp, path)


def trim_alpha_or_white(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    bbox = im.getchannel("A").getbbox()
    if bbox is None or bbox == (0, 0, im.width, im.height):
        rgb = im.convert("RGB")
        bg = Image.new("RGB", rgb.size, (255, 255, 255))
        bbox = ImageChops.difference(rgb, bg).getbbox()
    return im.crop(bbox) if bbox else im


# --- Microsoft: clean 4-color square ---------------------------------------
def make_microsoft():
    size = 600
    gap = 28  # ~5% gap between squares — matches the official mark
    half = (size - gap) // 2
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Top-left red, top-right green, bottom-left blue, bottom-right yellow.
    colors = [
        ((0, 0, half, half), (242, 80, 34, 255)),                # #F25022
        ((half + gap, 0, size, half), (127, 186, 0, 255)),       # #7FBA00
        ((0, half + gap, half, size), (0, 164, 239, 255)),       # #00A4EF
        ((half + gap, half + gap, size, size), (255, 185, 0, 255)),  # #FFB900
    ]
    for box, color in colors:
        d.rectangle(box, fill=color)
    atomic_save(img, DIR / "microsoft.png")
    print("microsoft.png: regenerated as 600x600 4-square mark")


# --- UrbanClap: crop to the dark UC monogram only --------------------------
def crop_urbanclap():
    src = DIR / "urbancompany.png"
    im = Image.open(src).convert("RGBA")
    # The dark UC tile occupies the top ~62% of the image; the rest is the
    # 'UrbanClap' wordmark below. Crop the upper portion, then trim slack.
    cropped = im.crop((0, 0, im.width, int(im.height * 0.62)))
    cropped = trim_alpha_or_white(cropped)
    atomic_save(cropped, src)
    print(f"urbancompany.png: cropped to UC monogram, now {cropped.size}")


make_microsoft()
crop_urbanclap()
