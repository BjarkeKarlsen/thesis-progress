# Worked example: the storage-update function F

This explains the notation

\[
F : \mathcal X \times \mathbb R_{\geq 0}^{|\mathcal K|} \times \mathbb R_{\geq 0}^{|E|} \times \mathbb R_{\geq 0}^{|E|} \to \mathcal X.
\]

The values below are invented only to demonstrate the meaning of the notation. The thesis specifies the exact forms of the objective terms later.

---

## 1. Small warehouse

Assume:

- Two SKU types: \(\mathcal K=\{A,B\}\).
- Three storage vertices: \(V_{\mathrm{str}}=\{s_1,s_2,s_3\}\).
- Four directed graph edges: \(E=\{e_1,e_2,e_3,e_4\}\).
- A storage update every \(\Delta=10\) timesteps.
- Each unit consumes one capacity unit; every storage vertex has capacity 8.

Therefore, the demand input contains two numbers, while the traversal and waiting inputs each contain four numbers.

## 2. Prior storage configuration

The configuration records units of each SKU at each storage vertex:

| SKU | \(s_1\) | \(s_2\) | \(s_3\) |
|---|---:|---:|---:|
| \(A\) | 8 | 0 | 0 |
| \(B\) | 0 | 5 | 3 |

For example,

\[
x_{t-\Delta}(A,s_1)=8.
\]

This says that eight units of SKU \(A\) are at vertex \(s_1\).

Check capacity:

| Vertex | Calculation | Capacity | Feasible? |
|---|---:|---:|---|
| \(s_1\) | \(8+0=8\) | 8 | Yes |
| \(s_2\) | \(0+5=5\) | 8 | Yes |
| \(s_3\) | \(0+3=3\) | 8 | Yes |

So the old configuration is feasible:

\[
x_{t-\Delta}\in\mathcal X.
\]

The free capacity is 0 at \(s_1\), 3 at \(s_2\), and 5 at \(s_3\).

## 3. Input 1: demand estimate

At the next storage epoch, suppose the demand estimate is

\[
\hat\rho_t=(20,6).
\]

The ordering is \(A,B\). Thus the estimate says that SKU \(A\) is expected to have demand 20, while SKU \(B\) is expected to have demand 6.

It is one vector with one entry for each SKU:

\[
\hat\rho_t\in\mathbb R_{\geq0}^{|\mathcal K|}.
\]

## 4. Input 2: traversal estimate

Suppose the edge order is \(e_1,e_2,e_3,e_4\), and the measured traffic estimate is

\[
\hat\mu_t=(90,85,20,15).
\]

This provides one estimate per edge. Here, \(e_1\) and \(e_2\) have been used much more often than the other edges. Imagine that the common route to \(s_1\) uses those two busy edges.

\[
\hat\mu_t\in\mathbb R_{\geq0}^{|E|}.
\]

## 5. Input 3: waiting estimate

Suppose the estimated waiting associated with the same edges is

\[
\hat w_t=(30,28,3,2).
\]

The first two entries are large. Therefore traffic near the route to \(s_1\) is not merely concentrated; it is also creating delays through contention.

\[
\hat w_t\in\mathbb R_{\geq0}^{|E|}.
\]

The estimates may be real-valued because they can be averages, rates, or smoothed predictions, rather than raw integer counts.

## 6. All inputs enter F together

The storage rule uses all four inputs:

\[
x_t=F(x_{t-\Delta},\hat\rho_t,\hat\mu_t,\hat w_t).
\]

It sees that:

- SKU \(A\) has high demand.
- The route serving its current storage vertex \(s_1\) is heavily used.
- That route also has high waiting.
- Vertex \(s_2\) has room for three more units.

A possible output is:

| SKU | \(s_1\) | \(s_2\) | \(s_3\) |
|---|---:|---:|---:|
| \(A\) | 5 | 3 | 0 |
| \(B\) | 0 | 5 | 3 |

The rule has moved three units of SKU \(A\) from \(s_1\) to \(s_2\). Future pickup tasks for \(A\) can now use either storage location, if the task-generation and assignment rules permit it.

Check the new capacities:

| Vertex | Calculation | Capacity | Feasible? |
|---|---:|---:|---|
| \(s_1\) | \(5+0=5\) | 8 | Yes |
| \(s_2\) | \(3+5=8\) | 8 | Yes |
| \(s_3\) | \(0+3=3\) | 8 | Yes |

Thus

\[
x_t\in\mathcal X.
\]

That final condition is crucial: F is allowed to adapt storage, but it is not allowed to overfill a vertex.

## 7. Why the SKUs are coupled

A tempting but infeasible decision would be to move five units of \(A\) into \(s_2\). Since \(s_2\) already holds five units of \(B\), the resulting occupancy would be

\[
5+5=10.
\]

The capacity is 8, so this would violate feasibility:

\[
10>8.
\]

Therefore, the placement decision for SKU \(A\) cannot be made without looking at SKU \(B\). Both compete for the same capacity at \(s_2\). This is the meaning of capacity coupling.

## 8. How the objective selects an output

A particular storage rule can compare feasible candidate configurations using

\[
\alpha D(x;\hat\rho_t)+\beta K(x;\hat\mu_t,\hat w_t)+\chi R(x,x_{t-\Delta}).
\]

The three terms represent different costs:

- \(D\): access cost. High-demand SKUs should not be unnecessarily far from the delivery area.
- \(K\): congestion exposure. High-demand SKUs should not force too many robots through the same busy corridor.
- \(R\): reassignment cost. Changing inventory locations has a cost, so the layout should not be reorganized for trivial gains.

For illustration, suppose the rule compares these candidates:

| Candidate | Description | \(D\) | \(K\) | \(R\) |
|---|---|---:|---:|---:|
| Old layout | Keep all A at \(s_1\) | 10 | 50 | 0 |
| Split A | Move 3 units of A to \(s_2\) | 14 | 20 | 3 |
| Spread A widely | Put A at all three vertices | 24 | 12 | 8 |

Set the illustrative weights to

\[
\alpha=1.
\]

\[
\beta=1.
\]

\[
\chi=2.
\]

For the split layout, multiply each term by its weight:

\[
1(14)=14.
\]

\[
1(20)=20.
\]

\[
2(3)=6.
\]

Then add the weighted costs:

\[
14+20+6=40.
\]

For the old layout:

\[
1(10)+1(50)+2(0)=60.
\]

For the widely spread layout:

\[
1(24)+1(12)+2(8)=52.
\]

In this example, the split layout has the smallest score:

\[
40<52<60.
\]

It would be selected. It accepts a modest increase in travel distance, but substantially reduces congestion without moving inventory everywhere.

## 9. What F does and does not specify

The type signature of F tells you:

1. What information the rule may receive.
2. That its output must be a feasible storage configuration.

It does not tell you the exact formulas for \(D\), \(K\), and \(R\), nor the exact algorithm used to search all feasible configurations. Those are design choices for the method.

The fixed-storage baseline is another valid rule:

\[
F_{\mathrm{fix}}(x,\hat\rho,\hat\mu,\hat w)=x.
\]

It accepts the same four inputs but ignores the estimates and returns the old configuration unchanged.

## 10. Recall check

In the example, why is moving three units of SKU A to \(s_2\) feasible, but moving five units there is infeasible?
