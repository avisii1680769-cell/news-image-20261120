"""Entry point: copy the bundled entry.png to the output directory.

Honours MAKEFUN_OUTPUT_DIR (defaults to /output). Writes byte-identical output
on every run.
"""
import os
import shutil
import struct
from pathlib import Path

SRC = Path(__file__).resolve().parent / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT = OUT_DIR / "entry.png"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576


def _png_size(data):
    # IHDR chunk follows the 8-byte signature: length(4) type(4) width(4) height(4)
    assert data[:8] == PNG_MAGIC, "output is not a PNG"
    assert data[12:16] == b"IHDR", "missing IHDR chunk"
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, OUT)
    # post-copy guard: verify the written file is a whole PNG within limits
    data = OUT.read_bytes()
    assert len(data) <= MAX_BYTES, "output exceeds 1 MiB"
    w, h = _png_size(data)
    assert (w, h) == (1024, 1024), "unexpected dimensions: %dx%d" % (w, h)
    assert len(data) == SRC.stat().st_size, "copy size mismatch"


if __name__ == "__main__":
    main()
