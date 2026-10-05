"""Shared LaTeX helpers for the thesis-validator scripts.

Standard library only. Every helper keeps line numbers intact, so each
extracted item can be traced back to a file and line.
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

INCLUDE_COMMANDS = ("input", "include", "subfile", "subfileinclude", "import", "subimport")
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "_minted", "build", "out"}


# ---------------------------------------------------------------- text


def strip_comments(text: str) -> str:
    """Remove LaTeX comments but keep every newline, so line numbers stay
    valid. An escaped percent sign (\\%) is kept."""
    out_lines = []
    for line in text.split("\n"):
        out_lines.append(_strip_line_comment(line))
    return "\n".join(out_lines)


def _strip_line_comment(line: str) -> str:
    i = 0
    while i < len(line):
        if line[i] == "\\":
            i += 2
            continue
        if line[i] == "%":
            return line[:i]
        i += 1
    return line


VERBATIM_ENVS = ("verbatim", "Verbatim", "lstlisting", "minted", "comment")


def blank_verbatim(text: str) -> str:
    """Replace the body of verbatim-like environments with blank lines, so
    their content is not parsed as LaTeX but line numbers are preserved."""
    for env in VERBATIM_ENVS:
        pattern = re.compile(
            r"(\\begin\{" + re.escape(env) + r"\*?\})(.*?)(\\end\{" + re.escape(env) + r"\*?\})",
            re.S,
        )
        text = pattern.sub(lambda m: m.group(1) + re.sub(r"[^\n]", " ", m.group(2)) + m.group(3), text)
    return text


def clean_source(text: str) -> str:
    return blank_verbatim(strip_comments(text))


def line_of(text: str, index: int) -> int:
    """1-based line number of a character offset."""
    return text.count("\n", 0, index) + 1


def read_group(text: str, start: int, open_ch: str = "{", close_ch: str = "}") -> tuple[str, int] | None:
    """Read a balanced group starting at text[start] == open_ch. Returns
    (content, index after the closing character), or None if unbalanced."""
    if start >= len(text) or text[start] != open_ch:
        return None
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == open_ch:
            depth += 1
        elif ch == close_ch:
            depth -= 1
            if depth == 0:
                return text[start + 1 : i], i + 1
        i += 1
    return None


def skip_spaces(text: str, i: int) -> int:
    while i < len(text) and text[i] in " \t\n":
        i += 1
    return i


def read_args(text: str, i: int, spec: str) -> tuple[list[str | None], int] | None:
    """Read command arguments after a command name, following a spec of
    'm' (mandatory {...}) and 'o' (optional [...]). Returns the arguments
    in order (None for an absent optional one) and the end index."""
    args: list[str | None] = []
    for kind in spec:
        j = skip_spaces(text, i)
        if kind == "o":
            if j < len(text) and text[j] == "[":
                group = read_group(text, j, "[", "]")
                if group is None:
                    return None
                args.append(group[0])
                i = group[1]
            else:
                args.append(None)
        else:
            if j < len(text) and text[j] == "{":
                group = read_group(text, j)
                if group is None:
                    return None
                args.append(group[0])
                i = group[1]
            elif j < len(text) and text[j] == "\\":
                m = re.match(r"\\[A-Za-z@]+|\\.", text[j:])
                args.append(m.group(0) if m else text[j])
                i = j + (len(m.group(0)) if m else 1)
            elif j < len(text):
                args.append(text[j])
                i = j + 1
            else:
                return None
    return args, i


# ---------------------------------------------------------------- macros


@dataclass
class MacroTemplate:
    """A user macro whose body contains \\label or \\includegraphics with an
    argument placeholder, e.g. \\myfig whose 4th argument becomes fig:#4."""

    name: str
    spec: str  # sequence of 'm' / 'o'
    label_templates: list[str] = field(default_factory=list)
    graphics_templates: list[str] = field(default_factory=list)
    caption_templates: list[str] = field(default_factory=list)
    environments: list[str] = field(default_factory=list)
    defined_in: str = ""
    line: int = 0

    def expand(self, template: str, args: list[str | None]) -> str | None:
        def sub(m: re.Match) -> str:
            k = int(m.group(1)) - 1
            value = args[k] if k < len(args) else None
            return value if value is not None else "\x00"

        result = re.sub(r"#(\d)", sub, template)
        return None if "\x00" in result else result.strip()


_XPARSE = re.compile(r"\\(?:New|Renew|Provide|Declare)DocumentCommand\s*\{?\s*\\([A-Za-z@]+)\s*\}?\s*")
_NEWCOMMAND = re.compile(r"\\(?:re)?newcommand\*?\s*\{?\s*\\([A-Za-z@]+)\s*\}?\s*")


def _xparse_spec(spec: str) -> str:
    out = []
    i = 0
    while i < len(spec):
        ch = spec[i]
        if ch in "mrRv":
            out.append("m")
        elif ch in "oO":
            out.append("o")
        elif ch in "sStdD":
            out.append("o")  # treated as optional; star detection is not needed here
        i += 1
        if i < len(spec) and spec[i] == "{":
            group = read_group(spec, i)
            i = group[1] if group else i + 1
    return "".join(out)


