import sys
src, dst = sys.argv[1:3]
s = open(src, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:70])
    s = s.replace(old, new)

DESC_OLD = "Use instead of grant-adversarial-estimate: the coordinator stages Project docs locally, ledgers go through simulate.py, Proposed rulings go to per-run files."
DESC_NEW = "Use instead of grant-adversarial-estimate: the coordinator stages the bundled docs locally, ledgers go through simulate.py, Proposed rulings go to per-run files. Self-contained prototype packaging: no Claude Project needed."
assert s.count(DESC_OLD) == 1
s = s.replace(DESC_OLD, DESC_NEW)

rep("# Adversarial grant estimate (v2)\n",
"""# Adversarial grant estimate (v2)

> **Prototype packaging.** This copy of the skill is self-contained: the standard documents ship in the `docs/` folder next to this file instead of living in a Claude Project. Three things in `docs/` are not the owner's originals, and every report must say so in its version line: (1) `simulate.py` and `ledger_template.csv` are reconstructions; (2) the Common Law files are split from the published version 2026-10-18.2, which ends at CL-62, so CL-63 to CL-83 are missing; (3) `milestones_added.md` is empty. See the repository README for details.
""")

rep("These live in the Autograntor Project. **Subagents cannot be relied on to have the Projects tool**, so only the coordinator reads from the Project; subagents read local copies in `grant_eval/_docs/` with the Read tool (see Setup). Never reconstruct weights or rulings from memory. If the session has no access to the Project, stop and ask the user to attach it.",
"These ship with this skill, in the `docs/` folder next to this SKILL.md (the skill's base directory, shown when the skill loads). The coordinator copies them once per session to `grant_eval/_docs/` (see Setup) and subagents read those copies with the Read tool. Never reconstruct weights or rulings from memory. If the `docs/` folder is missing or incomplete, stop and tell the user.")

rep("2. `common_law_index.md` — one line per ruling CL-1 to CL-83 with its topic file. This is how agents find precedents without loading every ruling.",
"2. `common_law_index.md` — one line per ruling CL-1 to CL-83 with its topic file. This is how agents find precedents without loading every ruling. CL-63 to CL-83 are marked Missing: their text is not in this package, so never cite, apply or guess them; a situation one of them might cover is treated as having no precedent.")

rep("The frozen original `claude/common_law.md` is the archival source of truth and is not read during runs.",
"The published Common Law (version 2026-10-18.2) is the source these files were split from; it is not read during runs.")

# ---- Setup section: replace from its heading to the Independence heading
a = s.index("## Setup — stage the standard documents once per session (coordinator)")
b = s.index("## Independence")
s = s[:a] + """## Setup — stage the standard documents once per session (coordinator)

Before the first subagent starts, the coordinator copies the skill's `docs/` folder to `grant_eval/_docs/` in the working directory. Steps:
1. Copy the whole folder in one Bash call: `mkdir -p grant_eval && cp -r "<skill base directory>/docs" grant_eval/_docs`. If `grant_eval/_docs/` already exists from an earlier step in this session, do not overwrite it (it may hold this session's new files in `common_law_proposed/`).
2. Verify the copy with one Python check in the same or the next Bash call, and paste its output into the run log: every `### CL-<n>` heading for n in 1..62 appears exactly once across `common_law_core.md` and `common_law_topics/*.md` (match the pattern `^### CL-[0-9]+`, which skips the ruling template in Part I); `common_law_index.md` has 83 `- CL-` lines; `python3 grant_eval/_docs/simulate.py --template` runs; and `diff -r` between the skill's `docs/` and `grant_eval/_docs/` reports no differences. If any check fails, delete the copy and copy again.
3. If the user keeps their own rulings from earlier runs (files they attach, or a folder they name), copy those files into `grant_eval/_docs/common_law_proposed/` now, unchanged.
4. Record in the run log which `common_law_proposed/` files were staged; the report's version line names the newest.

**Never correct, tidy or "fix typos" in a staged copy, and never delegate the staging to a subagent.** Subagents never edit the staged copies and never rebuild them; if a subagent cannot find a file under `grant_eval/_docs/`, it stops and says so rather than reconstructing it. Grant-specific material (the application, Commons documents) is still read by the pre-pass from its source.

""" + s[b:]

