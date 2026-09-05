---
theme: seriph
title: The Maximum Clique Problem in a Disk Graph Made Easy
info: |
  Undergraduate seminar in computational geometry.
  Keil & Mondal, SoCG 2025 — arXiv:2404.03751
class: text-center
transition: slide-left
mdc: true
---

# The Maximum Clique Problem<br>in a Disk Graph Made Easy

J. Mark Keil &middot; Debajyoti Mondal &mdash; SoCG 2025

<div class="pt-8 opacity-70 text-sm">
arXiv:2404.03751 &middot; presented by Guy Or
</div>

<!-- ~30s. Say the title, the venue, and one sentence: "a 35-year-old open
problem, solved with high-school geometry — the story is why nobody found
it sooner." -->

---

## Definitions

- A **disk graph** $\mathcal{D}$: vertices are disks, edges join intersecting disks.
- Adjacency is a distance condition: $D_{a,r_1}$ and $D_{b,r_2}$ intersect $\iff |ab| \le r_1 + r_2$.
- $\mathcal{D}_k$: disk graph with $k$ distinct radii ("radius types").
- A **clique**: pairwise intersecting disks. We want a **maximum** one.

<!-- ~1.5 min. Stress the iff: every adjacency claim later is secretly a
distance claim. The graph forgets the geometry — the disk representation is
part of the input. -->

---

## Why this problem is famous

<v-clicks>

- **1990** — Clark, Colbourn, Johnson: polynomial algorithm for **unit** disks.
- **Then: 35 years of nothing.** NP-hard for rays, ellipses, triangles, strings, balls… polynomial for unit disks, rectangles, trapezoids. Disk graphs: **unknown, either way.**
- Called *"a notorious open question in computational geometry"*, *"elusive with no new positive or negative results"*.
- **Cabello, 2015:** is even the **two-radii** case ($k=2$) polynomial? — Open.
- **This paper:** yes — $O(n^{2k}\,\mathrm{poly}(n))$, polynomial for every fixed $k$.

</v-clicks>

<div v-click class="pt-4 text-sm opacity-70">
Why every natural attack failed is a story for the end — if time permits.
</div>

<!-- ~2 min. The stakes slide. Don't explain CCJ, just name it. The last
line is the promissory note for the epilogue. -->

---
layout: two-cols
---

## The disk graph $\mathcal{D}_2$

<img src="../figs/chapter3/notation/disk_graph_fig.png" class="h-80" />

::right::

## Notation, on one arrangement

- blue = type-1 $(r_1)$, orange = type-2 $(r_2)$
- $C_i$ — a clique of only type-$i$ disks
- $\mathcal{C}$ — a maximum clique
- $\mathcal{C}_i$ — the type-$i$ disks **inside** $\mathcal{C}$

<div class="pt-4 text-sm opacity-70">
This arrangement stays with us for the whole talk.
</div>

<!-- ~1.5 min. Introduce the cast once. C_i vs calligraphic C_i distinction:
any single-type clique vs the type class of THE maximum clique. -->

---
layout: two-cols
---

## A maximum clique $\mathcal{C}$

<img src="../figs/chapter3/notation/max_clique_fig.png" class="h-80" />

::right::

## …mixes radius types

<img src="../figs/chapter3/notation/type_classes_fig.png" class="h-80" />

<div class="text-sm opacity-70">
$\mathcal{C} = \mathcal{C}_1 \cup \mathcal{C}_2$ — and this mixing is exactly
why unit-disk techniques don't transfer.
</div>

<!-- ~1.5 min. "Why can't we solve each radius type separately and glue?"
Because the maximum clique mixes types; the per-type maxima can live in
different corners of the arrangement. -->

---

## The algorithm, from ten kilometers

<div class="text-xl leading-relaxed pt-6">

**guess** a few special disks $\Psi$ &nbsp;→&nbsp; **slabs + filter** keep only compatible disks &nbsp;→&nbsp; survivors split into **two cliques** $X$, $Y$ &nbsp;→&nbsp; one **bipartite matching** picks the winners &nbsp;→&nbsp; take the **max over all guesses**

</div>

<div class="pt-8 text-sm opacity-70">
Each arrow is one act of this talk. The word to interrogate first: <b>"guess"</b>.
</div>