def find_macro_templates(files: list[Path], root: Path) -> dict[str, MacroTemplate]:
    templates: dict[str, MacroTemplate] = {}
    for path in files:
        try:
            text = clean_source(path.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        for m in _XPARSE.finditer(text):
            spec_group = read_group(text, skip_spaces(text, m.end()))
            if spec_group is None:
                continue
            body_group = read_group(text, skip_spaces(text, spec_group[1]))
            if body_group is None:
                continue
            _register(templates, m.group(1), _xparse_spec(spec_group[0]), body_group[0], path, root, text, m.start())
        for m in _NEWCOMMAND.finditer(text):
            i = skip_spaces(text, m.end())
            nargs, has_default = 0, False
            if i < len(text) and text[i] == "[":
                g = read_group(text, i, "[", "]")
                if g and g[0].strip().isdigit():
                    nargs = int(g[0].strip())
                    i = skip_spaces(text, g[1])
                    if i < len(text) and text[i] == "[":
                        g2 = read_group(text, i, "[", "]")
                        if g2:
                            has_default = True
                            i = skip_spaces(text, g2[1])
            body = read_group(text, i)
            if body is None:
                continue
            spec = ("o" + "m" * (nargs - 1)) if has_default and nargs else "m" * nargs
            _register(templates, m.group(1), spec, body[0], path, root, text, m.start())
    return templates


_ANY_DEFINITION = re.compile(
    r"\\(?:(?:New|Renew|Provide|Declare)DocumentCommand|(?:re)?newcommand\*?|providecommand\*?|def)(?![A-Za-z])"
)


def blank_definitions(text: str) -> str:
    """Blank out macro definitions (name, argument spec and body), keeping
    newlines, so a scan for macro uses or labels does not mistake a
    definition body for a use."""
    chars = list(text)
    for m in _ANY_DEFINITION.finditer(text):
        i = skip_spaces(text, m.end())
        # macro name, braced or bare
        if i < len(text) and text[i] == "{":
            g = read_group(text, i)
            if g is None:
                continue
            i = g[1]
        else:
            nm = re.match(r"\\[A-Za-z@]+", text[i:])
            if not nm:
                continue
            i += len(nm.group(0))
        # any number of [..] / {..} groups up to and including the body; the
        # body is the last group before something that is not a group.
        while True:
            j = skip_spaces(text, i)
            if j < len(text) and text[j] in "[{":
                g = read_group(text, j, text[j], "]" if text[j] == "[" else "}")
                if g is None:
                    break
                i = g[1]
                if text[j] == "{" and not _looks_like_spec(text[j + 1 : g[1] - 1]):
                    break
            elif m.group(0) == "\\def" and j < len(text) and text[j] == "#":
                k = text.find("{", j)
                if k < 0:
                    break
                i = k
            else:
                break
        for k in range(m.start(), i):
            if chars[k] != "\n":
                chars[k] = " "
    return "".join(chars)


def _looks_like_spec(group: str) -> bool:
    """An xparse argument spec such as 'O{htbp} m m', not a body."""
    stripped = re.sub(r"\{[^{}]*\}", "", group)
    return bool(stripped.strip()) and re.fullmatch(r"[\smoOrRvsStdDbe+!>=]*", stripped) is not None


def _register(templates, name, spec, body, path, root, text, offset) -> None:
    labels = [g for g in re.findall(r"\\label\s*\{([^{}]*#\d[^{}]*)\}", body)]
    graphics = [
        g for g in re.findall(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^{}]*#\d[^{}]*)\}", body)
    ]
    if not labels and not graphics:
        return
    captions = re.findall(r"\\caption\s*(?:\[[^\]]*\])?\s*\{([^{}]*#\d[^{}]*)\}", body)
    envs = re.findall(r"\\begin\{([A-Za-z*]+)\}", body)
    templates[name] = MacroTemplate(
        name=name,
        spec=spec,
        label_templates=labels,
        graphics_templates=graphics,
        caption_templates=captions,
        environments=envs,
        defined_in=rel(path, root),
        line=line_of(text, offset),
    )


# ---------------------------------------------------------------- paths / io


def rel(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def iter_project_files(root: Path):
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS or part.startswith(".") and part not in (".",) for part in path.relative_to(root).parts[:-1]):
            continue
        if path.is_file():
            yield path


def load_json(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(data, out: str | None) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if out:
        Path(out).write_text(text + "\n", encoding="utf-8")
    else:
        sys.stdout.write(text + "\n")


def templates_from_discovery(discovery: dict) -> dict[str, MacroTemplate]:
    return {
        t["name"]: MacroTemplate(
            name=t["name"],
            spec=t["spec"],
            label_templates=t["label_templates"],
            graphics_templates=t["graphics_templates"],
            caption_templates=t.get("caption_templates", []),
            environments=t["environments"],
            defined_in=t["defined_in"],
            line=t["line"],
        )
        for t in discovery.get("label_macros", [])
    }


def project_files_from_discovery(discovery: dict, root: Path) -> list[Path]:
    """The .tex files in reading order, as resolved by discover_project.py."""
    return [root / entry["file"] for entry in discovery["reading_order"]]


def style_files_from_discovery(discovery: dict, root: Path) -> list[Path]:
    return [root / f for f in discovery.get("style_files", [])]


def reading_position(discovery: dict):
    """Return a function (file, line) -> sort key in true reading order.

    The key is the tuple of include-command lines along the include chain,
    followed by the line itself, so text in main.tex after \\subfile{ch2}
    sorts after everything inside ch2. Files outside the reading order sort
    last."""
    edge_line: dict[tuple[str, str], int] = {}
    for edge in discovery.get("include_edges", []):
        if edge.get("resolved"):
            edge_line.setdefault((edge["from"], edge["resolved"]), edge["line"])
    chain_key: dict[str, tuple[int, ...]] = {}
    for entry in discovery["reading_order"]:
        chain = entry["include_chain"]
        if entry["file"] in chain_key:
            continue
        key = tuple(edge_line.get((a, b), 0) for a, b in zip(chain, chain[1:]))
        chain_key[entry["file"]] = key

    def position(file: str, line: int) -> tuple:
        if file not in chain_key:
            return (10**9, file, line)
        return chain_key[file] + (line,)

    return position
