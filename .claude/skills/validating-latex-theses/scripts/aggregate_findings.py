#!/usr/bin/env python3
"""Phase 5: turn deterministic results into findings, merge them with the
specialist audits' findings, and write one prioritised report.

Deterministic findings come from discover_project.py, compile_project.py,
collect_identifiers.py and extract_structure.py output. Specialist findings
are JSON files written by the auditing skills, each either a list of
findings or {"findings": [...]}, in the schema of
references/finding-schema.md.

Every finding is validated against the schema, duplicates are merged
(same rule, same file, same target, overlapping lines), and the result is
sorted by severity, then by reading order. Scores are not computed here:
they are a judgment for the main skill, written from this report.

Usage:
    aggregate_findings.py --discovery discovery.json [--compile compile.json]
        [--identifiers identifiers.json] [--structure structure.json]
        [--findings audit1.json audit2.json ...]
        [--overfull-threshold 10] [--out-json findings.json] [--out-md report.md]
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from pathlib import Path

from latex_common import load_json, reading_position, write_json

SEVERITIES = ["Blocker", "Critical", "Major", "Minor", "Suggestion"]
CONFIDENCES = ["High", "Medium", "Low"]
STATUSES = ["OK", "Needs Adjustment", "Not Assessable", "Accepted Exception"]
AUTOFIX = ["Yes", "No", "Review Required"]
REQUIRED = ["id", "category", "severity", "confidence", "status", "location", "excerpt", "explanation", "recommended_action", "automatic_fix", "source_skill"]
CATEGORY_ORDER = ["technical", "citation", "cross-reference", "definition", "notation", "structure", "rubric", "style"]
DETERMINISTIC = "validating-latex-theses (deterministic)"


def finding(rule, category, severity, confidence, file, line, excerpt, explanation, action,
            autofix="Review Required", end_line=None, related=None, status="Needs Adjustment", target=None):
    return {
        "id": rule,
        "category": category,
        "severity": severity,
        "confidence": confidence,
        "status": status,
        "location": {"file": file, "start_line": line, "end_line": end_line or line},
        "excerpt": excerpt,
        "explanation": explanation,
        "recommended_action": action,
        "automatic_fix": autofix,
        "related_locations": related or [],
        "criterion": None,
        "source_skill": DETERMINISTIC,
        "target": target,
    }


def loc(entry: dict) -> dict:
    return {"file": entry.get("file"), "start_line": entry.get("line"), "end_line": entry.get("end_line") or entry.get("line")}


# ---------------------------------------------------------------- deterministic findings


def from_discovery(d: dict) -> list[dict]:
    out = []
    for c in d.get("cycles", []):
        out.append(finding("TEX008", "technical", "Blocker", "High", c["from"], c["line"], f"\\{c['command']}{{{c['target']}}}",
                           "The include graph has a cycle, so the project cannot be traversed or compiled reliably: " + " -> ".join(c["cycle"]),
                           "Remove the include that closes the cycle.", "No", target=c["target"]))
    for m in d.get("missing_includes", []):
        out.append(finding("TEX007", "technical", "Critical", "High", m["from"], m["line"], f"\\{m['command']}{{{m['target']}}}",
                           "The included file does not exist, so its content is missing from the thesis.",
                           "Fix the path or restore the file.", "Review Required", target=m["target"]))
    for dup in d.get("duplicate_includes", []):
        out.append(finding("TEX009", "technical", "Minor", "High", dup["include_chain"][-2] if len(dup["include_chain"]) > 1 else dup["file"], None,
                           dup["file"], "The same file is included more than once, so its content appears twice.",
                           "Keep one include.", "Review Required", target=dup["file"]))
    return out


def from_compile(c: dict, threshold: float) -> list[dict]:
    out = []
    status = c.get("status")
    log = c.get("log", {})
    if status == "failed":
        first = (log.get("errors") or [{}])[0]
        out.append(finding("TEX001", "technical", "Blocker", "High", first.get("file") or c.get("root_document"), first.get("line"),
                           first.get("message", "no PDF produced"),
                           "The root document does not compile to a PDF. Every later check is provisional until it does.",
                           "Fix the first error in the log, then rebuild.", "No"))
    for e in log.get("errors", []):
        out.append(finding("TEX002", "technical", "Major" if status != "failed" else "Blocker", "High", e.get("file"), e.get("line"),
                           e["message"], "LaTeX reported an error. The PDF may be missing content or show it wrongly here.",
                           "Fix the error at this line.", "Review Required", target=e["message"]))
    for key in ("undefined_references", "undefined_citations"):
        for e in log.get(key, []):
            rule = "REF001" if key == "undefined_references" else "CIT006"
            out.append(finding(rule, "cross-reference" if rule == "REF001" else "citation", "Major", "High", e.get("file"), e.get("line"),
                               e["key"], "The build reports this key as undefined, so the output shows ?? in its place.",
                               "Add the missing label or bibliography entry, or correct the key.", "Review Required", target=e["key"]))
    for e in log.get("missing_files", []):
        out.append(finding("TEX010", "technical", "Major", "High", e.get("file"), e.get("line"), e["message"][:160],
                           "A file the build needs was not found.", "Add the file or fix its path.", "Review Required", target=e.get("key")))
    if log.get("rerun_requests"):
        out.append(finding("TEX012", "technical", "Minor", "Medium", c.get("root_document"), None, log["rerun_requests"][0]["message"][:160],
                           "The final pass still asks for a rerun, so references or labels may be out of date in the PDF.",
                           "Rebuild until the request disappears.", "Yes"))
    big = [b for b in log.get("overfull_boxes", []) if (b.get("amount_pt") or 0) > threshold]
    small = [b for b in log.get("overfull_boxes", []) if 0 < (b.get("amount_pt") or 0) <= threshold]
    for b in big:
        out.append(finding("TEX003", "technical", "Minor", "High", b.get("file"), b.get("line"), f"Overfull box, {b['amount_pt']:.1f}pt too wide",
                           "Content runs into the margin by a visible amount.", "Rewrap the line, resize the object, or split the equation.",
                           "Review Required", end_line=b.get("end_line")))
    if small:
        out.append(finding("TEX003", "technical", "Suggestion", "High", small[0].get("file"), small[0].get("line"),
                           f"{len(small)} overfull boxes of at most {threshold}pt",
                           "Small overflows, usually invisible in print.", "Check them in the PDF before submission.", "Review Required",
                           related=[loc(b) for b in small[1:]]))
    if log.get("underfull_boxes"):
        boxes = log["underfull_boxes"]
        out.append(finding("TEX004", "technical", "Suggestion", "High", boxes[0].get("file"), boxes[0].get("line"),
                           f"{len(boxes)} underfull boxes", "Loose lines or pages, a layout detail.", "Check spacing in the final layout.",
                           "Review Required", related=[loc(b) for b in boxes[1:]]))
    grouped = defaultdict(list)
    for w in log.get("warnings", []):
        grouped[(w["package"], re.sub(r"\d+", "N", w["message"])[:80])].append(w)
    for (package, _), ws in grouped.items():
        out.append(finding("TEX005", "technical", "Suggestion", "Medium", ws[0].get("file"), ws[0].get("line"),
                           f"{package} warning: {ws[0]['message'][:140]}" + (f" ({len(ws)} times)" if len(ws) > 1 else ""),
                           "A build warning. Most are harmless, but each should be understood once.",
                           "Read the warning and fix it or accept it.", "Review Required", related=[loc(w) for w in ws[1:]]))
    for issue in c.get("bibliography_tool_issues", []):
        out.append(finding("TEX011", "citation", "Major", "High", issue["tool_log"], None, issue["message"][:160],
                           "The bibliography tool reported a problem, so entries may be missing or wrong in the output.",
                           "Fix the entry the message names.", "Review Required", target=issue["message"]))
    by_number = defaultdict(list)
    for w in c.get("chktex", {}).get("warnings", []):
        by_number[(w.get("number"), w.get("message"))].append(w)
    for (number, message), ws in sorted(by_number.items(), key=lambda kv: -len(kv[1])):
        out.append(finding("TEX006", "technical", "Suggestion", "Low", ws[0]["file"], ws[0]["line"],
                           f"ChkTeX {number}: {message} ({len(ws)} times)",
                           "A lint pattern. ChkTeX reports many false positives, so review before changing anything.",
                           "Skim the occurrences and fix the real ones.", "Review Required", related=[loc(w) for w in ws[1:]]))
    return out


def from_identifiers(i: dict, discovery: dict) -> list[dict]:
    out = []
    undefined_cites = i.get("undefined_citations", [])
    distinct = {u["key"] for u in undefined_cites}
    for u in undefined_cites:
        out.append(finding("CIT006", "citation", "Critical" if len(distinct) >= 5 else "Major", "High", u["file"], u["line"], f"\\{u['command']}{{{u['key']}}}",
                           "No bibliography entry has this key.", "Add the entry or correct the key.", "Review Required", target=u["key"]))
    for u in i.get("citation_case_mismatches", []):
        out.append(finding("BIB002", "citation", "Major", "High", u["file"], u["line"], u["key"],
                           f"The key differs only in case from {', '.join(u['close_match'])}. Biber and BibTeX treat keys case-sensitively.",
                           "Use the exact key.", "Yes", target=u["key"]))
    for dup in i.get("duplicate_bib_keys", []):
        first = dup["entries"][0]
        out.append(finding("BIB001", "citation", "Major", "High", first["file"], first["line"], "@" + first["type"] + "{" + dup["key"] + ",",
                           "The same key is defined more than once. Only one entry is used, and which one is not obvious.",
                           "Keep one entry, or rename one and update its citations.", "Review Required",
                           related=[loc(e) for e in dup["entries"][1:]], target=dup["key"]))
    unused = i.get("unused_bib_entries", [])
    if unused:
        out.append(finding("CIT007", "citation", "Suggestion", "High", unused[0]["file"], unused[0]["line"],
                           ", ".join(e["key"] for e in unused[:12]) + (" ..." if len(unused) > 12 else ""),
                           f"{len(unused)} bibliography entries are never cited. With biblatex they do not appear in the bibliography, so this is only housekeeping.",
                           "Cite them where they support a claim, or remove them.", "No", related=[loc(e) for e in unused[1:]]))
    undefined_refs = i.get("undefined_references", [])
    distinct_refs = {u["key"] for u in undefined_refs}
    for u in undefined_refs:
        out.append(finding("REF001", "cross-reference", "Critical" if len(distinct_refs) >= 5 else "Major", "High", u["file"], u["line"],
                           f"\\{u['command']}{{{u['key']}}}", "No \\label defines this key.", "Add the label or correct the key.", "Review Required", target=u["key"]))
    for dup in i.get("duplicate_labels", []):
        first = dup["labels"][0]
        out.append(finding("REF002", "cross-reference", "Major", "High", first["file"], first["line"], dup["key"],
                           "The label is defined more than once, so references to it may point to the wrong object.",
                           "Rename one label and update its references.", "Review Required",
                           related=[loc(x) for x in dup["labels"][1:]], target=dup["key"]))
    for lab in i.get("empty_or_suspicious_labels", []):
        out.append(finding("REF011", "cross-reference", "Minor", "High", lab["file"], lab["line"], repr(lab["key"]),
                           "The label is empty or contains whitespace.", "Use a plain key such as fig:name.", "Review Required", target=lab["key"]))
    for g in i.get("missing_graphics", []):
        out.append(finding("TEX010", "technical", "Major", "High", g["file"], g["line"], f"{g['via']}: {g['path']}",
                           "The graphic file was not found, so the figure is missing or replaced by a box.",
                           "Add the file or correct the path.", "Review Required", target=g["path"]))
    for h in i.get("hardcoded_numbers", []):
        if h["likely_external"]:
            out.append(finding("REF003", "cross-reference", "Suggestion", "Low", h["file"], h["line"], h["context"].strip()[:160],
                               "A typed object number next to a citation, so it probably refers to the cited paper. Listed for a quick check.",
                               "Confirm it refers to the other paper. No change is needed if so.", "No", status="Not Assessable", target=h["text"]))
        else:
            out.append(finding("REF003", "cross-reference", "Minor", "Medium", h["file"], h["line"], h["context"].strip()[:160],
                               "A typed object number. If it refers to this thesis it breaks when numbering changes.",
                               "Replace it with \\cref{label} if it refers to this thesis.", "Review Required", target=h["text"]))
    capitalize = "capitalize" in discovery.get("packages", {}).get("cleveref", [])
    if not capitalize:
        for r in i.get("references", []):
            if r["command"] == "cref" and r.get("sentence_start"):
                out.append(finding("REF005", "cross-reference", "Minor", "Medium", r["file"], r["line"], "\\cref{" + ",".join(r["keys"]) + "}",
                                   "\\cref at the start of a sentence prints a lowercase name.", "Use \\Cref at a sentence start.", "Yes", target=",".join(r["keys"])))
    floats = [lab for lab in i.get("unreferenced_labels", []) if re.match(r"(fig|tab|alg|lst):", lab["key"])]
    for lab in floats:
        out.append(finding("REF012", "cross-reference", "Minor", "Medium", lab["file"], lab["line"], lab["key"],
                           "The figure or table is never referred to from the text, so the reader is not told why it is there.",
                           "Refer to it from the paragraph it supports, or check whether it is still needed.", "Review Required", target=lab["key"]))
    return out


def from_structure(s: dict) -> list[dict]:
    out = []
    for a in s.get("acronyms", []):
        if a["expanded_at_first_use"]:
            continue
        first = a["first_use"]
        if a["expanded_anywhere"]:
            out.append(finding("DEF002", "definition", "Minor", "Medium", first["file"], first["line"], a["acronym"],
                               "The acronym is used before the place where it is expanded.",
                               "Expand it at its first use in reading order (a title or abstract may count separately).", "Review Required", target=a["acronym"]))
        elif a["uses"] >= 2:
            out.append(finding("DEF002", "definition", "Minor", "Low", first["file"], first["line"], a["acronym"],
                               f"Used {a['uses']} times and never expanded. It may be a name, a standard term or a symbol rather than an acronym.",
                               "Expand it at first use if readers may not know it.", "Review Required", target=a["acronym"]))
    return out


# ---------------------------------------------------------------- normalisation


def normalise(f: dict, source: str) -> tuple[dict | None, list[str]]:
    problems = []
    f = dict(f)
    f.setdefault("source_skill", source)
    f.setdefault("related_locations", [])
    f.setdefault("criterion", None)
    location = f.get("location")
    if isinstance(location, str):
        m = re.match(r"(.+?):(\d+)(?:-(\d+))?$", location.strip())
        f["location"] = {"file": m.group(1), "start_line": int(m.group(2)), "end_line": int(m.group(3) or m.group(2))} if m else {"file": location, "start_line": None, "end_line": None}
    for name in REQUIRED:
        if name not in f or f[name] in (None, ""):
            if name == "excerpt":
                f[name] = ""
                continue
            problems.append(f"missing {name}")
    for name, allowed in (("severity", SEVERITIES), ("confidence", CONFIDENCES), ("status", STATUSES), ("automatic_fix", AUTOFIX)):
        if f.get(name) not in allowed:
            problems.append(f"{name}={f.get(name)!r} not in {allowed}")
    if problems:
        return None, problems
    return f, []


def dedupe(findings: list[dict]) -> list[dict]:
    kept: list[dict] = []
    for f in findings:
        merged = False
        for k in kept:
            if k["id"] != f["id"] or k["location"].get("file") != f["location"].get("file"):
                continue
            if (k.get("target") or k["excerpt"]) != (f.get("target") or f["excerpt"]):
                continue
            a0, a1 = k["location"].get("start_line"), k["location"].get("end_line")
            b0, b1 = f["location"].get("start_line"), f["location"].get("end_line")
            if a0 is None or b0 is None or not (a1 < b0 or b1 < a0):
                # Keep the more confident evidence; on a tie keep the higher severity.
                if (CONFIDENCES.index(f["confidence"]), SEVERITIES.index(f["severity"])) < (CONFIDENCES.index(k["confidence"]), SEVERITIES.index(k["severity"])):
                    f["related_locations"] = k["related_locations"] + [k["location"]] + f["related_locations"]
                    kept[kept.index(k)] = f
                else:
                    k["related_locations"].append(f["location"])
                merged = True
                break
        if not merged:
            kept.append(f)
    return kept


def category_of(f: dict) -> str:
    c = f["category"].lower()
    for name in CATEGORY_ORDER:
        if c.startswith(name.split("-")[0]):
            return name
    return c


# ---------------------------------------------------------------- report


def render_md(findings: list[dict], invalid: list[dict], unavailable: list[str], summary: dict) -> str:
    lines = ["# Thesis validation findings", ""]
    lines += ["## Summary", ""]
    lines.append("| Severity | Count |")
    lines.append("|---|---|")
    for s in SEVERITIES:
        lines.append(f"| {s} | {summary['by_severity'].get(s, 0)} |")
    lines.append("")
    lines.append("| Category | Count |")
    lines.append("|---|---|")
    for c, n in summary["by_category"].items():
        lines.append(f"| {c} | {n} |")
    lines.append("")
    if unavailable:
        lines += ["## Checks not completed", ""] + [f"- {u}" for u in unavailable] + [""]
    if invalid:
        lines += ["## Findings rejected by schema validation", ""]
        lines += [f"- from {x['source']}: {', '.join(x['problems'])}" for x in invalid] + [""]
    for cat in summary["by_category"]:
        group = [f for f in findings if category_of(f) == cat]
        lines += [f"## {cat.capitalize()}", ""]
        for f in group:
            l = f["location"]
            where = l.get("file") or "?"
            if l.get("start_line"):
                where += f":{l['start_line']}" + (f"-{l['end_line']}" if l.get("end_line") and l["end_line"] != l["start_line"] else "")
            lines.append(f"### {f['id']} · {f['severity']} · {f['confidence']} confidence")
            lines.append("")
            lines.append(f"- **Status:** {f['status']}")
            lines.append(f"- **Location:** `{where}`" + (f" ({f['section']})" if f.get("section") else ""))
            if f["excerpt"]:
                lines.append(f"- **Excerpt:** `{f['excerpt'][:200]}`")
            lines.append(f"- **Explanation:** {f['explanation']}")
            lines.append(f"- **Recommended action:** {f['recommended_action']}")
            lines.append(f"- **Automatic fix:** {f['automatic_fix']}")
            if f.get("criterion"):
                lines.append(f"- **Criterion:** {f['criterion']}")
            if f["related_locations"]:
                rel = [f"{r.get('file')}:{r.get('start_line')}" for r in f["related_locations"][:8]]
                more = len(f["related_locations"]) - len(rel)
                lines.append(f"- **Related:** {', '.join(rel)}" + (f" and {more} more" if more > 0 else ""))
            lines.append(f"- **Source:** {f['source_skill']}")
            lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--discovery", required=True)
    parser.add_argument("--compile")
    parser.add_argument("--identifiers")
    parser.add_argument("--structure")
    parser.add_argument("--findings", nargs="*", default=[])
    parser.add_argument("--overfull-threshold", type=float, default=10.0)
    parser.add_argument("--no-deterministic-heuristics", action="store_true", help="skip heuristic candidates (REF003, DEF002, REF012)")
    parser.add_argument("--out-json")
    parser.add_argument("--out-md")
    args = parser.parse_args()

    discovery = load_json(args.discovery)
    raw: list[tuple[dict, str]] = [(f, DETERMINISTIC) for f in from_discovery(discovery)]
    unavailable: list[str] = []
    if args.compile:
        comp = load_json(args.compile)
        raw += [(f, DETERMINISTIC) for f in from_compile(comp, args.overfull_threshold)]
        unavailable += comp.get("unavailable_checks", [])
    else:
        unavailable.append("compilation not run")
    if args.identifiers:
        raw += [(f, DETERMINISTIC) for f in from_identifiers(load_json(args.identifiers), discovery)]
    else:
        unavailable.append("identifier extraction not run")
    if args.structure:
        raw += [(f, DETERMINISTIC) for f in from_structure(load_json(args.structure))]
    for path in args.findings:
        data = load_json(path)
        items = data["findings"] if isinstance(data, dict) else data
        raw += [(f, Path(path).stem) for f in items]

    if args.no_deterministic_heuristics:
        raw = [(f, s) for f, s in raw if not (s == DETERMINISTIC and f["id"] in ("REF003", "DEF002", "REF012"))]

    valid, invalid = [], []
    for f, source in raw:
        normalised, problems = normalise(f, source)
        if normalised is None:
            invalid.append({"source": source, "problems": problems, "finding": f})
        else:
            valid.append(normalised)

    findings = dedupe(valid)
    position = reading_position(discovery)
    findings.sort(key=lambda f: (SEVERITIES.index(f["severity"]), position(f["location"].get("file") or "", f["location"].get("start_line") or 0)))

    by_category: dict[str, int] = {}
    for name in CATEGORY_ORDER + sorted({category_of(f) for f in findings} - set(CATEGORY_ORDER)):
        n = sum(1 for f in findings if category_of(f) == name)
        if n:
            by_category[name] = n
    summary = {
        "total": len(findings),
        "by_severity": {s: sum(1 for f in findings if f["severity"] == s) for s in SEVERITIES},
        "by_category": by_category,
        "rejected": len(invalid),
    }
    result = {"summary": summary, "unavailable_checks": unavailable, "findings": findings, "rejected": invalid}
    if args.out_json or not args.out_md:
        write_json(result, args.out_json)
    if args.out_md:
        Path(args.out_md).write_text(render_md(findings, invalid, unavailable, summary) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
