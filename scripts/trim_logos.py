"""Trim whitespace / transparent padding around each PNG logo so it fills
its tile uniformly. SVGs are left alone (their viewBox handles cropping)."""
from PIL import Image, ImageChops
from pathlib import Path

DIR = Path(__file__).resolve().parent.parent / "static" / "companies"


def trim(im: Image.Image) -> Image.Image:
    # Normalize to RGBA for consistent bbox detection.
    im = im.convert("RGBA")

    # First try: bbox by alpha channel (transparent backgrounds).
    bbox = im.getchannel("A").getbbox()

    # If the image is fully opaque (no transparency to key off of), fall
    # back to "trim against white" — diff against a pure-white canvas.
    if bbox is None or bbox == (0, 0, im.width, im.height):
        rgb = im.convert("RGB")
        bg = Image.new("RGB", rgb.size, (255, 255, 255))
        diff = ImageChops.difference(rgb, bg)
        bbox = diff.getbbox()

    if bbox:
        # Small margin so the logo doesn't kiss the tile edge.
        pad = int(max(im.width, im.height) * 0.03)
        left = max(0, bbox[0] - pad)
        top = max(0, bbox[1] - pad)
        right = min(im.width, bbox[2] + pad)
        bottom = min(im.height, bbox[3] + pad)
        return im.crop((left, top, right, bottom))
    return im


import os

for png in sorted(DIR.glob("*.png")):
    im = Image.open(png)
    before = im.size
    trimmed = trim(im)
    # Atomic save: write to a sibling tmp file, then rename over the original.
    # Prevents a running dev server from ever observing a 0-byte file mid-write.
    tmp = png.with_suffix(png.suffix + ".tmp")
    trimmed.save(tmp, "PNG")
    os.replace(tmp, png)
    print(f"{png.name}: {before} -> {trimmed.size}")
