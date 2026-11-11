#!/usr/bin/env python3
"""Build the plugin's docs/ folder from the three published Autograntor files.

Usage: python3 build_docs.py <commonlaw.md (pandoc gfm)> <percy.docx> <milestones.xlsx> <out docs dir>

Ruling text is copied, never rewritten. Only the packaging changes:
the single document is split into a core file, an index and topic files.
"""
import re
import subprocess
import sys
from pathlib import Path

import openpyxl

cl_md, percy_docx, xlsx, out = sys.argv[1:5]
out = Path(out)
(out / "common_law_topics").mkdir(parents=True, exist_ok=True)
(out / "common_law_proposed").mkdir(parents=True, exist_ok=True)

NOTE = ("> **Packaging note (prototype, not part of the Common Law).** {}\n\n")


def unescape(text):
    """Remove pandoc's markdown backslash escapes so agents read plain text."""
    return re.sub(r"\\([\[\]$<>*|#~_'\"`-])", r"\1", text)


raw = Path(cl_md).read_text(encoding="utf-8")

# ---- split into Part I / rulings --------------------------------------
part2 = raw.index("## Part II: Adopted rulings")
part3 = raw.index("## Part III: Proposed rulings")
header_and_part1 = raw[:part2]
adopted_block = raw[part2:part3]
proposed_block = raw[part3:]


def rulings(block):
    """Return [(number, title_line, full_text)] for each '### CL-n' section."""
    parts = re.split(r"(?m)^(?=### CL-\d+)", block)
    found = []
    for p in parts:
        m = re.match(r"### CL-(\d+): ?(.*)", p)
        if m:
            found.append((int(m.group(1)), m.group(2).strip(), p.rstrip() + "\n"))
    return found


adopted = rulings(adopted_block)
proposed = rulings(proposed_block)
all_rulings = {n: (title, text, "Adopted") for n, title, text in adopted}
for n, title, text in proposed:
    assert n not in all_rulings, n
    all_rulings[n] = (title, text, "Proposed")
PUBLIC_MAX = max(all_rulings)
assert sorted(all_rulings) == list(range(1, PUBLIC_MAX + 1)), "gap in public rulings"

# ---- Part I: put the ruling template in a code block -------------------
# (unescaped, its '### CL-<next number>' line would otherwise read as a real heading)
p1 = unescape(header_and_part1)
tmpl_start = p1.index("### CL-<next number>")
tmpl_end = p1.index("## Part II") if "## Part II" in p1 else len(p1)
template = p1[tmpl_start:tmpl_end].rstrip()
template = re.sub(r"\n\n+", "\n", template)
p1 = p1[:tmpl_start] + "```\n" + template + "\n```\n\n"

# ---- core file ----------------------------------------------------------
core = p1
core = core.replace(
    "# Autograntor Common Law\n",
    "# Autograntor Common Law — core\n\n"
    + NOTE.format(
        "This file holds Part I and every Adopted ruling from the published Common Law "
        "(version 2026-10-18.2), text unchanged. Proposed rulings are in `common_law_topics/`; "
        "`common_law_index.md` lists every ruling and its file. Where Part I says to append new "
        "rulings to Part III, the skill's instruction wins: write them to a new file in "
        "`common_law_proposed/`."
    ).rstrip("\n")
    + "\n",
    1,
)
core += "## Part II: Adopted rulings\n\n"
for n, title, text in adopted:
    core += unescape(text) + "\n"
(out / "common_law_core.md").write_text(core, encoding="utf-8")

