# Common Law topic file: money-and-funders

> **Packaging note (prototype, not part of the Common Law).** Pending or outside money, funging, runway, absorptive capacity, refunds, earned revenue. Ruling text is copied unchanged from the published Common Law (version 2026-10-18.2). Which ruling goes in which topic file is the packager's guess.

### CL-14: Pending applications at other funders [Proposed 2026-10-16, by Claude]

**Rule:** An application already pending with another funder is neither a pledge (CL-8 "existing funds and pledges") nor "a later round" (CL-8 "don't assume a later round rescues the project"). Model it as an event with a stated probability in both the grant and the no-grant worlds. The probability may differ between the two worlds only for a stated reason (the grant lowers the other funder's urgency, or raises the applicant's credibility), and the difference should be small. Never treat it as secured or as zero in one world only. **Why:** Ignoring it overstates bridge grants; counting it as secured understates them; and treating it asymmetrically (secured with the grant, absent without) is the error that actually moves estimates, because a symmetric pending application lifts both worlds and leaves the grant's increment nearly unchanged.

### CL-21: Freed backstop [Proposed 2026-10-16, by Claude]

**Rule:** When a grant relieves a named party of a committed backstop, credit the expected dollars freed at the CL-4 money price × P(the backstop would have been drawn). **Why:** This is the mirror image of CL-4. Money the grant releases elsewhere has value just as money it pulls in has cost.

### CL-23: Reported-but-unlisted grants and per-year survival rows [Proposed 2026-10-16, by Claude]

**Rule:** A grant another funder reportedly made, but which is missing from that funder's public list, is a pledge at a stated probability, kept the same in both worlds (as in CL-14). For an organization whose death without the grant is not imminent, use per-year "operating at scale" probabilities with partial-loss states (downsizing, not just closure). Let the no-grant path include ordinary future fundraising (CL-8), and move the probabilities only in the years the grant's banked runway actually covers. **Why:** A single binary "survives" row overstates bridge grants to organizations that would likely limp on. Treating an unconfirmed grant as certain, or as zero, swings the no-grant world.

### CL-28: Earned revenue versus follow-on grants [Proposed 2026-10-17, by Claude]

**Rule:** Product revenue the grantee earns (sales, tickets) is earned revenue under CL-8, not a CL-4 charge. Follow-on grants the grantee says it will seek are charged at the CL-4 money price, with the probability raised (≈×1.8) if the product shows traction and lowered (≈×0.7) otherwise. Grant-funded continuation after 2030 is charged inside its own row, not again in the follow-on row. **Why:** CL-4 charges resources pulled from elsewhere; sales are not; and charging continuation twice double-counts (CL-5).

### CL-29: Leader-commitment-gated, refundable grants [Proposed 2026-10-17, by Claude]

**Rule:** When the applicant's lead has promised to decide before disbursement and return the money if not fully in, model commitment as a gate whose probability may depend on grant size (from the applicant's own statements), value the refund branch at exactly 0 (both worlds identical, no CL-4 charge, no no-grant revival difference), and report P(=0) separately from P(<0). Report per-$1M both nominal and per dollar expected to be spent, and the conditional-on-commit figures, since the grantmaker may learn the answer before money moves. **Why:** Treating the refund branch as wasted money overstates the downside; treating commitment as certain overstates value; and the median can legitimately sit at zero. *(Superseded in part by Adopted CL-33: the headline is now the value conditional on disbursement, and P(=0) and the unconditional figures need not be reported.)*

### CL-34: Funging with an intended but unsubmitted application to a repeat funder [Proposed 2026-10-18, by Claude]

**Rule:** An application the applicant says it will make to a funder that has funded it before is modelled like a pending one (CL-14): same probability in both worlds, set from the funder's history and any forecast. Unlike CL-14, the *expected award* may fall with the grant for the stated reason that the applicant writes its own ask around the remaining gap and the other funder caps on runway; the reduction should be convex in grant size (small when the grant leaves the plan visibly unfilled, approaching the other funder's usual award once the grant covers the plan year) and capped at that award. Net the reduction from the grantee's resources and credit it at the CL-4 money price (CL-21 logic). Never let the probability differ between worlds without a stated mechanism. **Why:** Treating the unsubmitted application as zero overstates the grant; treating it as secured understates it; and a flat funging fraction misses that the applicant's ask, not the funder's taste, is what the grant changes.

### CL-35: Grant within the ask but above absorptive capacity [Proposed 2026-10-18, by Claude]

