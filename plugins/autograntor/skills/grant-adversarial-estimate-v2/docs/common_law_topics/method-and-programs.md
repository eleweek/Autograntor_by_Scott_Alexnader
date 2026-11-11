# Common Law topic file: method-and-programs

> **Packaging note (prototype, not part of the Common Law).** Simulation and spread, post-2030 share, attribution across years, lags and dated windows, venues, and programs that die without the grant. Ruling text is copied unchanged from the published Common Law (version 2026-10-18.2). Which ruling goes in which topic file is the packager's guess.

### CL-16: Report the spread of realised 2030 value, not of expectations [Proposed 2026-10-16, by Claude]

**Rule:** P10/median/P90 are quantiles of the grant's value as it will look from 2030 (CL-1, CL-7): simulate whether each outcome happens, and when it does, credit it at weight × (1 − P(it would have happened anyway)). Do not simulate noise around row expectations; that compresses the right tail. The mean must still equal the row-by-row EV. **Why:** The human user asked for P10 and P90 over value judged in 2030; a lumpy outcome (a lab practice visibly changed, a corpus recognised) is realised at several times its expected value or at zero.

### CL-18: What counts as "post-2030" under CL-7 [Proposed 2026-10-16, by Claude]

**Rule:** The post-2030 share means value from activity that occurs after 2030 (an organization still operating in 2031+, the post-2030 portion of a tail outcome), discounted for TAI. Unit prices on the weights list (researcher-year, fellowship, lab point) are already values judged from 2030 under the stated worldview, so the downstream of a pre-2030 output is not split again into pre- and post-2030 parts and discounted a second time. Report the downstream-inclusive share as a secondary figure. **Why:** Splitting and then discounting counts the worldview twice, and without a fixed definition the reported share moves a lot on reporting choices alone.

### CL-19: Hosted vs self-run programs at a venue or incubator [Proposed 2026-10-16, by Claude]

**Rule:** A program run by another organization and hosted at the grantee's venue gets only a venue/ops share of its counterfactual value, because it would mostly run elsewhere, worse or at higher cost (≈20% unless there is evidence otherwise). A program the grantee runs itself with the grant's money gets full counterfactual credit (CL-3) × P(it actually runs) × a first-run quality factor (≈0.7). **Why:** Without this, venue grants either claim hosted programs in full (overcounting) or apply arbitrary "shares" to their own programs (a credit pie).

### CL-31: Grant-caused continuation of a program that dies without the grant [Proposed 2026-10-17, by Claude]

**Rule:** When the no-grant world is "the program dies", credit continuation years the grant makes possible at stated per-year probabilities (CL-23 chain), valued on the same per-cohort ledger as the funded year (quality, P(run), downsides and mixture included), with a crowding decay (CL-6) and the CL-4 money charge for each year's fundraising (CL-28). A later round of the same funder is ordinary fundraising in the grant world (CL-8 forbids it only in the no-grant world), including a within-year top-up for a partial grant, credited net of the money charge. Always report the share of value from the funded year's spending; a continuation share above ~40% should trigger a re-check of the per-year probabilities. **Why:** Without this, estimators either valued continuation years at an undiscounted gross figure or ignored partial-grant top-ups entirely; both distort the ratio between grant sizes.

### CL-46: Attributing a multi-year outcome to one year's spending [Proposed 2026-10-18, by Claude]

**Rule:** When a grant funds one year of a multi-year campaign, attribute to that year the share f of the critical-path effort that falls in it (drafting, sponsor recruitment, session timing), stated per row, with the shares across the campaign's years summing to at most one. Do not attribute pro-rata by budget, do not credit the whole outcome to the funded year, and do not use a higher f for a longer-horizon outcome than for a nearer one. **Why:** Without a stated share, one year of an advocacy organisation is credited with whole laws, which fails CL-9 when multiplied over the years it actually takes.

### CL-52: Recruit-on-funding lags, dated windows and part-time roles [Proposed 2026-10-17, by Claude]

**Rule:**

- **Lag.** If funded activity starts only after recruitment, shift it by the stated lag (default 2–3 months from disbursement).

- **Dated windows.** Price rows tied to a dated window (an election, a summit) on the post-lag share of the critical-path work in that window, not the calendar share (CL-46). Don't give extra window credit to money above the ask that arrives after the window.

- **Part-time roles.** Value a 0.5-FTE relationship role at ≈0.5 of the full-time increment if it spans a dated window, ≈0.4 otherwise.

**Why:** Without a rule, estimators invent their own treatment, and rows tied to dated windows can differ by a large factor.

### CL-55: Amendment to CL-16, pivotal vs diffuse credit for traceable rows [Proposed 2026-10-17, by Claude]

**Rule:** When a 2030 evaluator can plausibly see whether the grant was on the causal path (a named legislator the hire briefed; a campaign team it met; a report it fed), simulate pivotal worlds (large credit, rare) and diffuse worlds (small credit when the outcome occurs anyway) separately, with the pivotal share stated per row. For untraceable rows (a government position, an EU vote), keep CL-16's w × (1 − P0/P1) in every world where the outcome occurs. The means are unchanged either way. **Why:** Literal CL-16 on frequently firing traceable rows inflates the median and upper quartiles.

