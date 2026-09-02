
# Definitions

* **A Disk Graph** - An intersection graph of disks in $\mathbb{R}^2$ .
* **An intersection graph** is a general recipe for turning a collection of geometric objects into a graph:
	- Take any family of objects — disks, line segments, rectangles, intervals on a line, whatever.
	- Make one **vertex** per object.
	- Draw an **edge** between two vertices exactly when their objects overlap (have at least one point in common).
* **Representation of a Disk** - usually given as $D(a, r)$ where $a \in \mathbb{R}^2$ is the center point of the disk  and $r \in \mathbb{R}$ is the disk's radius.
* **$|ab|$** is the **Euclidean distance** between points $a$ and $b$ (same as $||a-b||$ or $d(a,b)$)
* **An independent set** in graph theory is a set of vertices where no two vertices are connected by an edge.
* A **co-bipartite graph** is a graph whose complement is a bipartite graph.
* **A bipartite graph** is a network of dots (vertices) and lines (edges) where you can split all the dots into two separate groups so that no two connected dots belong to the same group.
## Notes

Two things worth internalizing for this paper on intersection graphs:

1. **The graph forgets the geometry.** Two very different disk arrangements can produce the same abstract graph. That's why the paper assumes the disk _representation_ (centers and radii) is given as input — recovering disks from an abstract graph is itself a hard problem (because its a complex constraints satisfaction problem).
2. **Adjacency = distance condition.** Disks D(a, r₁) and D(b, r₂) intersect exactly when |ab| ≤ r₁ + r₂. This little equivalence is used constantly in the proofs: every claim "these disks are adjacent" is really the claim "their centers are close enough." For unit disks (all radii 1), adjacent simply means centers within distance 2.
	1. Ergo - "Two disks intersect exactly when the distance between their centers is at most the sum of their radii." 

Computing a maximum clique in a **unit** disk graph (all radii are 1) was shown in polynomial time a long time ago.


## The main results
1. An algorithm for finding the maximum clique of the disk graph is found which is $O(n^{2k}poly(n))$ time complexity where $k$ is the distinct number of disk radii in the graph and $n$ are the number of disks. - Which means that for any *fixed* $k$ this is polynomial, and specifically $k=2$ which was *the* open problem.
2. An $O(n^{4/3})$ speedup factor of improvement was made to the problem of eagerly computing all rectangle range queries which find maximum cliques in a given unit disk graph of $n$ disks. Ergo - the authors precompute max cliques for all O(n⁴) canonical rectangles in O(n⁵ log n) total time, which is at least a factor n^{4/3} faster than solving each rectangle independently."
3. In contrast to the known NP-hardness result of Finding a maximum clique in an arbitrary ball graph - if we assume $k$ distinct radii of the balls and that their centers lie on $r$ parallel planes then an $O(n^{2rk}poly(n,r))$ time algorithm for computing their max clique was found by the authors.

## Why is the maximum clique problem is famous (even for k=2)?

#### Motivation for studying disk graphs
Disk graphs are useful in modelling applied contexts (e.g wireless networks) so being able to solve a maximum clique for any fixed k>1 in polynomial time is very valuable towards being able to model realistic scenarios rather than having to assume all disks are of the same radius, which forces a "degenerate" model of the problem.

#### Why it actually became famous

- **Its unresolved complexity status.** For 35+ years, nobody could prove the problem NP-hard _or_ find a polynomial algorithm. That limbo is rare and precious: most natural problems eventually fall on one side. Compare the neighbors listed in the intro — max clique is NP-hard for rays, ellipses, triangles, grounded strings, and _ball_ graphs, yet polynomial for unit disks, rectangles, trapezoids. Disk graphs sit exactly on the unmapped boundary between the two worlds.
- **The contrast with the 1990 unit-disk result.** Clark–Colbourn–Johnson solved the unit-radius case cleanly in 1990. Going from "all radii equal" to "even just _two_ radii allowed" broke every known technique — which is what made Cabello pose the k = 2 case explicitly as an open question in 2015. When a tiny generalization resists 35 years of attempts, that's fame.
- **Community attention.** The intro documents this deliberately: quoted as "an intriguing open question," "a notorious open question in computational geometry," "elusive with no new positive or negative results," a "long-standing open problem" — plus the fact that the best-known approximation (factor 2, via stabbing disks with four points) couldn't even be improved to 1.99.

