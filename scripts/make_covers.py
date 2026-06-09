"""Generate gradient + title placeholder cover PNGs for featured projects.

Palette matches the site (navy → green). Each cover is 1200x900 PNG.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "content" / "featured"

NAVY = (10, 25, 47)        # #0a192f
LIGHT_NAVY = (17, 34, 64)  # #112240
GREEN = (100, 255, 218)    # #64ffda
LIGHTEST_SLATE = (204, 214, 246)  # #ccd6f6
SLATE = (136, 146, 176)    # #8892b0

W, H = 1200, 900

COVERS = [
    {
        "dir": "ClearViewAssist",
        "title": "Clear View Assist",
        "subtitle": "AI accessibility plugin",
    },
    {
        "dir": "IntelliSummarizer",
        "title": "Intelli-Summarizer",
        "subtitle": "Azure OpenAI + Cognitive Services",
    },
    {
        "dir": "BumbleProductInnovation",
        "title": "Bumble Product Innovation",
        "subtitle": "PRFAQ • roadmap • strategy",
    },
]

# Try common font paths; fall back to default if none work.
FONT_CANDIDATES_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
FONT_CANDIDATES_REG = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]


def load_font(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def vertical_gradient(width, height, top, bottom):
    img = Image.new("RGB", (width, height), top)
    px = img.load()
    for y in range(height):
        t = y / max(1, height - 1)
        r = int(top[0] * (1 - t) + bottom[0] * t)
        g = int(top[1] * (1 - t) + bottom[1] * t)
        b = int(top[2] * (1 - t) + bottom[2] * t)
        for x in range(width):
            px[x, y] = (r, g, b)
    return img


def make_cover(out_path: Path, seed_key: str):
    """Generate a decorative-only cover (no text) — the page renders the
    title and description as React components on top of the cover image."""
    img = vertical_gradient(W, H, NAVY, LIGHT_NAVY)
    draw = ImageDraw.Draw(img)

    # Scatter dots for a subtle texture.
    import random
    random.seed(hash(seed_key) & 0xFFFFFFFF)
    for _ in range(220):
        x = random.randint(20, W - 20)
        y = random.randint(20, H - 20)
        r = random.choice([1, 2, 2, 3])
        # mix slate + green dots, mostly slate.
        color = GREEN if random.random() < 0.08 else SLATE
        draw.ellipse([(x, y), (x + r, y + r)], fill=color)

    # A few diagonal accent lines.
    for i in range(6):
        x0 = random.randint(-200, W)
        y0 = random.randint(-100, H)
        length = random.randint(200, 600)
        draw.line([(x0, y0), (x0 + length, y0 + length // 2)], fill=LIGHT_NAVY, width=2)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG")
    print(f"wrote {out_path}")


for cover in COVERS:
    out = ROOT / cover["dir"] / "cover.png"
    make_cover(out, cover["dir"])
