"""make.fun entry: Sum up 27 November's world news in one image.

Simplest program: copy the image this repo holds (entry.png)
to /output/entry.png.

The image itself is drawn programmatically by build_image.py
(Pillow, run at build time): a newspaper front page for Friday
27 November 2026 with the day's five biggest stories, each with
a drawn scene, headline and standfirst. This entrypoint only
copies those bytes, so both runs write identical bytes.
No network, no randomness, no timestamps, no external files.
Standard library only.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path


def _sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


SRC = Path(__file__).resolve().parent / "entry.png"
DEFAULT_DEST = Path("/output/entry.png")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    dest = Path(argv[0]) if argv else Path(os.environ.get("OUTPUT_PATH", DEFAULT_DEST))
    if not SRC.is_file():
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, dest)
    src_hash = _sha256(SRC)
    dest_hash = _sha256(dest)
    if src_hash != dest_hash:
        print("copy mismatch: %s != %s" % (src_hash, dest_hash), file=sys.stderr)
        return 1
    print("wrote %s (%d bytes, sha256 %s)" % (dest, dest.stat().st_size, dest_hash))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
