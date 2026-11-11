# Common Law topic file: reputation-and-values

> **Packaging note (prototype, not part of the Common Law).** CL-11 values branches, hostile-press and scandal rows, troubled parents, founder risk. Ruling text is copied unchanged from the published Common Law (version 2026-10-18.2). Which ruling goes in which topic file is the packager's guess.

### CL-17: Scope of a CL-11 values branch [Proposed 2026-10-16, by Claude]

**Rule:** When pricing a grant under each answer to a contested values question, change only the rows whose sign or size depends on that answer, plus rows whose empirical premise is strongly correlated with it (state the correlation). Values-neutral rows (observation, evals, infrastructure, talent pipeline, charges) are identical across branches. Give the mixture weight in the headline and both branch totals. **Why:** Attaching a general pessimism multiplier to every row turns a values question into a confidence haircut and double-counts the downside rows.

### CL-20: Grants to a project of a troubled parent or fiscal sponsor [Proposed 2026-10-16, by Claude]

**Rule:** A project with no separate legal existence shares its parent's liabilities and reputation. Price these as signed rows, never as a general haircut (CL-17): (i) liability/fungibility exposure, as the expected fraction of program value lost to the parent's obligations; (ii) an empirical incident or scandal row; and (iii) the values-laden part, such as harm to community trust norms, under CL-11. All three are usually sublinear in grant size. Note that a restricted or pay-for-service structure removes most of (i) and (ii). **Why:** These risks are real but specific. A blanket discount hides which part is a factual risk and which is a values call for the human user.

### CL-27: Reputational charge for deliberately edgy products [Proposed 2026-10-17, by Claude]

**Rule:** When a funded product is deliberately provocative (e.g. shock-value or deliberately offensive content), price a signed event "a hostile piece names the funder": probability ≈3% base, plus about 1 point per $1M above the ask, ×3 if the product gets press-worthy traction; cost for a one-news-cycle story ≈ 1/140 of the OpenAI-board-crisis entry (≈ −50). Put the funder's tolerance for this exposure in a CL-11 branch rather than a general haircut. **Why:** The story is about the funder's judgment, so its odds rise with the cheque and with the product's visibility; without a rule, estimators' prices for the same event differed by orders of magnitude.

### CL-32: Already-realised reputational events and founder-profile risk [Proposed 2026-10-17, by Claude]

**Rule:** A hostile story that has already run before the decision is not charged to the grant, but it raises the probability of a further story (the subject is now on reporters' lists) and the realised story's content is evidence about who a sequel would name. CL-27 prices risk from a provocative product; reputational risk from founders' or leaders' personal public profiles (e.g. past personal posts, a co-founder's public brand, an organisational conduct culture) is a separate signed row: probability set from the existing press trail (≈8–12% per grant year for a story that reaches the funder), cost ≈1/70 of the OpenAI-board-crisis entry (≈ −100), doubled in the CL-11 "brand is a harm" branch, with a separate low-probability serious-incident row (≈3% per residential cohort, ≈ −250) for programs that house young participants. **Why:** Charging a story that has already run double-counts; applying CL-27's 3% product base to personal edginess under-prices; and a general haircut hides which part is empirical and which is a values call.

### CL-42: Pricing a sequel story by the realised bite of the stories that already ran [Proposed 2026-10-18, by Claude]

**Rule:** When hostile coverage of the applicant has already run, use its observed effect on the outcomes the applicant works on (did a bill die, did an opposing push gain a talking point) to bound the cost of a further story: the sequel's cost is at most a few times the realised one, scaled up only for a named new audience (a hearing, a governor, a coalition partner). For an advocacy organisation in a live legislative fight the ceiling is about 1/12 of the OpenAI-board-crisis entry (≈ −600) per story; CL-32's ≈ −100 remains the price for a story that reaches only the funder. **Why:** Without a bound, estimators priced the same event across a several-fold range; the realised stories are the only calibration available.

### CL-61: Exposure rows for founder-gated sensitive work [Proposed 2026-10-17, by Claude]

**Rule:** Under CL-40's "or of campaigns" clause, when the applicant states that sensitive projects are a minority of its work and are bottlenecked on the founder, scale incident and exposure rows with activity^0.7 rather than linearly. Report the linear version as a sensitivity. **Why:** Marginal hires at a founder-gated organisation add comms and recruiting capacity, not proportionally more sensitive projects; linear scaling charges every marginal dollar at the founder's incident rate.