<!-- ~1.5 min. The roadmap; echo it before each act. Everything hard hides
inside the word "guess". -->

---

## "Just sort and take the extremes"?

The analysis says: let $a_i, b_i$ be the **leftmost and rightmost** centers…

<img src="../figs/chapter3/algorithm/sort_trap.png" class="h-95 mx-auto" />

<!-- ~1.5 min. Let them feel the temptation, then the trap: the sorted
extremes of the type-1 disks (s5, s4) are not even IN the maximum clique.
The extremes we need are extremes OF C_1 — a set nobody knows. -->

---

## The circularity, and its price

- $a_i, b_i$ are extremes **of $\mathcal{C}_i$** — a set defined by the solution $\mathcal{C}$.
- Knowing them in advance = knowing the answer. **No shortcut can exist.**

<v-click>

**Resolution — the guessing framework:** enumerate *every* candidate per type:

$$\underbrace{\binom{n}{0}}_{\text{type absent}} + \underbrace{\binom{n}{1}}_{a_i = b_i} + \underbrace{\binom{n}{2}}_{a_i \ne b_i} = O(n^2) \;\;\xrightarrow{\;k\text{ types}\;}\;\; O(n^{2k}) \text{ guesses}
$$

</v-click>

<v-clicks>

- *"Leftmost and rightmost" is a sentence from the **analysis**, not the **algorithm**.* The algorithm never detects the right pair — the right iteration simply **wins the final max**.
- The miracle: the unknowable information is only $2k$ disks. **A constant-size witness** — that's what makes the price affordable.

</v-clicks>

<!-- ~1.5 min. THE conceptual slide. n^{2k} is the price tag on circular
information. If they get this, the rest of the construction is bookkeeping. -->

---

## Slabs

<img src="../figs/chapter2/perliminaries/slab_geometry.png" class="h-80 mx-auto" />

Upper slab $U_{ab}$ and lower slab $\overline{U}_{ab}$ — the setting for the one geometric lemma.

<!-- ~1 min. Vertical lines through a and b; above / below the segment. -->

---

## Lemma 2.1 — the anchors are the worst case

> Let $q \in U_{ab}$, and let $p$ be any point with $y(p) \ge y(q)$.
> Then $|pq| \le \max\{|pa|, |pb|\}$.

<div class="pt-6">

In words: **no point hiding in the slab above $ab$ can be farther from $p$ than one of the two endpoints themselves.**

</div>

<div v-click class="pt-4 text-sm opacity-70">
Proof by sliding: shoot the ray $p \to q$, find where it exits the slab, and slide the exit point away from the closest point of the boundary — the distance only grows, and it ends at $a$ or $b$.
</div>

<!-- ~1.5 min. State it in words before symbols. The hypothesis y(p) >= y(q)
is load-bearing: it guarantees the ray exits, and powers the slide-down. -->

---

## Lemma 2.1 — exit through $ab$

<img src="../figs/chapter2/lemma21/lemma21_case_b.gif" class="h-80 mx-auto" />

The exit point $o$ slides along $\overline{ab}$, **away from $m$**.

<!-- ~1 min + pause. Freeze at the start and ask: "why must o move AWAY
from m?" — moving away from the closest point of a line monotonically
increases distance. That sentence IS the proof. -->

---

## Lemma 2.1 — exit through a wall

<img src="../figs/chapter2/lemma21/lemma21_case_c.gif" class="h-80 mx-auto" />

The exit point slides **down** the slab wall — same principle: away from the closest point.

<!-- ~1 min. Here y(p) >= y(q) is used again: p sits above the exit, so
down = away. -->

---

## Lemma 2.1 — degenerate case

<img src="../figs/chapter2/lemma21/lemma21_case_vertical.gif" class="h-80 mx-auto" />

$a, b$ share an $x$-coordinate: the slab **is** the wall — nothing new happens.

<!-- ~1 min total for this slide, can compress. Unification: in all three
cases o slides away from the point nearest p and lands on an endpoint. -->

---

## One guess, concretely

<img src="../figs/chapter3/algorithm/guess.png" class="h-95 mx-auto" />