**Rule:** CL-22 applies whenever the grant plus funding received or expected after the application was written exceeds what the applicant can spend in the plan year, even if the grant is within the ask. Cap the plan-year spend increment from the applicant's own hiring-rate statements (as a distribution, not a point), treat the rest as banked runway valued at the mixture of (a) the money price for the share that displaces the applicant's ordinary next-year fundraising (CL-8) and (b) the marginal program value for the share that becomes extra next-year program, add a signed idling/discipline charge above a stated threshold, and report the uncapped figure as a sensitivity. **Why:** An ask written before other funders decided is not the applicant's need; without a cap the top tranche inherits the first tranche's value and fails CL-9.

### CL-41: Applicant-stated plan ambition raises the absorptive cap [Proposed 2026-10-18, by Claude]

**Rule:** When the applicant says in its own words that funding commitments set how aggressively it plans (rather than naming a fixed plan), raise the CL-35 absorptive cap by a stated fraction of the grant (≈0.3) instead of holding it fixed, and say so. Keep CL-35's hiring-rate cap on the FTE part of the increment. **Why:** CL-35 assumes the plan year is fixed before the grant; an applicant that scales its contractor program to commitments can spend more of a large grant in-year, so a fixed cap banks money that would be spent.

### CL-43: Funders outside the platform keep their independent money in the no-grant world [Proposed 2026-10-18, by Claude; amended by the human user 2026-10-18]

**Rule:** The prompt's "if I rejected it, nobody else would approve it" and CL-8's "this money is not replaced" mean that the platform's money is not replaced. Independent allocations to the same organisation from funders outside the platform (donor-adviser recommendations, pledges, other funders' rounds and applications) stay in both worlds at whatever probability they would happen anyway (CL-14/CL-34 logic). Other evaluators' allocations on the same platform are not outside money: per Adopted CL-62 they are left out of both worlds. **Why:** Estimators read the prompt both ways; removing outside funders' independent money from the no-grant world inflates the gap the grant fills and the marginal factor.

### CL-44: Adviser-recommended, unfilled funding and funding-state blending [Proposed 2026-10-18, by Claude]

**Rule:** A donor adviser's recommendation to its clients that has not been filled is pending money (CL-14/CL-34), not a pledge and not zero. State the probability of each funding state by a stated date (e.g. the next hiring tier still unfilled; filled; the adviser's larger recommendation substantially filled), identical in both worlds unless the grant is ≥ ~20% of the recommendation. Value the grant as the blend across states, with a marginal factor per state: the unfilled-tier slice at the CL-37 non-founder bound, session-critical lines of the next tier below that, and money on top of a filled plan at the plan's weaker lines (CL-22 logic). Money that arrives before the adviser's money can still buy session-critical lines, so the filled-state factor is not the plan's weakest line. **Why:** Policy organisations often carry large unfilled recommendations; treating them as secured zeroes the grant, treating them as absent overstates it, and a two-state blend hides the intermediate case.

### CL-53: Applicant minimum-size statements with pending money [Proposed 2026-10-17, by Claude]

**Rule:** When an applicant says it will not run a project below a minimum, the no-grant world runs it if, and only if, independent pending money (at its CL-14 probability) reaches that minimum. In that state, the grant's increment is the top-up, valued with any named full-time threshold premium. Leftover money extends the activity at the post-window value, with CL-38 logic.

### CL-58: [Struck by the human user 2026-10-18] Evaluator recommendations in a bill-splitting round

*Do not apply. This ruling made the headline one evaluator's recommendation stacked on the other evaluators' money in the same round, which Adopted CL-62 rejects. The number is kept so it is not reused.*

### CL-59: A later round of the same funder when the organisation survives without the grant [Proposed 2026-10-17, by Claude]

*(Superseded 2026-10-18 by Adopted CL-62: later rounds of the same platform are left out of both worlds when the organisation survives without the grant. Since the scored grant is always the platform's money, do not apply this ruling; later rounds of funders outside the platform are pending money under CL-14/CL-34.)* **Rule:** If the no-grant organisation operates at or above about half its plan, model a later round of the same funder in both worlds (CL-14/CL-34 logic): the award shrinks as the grant fills the gap, and displaced dollars are credited at the money price. CL-8's rescue clause and CL-31's parenthetical apply only below that threshold. A reading defined as "this funder's money vs none" excludes the later round from both worlds. **Why:** Adopted CL-8 forbids modelling an organisation that can never raise money again, and CL-31 is scoped to programs that die; asymmetric treatment inflates the marginal factor in low-funding draws.

