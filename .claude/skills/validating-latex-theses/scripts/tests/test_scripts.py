"""Regression tests for the deterministic validator scripts.

Each test writes a small LaTeX project into a temporary directory, runs
the scripts on it as a user would, and checks the JSON they produce. The
fixtures follow the "Test Fixture Categories" of the skill suite. The
semantic fixtures (research question without experiment, formulaic
prose, and so on) test the language-model skills and are not automated.

Run from the scripts directory:
    python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent


def write(root: Path, files: dict[str, str]) -> None:
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(content).lstrip("\n"), encoding="utf-8")


def run(script: str, *args: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args], capture_output=True, text=True, cwd=SCRIPTS
    )
    if proc.returncode != 0:
        raise AssertionError(f"{script} failed: {proc.stderr}")
    return json.loads(proc.stdout)


class Project:
    def __init__(self, files: dict[str, str]):
        self.dir = Path(tempfile.mkdtemp(prefix="validator-test-"))
        write(self.dir, files)
        self.discovery_path = self.dir / "_discovery.json"
        self.discovery = run("discover_project.py", str(self.dir))
        self.discovery_path.write_text(json.dumps(self.discovery), encoding="utf-8")

    def identifiers(self) -> dict:
        return run("collect_identifiers.py", str(self.discovery_path))

    def structure(self) -> dict:
        return run("extract_structure.py", str(self.discovery_path))

    def cleanup(self) -> None:
        shutil.rmtree(self.dir, ignore_errors=True)


MAIN = r"""
\documentclass{article}
\usepackage[capitalize]{cleveref}
\begin{document}
\input{chapters/intro}
\input{chapters/method}
\bibliographystyle{plain}
\bibliography{refs}
\end{document}
"""

BIB = """
@article{ma2017, title={Lifelong MAPD}, author={Ma}, year={2017}, journal={J}}
@article{unused2020, title={Unused}, author={X}, year={2020}, journal={J}}
"""


class TestDiscovery(unittest.TestCase):
    def test_valid_multi_file_project_in_reading_order(self):
        p = Project({
            "main.tex": MAIN,
            "chapters/intro.tex": "\\section{Intro}\\label{sec:intro}\nSee \\cref{sec:method}.\n",
            "chapters/method.tex": "\\section{Method}\\label{sec:method}\nText \\citep{ma2017}.\n",
            "refs.bib": BIB,
            "notes/old.tex": "\\section{Old}\n",
        })
        try:
            d = p.discovery
            self.assertEqual(d["root_document"], "main.tex")
            self.assertEqual([e["file"] for e in d["reading_order"]], ["main.tex", "chapters/intro.tex", "chapters/method.tex"])
            self.assertEqual(d["unreached_tex_files"], ["notes/old.tex"])
            self.assertEqual(d["missing_includes"], [])
            self.assertEqual(d["bibliography"]["package"], "bibtex")
            self.assertIn("capitalize", d["packages"]["cleveref"])
        finally:
            p.cleanup()

    def test_missing_include(self):
        p = Project({"main.tex": "\\documentclass{article}\\begin{document}\n\\input{chapters/gone}\n\\end{document}\n"})
        try:
            self.assertEqual(len(p.discovery["missing_includes"]), 1)
            self.assertEqual(p.discovery["missing_includes"][0]["line"], 2)
        finally:
            p.cleanup()

    def test_include_cycle(self):
        p = Project({
            "main.tex": "\\documentclass{article}\\begin{document}\\input{a}\\end{document}\n",
            "a.tex": "\\input{b}\n",
            "b.tex": "\\input{a}\n",
        })
        try:
            self.assertEqual(len(p.discovery["cycles"]), 1)
            self.assertEqual(p.discovery["cycles"][0]["cycle"][-1], "a.tex")
        finally:
            p.cleanup()

    def test_commented_include_is_ignored(self):
        p = Project({
            "main.tex": "\\documentclass{article}\\begin{document}\n% \\input{gone}\n\\end{document}\n",
        })
        try:
            self.assertEqual(p.discovery["missing_includes"], [])
        finally:
            p.cleanup()

    def test_subfiles_child_is_not_the_root(self):
        p = Project({
            "main.tex": "\\documentclass{article}\\usepackage{subfiles}\\begin{document}\\subfile{ch/one}\\end{document}\n",
            "ch/one.tex": "\\documentclass[../main.tex]{subfiles}\\begin{document}\\section{One}\\end{document}\n",
        })
        try:
            self.assertEqual(p.discovery["root_document"], "main.tex")
            self.assertEqual([e["file"] for e in p.discovery["reading_order"]], ["main.tex", "ch/one.tex"])
        finally:
            p.cleanup()


class TestIdentifiers(unittest.TestCase):
    def test_citations_bibliography_and_cases(self):
        p = Project({
            "main.tex": MAIN,
            "chapters/intro.tex": "As \\citet{ma2017} show, and \\citep[see][p.~3]{Ma2017, nobody99}.\n",
            "chapters/method.tex": "% \\cite{commented}\n",
            "refs.bib": BIB + "\n@misc{ma2017, title={Again}}\n",
        })
        try:
            i = p.identifiers()
            self.assertEqual({u["key"] for u in i["undefined_citations"]}, {"Ma2017", "nobody99"})
            self.assertEqual([c["key"] for c in i["citation_case_mismatches"]], ["Ma2017"])
            self.assertEqual([d["key"] for d in i["duplicate_bib_keys"]], ["ma2017"])
            self.assertEqual([e["key"] for e in i["unused_bib_entries"]], ["unused2020"])
            cite = [c for c in i["citations"] if c["command"] == "citep"][0]
            self.assertEqual((cite["prenote"], cite["postnote"]), ("see", "p.~3"))
        finally:
            p.cleanup()

    def test_labels_references_and_forward_reference(self):
        p = Project({
            "main.tex": MAIN,
            "chapters/intro.tex": "\\section{Intro}\\label{sec:intro}\nSee \\cref{sec:method} and \\ref{fig:none}.\n",
            "chapters/method.tex": "\\section{Method}\\label{sec:method}\n\\label{sec:intro}\n",
            "refs.bib": BIB,
        })
        try:
            i = p.identifiers()
            self.assertEqual([u["key"] for u in i["undefined_references"]], ["fig:none"])
            self.assertEqual([d["key"] for d in i["duplicate_labels"]], ["sec:intro"])
            forward = [r for r in i["references"] if r["keys"] == ["sec:method"]][0]
            self.assertEqual(forward["forward"], ["sec:method"])
        finally:
            p.cleanup()

    def test_hard_coded_numbers(self):
        p = Project({
            "main.tex": MAIN,
            "chapters/intro.tex": "As Figure 3 shows, and as in Figure~2 of \\citet{ma2017}.\n",
            "chapters/method.tex": "",
            "refs.bib": BIB,
        })
        try:
            hard = p.identifiers()["hardcoded_numbers"]
            self.assertEqual([(h["text"], h["likely_external"]) for h in hard], [("Figure 3", False), ("Figure~2", True)])
        finally:
            p.cleanup()

    def test_labels_and_graphics_from_user_macros(self):
        p = Project({
            "main.tex": r"""
                \documentclass{article}
                \usepackage{graphicx}
                \NewDocumentCommand{\myfig}{O{htbp} m m m}{\begin{figure}[#1]\includegraphics{img/#2}\caption{#3}\label{fig:#4}\end{figure}}
                \newcommand{\simplefig}[3]{\begin{figure}\includegraphics{img/#1}\caption{#2}\label{fig:#3}\end{figure}}
                \begin{document}
                \myfig[t]{present.png}{A caption with words.}{one}
                \simplefig{absent.png}{Another caption.}{two}
                See \cref{fig:one}.
                \end{document}
            """,
            "img/present.png": "",
        })
        try:
            macros = {m["name"]: m for m in p.discovery["label_macros"]}
            self.assertEqual(macros["myfig"]["spec"], "ommm")
            self.assertEqual(macros["simplefig"]["spec"], "mmm")
            i = p.identifiers()
            self.assertEqual(sorted(l["key"] for l in i["labels"]), ["fig:one", "fig:two"])
            self.assertEqual([g["path"] for g in i["missing_graphics"]], ["img/absent.png"])
            self.assertEqual([l["key"] for l in i["unreferenced_labels"]], ["fig:two"])
            s = p.structure()
            captions = {o["labels"][0]: o["caption"] for o in s["objects"] if o["environment"].startswith("\\")}
            self.assertEqual(captions["fig:one"], "A caption with words.")
        finally:
            p.cleanup()


class TestStructure(unittest.TestCase):
    def test_reading_order_and_acronyms(self):
        p = Project({
            "main.tex": r"""
                \documentclass{article}
                \begin{document}
                \input{chapters/one}
                \section{Appendix}
                \end{document}
            """,
            "chapters/one.tex": (
                "\\section{One}\n"
                "We study MAPD here, as many systems do in many warehouses today.\n\n"
                "Multi-agent pickup and delivery (MAPD) is the problem of serving tasks.\n"
            ),
        })
        try:
            s = p.structure()
            self.assertEqual([x["title"] for x in s["sections"]], ["One", "Appendix"])
            mapd = [a for a in s["acronyms"] if a["acronym"] == "MAPD"][0]
            self.assertFalse(mapd["expanded_at_first_use"])
            self.assertTrue(mapd["expanded_anywhere"])
        finally:
            p.cleanup()


@unittest.skipUnless(shutil.which("latexmk") and shutil.which("pdflatex"), "latexmk/pdflatex not installed")
class TestCompile(unittest.TestCase):
    def _compile(self, files: dict[str, str]) -> dict:
        p = Project(files)
        try:
            return run("compile_project.py", str(p.discovery_path), "--outdir", str(p.dir / "_build"), "--no-chktex", "--wait", "0")
        finally:
            p.cleanup()

    def test_valid_document_compiles(self):
        result = self._compile({"main.tex": "\\documentclass{article}\\begin{document}\\section{A}\\label{a} See \\ref{a}.\\end{document}\n"})
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["pdf_produced"])

    def test_undefined_reference_is_reported_with_its_file(self):
        result = self._compile({
            "main.tex": "\\documentclass{article}\\begin{document}\\input{ch}\\end{document}\n",
            "ch.tex": "Text.\n\nSee \\ref{missing}.\n",
        })
        refs = result["log"]["undefined_references"]
        self.assertEqual([r["key"] for r in refs], ["missing"])
        self.assertEqual(refs[0]["file"], "ch.tex")

    def test_error_is_reported(self):
        result = self._compile({"main.tex": "\\documentclass{article}\\begin{document}\n\\undefinedmacro\n\\end{document}\n"})
        self.assertIn(result["status"], ("failed", "compiled_with_errors"))
        self.assertTrue(any("Undefined control sequence" in e["message"] for e in result["log"]["errors"]))


class TestAggregate(unittest.TestCase):
    def test_deterministic_and_specialist_findings_are_merged_and_sorted(self):
        p = Project({
            "main.tex": MAIN,
            "chapters/intro.tex": "See \\ref{fig:none} and \\citep{nobody99}.\n",
            "chapters/method.tex": "",
            "refs.bib": BIB,
        })
        try:
            ids = p.dir / "_ids.json"
            ids.write_text(json.dumps(p.identifiers()), encoding="utf-8")
            specialist = p.dir / "_cit.json"
            specialist.write_text(json.dumps({"findings": [
                {"id": "CIT006", "category": "citation", "severity": "Major", "confidence": "High", "status": "Needs Adjustment",
                 "location": "chapters/intro.tex:1", "excerpt": "\\citep{nobody99}", "target": "nobody99",
                 "explanation": "duplicate of the deterministic one", "recommended_action": "x", "automatic_fix": "No",
                 "source_skill": "auditing-thesis-citations"},
                {"id": "STY001", "category": "style", "severity": "Loud", "confidence": "High", "status": "OK",
                 "location": "chapters/intro.tex:1", "excerpt": "", "explanation": "bad severity", "recommended_action": "x",
                 "automatic_fix": "No", "source_skill": "reviewing-thesis-style"},
            ]}), encoding="utf-8")
            out = run("aggregate_findings.py", "--discovery", str(p.discovery_path), "--identifiers", str(ids), "--findings", str(specialist))
            ids_found = [f["id"] for f in out["findings"]]
            self.assertEqual(ids_found.count("CIT006"), 1, "the specialist duplicate is merged")
            self.assertIn("REF001", ids_found)
            self.assertEqual(out["summary"]["rejected"], 1, "an invalid severity is rejected, not silently kept")
            severities = [f["severity"] for f in out["findings"]]
            order = ["Blocker", "Critical", "Major", "Minor", "Suggestion"]
            self.assertEqual(severities, sorted(severities, key=order.index))
        finally:
            p.cleanup()


if __name__ == "__main__":
    unittest.main()