rep("If a task has not completed by the third check, fetch whatever `futuresearch_results` returns for it;",
    "If the session has no FutureSearch tools, skip FutureSearch entirely: record each question in the brief as \"FutureSearch not connected\" and say so in the report. If a task has not completed by the third check, fetch whatever `futuresearch_results` returns for it;")

rep("(CL-74 corners and fixed-weight spread come out automatically)",
    "(the corners, one per combination of answers, and the fixed-weight spread come out automatically; CL-74, the ruling that defines them, is not in this package, so cite the simulator's output, not CL-74)")

rep("- **Rulings.** Do not write to `claude/common_law.md`, `claude/common_law_core.md`, `claude/common_law_index.md` or the topic files. For the judge's candidate rulings that pass the bar in `common_law_proposed/README.md` (no existing ruling covers it; moved a headline mean by more than ~10%; reusable by other grants; at most three per run), find the next free number across the frozen file (CL-83) and the staged proposed folder, write the rulings to a local file `grant_eval/_docs/common_law_proposed/<YYYY-MM-DD>_<run-label>.md` in the template from Part I of the core file, and upload it with `project_write` (`local_path`) to `claude/common_law_proposed/<same name>`. Never edit an existing file there. Keep rulings free of grant names, applicant details and forecast results. A candidate that merely refines an existing ruling goes in the report as a one-line note, not a new number.",
    "- **Rulings.** Do not write to `common_law_core.md`, `common_law_index.md` or the topic files, in the staged copy or in the skill's own `docs/` folder. For the judge's candidate rulings that pass the bar in `common_law_proposed/README.md` (no existing ruling covers it; moved a headline mean by more than ~10%; reusable by other grants; at most three per run), find the next free number across the frozen file (CL-83) and the staged proposed folder, and write the rulings to a local file `grant_eval/_docs/common_law_proposed/<YYYY-MM-DD>_<run-label>.md` in the template from Part I of the core file. Never edit an existing file there. Keep rulings free of grant names, applicant details and forecast results. A candidate that merely refines an existing ruling goes in the report as a one-line note, not a new number. Send the new file to the user with the report and tell them two things: to reuse these rulings in a later session they attach the file (Setup step 3), and whether to send them to the Common Law's owner is their decision. Never submit rulings anywhere yourself.")

rep("- **Milestones.** New Proposed milestones still go at the end of the Proposed section of `milestones_added.md`: append to the staged local copy with the Edit tool and upload the whole file with `project_write` using `local_path` to `claude/milestones_added.md` (never re-type the file into a tool call).",
    "- **Milestones.** New Proposed milestones go at the end of the Proposed section of the staged `grant_eval/_docs/milestones_added.md`: append with the Edit tool, and send the updated file to the user with the report.")

rep("- Common Law version used (frozen version plus the newest proposed file staged).",
    "- Version line: Common Law version used (published 2026-10-18.2, CL-1 to CL-62, plus the newest proposed file staged), and the statement that `simulate.py` is the prototype reconstruction (give its `--version`).")

rep("Save the report to the Project as `claude/<Org>_grant_forecast_<date>.md` (upload with `local_path`) and send the judge's verdict if the user wants detail.",
    "Save the report as `grant_eval/<org>/<Org>_grant_forecast_<date>.md`, send that file to the user, and send the judge's verdict too if the user wants detail.")

open(dst, "w", encoding="utf-8").write(s)
for bad in ("project_read", "project_write", "project_info", "Projects tool", "claude/"):
    print(bad, s.count(bad))
