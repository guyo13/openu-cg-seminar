# Q&A Armor — reference notes (not slides)

Keep on the podium. These cover the load-bearing steps most likely to draw
follow-up questions, at *defending* depth.

## 1. The reduction chain (five hops — say them in order)

Goal per guess: maximum clique among the candidate disks X ∪ Y.

1. **Complement (definition, any graph).** Max clique in G[X ∪ Y] = max
   independent set in the complement H. Nothing deep: cliques and
   independent sets swap under complement.
2. **H is bipartite (Lemma 3.1).** X is a clique and Y is a clique, so H has
   no edges inside X nor inside Y — every H-edge crosses. Sides of the
   bipartition: X and Y.
3. **Gallai (any graph):** α(H) = |V(H)| − τ(H). Independent set =
   complement of a vertex cover.
4. **Kőnig (bipartite only — THIS is where it enters):** τ(H) = ν(H),
   min vertex cover = max matching. Requires bipartiteness, i.e. hop 2.
5. **Black box:** ν(H) via any max matching algorithm (e.g. Hopcroft–Karp)
   — this is the f(n) in the running time. The actual independent set is
   recovered from the matching (alternating-path argument; citable, not
   presentable).

Then: output = Ψ ∪ (that independent set, read as a clique in G).

**Numbers on the demo scene:** cand = {s3, b4, s6}; H has the single edge
s3–s6; ν = 1; α = 3 − 1 = 2; chosen = {s3, b4}; final = Ψ ∪ {s3, b4}, size 6.

## 2. The trap answer to avoid

"Max independent set of a bipartite graph = the larger side" — **FALSE.**
The larger side is *an* independent set (a lower bound), not the maximum.

Pocket counterexample: sides {a, b, c} and {d, e, f}, edges a–d and b–e.
Larger side gives 3. Truth: ν = 2, so α = 6 − 2 = 4, e.g. {b, c, d, f}
(check: b–e and a–d are the only edges; none inside the set). If asked "how
does the matching give the clique," recite hop 3 + 4, never "larger side."
(Our demo's coincidence — where the larger side happens to be optimal — is
why this false belief feels true on small pictures.)

## 3. XP vs FPT (Q5 vocabulary)

- **FPT:** f(k) · n^c, parameter multiplies, exponent constant.
- **XP:** n^{f(k)}, parameter in the exponent. **This paper is XP** via
  O(n^{2k}(f(n) + n²)); polynomial for each fixed k, degree grows with k.
- *Why* only XP: the guessed witness Ψ has size 2k and is
  solution-defined; enumerating it over n disks inherently costs
  n^{Θ(k)}. An FPT algorithm would have to avoid enumerating
  solution-defined anchors — nobody knows how.
- k unbounded ⇒ k can be Θ(n) ⇒ n^{Θ(n)}: not polynomial. General disk
  graph max clique: **open in both directions** (no poly algorithm, no
  hardness proof). Do NOT say "probably NP-hard" — the paper's ball-graph
  contrast (NP-hard there, poly here for fixed k, r) shows the boundary is
  subtle. FPT results exist for related settings (Bonnet et al., cited in
  the intro) — don't claim this paper is one of them.

## 4. Recurring subtleties (each burned me once in the stress quiz)

- **Ψ-validity check.** For arbitrary guesses, nothing forces the guessed
  disks to pairwise intersect. Discard guesses where Ψ is not a clique
  (O(k²) check). Without this, Ψ ∪ (matching result) can fail to be a
  clique. For the correct guess Ψ ⊆ 𝒞, so it passes trivially.
- **Soundness mechanism (why wrong guesses are safe).** Lemma 3.1's proof
  consumes exactly two properties of a disk in X: center in its type's
  slab, intersects all of Ψ. It never uses Ψ ⊆ 𝒞. Hence X, Y are cliques
  for every (valid) guess; wrong guesses output smaller-but-genuine
  cliques and lose the max. The correct guess is never *detected* — it is
  *out-competed for*.
- **Anchors come from the lower point's type.** In Lemma 3.1, whichever of
  p, q is lower supplies both the slab and the anchors; the higher point
  supplies the free position. Its disk meets the lower type's anchors
  (they're in Ψ) ⇒ bound r_i + r_j (or 2r_i when types match). This one
  rule generates all sub-cases.
- **Containment is strict.** Correct guess gives 𝒞 ⊆ Ψ ∪ X ∪ Y, not
  equality (demo: s6 is in the union, not in 𝒞). That gap is exactly why
  the matching step exists.
- **"Leftmost and rightmost" is a sentence from the analysis, not from the
  algorithm.** Sorting type-i disks finds extremes of the wrong set (demo:
  sorted type-1 extremes are s5 and s4 — both discarded; true anchors
  s1, s2 sit mid-order). The anchors are defined by the unknown 𝒞;
  enumeration over O(n²) pairs per type is the price of that circularity,
  and 2k-sized witnesses are what make the price affordable.

## 5. Per-guess cost ledger (for "where does the time go")

O(n²) guesses per type (absent / single / pair: C(n,0)+C(n,1)+C(n,2)) →
O(n^{2k}) total; per guess: O(k²) Ψ-check + O(nk) filter (each disk tested
once against its own type's slab — Σ nᵢ = n, not k·n) + O(n²) graph build +
f(n) matching. Total O(n^{2k}(f(n) + n²)).
