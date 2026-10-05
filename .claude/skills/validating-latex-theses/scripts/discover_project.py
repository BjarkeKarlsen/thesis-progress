#!/usr/bin/env python3
"""Phase 1: discover a LaTeX thesis project.

Finds the root document, follows \\input / \\include / \\subfile (and
\\import / \\subimport) recursively in document order, and reports the
effective reading order with include chains, missing, duplicate and
cyclic includes, files not reached from the root, the bibliography
backend and files, build configuration, and figure-like macros whose
labels are generated from an argument.

Usage:
    discover_project.py [PROJECT_ROOT] [--root main.tex] [--out discovery.json]
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from latex_common import (
    INCLUDE_COMMANDS,
    clean_source,
    find_macro_templates,
    iter_project_files,
    line_of,
    read_args,
    rel,
    skip_spaces,
    write_json,
)

TEX_EXT = {".tex"}
STYLE_EXT = {".sty", ".cls"}
BIB_EXT = {".bib"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".pdf", ".eps", ".svg", ".tikz", ".pgf"}
GLOSSARY_HINTS = ("glossar", "acronym", "abbrev", "nomencl")
CONFIG_NAMES = (".latexmkrc", "latexmkrc", "arara.yaml", ".arararc.yaml", "Makefile", "build.sh")

_INCLUDE_RE = re.compile(r"\\(" + "|".join(INCLUDE_COMMANDS) + r")\*?(?![A-Za-z])")


def find_root_candidates(root: Path, tex_files: list[Path]) -> list[dict]:
    candidates = []
    for path in tex_files:
        text = clean_source(path.read_text(encoding="utf-8", errors="replace"))
        m = re.search(r"\\documentclass\s*(\[[^\]]*\])?\s*\{([^}]*)\}", text)
        if not m:
            continue
        cls = m.group(2).strip()
        has_document = "\\begin{document}" in text
        includes = len(_INCLUDE_RE.findall(text))
        score = 0
        reasons = []
        if cls == "subfiles":
            score -= 10
            reasons.append("subfiles child (documentclass subfiles)")
        if has_document:
            score += 2
            reasons.append("has \\begin{document}")
        if includes:
            score += min(includes, 10)
            reasons.append(f"{includes} include commands")
        if path.stem.lower() in ("main", "thesis", "dissertation", "report"):
            score += 3
            reasons.append("conventional root name")
        if path.parent == root:
            score += 2
            reasons.append("at project root")
        candidates.append(
            {"file": rel(path, root), "documentclass": cls, "score": score, "reasons": reasons}
        )
    candidates.sort(key=lambda c: -c["score"])
    return candidates


def resolve_include(target: str, command: str, including: Path, root_doc: Path, import_dir: str | None) -> Path | None:
    """LaTeX resolves \\input paths against the directory of the root
    document (the compile directory). \\subfile, \\import and \\subimport
    are relative to the including file. Try the compile directory first,
    then the including file's directory."""
    target = target.strip()
    if not target:
        return None
    bases = []
    if command in ("import",) and import_dir is not None:
        bases.append(Path(import_dir) if Path(import_dir).is_absolute() else root_doc.parent / import_dir)
    elif command == "subimport" and import_dir is not None:
        bases.append(including.parent / import_dir)
    elif command == "subfile":
        bases += [including.parent, root_doc.parent]
    else:
        bases += [root_doc.parent, including.parent]
    for base in bases:
        candidate = (base / target)
        for path in (candidate, candidate.with_name(candidate.name + ".tex")):
            if path.is_file():
                return path.resolve()
    return None


def walk(root: Path, root_doc: Path) -> dict:
    reading_order: list[dict] = []
    include_edges: list[dict] = []
    missing: list[dict] = []
    cycles: list[dict] = []
    duplicates: list[dict] = []
    seen_count: dict[Path, int] = {}

    def visit(path: Path, chain: list[Path]) -> None:
        seen_count[path] = seen_count.get(path, 0) + 1
        if seen_count[path] > 1:
            duplicates.append(
                {"file": rel(path, root), "include_chain": [rel(p, root) for p in chain + [path]]}
            )
        reading_order.append({"file": rel(path, root), "include_chain": [rel(p, root) for p in chain + [path]]})
        text = clean_source(path.read_text(encoding="utf-8", errors="replace"))
        for m in _INCLUDE_RE.finditer(text):
            command = m.group(1)
            spec = "mm" if command in ("import", "subimport") else "m"
            parsed = read_args(text, m.end(), spec)
            if parsed is None:
                continue
            args, _ = parsed
            import_dir = args[0] if len(args) == 2 else None
            target = args[-1] or ""
            line = line_of(text, m.start())
            resolved = resolve_include(target, command, path, root_doc, import_dir)
            edge = {
                "from": rel(path, root),
                "line": line,
                "command": command,
                "target": target,
                "resolved": rel(resolved, root) if resolved else None,
            }
            include_edges.append(edge)
            if resolved is None:
                missing.append(edge)
                continue
            if resolved in chain or resolved == path:
                cycles.append({**edge, "cycle": [rel(p, root) for p in chain + [path, resolved]]})
                continue
            visit(resolved, chain + [path])

    visit(root_doc.resolve(), [])
    return {
        "reading_order": reading_order,
        "include_edges": include_edges,
        "missing_includes": missing,
        "cycles": cycles,
        "duplicate_includes": duplicates,
    }


