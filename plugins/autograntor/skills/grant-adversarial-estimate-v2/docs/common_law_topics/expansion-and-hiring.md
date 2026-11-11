# Common Law topic file: expansion-and-hiring

> **Packaging note (prototype, not part of the Common Law).** New hires, contractors, grants above the ask, the marginal factor, people charges. Ruling text is copied unchanged from the published Common Law (version 2026-10-18.2). Which ruling goes in which topic file is the packager's guess.

### CL-22: Grants above the amount asked [Proposed 2026-10-16, by Claude]

**Rule:** When the grant exceeds the applicant's ask, price the excess as runway extension plus the applicant's lowest-ranked or most speculative initiatives, add a signed discipline/idling charge, and don't scale the ask's ledger linearly. Positive rows may hold or rise per dollar between tiers only for a named threshold (e.g. runway that covers a specific year, a fixed-cost hire). Otherwise assume diminishing returns. **Why:** Without a rule, estimators either multiplied the ask's ledger up or guessed. Both failed CL-9.

### CL-36: Scaling risk as signed rows [Proposed 2026-10-18, by Claude]

**Rule:** For a grant that funds a headcount jump at an organisation with a thin management record, price (i) bad hires as a Poisson count at about one per three hires beyond the first one or two already-identified candidates, each costing one to two months of a senior person-year on the organisation's own ledger, and (ii) a management-breakdown episode whose probability rises steeply (≈cubic) with the expansion relative to the current team, costing about a senior person-year. Do not add a separate per-hire management drag: the manager time an ordinary hire consumes is already inside the marginal-vs-average factor (CL-17, price once). Report the charges separately from the marginal factor so the two cannot double-count. **Why:** Without a rule, estimators' charges varied widely and included a drag term and a "managers stretched" tier that priced the same cost twice.

### CL-37: The marginal factor for expansion grants is bounded by the non-founder average dollar [Proposed 2026-10-18, by Claude]

**Rule:** When a grant buys additional staff at an existing organisation, state the share of the organisation's value produced by its senior people and derive the average value of a non-founder dollar; the first tranche of new hires is worth at most that non-founder average (an un-bottlenecking argument can put it at the top of the range, not above it), with later tranches declining. A correlated execution factor on program rows (did the hires work) is consistent with CL-16 as a realised 2030 fact, but it must not multiply the charge rows and must not be compounded with a second dispersion on the same factor. **Why:** This is CL-9/CL-15 applied inside the organisation; without it estimators can price the first marginal dollar above the dollars already spent on non-founders, or widen the spread with stacked multipliers.

### CL-38: Persistence of grant-funded hires at an organisation that survives without the grant [Proposed 2026-10-18, by Claude]

**Rule:** When the no-grant organisation survives and fundraises normally (CL-8), credit the next-year persistence of grant-funded hires only as a timing gain: roughly 0.1–0.2 of the plan-year increment (months ahead × retention × the share the no-grant organisation would not have hired anyway), net of a CL-4 money charge for the next-year money that pays them. CL-31 (continuation of a program that dies) does not apply. **Why:** Crediting 30%+ of a second program-year quietly credits other funders' next-year money; crediting nothing ignores that hiring is slow.

### CL-39: Expansion grants at organisations whose marginal spend is external contractors [Proposed 2026-10-18, by Claude]

**Rule:** When the marginal dollar mostly buys lobbyists, comms firms or other contractors rather than staff, apply CL-36's bad-hire and breakdown rows to FTE hires only (state the hires per $1M), charge no CL-4 people cost on contractor spend (those contractors would otherwise work for someone else), set CL-38 persistence at the bottom of its 0.1–0.2 range, and scale exposure-type downside rows (press, integrity incidents) with the number of campaigns rather than with the marginal factor. **Why:** CL-36/37/38 are written for headcount growth; applied literally to contractor spend they charge contractors as scarce safety people and price a bad campaign twice (as a bad hire and through the execution factor).

### CL-40: Which downside rows inherit the marginal factor [Proposed 2026-10-18, by Claude]

**Rule:** Downside rows that are consequences of the substantive work the marginal dollar does (a watered-down law anchoring a weak standard, a position softened for access, a weak federal bargain) scale with share × marginal factor, like the positive rows they follow from. Exposure rows (a hostile story, a scandal, partisan coding) scale with the grant's share of activity (or of campaigns), not with the marginal factor, because a weak campaign generates incidents at the average rate. Neither kind is multiplied by the execution factor (CL-17). **Why:** Scaling every downside by share alone overcharges marginal dollars that produce below-average laws; scaling every downside by m undercharges incident risk from marginal campaigns.

### CL-54: Volunteer labour in CL-15 and CL-37 comparators [Proposed 2026-10-17, by Claude]

**Rule:** For an organisation whose labour is mostly unpaid, report the average dollar on cash and on cash plus imputed volunteer labour (≈1/3 of a loaded junior salary per volunteer FTE). When a grant converts volunteer work into paid work, the CL-37 comparator is a blend of the two, with this weight on the labour-inclusive basis:

- ≈0.2 if the paid role partly does work volunteers cannot (credentialed, sustained access);

- ≈0.5 if it mostly substitutes for volunteers;

- 0 if it is a wholly different function.

**Why:** A cash-only average is flattered by free labour; a labour-only average ignores what pay buys.

### CL-56: CL-37 comparator anchored on the track record; CL-15 vs CL-37 [Proposed 2026-10-17, by Claude]

**Rule:**

1.  The org value V used for the CL-37 non-founder average must be checked against the organisation's track record (CL-9). A forward per-dollar value more than ~1.5× the track-record figure needs a stated, specific reason (a new paid function, a dated window). Even then, put the cap at the top of the range, not above it.

2.  CL-15's "strongest line" exception (Adopted) can lift a new hire above the CL-37 bound only for a checkable reason specific to the hire: an identified candidate with a record in that line, or an existing line the grant scales. Absent that, there is no conflict to resolve and the CL-37 bound applies.

**Why:** Otherwise estimators can agree on a mean only by pairing a cap built on an org ledger far above its track record with offsetting row choices.

### CL-57: Charges excluded from the CL-15 comparison [Proposed 2026-10-17, by Claude; marked optional]

**Rule:** When comparing the grant with the org's average dollar, report the grant figure both with and without funder-specific rows (a CL-32 story that reaches the funder) and hire-specific CL-36 rows, which have no org-level analogue. The gap to the org average should be explained after removing them.

### CL-60: CL-36 charges against an execution factor that contains a collapse state [Proposed 2026-10-17, by Claude; second clause amended by the human user 2026-10-18]

**Rule:** When the correlated execution factor includes a collapse or bus-factor state, set the CL-36 breakdown charge to zero in those worlds and set its level consistently with that state's probability. When money from outside the platform already pays the identified candidates' salaries in the no-grant world (CL-8, CL-43), CL-36's "beyond the first one or two already-identified candidates" offset is zero for grant-funded hires. Other evaluators' same-round allocations on the platform are not such money (CL-62), so candidates only they would have paid count as grant-funded and keep the offset. **Why:** A breakdown inside a world already scored as a collapse is the same event priced twice; identified candidates are not grant-funded when other money already pays them.

