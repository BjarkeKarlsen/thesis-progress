#!/usr/bin/env python3
"""Phase 3: build a document model for the semantic audits.

Walks the thesis in reading order and records, each with file, line
range and section path:
  - the sectioning hierarchy (part ... paragraph) and section labels
  - prose paragraphs, with flags for display math, citations and refs
  - numbered objects: figures, tables, equations, algorithms, listings,
    theorem-like environments, and figures made by user macros
  - research questions (\\item[RQ1:] and similar)
  - acronym candidates and whether their first use is expanded
  - definition-phrase candidates ("we define", "denotes", "let ...")

Comments, verbatim and listing bodies are excluded. Captions, footnotes
and table cells are kept, since they can hold claims and citations.

Usage:
    extract_structure.py DISCOVERY_JSON [--out structure.json] [--max-paragraph-chars N]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from latex_common import MacroTemplate, blank_definitions, reading_position, templates_from_discovery, clean_source, line_of, load_json, read_args, read_group, skip_spaces, write_json

SECTION_LEVELS = ["part", "chapter", "section", "subsection", "subsubsection", "paragraph", "subparagraph"]
SECTION_RE = re.compile(r"\\(" + "|".join(SECTION_LEVELS) + r")(\*?)\s*(?=[\[{])")
OBJECT_ENVS = {
    "figure": "figure", "figure*": "figure", "wrapfigure": "figure", "subfigure": "subfigure",
    "table": "table", "table*": "table", "longtable": "table",
    "equation": "equation", "equation*": "equation", "align": "equation", "align*": "equation",
    "gather": "equation", "multline": "equation", "eqnarray": "equation", "flalign": "equation",
    "algorithm": "algorithm", "algorithm*": "algorithm", "lstlisting": "listing", "listing": "listing",
    "theorem": "theorem", "lemma": "theorem", "proposition": "theorem", "corollary": "theorem",
    "definition": "definition", "example": "example", "remark": "remark", "assumption": "assumption",
}
NUMBERED_EQ = {"equation", "align", "gather", "multline", "eqnarray", "flalign"}
DISPLAY_MATH_RE = re.compile(r"\\begin\{(equation|align|gather|multline|eqnarray|flalign)\*?\}|\\\[|\$\$")
DEFINITION_RE = re.compile(
    r"(?:\bis defined as\b|\bwe define\b|\bdefine[sd]?\b|\bdenotes?\b|\brefers? to\b|\bis called\b|"
    r"\bwe call\b|\bLet\s+\$|\bLet\s+\\\(|\blet\s+\$|\blet\s+\\\()",
)
ACRONYM_RE = re.compile(r"(?<![\\A-Za-z])([A-Z][A-Z0-9]{1,6}s?)(?![A-Za-z])")
ACRONYM_IGNORE = {"I", "A", "II", "III", "IV", "TBD", "PDF", "PNG", "URL", "OK", "AND", "OR", "NOT", "RQ", "TODO"}
RQ_RE = re.compile(r"\\item\s*\[\s*(?:\\textbf\{)?\s*(RQ\s*\d*[^\]:]*?)\s*:?\s*\}?\s*\]|\\textbf\{(RQ\d*)\s*:?\}")


def section_entries(text: str, rel_path: str, order: int) -> list[dict]:
    out = []
    for m in SECTION_RE.finditer(text):
        parsed = read_args(text, m.end(), "om")
        if parsed is None:
            continue
        (short, title), end = parsed
        label_m = re.match(r"\s*\\label\s*\{([^{}]*)\}", text[end:end + 200])
        out.append(
            {
                "level": m.group(1),
                "depth": SECTION_LEVELS.index(m.group(1)),
                "starred": bool(m.group(2)),
                "title": re.sub(r"\s+", " ", (title or "").strip()),
                "label": label_m.group(1) if label_m else None,
                "file": rel_path,
                "line": line_of(text, m.start()),
                "order": order,
            }
        )
    return out


def object_entries(text: str, rel_path: str, templates: dict[str, MacroTemplate]) -> list[dict]:
    out = []
    for m in re.finditer(r"\\begin\{([A-Za-z*]+)\}", text):
        env = m.group(1)
        if env not in OBJECT_ENVS:
            continue
        end_m = re.search(r"\\end\{" + re.escape(env) + r"\}", text[m.end():])
        body = text[m.end(): m.end() + end_m.start()] if end_m else ""
        caption = None
        cm = re.search(r"\\caption\s*(?:\[[^\]]*\])?\s*(?=\{)", body)
        if cm:
            g = read_group(body, cm.end())
            caption = re.sub(r"\s+", " ", g[0]).strip() if g else None
        labels = re.findall(r"\\label\s*\{([^{}]*)\}", body)
        numbered = not env.endswith("*") and (env.rstrip("*") not in ("lstlisting",) or "label" in body)
        out.append(
            {
                "type": OBJECT_ENVS[env],
                "environment": env,
                "labels": labels,
                "caption": caption,
                "caption_words": len(caption.split()) if caption else 0,
                "numbered": numbered,
                "file": rel_path,
                "line": line_of(text, m.start()),
                "end_line": line_of(text, m.end() + (end_m.end() if end_m else 0)),
            }
        )
    for name, template in templates.items():
        for m in re.finditer(r"\\" + re.escape(name) + r"(?![A-Za-z@])", text):
            parsed = read_args(text, m.end(), template.spec)
            if parsed is None:
                continue
            args, end = parsed
            # The caption is the argument passed to \\caption in the body.
            out.append(
                {
                    "type": "figure",
                    "environment": "\\" + name,
                    "labels": [k for k in (template.expand(t, args) for t in template.label_templates) if k],
                    "caption": (caption := _macro_caption(name, template, args)),
                    "caption_words": len((caption or "").split()),
                    "numbered": True,
                    "file": rel_path,
                    "line": line_of(text, m.start()),
                    "end_line": line_of(text, end),
                }
            )
    return out


def _macro_caption(name: str, template: MacroTemplate, args: list[str | None]) -> str | None:
    for ct in template.caption_templates:
        caption = template.expand(ct, args)
        if caption:
            return re.sub(r"\s+", " ", caption).strip()
    return None


def paragraphs(text: str, rel_path: str, order: int, max_chars: int) -> list[dict]:
    """Split on blank lines. Blocks that are only environment wrappers or
    commands (no running text) are skipped."""
    out = []
    lines = text.split("\n")
    start = None
    buf: list[str] = []

    def flush(end_idx: int) -> None:
        nonlocal buf, start
        block = "\n".join(buf).strip()
        if start is not None and block:
            prose = re.sub(r"\\[A-Za-z@]+\*?(\[[^\]]*\])?", " ", block)
            prose = re.sub(r"\$[^$]*\$|\\\(.*?\\\)", " MATH ", prose)
            words = re.findall(r"[A-Za-z]{2,}", prose)
            if len(words) >= 6:
                out.append(
                    {
                        "file": rel_path,
                        "line": start + 1,
                        "end_line": end_idx,
                        "order": order,
                        "words": len(words),
                        "sentences": max(1, len(re.findall(r"[.!?](\s|$)", block))),
                        "has_display_math": bool(DISPLAY_MATH_RE.search(block)),
                        "has_citation": bool(re.search(r"\\[A-Za-z]*cite[A-Za-z]*", block)),
                        "has_reference": bool(re.search(r"\\(?:ref|eqref|cref|Cref|autoref)\b", block)),
                        "text": block if len(block) <= max_chars else block[:max_chars] + " ...",
                    }
                )
        buf, start = [], None

    for idx, line in enumerate(lines):
        if line.strip() == "":
            flush(idx)
        else:
            if start is None:
                start = idx
            buf.append(line)
    flush(len(lines))
    return out


def acronym_candidates(text: str, rel_path: str, order: int) -> list[dict]:
    out = []
    prose = re.sub(r"\$[^$]*\$|\\\(.*?\\\)|\\\[.*?\\\]", " ", text, flags=re.S)
    prose = re.sub(r"\\(?:label|ref|cref|Cref|eqref|cite\w*|includegraphics|begin|end|usepackage)\s*(\[[^\]]*\])?\{[^}]*\}", " ", prose)
    for m in ACRONYM_RE.finditer(prose):
        token = m.group(1)
        base = token[:-1] if token.endswith("s") and token[:-1].isupper() else token
        if base in ACRONYM_IGNORE or len(base) < 2 or re.fullmatch(r"(RQ|H|C|P)\d+", base):
            continue
        window = prose[max(0, m.start() - 80): m.end() + 80]
        expanded = bool(re.search(r"\(\s*" + re.escape(base) + r"s?\s*\)", window))
        out.append({"acronym": base, "file": rel_path, "line": line_of(prose, m.start()), "order": order, "expanded_here": expanded})
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("discovery", help="output of discover_project.py")
    parser.add_argument("--out", help="write JSON here instead of stdout")
    parser.add_argument("--max-paragraph-chars", type=int, default=1200)
    args = parser.parse_args()

    discovery = load_json(args.discovery)
    root = Path(discovery["project_root"])
    templates = templates_from_discovery(discovery)

    sections, paras, objects, rqs, acronyms, definitions = [], [], [], [], [], []
    seen = set()
    for order, entry in enumerate(discovery["reading_order"]):
        rel_path = entry["file"]
        if rel_path in seen:
            continue
        seen.add(rel_path)
        text = blank_definitions(clean_source((root / rel_path).read_text(encoding="utf-8", errors="replace")))
        sections += section_entries(text, rel_path, order)
        paras += paragraphs(text, rel_path, order, args.max_paragraph_chars)
        objects += [{**o, "order": order} for o in object_entries(text, rel_path, templates)]
        for m in RQ_RE.finditer(text):
            name = (m.group(1) or m.group(2) or "").strip()
            following = text[m.end(): m.end() + 400]
            rqs.append({"id": re.sub(r"\s+", " ", name), "file": rel_path, "line": line_of(text, m.start()), "text": re.sub(r"\s+", " ", following.split("\\item")[0]).strip()})
        acronyms += acronym_candidates(text, rel_path, order)
        for m in DEFINITION_RE.finditer(text):
            line = line_of(text, m.start())
            line_text = text.split("\n")[line - 1].strip()
            definitions.append({"phrase": m.group(0), "file": rel_path, "line": line, "line_text": line_text[:200]})

    # Attach a section path to each paragraph and object, in true reading
    # order (text after an include point comes after the included file).
    position = reading_position(discovery)
    for item in sections + paras + objects:
        item["position"] = list(position(item["file"], item["line"]))
    sections.sort(key=lambda s: s["position"])
    paras.sort(key=lambda p: p["position"])
    objects.sort(key=lambda o: o["position"])

    def path_for(item: dict) -> str:
        stack: list[dict] = []
        for s in sections:
            if s["position"] > item["position"]:
                break
            while stack and stack[-1]["depth"] >= s["depth"]:
                stack.pop()
            stack.append(s)
        return " > ".join(s["title"] for s in stack)

    for item in paras + objects:
        item["section"] = path_for(item)

    acronyms.sort(key=lambda a: position(a["file"], a["line"]))
    first_use: dict[str, dict] = {}
    for a in acronyms:
        first_use.setdefault(a["acronym"], a)
    acronym_summary = [
        {
            "acronym": k,
            "first_use": {"file": v["file"], "line": v["line"]},
            "expanded_at_first_use": v["expanded_here"],
            "expanded_anywhere": any(x["expanded_here"] for x in acronyms if x["acronym"] == k),
            "uses": sum(1 for x in acronyms if x["acronym"] == k),
        }
        for k, v in first_use.items()
    ]

    numbered_labels = {lab for o in objects for lab in o["labels"]}
    result = {
        "root_document": discovery["root_document"],
        "sections": sections,
        "paragraphs": paras,
        "objects": objects,
        "research_questions": rqs,
        "acronyms": sorted(acronym_summary, key=lambda a: -a["uses"]),
        "definition_candidates": definitions,
        "counts": {
            "sections": len(sections),
            "paragraphs": len(paras),
            "objects": len(objects),
            "figures": sum(1 for o in objects if o["type"] == "figure"),
            "tables": sum(1 for o in objects if o["type"] == "table"),
            "equations": sum(1 for o in objects if o["type"] == "equation"),
            "labelled_objects": len(numbered_labels),
            "research_questions": len(rqs),
        },
    }
    write_json(result, args.out)


if __name__ == "__main__":
    main()