def detect_bibliography(root: Path, files: list[Path]) -> dict:
    backend = {"package": None, "backend": None, "style": None, "resources": [], "commands": []}
    for path in files:
        text = clean_source(path.read_text(encoding="utf-8", errors="replace"))
        m = re.search(r"\\usepackage\s*(\[[^\]]*\])?\s*\{([^}]*biblatex[^}]*)\}", text)
        if m:
            backend["package"] = "biblatex"
            options = m.group(1) or ""
            b = re.search(r"backend\s*=\s*(\w+)", options)
            backend["backend"] = b.group(1) if b else "biber"
            s = re.search(r"style\s*=\s*([\w-]+)", options)
            backend["style"] = s.group(1) if s else None
            if re.search(r"natbib\s*=\s*true", options):
                backend["commands"].append("natbib-compatible commands enabled")
        if re.search(r"\\usepackage\s*(\[[^\]]*\])?\s*\{[^}]*\bnatbib\b", text) and backend["package"] is None:
            backend["package"] = "natbib"
            backend["backend"] = "bibtex"
        for r in re.finditer(r"\\addbibresource\s*(\[[^\]]*\])?\s*\{([^}]*)\}", text):
            backend["resources"].append({"resource": r.group(2), "declared_in": rel(path, root), "line": line_of(text, r.start())})
        for r in re.finditer(r"\\bibliography\s*\{([^}]*)\}", text):
            for name in r.group(1).split(","):
                name = name.strip()
                backend["resources"].append(
                    {"resource": name if name.endswith(".bib") else name + ".bib", "declared_in": rel(path, root), "line": line_of(text, r.start())}
                )
            if backend["package"] is None:
                backend["package"] = "bibtex"
                backend["backend"] = "bibtex"
    return backend


def detect_packages(files: list[Path]) -> dict[str, list[str]]:
    """Every \\usepackage / \\RequirePackage with its options, so checks can
    respect them (cleveref's capitalize makes \\cref print capitals)."""
    packages: dict[str, list[str]] = {}
    for path in files:
        text = clean_source(path.read_text(encoding="utf-8", errors="replace"))
        for m in re.finditer(r"\\(?:usepackage|RequirePackage)\s*(?:\[([^\]]*)\])?\s*\{([^}]*)\}", text):
            options = [o.strip() for o in (m.group(1) or "").split(",") if o.strip()]
            for name in m.group(2).split(","):
                packages.setdefault(name.strip(), []).extend(options)
    return packages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("project_root", nargs="?", default=".")
    parser.add_argument("--root", help="root document, relative to the project root (default: auto-detect)")
    parser.add_argument("--out", help="write JSON here instead of stdout")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    files = list(iter_project_files(root))
    tex_files = [p for p in files if p.suffix in TEX_EXT]
    style_files = [p for p in files if p.suffix in STYLE_EXT]

    candidates = find_root_candidates(root, tex_files)
    if args.root:
        root_doc = (root / args.root).resolve()
    elif candidates:
        root_doc = (root / candidates[0]["file"]).resolve()
    else:
        write_json({"error": "no file with \\documentclass found", "project_root": str(root)}, args.out)
        raise SystemExit(2)

    walked = walk(root, root_doc)
    reached = {entry["file"] for entry in walked["reading_order"]}
    # Style files in the project are read for preamble macros too, as the
    # thesis loads them with \usepackage rather than \input.
    preamble_sources = [root / f for f in reached] + style_files
    templates = find_macro_templates(preamble_sources, root)
    bib = detect_bibliography(root, preamble_sources)
    bib_files = sorted({rel(p, root) for p in files if p.suffix in BIB_EXT})

    result = {
        "project_root": str(root),
        "root_document": rel(root_doc, root),
        "root_candidates": candidates,
        "reading_order": walked["reading_order"],
        "include_edges": walked["include_edges"],
        "missing_includes": walked["missing_includes"],
        "cycles": walked["cycles"],
        "duplicate_includes": walked["duplicate_includes"],
        "unreached_tex_files": sorted(rel(p, root) for p in tex_files if rel(p, root) not in reached),
        "style_files": [rel(p, root) for p in style_files],
        "bib_files": bib_files,
        "bibliography": bib,
        "packages": detect_packages(preamble_sources),
        "image_files": sorted(rel(p, root) for p in files if p.suffix.lower() in IMAGE_EXT),
        "glossary_files": sorted(rel(p, root) for p in files if any(h in p.name.lower() for h in GLOSSARY_HINTS)),
        "config_files": sorted(rel(p, root) for p in files if p.name in CONFIG_NAMES),
        "label_macros": [
            {
                "name": t.name,
                "spec": t.spec,
                "label_templates": t.label_templates,
                "graphics_templates": t.graphics_templates,
                "caption_templates": t.caption_templates,
                "environments": t.environments,
                "defined_in": t.defined_in,
                "line": t.line,
            }
            for t in templates.values()
        ],
    }
    write_json(result, args.out)


if __name__ == "__main__":
    main()
