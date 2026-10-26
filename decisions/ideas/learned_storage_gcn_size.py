"""Parameter count and peak memory of a storage GCN that scores every storage vertex.

Run once per fleet size in a fresh process so the peak RSS belongs to that size alone:
    ~/.venvs/rl/bin/python gcn_size.py <num_agents> <batch> <extra_features>
"""

import resource
import sys

import torch
from torch import nn

import slap_mapd_coupling.models.gnn_encoder as ge
from slap_mapd_coupling.instances.generator import GeneratorParams, fleet_defaults, generate_instance

m, batch, extra = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
torch.manual_seed(0)

graph = generate_instance(GeneratorParams(**fleet_defaults(m), wait_cost=0.2)).graph
movable = [v for v, x in graph.vertices.items() if x.role.movable]
storage = [v for v, x in graph.vertices.items() if x.role.storage]
index = {v: i for i, v in enumerate(movable)}
pairs = {tuple(sorted((index[e.source], index[e.target]))) for e in graph.edges}
n, e = len(movable), len(pairs)

# The router encoder with extra vertex features for storage (shelf fill, units of the SKU there,
# traffic and waiting through the vertex, trip distance).
ge.NODE_FEATURE_DIM = 8 + extra
enc = ge.GNNEncoder(ge.GNNEncoderConfig(num_rounds=2, hidden_width=32, communication=False, pooling="mean"))
sku_dim = 3  # demand estimate, unit size, units still to place
z_dim = enc.embedding_dim + sku_dim  # pooled mean of the whole graph plus the SKU
score = nn.Sequential(nn.Linear(z_dim + enc.embedding_dim, 32), nn.ReLU(), nn.Linear(32, 1))
value = nn.Sequential(nn.Linear(z_dim, 32), nn.ReLU(), nn.Linear(32, 1))
params = sum(p.numel() for mod in (enc, score, value) for p in mod.parameters())

x = torch.rand(batch, n, ge.NODE_FEATURE_DIM)
node_mask = torch.ones(batch, n)
edge_index = torch.tensor(sorted(pairs)).unsqueeze(0).expand(batch, -1, -1).contiguous()
edge_mask = torch.ones(batch, e)
store_idx = torch.tensor([index[v] for v in storage])
sku = torch.rand(batch, sku_dim)

before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
h = enc._embed_padded(x, node_mask, edge_index, edge_mask)  # [B, N, D]
z = torch.cat([h.mean(dim=1), sku], dim=-1)
h_s = h[:, store_idx]  # [B, S, D]
logits = score(torch.cat([z.unsqueeze(1).expand(-1, len(storage), -1), h_s], dim=-1)).squeeze(-1)
loss = torch.log_softmax(logits, -1).mean() + value(z).mean()
loss.backward()
after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

obs_bytes = n * ge.NODE_FEATURE_DIM * 4 + len(storage) * 1  # features + action mask, edges static
print(
    f"m={m:3d} |V|={n:5d} edges={e:5d} shelves={len(storage):3d} params={params:6d} "
    f"peak_fwd_bwd_MB={(after - before) / 1024:7.1f} obs_KB={obs_bytes / 1024:6.1f}"
)