<!-- ~1 min. One iteration of the O(n^{2k}): anchors per type, Psi = the
2k guessed disks. This happens to be the CORRECT guess — the algorithm
doesn't know that. -->

---

## Most guesses are nonsense — and that's fine

<img src="../figs/chapter3/algorithm/invalid_guess.png" class="h-90 mx-auto" />

<div class="text-sm opacity-70">
If $\Psi$ isn't itself pairwise intersecting: discard (an $O(k^2)$ check). Wrong-but-valid guesses just produce smaller cliques and lose the max.
</div>

<!-- ~1 min, cuttable. Soundness in one breath: no guess can output a
non-clique; the correct guess is never detected, only out-competed for. -->

---

## The slabs of the guess

<img src="../figs/chapter3/algorithm/slabs.png" class="h-95 mx-auto" />

<!-- ~1 min. For the correct guess, every disk of C has its center in its
own type's slab — that's what "leftmost/rightmost of C_i" MEANS. -->

---

## The filter: $X$ and $Y$ are born

<img src="../figs/chapter3/algorithm/filter.png" class="h-95 mx-auto" />

<!-- ~1.5 min. Keep a disk iff center in its type's slab AND intersects
every disk of Psi. Upper survivors X (violet), lower Y (magenta). Read the
discard reasons aloud: slab misses, Psi misses. -->

---

## Lemma 3.1 — the survivors are two cliques

> For all $i, j$: the disks of $X_i \cup X_j$ are mutually adjacent. (Same for $Y$.)

**One rule generates every case:** the anchors come from the type of the **lower** point.

<v-clicks>

- lower point $q$ (type $j$) supplies the slab **and** the anchors $a_j, b_j$;
- Lemma 2.1: $|pq| \le \max\{|pa_j|, |pb_j|\}$;
- $p$'s disk intersects both anchor disks (they're in $\Psi$!) $\Rightarrow \max\{|pa_j|, |pb_j|\} \le r_i + r_j$;
- $|pq| \le r_i + r_j$ — **exactly** the intersection condition. $\square$

</v-clicks>

<!-- ~2 min. The relay: geometry (2.1) hands off to filtering (Psi
distances). The bound produced is always exactly the bound needed. Note
what the proof DOESN'T use: that the guess is correct. That's soundness. -->

---

## $X$ is one clique — guaranteed

<img src="../figs/chapter3/algorithm/x_clique.png" class="h-95 mx-auto" />

<!-- ~1 min. Bold edge: within X. Thin gray: to Psi, by construction. Holds
for EVERY valid guess, not just the correct one. -->

---

## But $X \cup Y$ is **not** a clique

<img src="../figs/chapter3/algorithm/missing_edges.png" class="h-95 mx-auto" />

<!-- ~1 min. s3 and s6 both survived, but can't coexist. Also note: s6 is in
the union but NOT in C — the containment C ⊆ Psi∪X∪Y is strict. This gap
is exactly why one more step exists. -->

---

## The reduction: two cliques + missing cross-edges

<img src="../figs/chapter3/algorithm/complement.png" class="h-90 mx-auto" />

<v-click>

<div class="text-sm">

clique in $X \cup Y$ $=$ independent set in complement $H$ *(definition)* — $H$ **bipartite** *(Lemma 3.1)* — $\alpha(H) = |X{\cup}Y| - \tau(H)$ *(Gallai)* — $\tau(H) = \nu(H)$ *(Kőnig, bipartite)* — $\nu$ by max matching: **solved problem**, this is the $f(n)$.

</div>

</v-click>

<!-- ~2.5 min. Do the arithmetic aloud: 3 - 1 = 2, chosen {s3, b4}. The
chain is stated, the computation black-boxed. If asked "how does the
matching give the clique": Gallai then Konig — NEVER "take the larger
side" (false in general; see Q&A notes). -->

---

## Assembly

<img src="../figs/chapter3/algorithm/assembly.png" class="h-95 mx-auto" />

<!-- ~1 min. Output = Psi ∪ chosen: a genuine clique (everything meets
Psi; Psi validated). Take the max over all O(n^{2k}) iterations. For the
correct guess the output has size >= |C|; soundness caps it at |C|. -->

---

## The cost ledger

