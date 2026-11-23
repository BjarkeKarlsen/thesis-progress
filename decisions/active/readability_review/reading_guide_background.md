# Reading guide for the Background and Related Work review

Written 2026-11-18 for `review_background_related.pdf`. Each entry gives the link, a TL;DR, what the
thesis uses it for and what to check while reading.

**About the TL;DRs.** Unless an entry says otherwise, I wrote the TL;DR and the link from memory.
The titles were checked on Crossref in the last session, but the DOIs and arXiv numbers were not.
Check that each link opens the right paper. Tick an entry once its abstract (at least) is read.

Order: read part 1 first, because those sources replace weak ones that are already in the text.

---

## 1. Replacements for weak sources (Question 5)

### [x] Reyes, Solano-Charris and Montoya-Torres (2019). The storage location assignment problem: A literature review
- Link: https://doi.org/10.5267/j.ijiec.2018.8.001 (International Journal of Industrial Engineering Computations 10(2))
- TL;DR: A survey of the storage location assignment problem (SLAP). It sorts the work by the
  information it uses (item, product, or no information) and by the storage policy (random, dedicated,
  class-based). It also sorts it by how the problem is solved (exact, heuristic, metaheuristic).
- Replaces: Gadeyne (2024), a company blog.
- Thesis uses it for: what "cheap" means in storage (short travel distance or picking time) and that
  storage is chosen by a rule.
- Check: that it states the cost is usually travel distance or time, and that it names random storage
  next to the two classic rules.

### [x] Ma (2022). Graph-Based Multi-Robot Path Finding and Planning
- Link: https://doi.org/10.1007/s43154-022-00083-8 (Current Robotics Reports 3). **Already in
  `papers/crr22.pdf`.**
- TL;DR: A short survey of MAPF and its variants, including lifelong MAPD. It covers the main solver
  families, search based such as CBS, prioritised planning and rule based, and what each guarantees.
- Replaces: Hönig et al., a teaching handout.
- Thesis uses it for: why prioritised planning gives no guarantee (already checked last session). It
  could also give the sentence "solvers are centralised, decentralised or a mix" that would replace
  Wang (2009), see Question 4.
- Check: whether it says that centralised and decentralised solvers are two ends of one range, in words
  close enough to cite.

### [x] Yu and LaValle (2013). Structure and Intractability of Optimal Multi-Robot Path Planning on Graphs
- Link: https://doi.org/10.1609/aaai.v27i1.8541 (AAAI 2013)
- TL;DR: It proves that finding the best MAPF solution on a graph is NP-hard, whether "best" means
  the shortest makespan or the shortest total distance.
- Replaces: LaValle (2006), a planning textbook.
- Thesis uses it for: "finding the cheapest solution is NP-hard".
- Check: which cost measures the proof covers. The thesis should only claim those.

### [x] Hardin (1968). The Tragedy of the Commons
- Link: https://math.uchicago.edu/~shmuel/Modeling/Hardin,%20Tragedy%20of%20the%20Commons.pdf (Science 162)
- TL;DR: An essay, not an experiment. Herders who each add one more animal to a shared pasture
  each gain a little, but together they ruin the pasture. A shared resource that everyone may use
  freely tends to be overused.
- Replaces: the CoMSES Net model page.
- Thesis uses it for: congestion as a commons. Each agent's choice looks sensible on its own, but
  together the choices overload the aisles.
- Check: nothing special. It is the standard source for this idea.

### [ ] Tien and Qi-lee (2022). Enhancing vehicle routing problem solutions through deep reinforcement learning and graph neural networks
- Link: https://ieia.ristek.or.id/index.php/ieia/article/view/64 (International Journal of Enterprise Modelling 16(3)).
  This one is from `references.bib`.
- TL;DR: Combines a GNN with deep reinforcement learning to solve vehicle routing problems.
- Status: it stays for now, but it is a small journal. If you know a better-known paper on a GNN with
  RL for routing, it can replace this one. Kool, van Hoof and Welling (2019), "Attention, Learn to
  Solve Routing Problems!" (ICLR), is the usual one, but it uses attention, not a GNN in the strict sense.
- Check: that the paper really uses a GNN and RL on a VRP.
Here the link was bad but working in the latex bib reference and was different in there... however it does not work and maybe should just be removed.-.
---

## 2. New papers to add (Question 6)

These go in the merged section on graph policies and messages between agents, and in the
congestion section (Gue et al.).

### [x] Q. Li, Gama, Ribeiro and Prorok (2020). Graph Neural Networks for Decentralized Multi-Robot Path Planning
- Link: https://arxiv.org/abs/1912.06095 (IROS 2020)
- TL;DR: Each robot sees a small window of a grid map. A CNN turns the window into features, and a
  GNN over the robots passes those features to nearby robots, so robots that cannot see far share
  what they see. It is trained by copying an expert planner (imitation learning), not by RL.
- Thesis uses it for: one example of a GNN over agents that lets agents exchange messages.
- Check: that it is imitation learning only. If so, the text must not call it reinforcement learning.

