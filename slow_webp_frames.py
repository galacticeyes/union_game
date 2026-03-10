#!/usr/bin/env python3
"""Modify animated WebP frame durations. Usage: python slow_webp_frames.py [speed_factor]
   speed_factor: 0.8 = 0.8x speed (slower), 1.2 = 1.2x speed (faster)"""
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Need Pillow: pip install Pillow")
    sys.exit(1)


def main():
    speed = float(sys.argv[1]) if len(sys.argv) > 1 else 0.8
    scale = 1 / speed  # 0.8x speed => 1.25x duration; 1.2x speed => 1/1.2 duration
    path = Path(__file__).parent / "rouge_webps" / "player.webp"
    if not path.exists():
        print(f"Not found: {path}")
        sys.exit(1)

    img = Image.open(path)
    if not getattr(img, "is_animated", False):
        print("Not an animated WebP")
        sys.exit(1)

    frames = []
    durations = []

    try:
        n = 0
        while True:
            img.seek(n)
            frames.append(img.copy().convert("RGBA"))
            d = img.info.get("duration", 100)
            durations.append(int(d * scale))
            n += 1
    except EOFError:
        pass

    if not frames:
        print("No frames")
        sys.exit(1)

    out_path = path
    back_path = path.with_suffix(".webp.bak")
    back_path.write_bytes(path.read_bytes())

    loop = img.info.get("loop", 0)
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=loop,
        format="WEBP",
    )
    print(f"Updated {path}: {len(frames)} frames, speed x{speed} (durations x{scale:.3f})")
    print(f"Backup: {back_path}")


if __name__ == "__main__":
    main()