# ---- topic files --------------------------------------------------------
# The split below is the packager's guess, guided by the topic list in the v2 skill.
TOPICS = {
    "method-and-programs": (
        "Simulation and spread, post-2030 share, attribution across years, lags and dated windows, "
        "venues, and programs that die without the grant.",
        [16, 18, 19, 31, 46, 52, 55],
    ),
    "money-and-funders": (
        "Pending or outside money, funging, runway, absorptive capacity, refunds, earned revenue.",
        [14, 21, 23, 28, 29, 34, 35, 41, 43, 44, 53, 58, 59],
    ),
    "expansion-and-hiring": (
        "New hires, contractors, grants above the ask, the marginal factor, people charges.",
        [22, 36, 37, 38, 39, 40, 54, 56, 57, 60],
    ),
    "media-and-persuasion": (
        "Media, audiences, creators, games and campaigns. Read with `PERCYs_v3.7_compact.md`.",
        [24, 25, 26, 30],
    ),
    "policy-and-laws": (
        "Advocacy and policy organisations, law rows, c3/c4, electoral work, non-US actors.",
        [45, 47, 48, 49, 50, 51],
    ),
    "reputation-and-values": (
        "CL-11 values branches, hostile-press and scandal rows, troubled parents, founder risk.",
        [17, 20, 27, 32, 42, 61],
    ),
}
topic_of = {}
for name, (blurb, nums) in TOPICS.items():
    for n in nums:
        assert n not in topic_of, n
        topic_of[n] = name
adopted_nums = {n for n, _, _ in adopted}
missing = [n for n in all_rulings if n not in adopted_nums and n not in topic_of]
assert not missing, f"rulings with no topic: {missing}"

for name, (blurb, nums) in TOPICS.items():
    body = f"# Common Law topic file: {name}\n\n"
    body += NOTE.format(
        f"{blurb} Ruling text is copied unchanged from the published Common Law "
        "(version 2026-10-18.2). Which ruling goes in which topic file is the packager's guess."
    )
    for n in nums:
        body += unescape(all_rulings[n][1]) + "\n"
    (out / "common_law_topics" / f"{name}.md").write_text(body, encoding="utf-8")

# ---- index --------------------------------------------------------------
SKILL_MAX = 83  # the v2 skill refers to rulings CL-1 .. CL-83
idx = "# Common Law index\n\n"
idx += NOTE.format(
    "One line per ruling. Fetch the full text from the named file before citing a ruling. "
    f"The published Common Law stops at CL-{PUBLIC_MAX}; CL-{PUBLIC_MAX + 1} to CL-{SKILL_MAX} "
    "exist in the owner's private copy and are NOT in this package. Do not guess their content: "
    "treat a situation one of them might cover as having no precedent."
)
for n in range(1, SKILL_MAX + 1):
    if n in all_rulings:
        title, _, status = all_rulings[n]
        title = unescape(title)
        short = re.sub(r"\s*\[(Adopted|Proposed)[^\]]*\]\s*$", "", title).strip()
        if short.startswith("[Struck"):
            status = "Struck"
        elif "Superseded" in all_rulings[n][1][:400]:
            status = status + ", superseded"
        if n in adopted_nums:
            where = "common_law_core.md"
        else:
            where = f"common_law_topics/{topic_of[n]}.md"
        idx += f"- CL-{n}: {short} — {status} — `{where}`\n"
    else:
        idx += f"- CL-{n}: (not in the published Common Law; text unavailable) — Missing — none\n"
(out / "common_law_index.md").write_text(idx, encoding="utf-8")

# ---- proposed folder README ---------------------------------------------
(out / "common_law_proposed" / "README.md").write_text(
    """# Proposed rulings added since the freeze

> **Packaging note (prototype).** This README is reconstructed from the v2 skill's description
> of the bar; the owner's original README was not published.

Each run that produces new rulings writes ONE new file here, named
`<YYYY-MM-DD>_<run-label>.md`. Never edit or delete an existing file in this folder.

## The bar for a new ruling

A candidate becomes a Proposed ruling only if all of these hold:

1. No existing ruling covers it (search `common_law_index.md` and every file in this folder first).
2. It moved a headline mean by more than about 10%.
3. Another grant could plausibly raise the same question.
4. At most three new rulings per run.

A candidate that merely refines an existing ruling goes in the grant report as a one-line note,
not a new number.

## Numbering

The frozen Common Law ends at CL-83 (this package holds the text of CL-1 to CL-62 only).
New rulings take the next free number above 83, checking every file in this folder.

## Format

Use the template in Part I of `common_law_core.md`. State rulings generally: no grant names,
applicant details, people, funders or forecast results.

## Sending rulings upstream

Files here stay on the user's machine. Offer them to the user at the end of the run; the user
decides whether to send them to the Common Law's owner.
""",
    encoding="utf-8",
)

