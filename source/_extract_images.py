"""Pull every embedded image out of the source docx, then label each
with the nearest figure caption above/below it. Writes the renamed
images into images/ in the repo root, and a CONTENTS.md alongside.

The original docx lives outside this repository (OneDrive) and is the
authoring source for figures only. Pin data lives in source/altium-*.tsv.
"""
from __future__ import annotations

import re
import shutil
import sys
import zipfile
from pathlib import Path

import docx
from docx.document import Document as _Doc
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph

DOCX = Path(r"C:/OneDrive - Alp Electronix/E1M Project - Documents/"
             "Alp Lab - E1M Standard.docx")
ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images"

CAPTION_RE = re.compile(r"^\s*(Figure|Table)\s+(\d+)\s*:\s*(.*?)\s*$",
                         re.IGNORECASE)


def safe(s: str) -> str:
    s = re.sub(r"[^\w\-. ]+", "_", s)
    s = re.sub(r"\s+", "-", s).strip("_-.")
    return s.lower()[:80]


def main() -> int:
    if not DOCX.exists():
        print(f"Source docx missing: {DOCX}", file=sys.stderr)
        return 1
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Walk paragraphs, recording image rIds in order.
    doc = docx.Document(str(DOCX))
    rels = doc.part.rels
    rid_to_target = {rid: rel.target_ref for rid, rel in rels.items()
                     if "image" in rel.reltype}
    target_to_rid = {v: k for k, v in rid_to_target.items()}

    # Build (rId, surrounding-context) by walking paragraphs.
    encountered: list[tuple[str, str | None, str | None]] = []
    last_caption: str | None = None
    pending_caption_for_next_image = False
    paragraphs = list(doc.paragraphs)
    for i, p in enumerate(paragraphs):
        style = (p.style.name or "").lower() if p.style else ""
        text = p.text.strip()
        if "caption" in style and text:
            last_caption = text
            pending_caption_for_next_image = True
        # Look at inline images in this paragraph.
        # python-docx doesn't easily expose inline shape -> rId mapping
        # at the paragraph level, so we walk the XML.
        for blip in p._p.iter(qn("a:blip")):
            embed = blip.get(qn("r:embed"))
            if not embed:
                continue
            # Find the next caption AFTER this paragraph for "below" context.
            next_caption = None
            for q in paragraphs[i + 1: i + 6]:
                qstyle = (q.style.name or "").lower() if q.style else ""
                qtext = q.text.strip()
                if "caption" in qstyle and qtext:
                    next_caption = qtext
                    break
            encountered.append((embed, last_caption, next_caption))

    print(f"Found {len(encountered)} inline image references in body.")
    print(f"Total image relationships in part: {len(rid_to_target)}")

    # Export. For images we encountered with a caption, give them a
    # readable filename. For the rest, use the original media filename.
    contents_lines: list[str] = ["# images/", "",
        "Extracted from `Alp Lab - E1M Standard.docx` (the historical "
        "authoring source, kept on OneDrive). One row per image.\n"]
    contents_lines.append("| File | Caption (best guess) | Original media path |")
    contents_lines.append("| --- | --- | --- |")

    used_names: set[str] = set()
    written: list[tuple[str, str]] = []
    seen_rids: set[str] = set()

    with zipfile.ZipFile(DOCX) as z:
        for rid, cap_above, cap_below in encountered:
            target = rid_to_target.get(rid)
            if not target:
                continue
            seen_rids.add(rid)
            archive_path = "word/" + target
            if archive_path not in z.namelist():
                continue
            ext = Path(target).suffix.lower()
            base = (cap_above or cap_below or Path(target).stem)
            base = base.replace("Error! Bookmark not defined.", "").strip()
            base = re.sub(r"^(Figure|Table)\s+\d+\s*:\s*", "", base,
                          flags=re.IGNORECASE).strip()
            if not base:
                base = Path(target).stem
            name = safe(base) + ext
            i = 2
            while name in used_names:
                name = f"{safe(base)}-{i}{ext}"
                i += 1
            used_names.add(name)
            with z.open(archive_path) as src, (IMAGES_DIR / name).open("wb") as dst:
                shutil.copyfileobj(src, dst)
            cap = cap_above or cap_below or "_(no caption)_"
            contents_lines.append(f"| `{name}` | {cap} | `word/{target}` |")
            written.append((name, cap))

        # Any image relationships not encountered inline (e.g. floating
        # behind text). Drop them too with their original names.
        for rid, target in rid_to_target.items():
            if rid in seen_rids:
                continue
            archive_path = "word/" + target
            if archive_path not in z.namelist():
                continue
            ext = Path(target).suffix.lower()
            name = "unplaced-" + Path(target).name
            with z.open(archive_path) as src, (IMAGES_DIR / name).open("wb") as dst:
                shutil.copyfileobj(src, dst)
            contents_lines.append(
                f"| `{name}` | _(not inline; floating)_ | `word/{target}` |")
            written.append((name, "(floating)"))

    (IMAGES_DIR / "CONTENTS.md").write_text(
        "\n".join(contents_lines) + "\n", encoding="utf-8")

    print(f"Wrote {len(written)} images to {IMAGES_DIR}")
    for n, c in written:
        print(f"  {n}  <- {c}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
