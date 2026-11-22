"""Scale the 2x screenshot down to a 1024 x 1024 PNG and keep it under the 1 MiB cap."""
import os
import sys

from PIL import Image

src, dst = sys.argv[1], sys.argv[2]
im = Image.open(src).convert("RGB").resize((1024, 1024), Image.LANCZOS)
im.save(dst, optimize=True)
if os.path.getsize(dst) > 1_000_000:
    im.quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dst, optimize=True)
print(f"{dst}: {im.size[0]}x{im.size[1]}, {os.path.getsize(dst)} bytes")
