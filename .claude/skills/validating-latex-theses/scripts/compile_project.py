#!/usr/bin/env python3
"""Phase 2: compile the thesis and collect deterministic build findings.

Builds the root document with latexmk into a separate output directory,
so an editor that runs its own latexmk in the project folder never sees
half-written .aux files. latexmk runs as many passes as references and
the bibliography need. The log is parsed for errors, warnings, undefined
references and citations, missing files and over/underfull boxes, each
attributed to a source file where the log allows it. ChkTeX is run over
every file in the reading order when it is installed.

Usage:
    compile_project.py DISCOVERY_JSON [--outdir DIR] [--engine pdf|xelatex|lualatex]
                       [--no-chktex] [--timeout SECONDS] [--out compile.json]
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from latex_common import load_json, write_json

ENGINE_FLAGS = {"pdf": "-pdf", "xelatex": "-xelatex", "lualatex": "-lualatex"}


def tool_version(cmd: list[str]) -> str | None:
    if shutil.which(cmd[0]) is None:
        return None
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = (out.stdout or out.stderr).strip().splitlines()
    return text[0] if text else None


def wait_for_other_builds(max_wait: float) -> bool:
    """Wait while another pdflatex/xelatex/lualatex is running (an editor
    build). Returns False if one was still running after max_wait."""
    if shutil.which("pgrep") is None:
        return True
    deadline = time.time() + max_wait
    while time.time() < deadline:
        busy = subprocess.run(["pgrep", "-x", "pdflatex|xelatex|lualatex"], capture_output=True)
        if busy.returncode != 0:
            return True
        time.sleep(2)
    return False


# ---------------------------------------------------------------- log parsing

_FILE_OPEN = re.compile(r"\((\.{0,2}/[^\s()]+?\.(?:tex|sty|cls|bbl|aux|toc|cfg|def|clo|fd))")


def unwrap_log(text: str) -> str:
    """TeX wraps log lines at 79 characters. Rejoin lines that are exactly
    that long, so file names and messages are not split."""
    out, buf = [], ""
    for line in text.split("\n"):
        buf += line
        if len(line) != 79:
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return "\n".join(out)


def parse_log(log_text: str, project_root: Path) -> dict:
    text = unwrap_log(log_text)
    lines = text.split("\n")
    findings: dict[str, list] = {
        "errors": [],
        "warnings": [],
        "undefined_references": [],
        "undefined_citations": [],
        "missing_files": [],
        "overfull_boxes": [],
        "underfull_boxes": [],
        "rerun_requests": [],
    }
    stack: list[str] = []

    def current_file() -> str | None:
        for name in reversed(stack):
            if name.endswith(".tex"):
                return name.lstrip("./") if name.startswith("./") else name
        return None

    for i, line in enumerate(lines):
        # Track the file stack: "(./file.tex" opens, ")" closes. A heuristic,
        # since parentheses in messages also count, so file attribution is
        # best-effort and marked as such.
        for token in re.finditer(r"\(|\)", line):
            if token.group() == "(":
                m = _FILE_OPEN.match(line, token.start())
                stack.append(m.group(1) if m else "")
            elif stack:
                stack.pop()

        if line.startswith("! "):
            context = [l for l in lines[i + 1 : i + 6] if l.strip()]
            src_line = None
            for l in context:
                lm = re.match(r"l\.(\d+)", l)
                if lm:
                    src_line = int(lm.group(1))
                    break
            findings["errors"].append(
                {"message": line[2:].strip(), "file": current_file(), "line": src_line, "context": context[:3]}
            )
            continue

        m = re.search(r"(?:LaTeX|Package (\S+)|Class (\S+)) Warning: (.*)", line)
        if m:
            message = m.group(3)
            j = i + 1
            while j < len(lines) and lines[j].startswith(" " * 4) and j < i + 6:
                message += " " + lines[j].strip()
                j += 1
            lm = re.search(r"on input line (\d+)", message)
            entry = {
                "package": m.group(1) or m.group(2) or "LaTeX",
                "message": message.strip(),
                "file": current_file(),
                "line": int(lm.group(1)) if lm else None,
            }
            ref = re.search(r"Reference `([^']+)' on page", message)
            cite = re.search(r"Citation `([^']+)'", message)
            if ref:
                findings["undefined_references"].append({**entry, "key": ref.group(1)})
            elif cite:
                findings["undefined_citations"].append({**entry, "key": cite.group(1)})
            elif "Rerun" in message or "rerun" in message:
                findings["rerun_requests"].append(entry)
            elif re.search(r"File `[^']+' not found|not found", message):
                findings["missing_files"].append(entry)
            else:
                findings["warnings"].append(entry)
            continue

        m = re.match(r"(Overfull|Underfull) \\[hv]box \((?:(\d+(?:\.\d+)?)pt too \w+|badness (\d+))\) (?:in paragraph at lines (\d+)--(\d+)|detected at line (\d+)|.*)", line)
        if m:
            entry = {
                "kind": m.group(1),
                "amount_pt": float(m.group(2)) if m.group(2) else None,
                "badness": int(m.group(3)) if m.group(3) else None,
                "file": current_file(),
                "line": int(m.group(4) or m.group(6)) if (m.group(4) or m.group(6)) else None,
                "end_line": int(m.group(5)) if m.group(5) else None,
            }
            findings["overfull_boxes" if m.group(1) == "Overfull" else "underfull_boxes"].append(entry)
            continue

        m = re.search(r"LaTeX Error: File `([^']+)' not found", line)
        if m:
            findings["missing_files"].append({"message": line.strip(), "file": current_file(), "line": None, "key": m.group(1)})

    # Deduplicate undefined keys reported once per pass.
    for key in ("undefined_references", "undefined_citations"):
        seen, unique = set(), []
        for entry in findings[key]:
            sig = (entry["key"], entry["file"], entry["line"])
            if sig not in seen:
                seen.add(sig)
                unique.append(entry)
        findings[key] = unique
    findings["file_attribution"] = "best-effort (parsed from the TeX log file stack)"
    return findings


def parse_biber_or_bibtex(outdir: Path, stem: str) -> list[dict]:
    issues = []
    for ext in (".blg",):
        path = outdir / (stem + ext)
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            if re.search(r"\b(WARN|ERROR)\b|^Warning--|error message", line):
                issues.append({"tool_log": path.name, "message": line.strip()})
    return issues


# ---------------------------------------------------------------- chktex


def run_chktex(project_root: Path, files: list[str], timeout: int) -> dict:
    if shutil.which("chktex") is None:
        return {"available": False, "warnings": []}
    warnings = []
    for rel_path in files:
        path = project_root / rel_path
        try:
            proc = subprocess.run(
                ["chktex", "-q", "-v0", "-I0", "-f%f:%l:%c:%n:%m\n", str(path)],
                capture_output=True,
                text=True,
                cwd=project_root,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            warnings.append({"file": rel_path, "line": None, "number": None, "message": "chktex timed out"})
            continue
        for line in proc.stdout.splitlines():
            parts = line.split(":", 4)
            if len(parts) == 5 and parts[1].isdigit():
                warnings.append(
                    {
                        "file": rel_path,
                        "line": int(parts[1]),
                        "column": int(parts[2]) if parts[2].isdigit() else None,
                        "number": int(parts[3]) if parts[3].isdigit() else None,
                        "message": parts[4].strip(),
                    }
                )
    return {"available": True, "warnings": warnings}


# ---------------------------------------------------------------- main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("discovery", help="output of discover_project.py")
    parser.add_argument("--outdir", help="build directory (default: a fresh temporary directory)")
    parser.add_argument("--engine", choices=sorted(ENGINE_FLAGS), default="pdf")
    parser.add_argument("--no-chktex", action="store_true")
    parser.add_argument("--timeout", type=int, default=600, help="latexmk timeout in seconds")
    parser.add_argument("--wait", type=int, default=120, help="seconds to wait for another TeX build to finish")
    parser.add_argument("--out", help="write JSON here instead of stdout")
    args = parser.parse_args()

    discovery = load_json(args.discovery)
    project_root = Path(discovery["project_root"])
    root_doc = project_root / discovery["root_document"]
    outdir = Path(args.outdir) if args.outdir else Path(tempfile.mkdtemp(prefix="thesis-validate-"))
    outdir.mkdir(parents=True, exist_ok=True)

    result: dict = {
        "root_document": discovery["root_document"],
        "outdir": str(outdir),
        "tools": {
            "latexmk": tool_version(["latexmk", "-v"]),
            "pdflatex": tool_version(["pdflatex", "--version"]),
            "biber": tool_version(["biber", "--version"]),
            "bibtex": tool_version(["bibtex", "--version"]),
            "chktex": tool_version(["chktex", "--version"]),
        },
        "unavailable_checks": [],
    }

    if not wait_for_other_builds(args.wait):
        result["unavailable_checks"].append("another TeX build was still running; compiled anyway into a separate outdir")

    if shutil.which("latexmk") is None:
        result["status"] = "not_run"
        result["unavailable_checks"].append("latexmk not installed: compilation skipped")
    else:
        cmd = [
            "latexmk",
            ENGINE_FLAGS[args.engine],
            "-interaction=nonstopmode",
            f"-outdir={outdir}",
            root_doc.name,
        ]
        started = time.time()
        try:
            proc = subprocess.run(
                cmd, cwd=root_doc.parent, capture_output=True, text=True, timeout=args.timeout
            )
            result["exit_code"] = proc.returncode
            result["latexmk_tail"] = proc.stdout.splitlines()[-15:] + proc.stderr.splitlines()[-15:]
        except subprocess.TimeoutExpired:
            result["exit_code"] = None
            result["unavailable_checks"].append(f"latexmk timed out after {args.timeout}s")
        result["seconds"] = round(time.time() - started, 1)
        result["command"] = " ".join(cmd)

        stem = root_doc.stem
        log_path = outdir / (stem + ".log")
        pdf_path = outdir / (stem + ".pdf")
        result["pdf_produced"] = pdf_path.exists()
        if log_path.exists():
            result["log"] = parse_log(log_path.read_text(encoding="utf-8", errors="replace"), project_root)
        else:
            result["unavailable_checks"].append("no TeX log produced")
        result["bibliography_tool_issues"] = parse_biber_or_bibtex(outdir, stem)
        errors = result.get("log", {}).get("errors", [])
        if not result["pdf_produced"]:
            result["status"] = "failed"
        elif errors or result.get("exit_code"):
            result["status"] = "compiled_with_errors"
        else:
            result["status"] = "ok"

    if args.no_chktex:
        result["chktex"] = {"available": False, "warnings": [], "skipped": True}
    else:
        files = [entry["file"] for entry in discovery["reading_order"]]
        result["chktex"] = run_chktex(project_root, files, timeout=60)
        if not result["chktex"]["available"]:
            result["unavailable_checks"].append("chktex not installed")

    write_json(result, args.out)


if __name__ == "__main__":
    main()
