# PERCYs (v3.7, compact) — pricing persuasion and communication grants

**Unit.** 1 PERCY = one average US adult moved one full unit higher on a −1 to +1 AI-risk opinion scale, held for one year, quality-weighted.  
**Conversions.** 1,000,000 PERCYs = 1,200 utility points (from the milestone weights list). About 1.5M PERCYs ≈ 1 percentage point of US public opinion (sanity check only).

## 1. The formula

A grant's value is the sum of its rows. Each row is one audience.

**Field row (F):** `PERCYs = N × Q × Δ × Y × cf`

| Term | Meaning                                                                                                                    |
|------|----------------------------------------------------------------------------------------------------------------------------|
| N    | **Unique people** reached in the period (never views, downloads or impressions) × the grant's owned fraction of that reach |
| Q    | Quality bin of the *typical* member (table below)                                                                          |
| Δ    | Average opinion shift per person reached, including those who don't move; may be negative                                  |
| Y    | Years-equivalent of persistence, fixed by exposure class (table below)                                                     |
| cf   | Probability the activity would not happen without the grant (×gate probability if delivery is uncertain)                   |

**Quality bins (Q).** Bin the typical member, never the best one.

| Bin                     | Q   | Typical member                                                                        | Examples                                                           |
|-------------------------|-----|---------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| General                 | 1   | Met it in a feed; wouldn't seek it out                                                | TikTok/Instagram passive reach; a documentary's streaming audience |
| Engaged                 | 3   | Chooses AI content; tech-literate                                                     | Rob Miles's viewers (returning and drive-by)                       |
| Professional-adjacent   | 10  | Works in or near tech, policy, media                                                  | ACX readership; MIT Tech Review AI readers; festival audiences     |
| Field-insider           | 30  | AI researchers, grad students, safety community, policy-adjacent                      | 80,000 Hours listeners; ACX's survey-identified core (~30,000)     |
| Decision-maker-adjacent | 100 | Rooms only (≤500 people): senior lab staff, committee staffers, think-tank principals | A DC screening; an internal lab exercise                           |

**Exposure classes (Δ band and Y).**

| Class     | What the person gets                                     | Δ band    | Y   |
|-----------|----------------------------------------------------------|-----------|-----|
| Glance    | One short piece, clip, ad, scroll-past                   | 0.01–0.03 | 0.5 |
| Long-form | One documentary, long episode, book, or multi-day event  | 0.03–0.08 | 1   |
| Sustained | A returning audience over a year, a course, a fellowship | 0.10–0.30 | 3   |

## 2. Counted elite classes (E)

Two groups are counted, never binned:

| Class                                          | Weight w | World pool |
|------------------------------------------------|----------|------------|
| Frontier-lab employees and government AI staff | 3,000    | ~50,000    |
| AI-beat journalists and editors                | 10,000   | ~3,000     |

`PERCYs = count × w × Δ_E × Y (× cf for a grant)`

- **Channels:** count = class members who follow the channel monthly or better. These are the returning core by definition, so Y = 3.

- **One-off events (rooms, screenings):** count members present; use the event's own Δ and exposure class.

- **Δ_E** is the *counterfactual* annual shift: how much less convinced these members would be if this channel didn't exist, given everything else they read. Normal range is 0.3–3× the channel's audience Δ. Reference values: ACX 0.12 lab / 0.10 journalists; 80,000 Hours 0.12 / 0.06; Rob Miles 0.06 / 0.04; MIT Tech Review 0.03 / 0.06; a general-audience creator 0.02 / 0.02; a single guest appearance 0 to −0.01.

- If E exceeds F for a grant, say so; the headcount needs a second look.

## 3. Named decision-makers (M)

Only for people the application **names**, or a category it **enumerates with a number** ("the staff of the Senate Commerce Committee"). "Senior staff" with no names or numbers is an F row at bin 100. Weights: committee staffer 3,000; House member or named senior lab researcher 30,000; Chinese senior AI academic / State Council advisor 100,000; median Senator 300,000; leadership Senator, frontier-lab CEO or Cabinet principal 1,000,000; President 10,000,000; Xi 20,000,000. Value = persons × weight × Δ (or × probability of a specific verifiable action) × Y × cf.

## 4. Kinds of claim

- **Direct:** the grant reaches an audience itself. Use the formulas above.

