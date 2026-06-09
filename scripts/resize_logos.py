"""Pre-resize PNG logos to roughly 4x their final display size with
high-quality Lanczos resampling, so the browser does minimal additional
scaling. Eliminates the downscale-blur on very large source images."""
from PIL import Image
from pathlib import Path
import os

DIR = Path(__file__).resolve().parent.parent / "static" / "companies"

# Tile content area is ~76x28 (92x40 minus padding). Render at 4x = ~300x110.
TARGET_HEIGHT = 160  # 4x display height; width scales by aspect.


def atomic_save(im: Image.Image, path: Path):
    tmp = path.with_suffix(path.suffix + ".tmp")
    im.save(tmp, "PNG", optimize=True)
    os.replace(tmp, path)


for png in sorted(DIR.glob("*.png")):
    im = Image.open(png).convert("RGBA")
    w, h = im.size
    if h <= TARGET_HEIGHT:
        print(f"{png.name}: {im.size} (already small, skipping)")
        continue
    new_h = TARGET_HEIGHT
    new_w = round(w * (new_h / h))
    resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    atomic_save(resized, png)
    print(f"{png.name}: {(w, h)} -> {(new_w, new_h)}")
