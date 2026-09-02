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

---

## Definitions

- A **disk graph** $\mathcal{D}$: vertices are disks, edges join intersecting disks.
- $\mathcal{D}_k$: disk graph with $k$ distinct radii ("radius types").
- A **clique** $C$: pairwise intersecting disks.

<!-- Speaker notes go after an empty HTML comment like this. -->

---
layout: two-cols
---

## The disk graph $\mathcal{D}_2$

<img src="../figs/chapter3/notation/disk_graph_fig.png" class="h-80" />

::right::

## A maximum clique $\mathcal{C}$

<img src="../figs/chapter3/notation/max_clique_fig.png" class="h-80" />

---

## Why this problem is famous

Motivation for disk graphs, and why the $k=2$ case became the interesting one.

- TODO: motivation (wireless networks, coverage)
- TODO: complexity landscape — what is open, what is settled

---

## The deception of the lens

The Clark&ndash;Colbourn&ndash;Johnson approach for **unit** disk graphs.

<img src="../figs/chapter2/perliminaries/lens_geometry.png" class="h-72 mx-auto" />

- The lens region is co-bipartite &rArr; max clique via bipartite matching.
- TODO: why this breaks for two radii.

---

## Slab geometry

<img src="../figs/chapter2/perliminaries/slab_geometry.png" class="h-80 mx-auto" />

Upper and lower slabs — the setting for Lemma 2.1.

---

## Lemma 2.1 — case (b)

<img src="../figs/chapter2/lemma21/lemma21_case_b.gif" class="h-80 mx-auto" />

The exit point $o$ slides along $\overline{ab}$, away from $m$.

---

## Lemma 2.1 — case (c)

<img src="../figs/chapter2/lemma21/lemma21_case_c.gif" class="h-80 mx-auto" />

The exit point slides down the vertical slab wall.

---

## Lemma 2.1 — degenerate case

<img src="../figs/chapter2/lemma21/lemma21_case_vertical.gif" class="h-80 mx-auto" />

$a$ and $b$ share an $x$-coordinate; the slab collapses to a line.

---
layout: two-cols
---

## Same-type clique $C_1$

<img src="../figs/chapter3/notation/single_type_clique_fig.png" class="h-80" />

::right::

## Type classes $\mathcal{C}_1, \mathcal{C}_2$

<img src="../figs/chapter3/notation/type_classes_fig.png" class="h-80" />

---

## The algorithm

TODO: Section 3 — the main algorithm and its running time.

---
layout: center
class: text-center
---

# Thank you

Questions?