### [x] Q. Li, Lin, Liu and Prorok (2021). Message-Aware Graph Attention Networks for Large-Scale Multi-Robot Path Planning (MAGAT)
- Link: https://arxiv.org/abs/2011.13219 (IEEE Robotics and Automation Letters 6(3))
- TL;DR: The follow-up to the paper above. Each robot weighs the messages it receives with attention,
  so it can listen more to the neighbours that matter. It scales to larger teams than it was trained on.
- Thesis uses it for: a second GNN over agents, with attention on the messages.
- Check: that it is also imitation learning, and how many robots it was tested with.

### [ ] Ma, Luo and Ma (2021). Distributed Heuristic Multi-Agent Path Finding with Communication (DHC)
- Link: https://arxiv.org/abs/2106.11365 (ICRA 2021)
- TL;DR: A decentralised MAPF policy trained with reinforcement learning. Each agent gets heuristic
  hints, the shortest-path distances to its goal along several routes. Agents talk to nearby agents
  through a graph network. It needs no expert planner to copy.
- Thesis uses it for: a GNN over agents trained by RL without copying a planner, the closest of the
  three to the decentralised controller with messages.
- Check: that it is RL without imitation, and what its heuristic input is. The thesis's distance
  label on each vertex may be similar.

### [x] Gue, Meller and Skufca (2006). The effects of pick density on order picking areas with narrow aisles
- Link: https://doi.org/10.1080/07408170600809341 (IIE Transactions 38(10))
- TL;DR: Human pickers in narrow aisles cannot pass each other, so they wait and lose time. The
  paper models how much time is lost as more items are picked per aisle (pick density).
- Thesis uses it for: "Pickers in narrow aisles lose time blocking each other." This sentence is
  marked orange (from memory).
- Check: the abstract, and that blocking is the subject. If so, the sentence stands.

---

## 3. Already cited, still unchecked (orange "Check" lines)

### [x] Weidinger, Boysen and Briskorn (2018). Storage Assignment with Rack-Moving Mobile Robots in KIVA Warehouses
- Link: https://doi.org/10.1287/trsc.2018.0826 (Transportation Science 52(6)). This one is from `references.bib`.
- TL;DR: In a Kiva warehouse a robot carries a whole shelf to a picker and then has to put it back
  somewhere. The paper decides where each shelf goes back, so later trips are short.
- Text says: "decide where a robot puts a shelf back after each visit". There is no result yet.
- Check: the main result in one sentence (how much shorter the trips are, compared with what).
- I do not have access

### [x] Merschformann, Lamballais, de Koster and Suhl (2019). Decision Rules for Robotic Mobile Fulfillment Systems
- Link: https://doi.org/10.1016/j.orp.2019.100128 (Operations Research Perspectives 6). This one is from `references.bib`.
- TL;DR: A simulation study of robotic warehouses where robots carry shelves. It compares simple rules
  for assigning orders, choosing shelves and storing them, and finds which choices matter most for
  throughput.
- Text says: "compare simple decision rules ... in a simulation with realistic robot movement". There
  is no result yet.
- Check: which decision mattered most. That is the one-sentence result to add.

### [ ] Y. Li, Zhang, Wang and Chen (2023). Adaptive Warehouse Storage Location Assignment with Considerations to Order-Picking Efficiency and Worker Safety
- Bib entry: Engineering Management in Production and Services 15(4), pages 7 to 20.
- **Check first that it exists.** The bib entry says Taylor & Francis as the publisher, but that
  journal is published by Sciendo (De Gruyter). The text describes it only from its title. Search the
  exact title on Google Scholar. If no paper with this title and these authors turns up, remove it.
- Text says: "adapt storage to picking efficiency and to worker safety".
- https://dro.deakin.edu.au/articles/journal_contribution/Adaptive_warehouse_storage_location_assignment_with_considerations_to_order-picking_efficiency_and_worker_safety/24313819?file=47420341

### [x] Lau and Sengupta (2022). The Multi-Agent Pickup and Delivery Problem: MAPF, MARL and Its Warehouse Applications
- Link: https://arxiv.org/abs/2203.07092. **Already in `papers/2203.07092v1.pdf`.**
- TL;DR: A survey of MAPD in warehouses, covering both planning (MAPF) and learning (MARL) methods.
  The word "storage" does not appear in it (checked last session).
- One old sentence still to check: "In the systems they survey, the pickup and delivery locations a
  policy trains on are fixed by the environment." Skim the warehouse section. If the survey does not
  say this or show it clearly, cut the sentence.

---

## 4. From memory, to confirm

The review marks these orange because I described them without reading them. Most overlap with part 2.

- [ ] Gue et al. (2006), see part 2.
- [ ] MAGAT, see part 2.
- [ ] DHC, see part 2.

---

## After reading

For each paper, note one of these, so the next version of the review can use it:
- **keep**, with the one-sentence result if the text needs one
- **change**, with what the text gets wrong
- **drop**, because the paper does not exist or does not say what the thesis needs
