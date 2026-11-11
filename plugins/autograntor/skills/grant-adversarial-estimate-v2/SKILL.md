---
name: "grant-adversarial-estimate-v2"
description: "Score a grant in Autograntor utility units with a structural pre-pass, two estimators, an adaptive critique round and a judge. Use instead of grant-adversarial-estimate: the coordinator stages the bundled docs locally, ledgers go through simulate.py, Proposed rulings go to per-run files. Self-contained prototype packaging: no Claude Project needed."
---

# Adversarial grant estimate (v2)

> **Prototype packaging.** This copy of the skill is self-contained: the standard documents ship in the `docs/` folder next to this file instead of living in a Claude Project. Three things in `docs/` are not the owner's originals, and every report must say so in its version line: (1) `simulate.py` and `ledger_template.csv` are reconstructions; (2) the Common Law files are split from the published version 2026-10-18.2, which ends at CL-62, so CL-63 to CL-83 are missing; (3) `milestones_added.md` is empty. See the repository README for details.

Use when the user wants a grant (or several grant sizes) scored on their utility scale (Plan A-style US–China pause treaty = 1,000,000). This version replaces `grant-adversarial-estimate`. Changes from v1: no per-grant inputs file (the coordinator stages the standard documents once per session and subagents read local copies); a cheap structural pre-pass that fixes the facts and the no-grant world before the estimators start; a shared ledger format and simulator; a fixed prompt layout with the standard documents first; the Common Law split into an always-read core, a one-line index and topic files; a critique round only when the estimators diverge, and no rebuttal round; Proposed rulings written to one small file per run; call budgets for every agent.

## Cost model and call budgets