- **Relay:** the grant changes what a communicator produces. Value = (the communicator's channel value × the extra goal-relevant output caused) × cf. Estimate the extra output concretely (pieces × audience). At most two hops.

- **Volume:** the grant keeps an existing channel running. Value = channel's annual PERCYs × attributable share × years. Shares across all funders of one channel sum to ≤ 1.

- **Pipeline (P):** programs that create communicators. Forecast the alumni's total goal-relevant output (views, reads, people in roles), including the chance of a breakout, and convert using a comparable channel's PERCYs per unit of output (field layer only): short-form video ≈ 6 per 1,000 views; long-form video ≈ 16 per 1,000 views; newsletter ≈ 47 per 1,000 reads; one person in a lab or policy role ≈ 1,500 per person-year. Multiply by years of continued output and the program's share of each alumnus's existence as a communicator.

## 5. Rules that most often change the answer

1.  **Split a channel's audience into a returning core (Sustained) and a drive-by tail (Glance or Long-form by piece length).** Split both Δ and Y; never blend.

2.  **Count unique people,** not views. Borrowed reach (a guest spot) is Glance or Long-form, never Sustained.

3.  **Uncertain future events** (will the film get distribution; will cohorts run) are forecast questions. Research base rates rather than taking the applicant's word, and report any single gate carrying over half the value.

4.  **Volume vs direct:** if the output would continue without the grant, it's a volume claim with an attributable share; if it wouldn't exist, it's direct with cf. State which.

5.  **Coverage:** state what share of the grant's theory of change your rows price. If it's mostly not opinion change (community, art, infrastructure) or mostly runs through unnamed senior people, say the total is a floor.

## 6. Worked examples (correct calculations)

**A. Rob Miles, one year (reference channel; cf = 1).** 650,000 unique viewers; 26% returning.

| Row                                  | Calculation              | PERCYs                      |
|--------------------------------------|--------------------------|-----------------------------|
| F core (169,000, Engaged, Sustained) | 169,000 × 3 × 0.12 × 3   | 182,520                     |
| F tail (481,000, Engaged, Long-form) | 481,000 × 3 × 0.04 × 1   | 57,720                      |
| E lab staff (3,000 monthly)          | 3,000 × 3,000 × 0.06 × 3 | 1,620,000                   |
| E journalists (100 monthly)          | 100 × 10,000 × 0.04 × 3  | 120,000                     |
| **Total**                            |                          | **≈1.98M (≈2,400 utility)** |

E exceeds F here, as it does for most text, audio and technical channels.

**B. ACX, one year (reference channel).** 300,000 unique readers; 33% returning; whole readership Professional-adjacent.

| Row                        | Calculation               | PERCYs                     |
|----------------------------|---------------------------|----------------------------|
| F core (99,000, Sustained) | 99,000 × 10 × 0.15 × 3    | 445,500                    |
| F tail (201,000, Glance)   | 201,000 × 10 × 0.02 × 0.5 | 20,100                     |
| E lab staff (4,000)        | 4,000 × 3,000 × 0.12 × 3  | 4,320,000                  |
| E journalists (250)        | 250 × 10,000 × 0.10 × 3   | 750,000                    |
| **Total**                  |                           | **≈5.5M (≈6,600 utility)** |

**C. Short-form creator grant (direct claims).**

| Row                                                   | Calculation                      | PERCYs |
|-------------------------------------------------------|----------------------------------|--------|
| Passive viewers (3.5M, General, Glance, cf 0.8)       | 3,500,000 × 1 × 0.01 × 0.5 × 0.8 | 14,000 |
| Engaged viewers (160,000, Engaged, Long-form, cf 0.6) | 160,000 × 3 × 0.05 × 1 × 0.6     | 14,400 |

**D. A convening (direct room claim).** 340 attendees at Field-insider, Long-form, Δ 0.07, cf 0.75, of whom 80 are lab staff and 40 journalists.

| Row                         | Calculation                   | PERCYs |
|-----------------------------|-------------------------------|--------|
| F (the other 220 attendees) | 220 × 30 × 0.07 × 1 × 0.75    | 346    |
| E lab staff                 | 80 × 3,000 × 0.07 × 1 × 0.75  | 12,600 |
| E journalists               | 40 × 10,000 × 0.07 × 1 × 0.75 | 21,000 |

**E. Volume claim.** A grant funds 45% of a channel worth 1,000,000 PERCYs/yr for one year: 1,000,000 × 0.45 × 1 = 450,000.

**F. Pipeline.** A creator incubator, 3 cohorts. Forecast alumni output: mean ≈188M short-form views/yr (median 60M; 3% chance of a 2B breakout). Value = 188M × 6/1,000 × 2.5 years × 0.5 (program's share of alumni's careers) × 0.5 (chance the cohorts run) × 0.85 (cf) ≈ 600,000 PERCYs.
