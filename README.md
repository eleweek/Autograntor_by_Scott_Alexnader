# Autograntor plugin (unofficial prototype)

A self-contained packaging of the `grant-adversarial-estimate-v2` skill from Scott Alexander's
[Towards The Autograntor](https://www.lesswrong.com/posts/Sfkv6JF2ozmAkggKu), so that it can be
installed from one place and run without a private Claude Project.

**This is a prototype by a third party, not an official release.** The Common Law, the milestone
weights, the PERCYs module and the skill are Scott Alexander's work. Some pieces the skill needs
were never published; here they are reconstructed or left empty, and are marked as such below.
Results from this package are **not comparable** with the owner's own runs until the original
files are swapped in.

## What is in the package

| File (under `plugins/autograntor/skills/grant-adversarial-estimate-v2/`) | Status |
|---|---|
| `SKILL.md` | The published v2 skill with targeted edits (see "Changes to the skill"). |
| `docs/common_law_core.md` | **Converted.** Part I and the 16 Adopted rulings from the published Common Law, version 2026-10-18.2. Ruling text unchanged. |
| `docs/common_law_topics/*.md` | **Converted.** The 46 Proposed rulings, text unchanged. **Which ruling sits in which topic file is a guess.** |
| `docs/common_law_index.md` | **Rebuilt.** One line per ruling, CL-1 to CL-83. |
| `docs/common_law_proposed/README.md` | **Reconstructed** from the skill's description of the bar for new rulings. |
| `docs/milestones_weights.md` | **Converted** from the published spreadsheet; all 85 values unchanged. |
| `docs/milestones_added.md` | **Empty placeholder.** The owner's added milestones were not published. |
| `docs/PERCYs_v3.7_compact.md` | **Converted** from the published document; text unchanged. |
| `docs/simulate.py`, `docs/ledger_template.csv` | **Reconstructed.** Not the original. See "The simulator". |

`originals/` holds the four published files exactly as downloaded, for comparison.

### Known gaps

1. **CL-63 to CL-83 are missing.** The v2 skill refers to 83 rulings; the published Common Law
   stops at CL-62. The index marks the missing ones and the skill is told never to cite or guess
   them. One of them (CL-74) defines how values-question "corners" are reported.
2. **`simulate.py` is a reconstruction** (next section).
3. **`milestones_added.md` is empty.** The Common Law mentions at least one Proposed milestone
   ("member of Congress champion", CL-51) that is not in the published weights.
4. **Run end to end once only** (one grant, 2026-11-11; see `NOTES_FOR_SCOTT.md`). The run was driven from the repository folder, not from an installed plugin, so the install step itself is untested.

### To replace placeholders with the originals

Drop the owner's files over the ones in `docs/`, keeping the file names: `simulate.py`,
`ledger_template.csv`, `common_law_core.md`, `common_law_index.md`, `common_law_topics/*.md`,
`common_law_proposed/*`, `milestones_weights.md`, `milestones_added.md`. Then, in `SKILL.md`,
remove the "Prototype packaging" note, the two sentences about missing CL-63 to CL-83 and CL-74,
and change the ruling count in the Setup check from 62 back to 83.

## Install

**Claude app:** Customize > Plugins > Add > Add marketplace > Add from a repository, and enter this
repository's address. Then install `autograntor`.

**Claude Code:**

```
/plugin marketplace add <owner>/<repo>
/plugin install autograntor@autograntor-prototype
```

**Without a repository:** zip the `plugins/autograntor` folder and upload it as a custom plugin, or
in Claude Code run `claude --plugin-dir ./plugins/autograntor`.

Then ask, for example: *"Use the grant-adversarial-estimate-v2 skill to score [grant name] at
$200K. The application is at [link or attached file]."* The skill uses subagents (one Sonnet
pre-pass, one Opus and one Fable estimator, a Fable judge), so a run takes a while. FutureSearch
is optional; without the connector the skill skips it and says so.

## Changes to the skill

`originals/SKILL_v2_as_published.md` is the published text; `tools/edit_skill.py` applies every
change, so the difference is reviewable. In short:

- **Documents come from the skill's own `docs/` folder**, copied to the working directory with one
  command, instead of being read from a Claude Project file by file.
- **New Proposed rulings and milestones are written locally and handed to the user**, not uploaded
  to a Project. The user can attach them in a later session to reuse them. Nothing is submitted
  anywhere automatically.
- **The report is saved locally and sent to the user.**
- **FutureSearch is skipped cleanly** when the connector is absent.
- **Notes about the gaps above**, and a version line in every report stating that the simulator is
  the reconstruction.

Everything else (the pre-pass, estimators, critique rule, judge, call budgets) is untouched.

## The simulator

`simulate.py` takes a ledger (a CSV with one row per consequence of the grant) and reports the
mean, median, P10/P90, P(negative), post-2030 share, group totals and values-branch corners. A
`--diff` mode compares two ledgers and applies the skill's agreement test. Run
`python3 simulate.py --help` for the column definitions.

Taken from the published sources:

- An event row is worth weight × (P with grant − P without). (CL-1, CL-2)
- Quantiles are of realised value: simulate whether each outcome happens and credit it at
  weight × (1 − P0/P1) when it does; the mean still equals the row-by-row expected value. (CL-16)
- Optional pivotal/diffuse split per row, which changes the spread and not the mean. (CL-55)
- A correlated execution factor scales program rows and never charges. (CL-37, CL-40)
- Values questions change only the rows that depend on them. (CL-11, CL-17)
- The agreement test thresholds: means within 30% (or both within 50 of zero), same largest group,
  no group differing by more than 30% of the larger mean. (v2 skill, Step 2)

**Guesses**, where the sources are silent. These are the places the original most likely differs:

| Convention | What this version does |
|---|---|
| The fixed list of `group` categories | The skill names only `uptake`, `values` and `exposure`. The other nine are invented here. |
| `--corr` | Keyed by group name (or `*`): rows in that group share one common factor. |
| `--exec` format | A list of `[probability, multiplier]` states, a lognormal, or a constant. |
| `exec_mode` | `credit` multiplies the increment (P1 − P0); `p1` multiplies P1 only. |
| "Fixed-weight spread" (CL-74, unpublished) | In each simulated world, value is the weighted average across the branch answers. Each corner is also reported separately. |
| Post-2030 share | Sum of (row mean × the row's `post2030` share) ÷ total mean. |
| Rows where the grant lowers a probability | Credited when the outcome is averted, mirroring CL-16. |
| Costs that exist only if an event happens | Optional `given` column: the row counts only in worlds where the named event row happens; the mean is unchanged. Not described in the skill. |

### Tests

```
python3 tests/test_simulate.py
```

Fifteen tests with numbers that can be checked by hand (for example CL-2's own example: a law
moved from 10% to 12% earns 2% of its weight). They show the arithmetic does what this README
says. They do not show it matches the original simulator.

The document conversion was checked separately: all 62 published rulings, the PERCYs text and the
85 milestone values match the originals word for word. `tools/build_docs.py` regenerates `docs/`
from the published files.

## Open questions for the owner

1. Should this be public, and under whose account?
2. Where should Proposed rulings from other people's runs go: nowhere, an issue, or a pull request?
3. Are outside contributions to the Common Law wanted at all?
4. Should users be able to layer their own weights and rulings on top, and how should reports label
   results produced that way?
5. Licence for the Common Law, weights and skill. None is stated here; all rights remain with the
   author until he says otherwise.