# ---- PERCYs -------------------------------------------------------------
percy = subprocess.run(
    ["pandoc", "-f", "docx", "-t", "gfm", "--wrap=none", percy_docx],
    check=True, capture_output=True, text=True,
).stdout
percy = unescape(percy)
percy = re.sub(r"(?m)^(\d)\\\. ", r"\1. ", percy)
percy = percy.replace("\u0394" + chr(92) * 2 + "E", "\u0394_E")
percy = re.sub(r"(?m)^(PERCYs \(v3\.7, compact\).*)$", r"# \1", percy, count=1)
percy = re.sub(r"(?m)^(\d)\. (The formula|Counted elite classes \(E\)|Named decision-makers \(M\)|"
               r"Kinds of claim|Rules that most often change the answer|Worked examples.*)$",
               r"## \1. \2", percy)
# pandoc emits an empty header row above each table; drop it so the real header row leads
percy = re.sub(r"(?m)^\|[ |]+\|\n(\|[-|]+\|\n)(\|.*\|\n)", r"\2\1", percy)
(out / "PERCYs_v3.7_compact.md").write_text(percy, encoding="utf-8")

# ---- milestones ---------------------------------------------------------
wb = openpyxl.load_workbook(xlsx)
ws = wb["All entries"]
mult = {}
for r in range(3, 12):
    mult[ws.cell(r, 1).value] = ws.cell(r, 5).value
rows = []
for r in range(16, ws.max_row + 1):
    cat, entry, who, when, val, _, _, override = [ws.cell(r, c).value for c in range(1, 9)]
    if not cat:
        continue
    base = override if override not in (None, "") else val
    rows.append((cat, entry, who, when, base * mult[cat]))
notes = [(a, b) for a, b in wb["Notes"].iter_rows(values_only=True) if a]

md = "# Milestone weights (Canonical)\n\n"
md += NOTE.format(
    "Converted from the published `autograntor_milestones.xlsx` (sheet 'All entries'), values "
    "unchanged; every category multiplier in the published file is 1. To use different weights, "
    "edit the Value column here. Values are utility points; Plan A = 1,000,000."
)
md += f"{len(rows)} entries. Entries overlap and must never be summed (CL-5).\n\n"
cur = None
for cat, entry, who, when, val in rows:
    if cat != cur:
        cur = cat
        md += f"\n## {cat}\n\n| Entry | Who / status | When | Value |\n|---|---|---|---:|\n"
    cell = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    v = f"{val:,.0f}" if float(val).is_integer() else f"{val:,}"
    md += f"| {cell(entry)} | {cell(who)} | {cell(when)} | {v} |\n"
md += "\n## Notes from the spreadsheet\n\n"
for a, b in notes:
    md += f"- **{a}.** {b}\n"
(out / "milestones_weights.md").write_text(md, encoding="utf-8")

(out / "milestones_added.md").write_text(
    """# Added milestones

> **Packaging note (prototype).** The owner's list of added milestones was not published, so both
> sections start empty. The Common Law refers to at least one Proposed milestone that is missing
> here ("member of Congress champion", CL-51); price such an item under CL-10 and say so.

## Approved

(none in this package)

## Proposed

(none in this package; append new Proposed milestones below this line)
""",
    encoding="utf-8",
)

print(f"adopted {len(adopted)}, proposed {len(proposed)}, public max CL-{PUBLIC_MAX}, "
      f"milestones {len(rows)}")