## "The Deception of the Lens" - why the lens-based approach fails for two radii

### Clark–Colbourn–Johnson algorithm for max clique in UDGs

The idea here is that the intersection of disks forms a lens region such that disks whose centers are located inside the lens region, form a co-bipartite graph in the Unit Disk Graph (UDG) in which we can be find a maximum clique in polynomial time. We then simply brute-force (aka "guess") through all combinations of the two len-forming disks and report the max clique found. 

#### Why is the lens region co-bipartite?

Because if we divide it in half by line $uv$  we get 2 lens halves which are convex shapes. The extreme points of these lens halves are always distanced $d$ from each other which implies that any two points (possible disk centers) are distanced at mximum $d$ from each other which means they intersect.

**Important** - Disks from the top and bottom halves also may intersect each other! this is why it is hard to directly find the maximum clique in the subgraph of the UDG induced by the lens (it may be composed of disks from both sides!). Instead the complemantary graph is used and a max-independent-set algorithm yields exactly the max clique in the original subgraph.

**Important** - The lens we are examining here is the one formed by the two circles of radius $d$ around $u$ and $v$ it is NOT the intersection of the 2 unit disks centered at $u$ and $v$ - this is the confusing part.

**Important** - We dont really have to construct a lens in the algorithm and do all of the parititioning - simply filtering the vertices by distance to u and v suffices - the resulting subgraph is the co-bipartite one on which we compute the 2 final steps (inversion and bipartite matching). 
![](../figs/chapter2/perliminaries/lens_geometry.png)

#### Pseudo-code

```
function FindMaxCliqueUDG(Vertices, edge_threshold):
    max_clique_size = 0
    best_clique = []

    // Edge case: empty graph
    if Vertices is empty:
        return best_clique

    // Step 1: Guess the diameter pair
    for u in Vertices:
        for v in Vertices:
            d = distance(u, v)
            
            // If u and v are further apart than the graph's threshold, 
            // they do not share an edge. Skip this pair.
            if d > edge_threshold:
                continue
            
            SetA = []
            SetB = []
            
            // Step 2: Isolate the lens and partition (The Cross-Product trick)
            for w in Vertices:
                // w must be inside the lens (within distance d of both u and v)
                if distance(w, u) <= d and distance(w, v) <= d:
                    
                    // Determine which side of the uv line vertex w falls on
                    cross_product = (v.x - u.x)*(w.y - u.y) - (v.y - u.y)*(w.x - u.x)
                    
                    if cross_product >= 0:
                        SetA.append(w)
                    else:
                        SetB.append(w)
            
            // Step 3: Build the Bipartite Complement Graph
            // An edge exists here ONLY if it is missing in the original UDG
            ComplementEdges = []
            for a in SetA:
                for b in SetB:
                    // If they don't intersect in the UDG, add an edge in the complement
                    if distance(a, b) > edge_threshold: 
                        ComplementEdges.append((a, b))
            
            // Step 4: Solve via Bipartite Matching (Kőnig's Theorem)
            // Find the maximum bipartite matching (e.g., using Hopcroft-Karp)
            matching_edges = HopcroftKarp(SetA, SetB, ComplementEdges)
            
            // The size of the Maximum Independent Set is the total number 
            // of vertices minus the size of the maximum matching
            current_clique_size = (length(SetA) + length(SetB)) - length(matching_edges)
            
            // Step 5: Update global maximum
            if current_clique_size > max_clique_size:
                max_clique_size = current_clique_size
                // Extract the actual vertices of the independent set from the matching
                best_clique = ExtractIndependentSet(SetA, SetB, matching_edges)
                
    return best_clique
```
#### Why is this even working for UDGs?