Measured on past runs: each model call re-reads the whole conversation so far, and the fixed part of that context (the harness's own instructions and tool list) is large, so **the cost of a run is roughly proportional to the number of model calls, not to the size of the documents**. Output tokens are the other large item. So every agent works to a call budget and the rules below. These are rules against waste, not a cap on judgment: a fact-check on a row that moves the mean by more than ~10%, or a second simulation pass after the first one shows a problem, is never skipped to stay within budget. Each agent reports its call count in its reply, and the report's cost table shows calls per agent next to tokens.

Rules for every subagent:
- Read all the standard documents you need in **one step**, as parallel Read calls, before doing anything else; read the brief and application in the same step or the next one.
- **Never re-read a file that is already in your context.** If you need a number from a document you have read, find it in your context.
- Do web research in batches: several searches in one step, then several fetches in one step.
- Write each output file **once**, complete, with a single Write call; do not build it up over many Edit calls.
- Run `simulate.py` on your ledger at most three times (first run, one revision, one final check). Fix several rows per revision, not one per run.
- Do not narrate between tool calls; a step that only contains commentary is a wasted call.
- **Never poll in a loop.** A tool that returns "still running" gets at most three further checks, spaced out; after that use whatever partial result is available, say so, and move on.

Targets (calls, including reads): pre-pass ~15 for a listing-only grant and ~30 for a Commons grant with transcripts; each estimator ~25; each critique ~6; judge ~25; coordinator ~30 for the whole run. An agent that expects to exceed its target by half says why in its reply.

Rules for the coordinator: issue parallel tool calls wherever steps are independent (all staging Writes in one step, both estimators in one step, both critiques in one step, the verification checks in one Bash call); do not re-read staged files; one grant per session, since a longer conversation makes every later call dearer.

## External tools: FutureSearch and GitHub

**FutureSearch.** Submit all questions in one step, then check progress at most three times, at least a few minutes apart (use the wait or monitor facility the session offers rather than repeated status calls). If the session has no FutureSearch tools, skip FutureSearch entirely: record each question in the brief as "FutureSearch not connected" and say so in the report. If a task has not completed by the third check, fetch whatever `futuresearch_results` returns for it; if that is empty, record the question as "not resolved in time" in the brief and continue. The widget or status may never show "completed" even when results exist, so always try the results download before giving up. Never spend more than about six calls in total on FutureSearch.

**GitHub.** The GitHub API is often blocked from the sandbox; do not retry it or work around it. Use, in this order: (1) `git ls-remote --heads --tags <repo url>` for the branch list, and `git clone --bare --filter=blob:none` (or a shallow clone) when commit dates are needed, since plain git over HTTPS works; (2) `WebFetch` of the organisation's GitHub page (`github.com/<org>?tab=repositories`) to list **every repository in the organisation**, not only the one the application names, because side repositories (a hiring take-home, a tooling repo) are evidence about activity; (3) `WebFetch` of a repository's commits page for the latest commit date on each branch. Report the date of the latest commit on any branch of any repo in the org.

## The standard documents

These ship with this skill, in the `docs/` folder next to this SKILL.md (the skill's base directory, shown when the skill loads). The coordinator copies them once per session to `grant_eval/_docs/` (see Setup) and subagents read those copies with the Read tool. Never reconstruct weights or rulings from memory. If the `docs/` folder is missing or incomplete, stop and tell the user.

**Always read, in this order, in full:**
1. `common_law_core.md` — Part I (how to use the Common Law) and every Adopted ruling (CL-1 to 13, 15, 33, 62).
2. `common_law_index.md` — one line per ruling CL-1 to CL-83 with its topic file. This is how agents find precedents without loading every ruling. CL-63 to CL-83 are marked Missing: their text is not in this package, so never cite, apply or guess them; a situation one of them might cover is treated as having no precedent.
3. Every file in `common_law_proposed/` (read `README.md` there first) — rulings added since the freeze, in full.
4. `milestones_weights.md` — the Canonical milestone weights.
5. `milestones_added.md` — Approved and Proposed milestones.
6. `simulate.py` and `ledger_template.csv` — the ledger format and simulator (`python3 simulate.py --help` gives the column definitions and the group definitions).

**Read when relevant (the coordinator names which in the grant block; agents may add others):**
- `common_law_topics/method-and-programs.md` — CL-16, 18, 55 (simulation and post-2030 share; every grant), CL-19, 31 (venues, programs that die without the grant).
- `common_law_topics/money-and-funders.md` — pending or outside money, funging, runway, absorptive capacity, refunds, unrestricted money.
- `common_law_topics/expansion-and-hiring.md` — new hires, contractors, grants above the ask, the marginal factor, people charges.
- `common_law_topics/media-and-persuasion.md` — with `PERCYs_v3.7_compact.md`, for any media, audience, creator, game or campaign rows.
- `common_law_topics/policy-and-laws.md` — advocacy and policy orgs, law rows, c3/c4, electoral work, non-US actors.
- `common_law_topics/reputation-and-values.md` — CL-11 values questions, hostile-press or scandal rows, conflicts of interest, troubled parents, withheld plans.

Before citing any ruling not in the core file, an agent fetches its full text from its topic file (the index names it); citing from the index line alone is not allowed. The published Common Law (version 2026-10-18.2) is the source these files were split from; it is not read during runs.

Order of authority: the user's instructions in the current prompt, then Adopted rulings, then Proposed rulings, then the agents' own judgment. Cite rulings by number. When an agent disagrees with a ruling, it applies it anyway and reports the affected rows recomputed under its alternative.

## Setup — stage the standard documents once per session (coordinator)

Before the first subagent starts, the coordinator copies the skill's `docs/` folder to `grant_eval/_docs/` in the working directory. Steps:
1. Copy the whole folder in one Bash call: `mkdir -p grant_eval && cp -r "<skill base directory>/docs" grant_eval/_docs`. If `grant_eval/_docs/` already exists from an earlier step in this session, do not overwrite it (it may hold this session's new files in `common_law_proposed/`).
2. Verify the copy with one Python check in the same or the next Bash call, and paste its output into the run log: every `### CL-<n>` heading for n in 1..62 appears exactly once across `common_law_core.md` and `common_law_topics/*.md` (match the pattern `^### CL-[0-9]+`, which skips the ruling template in Part I); `common_law_index.md` has 83 `- CL-` lines; `python3 grant_eval/_docs/simulate.py --template` runs; and `diff -r` between the skill's `docs/` and `grant_eval/_docs/` reports no differences. If any check fails, delete the copy and copy again.
3. If the user keeps their own rulings from earlier runs (files they attach, or a folder they name), copy those files into `grant_eval/_docs/common_law_proposed/` now, unchanged.
4. Record in the run log which `common_law_proposed/` files were staged; the report's version line names the newest.

**Never correct, tidy or "fix typos" in a staged copy, and never delegate the staging to a subagent.** Subagents never edit the staged copies and never rebuild them; if a subagent cannot find a file under `grant_eval/_docs/`, it stops and says so rather than reconstructing it. Grant-specific material (the application, Commons documents) is still read by the pre-pass from its source.

## Independence

Estimators A and B must not read each other's files, transcripts or replies before the critique round, and no subagent reads another subagent's transcript at any point: the only shared inputs are the staged documents, `brief.md`, and `grant_eval/<org>/source/`. Every subagent prompt states this. An estimator that discovers another agent's reasoning by accident says so in its reply.

## Prompt layout for every subagent

Write each subagent prompt in this fixed order, so the shared part is identical across agents and runs:

1. **Standard documents block** (identical text every time): the always-read list and the topic-file list above, prefixed with the local root `grant_eval/_docs/`, with the instruction to read the always-read files in one step with the Read tool, the call-budget rules and the agent's target, the external-tools rules, the independence rule, and the one-paragraph description of the ledger CSV and `simulate.py` usage.
2. **Role block**: pre-pass / estimator / critic / judge instructions (below).
3. **Grant block**: the organisation, grant sizes, the grant's source class (Commons with transcripts and evaluator material, or listing-only), which topic files apply (the pre-pass recommends them; method-and-programs always), the path to `grant_eval/<org>/brief.md`, and (for the pre-pass only) where the raw material is.

Keep all working files in `grant_eval/<org>/` in the working directory.

## Ledger format and simulation

Every estimate and the judge's verdict carry a ledger CSV in the `ledger_template.csv` format (one row per consequence, with `size`, `kind`, `weight`/`p1`/`p0` for events, `ev`/`sigma` for continuous and charge rows, `pivotal`, `exec`, `exec_mode`, `group`, `branch`/`branch_val`, `post2030`). Agents do not write their own Monte Carlo code. They run:

```
python3 grant_eval/_docs/simulate.py <X>_ledger.csv --branches '{...}' --corr '{...}' --exec '{...}'
```

and paste the output into their report. The analytic mean is the headline; quantiles are descriptive (CL-16). Values questions (CL-11) are `branch` columns with their weights in `--branches` (the corners, one per combination of answers, and the fixed-weight spread come out automatically; CL-74, the ruling that defines them, is not in this package, so cite the simulator's output, not CL-74). The correlated execution factor goes in `--exec` and applies only to program rows, never charges (CL-37, CL-40).

Every estimate states, in one line near the top, the exact `--branches`, `--corr` and `--exec` arguments it used, so the coordinator and judge can rerun it and feed `--diff`.

Two columns matter for comparability and are mandatory:
- **`group`**: every row carries one of the fixed categories defined in `simulate.py --help`. **File by the causal path, not by sign or branch**: a harm-branch mirror of a positive row takes the same group as that row (a "harness is net capabilities" row goes in `uptake` with "harness is used"; a "retrospective normalises automated R&D" row goes wherever the retrospective's positive row went). `values` is only for rows that exist in no causal path (pure signalling or trust-norm rows); `exposure` is only for press, scandal, partisan-coding and incident rows. Independent estimators never share row names, so `--diff` and the agreement test compare group totals.
- **`exec_mode`** on event rows with an execution factor: `credit` when the no-grant probability is the chance the same work happens anyway (the whole increment scales); `p1` when p0 is a base rate from other causes that does not depend on whether this team executes (only the with-grant probability scales). State the choice once in the estimate; it changes the mean.

An overlap row that corrects program rows carries the same `exec` group and `branch` as the rows it corrects; the "never multiply charges" rule applies to money, people and exposure charges.

`simulate.py --diff A.csv B.csv --size <s> --branches-a '{...}' --exec-a '{...}' --branches-b '{...}' --exec-b '{...}'` prints each ledger's headline mean under its own weights and factor, the group-total comparison the agreement test uses, then row-level differences by name. Always pass both ledgers' own settings; without them the diff compares raw EVs and misleads.

## Inputs (ask for anything missing)
- Where the proposal, interview notes and evaluator material are (Lightcone Commons via the access skill, or attached files, or a grantmaking.ai listing).
- Grant sizes to score (default: whatever the user names; otherwise $250K / $1M / $3M).
- Optional facts from the applicant: spending by year, what each grant size buys, c3 vs c4.
- For a platform that has already given the applicant money in an earlier round: whether that money is in both worlds (the default under CL-8/CL-43 for disbursed money) and whether the grant is scored as funding the plan in full with no discount for time already elapsed. Ask once, before the pre-pass, if the listing shows an earlier award.

## Step 0 — Structural pre-pass (one `sonnet` agent)
Start one Agent subagent (general-purpose, model `sonnet`) before the estimators. It is the only agent that reads the raw Commons material in full, and the only one that runs web searches for funding facts and FutureSearch. Its job is the structure of the grant, not its value: it never estimates utility. It always runs, but its scope depends on the source class:
- **Commons grant** (transcripts, evaluator notes, comment threads): all eleven sections below; target ~30 calls.
- **Listing-only grant** (an application page and nothing else, e.g. grantmaking.ai): sections 1, 2, 3, 7, 8, 9, 10 and 11 only, with section 2 reduced to what is public; skip the evaluator table and quotes unless such material exists; target ~15 calls. The web checks and FutureSearch are kept, because they are what the estimators would otherwise each do separately and differently.

Role block for the pre-pass:
- Read the always-read documents and the index from `grant_eval/_docs/` in one step, then all raw material for this grant: the application, interview transcripts, evaluator notes and comment threads, shared notes. Submit the FutureSearch questions early, in the same step as the first web searches, so they run while you read; follow the FutureSearch and GitHub rules above.
- Write `grant_eval/<org>/brief.md` with these sections, each short and sourced (document name and location for Commons material; URL for the web):
  1. **The organisation and the ask.** What it does, team size and seniority, what each grant size buys in the applicant's own words, and the plan year.
  2. **Funding facts.** Cash and runway, revenue, latest Form 990 figures (revenue, expenses, net assets), grants from each major funder by year with sources, grants pending or intended elsewhere, matching pledges, debts to the platform or evaluators, and any earlier award from the same platform. Flag anything an AI-written evaluation asserts without a source.
  3. **The no-grant world under CL-8, CL-43 and CL-62.** Money that stays in both worlds, money that is pending (CL-14/CL-34) with your probability and the reason, and what the organisation does without the grant.
  4. **Absorptive capacity.** The applicant's own statements about hiring rate and bottlenecks, quoted verbatim; the share of each grant size that can be spent in the plan year under CL-35, and what the rest becomes.
  5. **Evaluator views (CL-12).** A table: evaluator, position or rank, amount they fund to, conflict of interest, one-line view. Mark AI-written evaluations as such.
  6. **Verbatim quotes that matter.** Up to 15 short quotes from transcripts or notes that an estimator would otherwise need the full transcript to find (hiring caps, minimum sizes, what they would cut first, admissions of risk).
  7. **Facts checked on the web.** Each with a source. Include track-record items (past outputs, press, audits of reach claims under CL-30) and, for code projects, every repository in the organisation with its latest commit date.
  8. **Values questions (CL-11).** The contested values questions this grant raises, stated neutrally, with the rows each one would affect. Do not pick an answer.
  9. **FutureSearch.** At most four forecast questions (at most two for a listing-only grant), chosen for what moves the structure: the main other funder's next award (P and size), one key base rate the ledger will need, and nothing the estimators could settle by reading. Report each result with its session id, or "not resolved in time".
  10. **Open gaps.** Facts you could not establish, for the estimators to treat as uncertain and the report to list as open questions.
  11. **Topic files and rulings likely to apply.** Which `common_law_topics` files this grant needs, and the index lines of the rulings most likely to matter.
- Save the application text (and any Commons document an estimator is likely to need in full) as files under `grant_eval/<org>/source/`, so the estimators can read them locally.
- Keep the brief under about 3,000 words (about 1,500 for a listing-only grant). Quotes count toward that; prose does not need to.
- Reply with the no-grant world in three sentences, the absorptive-capacity shares by size, the topic files recommended, and your call count.

The coordinator reads the brief before continuing. If section 3 or 4 is missing something the user can answer, ask once now rather than letting the estimators guess.

## Step 1 — Two independent estimates (run in parallel)
Start two Agent subagents (general-purpose), Estimator A with model `opus`, Estimator B with model `fable`, with identical prompts in the layout above, launched in the same step. Neither sees the other. Both get `brief.md` and the application from `grant_eval/<org>/source/`; they do not get the transcripts or evaluator notes pre-loaded. If an estimator needs a Commons document the pre-pass did not save, it asks the coordinator (in its reply) rather than failing silently; the coordinator fetches it and continues the agent.

Role block for estimators:
- Work independently; don't look for other forecasts of this grant and don't read any other agent's files or transcript. Read the always-read documents, the topic files named in the grant block, `brief.md` and the application in one step. Use the index to find any other ruling you need and fetch its full text from its topic file before citing it. Take the brief's funding facts, no-grant world, absorptive-capacity shares and FutureSearch results as given; if you think one is wrong, say so in a flagged line and price it the brief's way for the headline, your way as a sensitivity. Web search is for facts about the ledger rows, not for facts the brief already settles.
- Question: expected utility of each grant size vs. not making the grant, at the listed weights, following the Common Law (especially CL-1 to CL-10). Cite rulings by number where you apply them.
- Required steps: (1) what each size buys; (2) org-level ledger for the org's whole next-year program (outcome | type per CL-5 | weight | P with the program | P without | contribution, plus the fraction attributable to next year's spending), scaled to each grant with an explicit marginal-vs-average factor; charges for follow-on resources (CL-4), overlap, and downside as separate signed lines; (3) scale-up and track-record checks (CL-9, CL-15; for a team with no budget beyond the grant, compare instead with the researcher-year band and the nearest large organisation's historical rate as a CL-6 upper bound); (4) the grant ledger as `<X>_ledger.csv` in the template format with `group` filled on every row per the filing rule and `exec_mode` stated for event rows, run through `simulate.py`, with the output and the exact arguments pasted in (mean, median, P10/P90, P(negative), post-2030 share per CL-18); (5) every values question from the brief's section 8 priced both ways as a `branch` (CL-11), plus any you add; (6) any situation the Common Law doesn't cover, with the call you made, and any ruling you disagree with, with the affected rows recomputed. Small research outputs get no separate first-run or "toy" quality factor on top of the execution factor (CL-37: no second dispersion on the same thing); CL-19's quality factor is for venue programmes.
- Output: `<X>_estimate.md` with the ledger tables and one line of reasoning per row (every row gets its line; keep narrative outside the tables short), plus `<X>_ledger.csv`, each written once; reply with the summary table (mean, median, P10, P90, P(negative), per $1M, % post-2030), the `simulate.py` arguments, the names of your three largest rows at $1M, and your call count.

## Step 2 — Decide whether a critique round is needed
The coordinator runs `simulate.py --diff A_ledger.csv B_ledger.csv --size <smallest common size>` **with each estimator's own `--branches-a/--exec-a` and `--branches-b/--exec-b`** (from their replies) and reads the output. The estimates **agree** when all of these hold at the $1M size (or the smallest size scored): the headline means are within 30% of the larger one's absolute value, or both are within 50 utility of zero (the diff prints this); the largest group is the same in both (the diff prints this); and no group total differs by more than 30% of the larger mean (the diff prints the count). Row names are not compared. If the only flagged groups look like filing differences (the same causal path in different groups), note that in the report but still run the critique; the filing rule exists to make this rare.

- **Agree:** skip to Step 3 with no critiques. Record in the report that the critique round was skipped and why.
- **Diverge:** continue both estimators with SendMessage in the same step. Each reads the other's estimate and ledger, runs `simulate.py --diff` with both settings, and writes `<X>_critique_of_<Y>.md` in one Write: the groups and rows that move the $1M mean most, what the other assumed, why it's wrong, what number to use instead, any misapplied Common Law ruling, then a one-line list of any smaller disagreements, plus anything the other did better. No self-revision and no rebuttal: the judge weighs the critiques against the estimates directly.

## Step 3 — One neutral judge
Start one fresh `fable` judge that made no estimate, with the same prompt layout. Point it at `brief.md`, both estimates and ledgers, and the critiques if any were written, with this role block:
- You made no estimate. Read the standard documents, the brief, both estimates, both ledgers and any critiques in one step. Run `simulate.py --diff` on the two ledgers with each estimator's own settings and identify every remaining difference, by group and then by row, that moves the $1M mean by more than ~10% (include the marginal-vs-average factor and the post-2030 discount). Where critiques exist, treat each critique as the strongest case against that estimate; where none exist, the estimates agree and your job is mainly to check them against the brief and the Common Law.
- Decide each difference: A's value, B's value, or your own, with one line of reasoning; judge evidence, not confidence, length or tone; no default midpoints. Apply the Common Law where it speaks to the dispute and cite the ruling (fetch full text from the topic file before citing). If you land outside the range of the two estimates, say so and show both alternatives.
- Web-check any factual claim that moves the result >10% and is not already sourced in the brief; batch the checks.
- Compare your P10–P90 with the spread of comparable outcomes; if yours is much narrower, justify it or widen it.
- Write `judge_ledger.csv` (with `group` on every row), run `simulate.py` for all sizes, and give mean, median, P10/P90, P(negative), the share of value from post-2030 effects, and up to 4 open questions only the grantmaker or applicant can answer (start from the brief's section 10).
- Candidate rulings: for each judgment call you think the Common Law should cover, first search `common_law_index.md` and the proposed folder for a ruling that already does; if one does, cite it instead. List as candidates only calls that no ruling covers, that moved a headline mean by more than ~10%, and that another grant could plausibly raise. At most three.
- Write `judge_verdict.md` once, with the ledger tables and one line per decision; keep narrative short. Reply with summary table, the three decisions that mattered most, open questions, candidate rulings, sources, the `simulate.py` arguments, and your call count.

## Step 4 — Common Law and milestone upkeep (coordinator)
- **Rulings.** Do not write to `common_law_core.md`, `common_law_index.md` or the topic files, in the staged copy or in the skill's own `docs/` folder. For the judge's candidate rulings that pass the bar in `common_law_proposed/README.md` (no existing ruling covers it; moved a headline mean by more than ~10%; reusable by other grants; at most three per run), find the next free number across the frozen file (CL-83) and the staged proposed folder, and write the rulings to a local file `grant_eval/_docs/common_law_proposed/<YYYY-MM-DD>_<run-label>.md` in the template from Part I of the core file. Never edit an existing file there. Keep rulings free of grant names, applicant details and forecast results. A candidate that merely refines an existing ruling goes in the report as a one-line note, not a new number. Send the new file to the user with the report and tell them two things: to reuse these rulings in a later session they attach the file (Setup step 3), and whether to send them to the Common Law's owner is their decision. Never submit rulings anywhere yourself.
- **Milestones.** New Proposed milestones go at the end of the Proposed section of the staged `grant_eval/_docs/milestones_added.md`: append with the Edit tool, and send the updated file to the user with the report.

## Step 5 — Report to the user (short)
- Version line: Common Law version used (published 2026-10-18.2, CL-1 to CL-62, plus the newest proposed file staged), and the statement that `simulate.py` is the prototype reconstruction (give its `--version`).
- Summary table per grant size: the judge's mean, median, P10/P90, per $1M, % of value from post-2030 effects.
- How the estimates moved: initial A vs B, whether the critique round ran (and why, quoting the group-total test), judge.
- The 3 decisions that mattered most and the facts verified (with sources).
- Rulings: any Proposed rulings applied, any new Proposed rulings written (file name), candidates rejected at the bar and why, and any disagreements with Adopted rulings (with the recomputed difference).
- Contested values questions priced both ways (CL-11), with the CL-74 corners from `simulate.py`.
- Open questions for the user or the applicant.
- **Cost.** The Agent tool results do not carry usage figures; take them from the session's own usage log (the same source the `explain-usage` route reads). A table per agent (coordinator, pre-pass, A, B, critiques if run, judge): model calls, uncached input, cache reads, cache writes, output; the totals; the source class; and whether the critique round ran. Say "not reported" for any figure the log does not supply.
- Note anything that looked off, including any brief fact an estimator flagged as wrong, any staging check that failed, and any agent that exceeded its call target by half (with its reason).

Save the report as `grant_eval/<org>/<Org>_grant_forecast_<date>.md`, send that file to the user, and send the judge's verdict too if the user wants detail.