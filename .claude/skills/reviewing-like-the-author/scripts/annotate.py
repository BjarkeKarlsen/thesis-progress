"""Write review comments in red into a wide right margin of a thesis PDF.

Usage (from anywhere, needs pymupdf):
    uv run -q --with pymupdf python -I annotate.py IN.pdf COMMENTS.json OUT.pdf

COMMENTS.json is a list of {"page": 1-based int, "quote": "text on the page",
"comment": "the note"}. The quote is searched on the page (its first 60
characters, then shorter) and highlighted. The note sits in the margin at the
same height, in the red the author uses. Notes that do not fit are moved down.
"""
import json
import sys

import pymupdf

RED = (0.75, 0.11, 0.16)
MARGIN = 230  # extra width added on the right, in points
FONT = 7.5


def find(page, quote):
    q = " ".join(quote.split())
    for n in (60, 40, 25, 15):
        hits = page.search_for(q[:n])
        if hits:
            return hits
    return []


def main(src, notes_path, out):
    notes = json.load(open(notes_path))
    doc = pymupdf.open(src)
    new = pymupdf.open()
    for i, page in enumerate(doc):
        r = page.rect
        wide = new.new_page(width=r.width + MARGIN, height=r.height)
        wide.show_pdf_page(r, doc, i)
        mine = [n for n in notes if n["page"] == i + 1]
        placed = []
        for n in mine:
            hits = find(page, n["quote"])
            y = hits[0].y0 if hits else 40
            placed.append((y, hits, n))
        placed.sort(key=lambda t: t[0])
        bottom = 30
        for y, hits, n in placed:
            for h in hits[:3]:
                a = wide.add_highlight_annot(h)
                a.set_colors(stroke=(1, 0.85, 0.85))
                a.update(opacity=0.5)
            top = max(y, bottom)
            box = pymupdf.Rect(r.width + 8, top, r.width + MARGIN - 8, r.height - 20)
            spare = wide.insert_textbox(box, n["comment"], fontsize=FONT,
                                        fontname="helv", color=RED)
            used = box.height - spare if spare >= 0 else box.height
            if hits:
                wide.draw_line(pymupdf.Point(hits[0].x1, hits[0].y1),
                               pymupdf.Point(r.width + 6, top + FONT),
                               color=RED, width=0.4)
            bottom = top + used + 8
            if spare < 0:
                print(f"page {i+1}: note did not fit: {n['comment'][:50]}")
            if not hits:
                print(f"page {i+1}: quote not found: {n['quote'][:50]}")
    new.save(out, garbage=3, deflate=True)
    print(f"wrote {out} with {len(notes)} notes")


if __name__ == "__main__":
    main(*sys.argv[1:4])