1. Because geometrically, every max clique has a "diameter" - it is finite so there are 2 disks $u^*, v^*$  such that $d^* = d(u^*,v^*)$ and the distance between any other pair of disks is less than or equal to $d^*$.
2. The Inescapable Lens Containment - because of the existence of $d^*$ there can be no other vertex in the clique that will be further apart than length $d^*$ from  either $u^*, v^*$.
3. The exhaustive loop - we consider all pairs therefore we will stumble upon $u^*, v^*$.
4. The optimal len is co-bipartite - therefore - the bipartite matching algorithm on the complement graph is mathematically guaranteed to find the _exact_ Maximum Independent Set (which is equivalent to the maximum clique in the UDG).

##### The deception

The deceptive assumption was that CCJ's diameter-pair-plus-lens recipe generalizes to mixed radii — but the lens split no longer forces the two mutually-adjacent camps needed for a co-bipartite complement, and no amount of additional guessing visibly repairs it. The paper escapes by changing the guess itself: extreme-left and extreme-right disks per radius type, with slabs replacing lenses.

## Phase 3 — Lemma 2.1 (the foundation)

#### Visualization of Upper and Lower slabs
![](../figs/chapter2/perliminaries/slab_geometry.png)

### Lemma 2.1
Let $ab$ be a line segment and let $U_{ab}$ be the upper slab of ab.
Let $q = (x_q, y_q)$ be a point in $U_{ab}$.
Let $p = (x_p, y_p)$ such that $y_p \geq y_q$.
Then $|pq| \leq max\{|pa|, |pb|\}$.

Distinguish 2 scenarios:
1. $ab$ is not vertical ($x$ coords of $a$ and $b$ are different)
	1. $o$ is on $ab$
	2. $o$ is on $U_{ab}$'s wall
2. $ab$ is vertical

#### Scenario 1:
* The ray that starts at $p$ and passes through $q$ must intersect the boundary of  $U_{ab}$ at point $o$ ** because $y_p \geq y_q$**.
* It intersects either $ab$ or the sides of the slab.
* $m$ is a point such that $pm$ is perpendicular to the line on which the ray hits the boundary of $U_{ab}$.
* "Silding" $o$ away from $m$, in either direction, increases the length of $po$ monotonically up to $max\{|pa|, |pb|\}$. 
* And we get: $|pq| \leq |po| \leq max\{|pa|, |pb|\}$
#### Scenario 1 Visualized:
![](../figs/chapter2/lemma21/lemma21_case_b.gif)

![](../figs/chapter2/lemma21/lemma21_case_c.gif)


#### Scenario 2:
* $x$ coords of $a, b$ are the same ($ab$ is a vertical segment and $U_{ab}$ is a ray)
* If $y_a < y_b$ then $|pq| \leq |pa|$
* Else $y_b < y_a$ then $|pq| \leq |pb|$
#### Scenario 2 Visualized:
![](../figs/chapter2/lemma21/lemma21_case_vertical.gif)
## Phase 4 -  The Main Algorithm (Section 3)

#### Notation
* $\mathcal{D}_k$ a disk graph where the number of different types of radii is at most $k$
* The radii of $\mathcal{D_k}$ are denoted: $r_1,..,r_k: \forall_{1\leq i < j \leq k}: r_i<r_j$
* *type-i disk* is a disk of radius $r_i$
* $C_i$ is a clique that contains only disks of type $i$
* $\mathcal{C}$  is a maximum clique of $\mathcal{D}_k$ 
* $\mathcal{C_i}$  is a maximal clique in $\mathcal{C}$ where all disks are of type $i$

#### Notation Visualizations
##### Disk Graph

![](../figs/chapter3/notation/disk_graph_fig.png)
#####  Single type clique

![](../figs/chapter3/notation/single_type_clique_fig.png)

##### Maximum clique
![](../figs/chapter3/notation/max_clique_fig.png)

##### Maximum same-type cliques
![](../figs/chapter3/notation/type_classes_fig.png)
#### The algorithm in a nutshell
* We guess