| step | cost |
| --- | --- |
| guesses: $\left[\binom{n}{0}+\binom{n}{1}+\binom{n}{2}\right]^k$ | $O(n^{2k})$ iterations |
| $\Psi$ pairwise check | $O(k^2)$ |
| filter — each disk tested once **against its own type**, $\sum_i n_i = n$ | $O(nk)$ |
| build the graph on $X \cup Y$ | $O(n^2)$ |
| maximum matching | $f(n)$ |

$$\textbf{Total: } O\!\left(n^{2k}\,(f(n) + n^2)\right)$$

<!-- ~2 min. The n^{2k} IS the guessing. Inside each guess everything is
cheap. The "each disk once" beat: no k·n double count. -->

---

## Results

**Theorem 3.2.** A maximum clique in a disk graph with $k$ radius types is computable in $O(n^{2k}(f(n)+n^2))$ time.

<v-clicks>

- **Settles Cabello's question:** $k = 2$ is polynomial. ✓
- Same slab idea → precompute max cliques for **all rectangular range queries** over unit disks in $O(n^5 \log n)$ — factor $n^{4/3}$ faster than lens-based.
- Extends to **ball graphs** with centers on $r$ planes: $O(n^{2rk}\,\mathrm{poly}(n,r))$ — contrast: general ball graphs are NP-hard.

</v-clicks>

<!-- ~1.5 min. Bonus results at one-sentence depth each; the technique
generalizes, details in the paper. -->

---

## What this is — and isn't

- Polynomial **for every fixed $k$** — but $k$ sits in the exponent: this is **XP**, not FPT ($f(k)\cdot n^c$).
- Why: the witness $\Psi$ is **solution-defined**; enumerating a size-$2k$ witness costs $n^{\Theta(k)}$. Avoiding that enumeration — nobody knows how.
- General disk graphs (unbounded radii): **open in both directions.** No algorithm, no hardness. The ball-graph contrast says the boundary is genuinely subtle.

<!-- ~1.5 min. Vocabulary matters here: XP not FPT. Don't speculate on
NP-hardness. The witness-size framing ties back to the misconception
slide: difficulty = how much solution-defined information you must buy. -->

---
layout: center
class: text-center
---

# Epilogue

### Why did this take 35 years?

<div class="pt-4 text-sm opacity-70">(the promised story — time permitting)</div>

<!-- Transition. If short on time: skip to Thank You, tell them the
epilogue is in the slides. -->

---

## 1990: the lens

<img src="../figs/chapter4/ccj_lens.png" class="h-95 mx-auto" />

<!-- ~2.5 min. CCJ's recipe in our color grammar: guess the farthest pair
(green), members live in the lens, the line through the pair splits it
into two guaranteed cliques — cross edges sometimes missing — matching.
Sound familiar? Same skeleton. Companion figure: the equilateral-triangle
lens split (chapter2 lens_geometry) if asked how the split is proven. -->

---

## The deception of the lens

<img src="../figs/chapter6/lens_deception.png" class="h-95 mx-auto" />

<!-- ~2.5 min. Two radii, same recipe: small-lens split still works, but
u1, u2 — same side, both legal — miss each other. Each extra guess makes
more slices adjacent; you always feel ONE guess away. That's why 35 years:
the lens seduces. The fix wasn't more guessing — it was a different split. -->

---
layout: center
---

## Same framework — different split

| | CCJ 1990 (unit) | Keil–Mondal 2025 ($k$ radii) |
| --- | --- | --- |
| guess | farthest pair | leftmost + rightmost **per type** |
| region | lens | vertical slabs |
| two camps | lens halves | upper / lower slabs |
| forced by | farthest-pair geometry | **Lemma 2.1** |
| finish | bipartite matching | bipartite matching |

<div class="pt-4 text-center text-sm opacity-80">
The framework was right all along. The <b>split</b> was wrong.
</div>

<!-- ~1 min. The closing beat. Land the last sentence and stop talking. -->

---
layout: center
class: text-center
---

# Thank you

Questions?

<div class="pt-8 opacity-60 text-sm">
Keil & Mondal, SoCG 2025 &middot; arXiv:2404.03751<br>
figures: github.com/guyo13/openu-cg-seminar
</div>
