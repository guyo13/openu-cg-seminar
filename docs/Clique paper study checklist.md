# Study Checklist — "The Maximum Clique Problem in a Disk Graph Made Easy" (Keil & Mondal, SoCG 2025)

## Phase 1 — Big Picture (target: ~30 min)

- [x] Read the abstract and list the paper's 3 results in my own words
- [x] Read the Introduction; write one sentence: _why was this problem famous?_
- [x] Read Section 6.1 ("The Deception of the Lens"); explain in my own words why the lens-based approach fails for two radii
- [x] Can answer: "If the solution is so easy, why was it open since 1990?"

## Phase 2 — Background Refreshers

- [ ] Review bipartite graphs and maximum matching (Kleinberg–Tardos or any algorithms textbook)
- [ ] Review König's theorem: max matching = min vertex cover in bipartite graphs
- [ ] Derive: max independent set in bipartite graph = n − max matching
- [x] Understand "co-bipartite graph" and why its complement being bipartite matters
- [x] Read the overview of Clark–Colbourn–Johnson's lens-based unit-disk algorithm (start of Section 4)
- [x] Can explain the contrast: lens (farthest pair) vs. slab (leftmost/rightmost pair)

## Phase 3 — Lemma 2.1 (the foundation)

- [x] Draw the setup myself: segment ab, upper slab, points p and q
- [ ] Reprove Case 1a: ray exits through segment ab (Figure 1(b))
- [ ] Reprove Case 1b: ray exits through a vertical side (Figures 1(c)–(d))
- [ ] Reprove Case 2: ab is vertical
- [ ] Closed-book test: state and prove Lemma 2.1 from scratch on blank paper

## Phase 4 — The Main Algorithm (Section 3)

- [ ] Write the algorithm pipeline in my own words: guess → filter → two cliques → bipartite complement → matching
- [ ] Understand why guessing leftmost/rightmost centers per radius type is legitimate (some guess must be correct)
- [ ] Prove Lemma 3.1, case i = j (why |pq| ≤ 2rᵢ suffices)
- [ ] Prove Lemma 3.1, case i ≠ j, both sub-cases (who is higher, p or q?)
- [ ] Verify: why is C ⊆ Ψ ∪ X ∪ Y?
- [ ] Verify: why is the complement of the graph on X ∪ Y bipartite?
- [ ] Rederive the running time O(n²ᵏ(f(n) + n²)) — where does each factor come from?
- [ ] Understand why this settles Cabello's open question for k = 2

## Phase 5 — Worked Example (do not skip!)

- [ ] Construct a concrete example: 5–6 unit disks (k = 1), coordinates chosen by hand
- [ ] Run the algorithm on it: pick a, b; draw the slab; build X and Y
- [ ] Verify Lemma 3.1 numerically on my example
- [ ] Draw the complement graph and find the max independent set by hand
- [ ] Repeat mentally for k = 2 (small example with two radii)

## Phase 6 — Secondary Content (light touch)

- [ ] Skim Section 4 (rectangular range queries): one-sentence summary of the idea
- [ ] Skim Section 5 (ball graphs): one-sentence summary of what carries over
- [ ] Decide what (if anything) from Sections 4–5 goes on my closing slide

## Phase 7 — Presentation Readiness

- [ ] Can state the problem and its history in under 2 minutes
- [ ] Can present Lemma 2.1 proof at the board without notes
- [ ] Can present the full Section 3 argument end-to-end without notes
- [ ] Prepared answers for likely questions:
    - [ ] "Why doesn't this solve the general disk graph case?" (k appears in the exponent)
    - [ ] "Where exactly does the proof use that there are finitely many radius types?"
    - [ ] "How is the matching actually computed?" (Hopcroft–Karp, f(n))
    - [ ] "What's the difference between this and the 1990 unit-disk algorithm?"
- [ ] Dry-run the full talk once, timed
- [ ] Dry-run a second time in front of a friend / recorded

## Milestones

- [ ] ✅ Phase 1–2 done → I understand the context
- [ ] ✅ Phase 3–4 done → I own the proofs
- [ ] ✅ Phase 5 done → I can survive any board question
- [ ] ✅ Phase 7 done → ready to present