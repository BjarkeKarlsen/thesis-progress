# warehouse_types.py
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Set, Tuple, Optional, Iterable, Any, Protocol

# ---------- Basic identifiers ----------

VertexId = int
ItemTypeId = str
ItemUnitId = int
OrderId = int
TaskId = int
AgentId = int

# ---------- Warehouse graph G = (V, E) ----------

class VertexKind(Enum):
    """Partition V = V^S ∪ V^D ∪ V^B ∪ V^O."""
    STORAGE = auto()      # V^S
    DEPOT = auto()        # V^D
    BASE = auto()         # V^B
    TRANSIT = auto()      # V^O


@dataclass(frozen=True)
class Vertex:
    """A vertex v ∈ V."""
    id: VertexId
    kind: VertexKind


@dataclass(frozen=True)
class Edge:
    """An edge e ∈ E with traversal time c(e) > 0."""
    src: VertexId
    dst: VertexId
    traversal_time: float


@dataclass
class WarehouseGraph:
    """
    Directed warehouse graph G = (V, E).
    Vertices and edges can be extended with metadata as needed.
    """
    vertices: Dict[VertexId, Vertex] = field(default_factory=dict)
    edges: Dict[Tuple[VertexId, VertexId], Edge] = field(default_factory=dict)

    def add_vertex(self, vertex: Vertex) -> None:
        self.vertices[vertex.id] = vertex

    def add_edge(self, edge: Edge) -> None:
        if edge.src not in self.vertices or edge.dst not in self.vertices:
            raise ValueError("Both src and dst must be existing vertices.")
        self.edges[(edge.src, edge.dst)] = edge

    def outgoing(self, v: VertexId) -> Iterable[Edge]:
        for (src, _), e in self.edges.items():
            if src == v:
                yield e

    def incoming(self, v: VertexId) -> Iterable[Edge]:
        for (_, dst), e in self.edges.items():
            if dst == v:
                yield e


# ---------- Items I and units Q ----------

@dataclass(frozen=True)
class ItemType:
    """Item type i ∈ I."""
    id: ItemTypeId
    name: str


@dataclass(frozen=True)
class ItemUnit:
    """
    Item unit q ∈ Q with assignment ι : Q → I.
    """
    id: ItemUnitId
    type_id: ItemTypeId


# ---------- Storage placement p_t and policy s_t ----------

@dataclass
class StoragePlacement:
    """
    Storage placement p_t : Q → V^S at a given time t.
    Maps each item unit to a storage vertex.
    """
    unit_to_vertex: Dict[ItemUnitId, VertexId] = field(default_factory=dict)

    def place(self, unit_id: ItemUnitId, vertex_id: VertexId) -> None:
        self.unit_to_vertex[unit_id] = vertex_id

    def location_of(self, unit_id: ItemUnitId) -> VertexId:
        return self.unit_to_vertex[unit_id]


@dataclass
class StoragePolicySnapshot:
    """
    Storage policy s_t : I → 2^{V^S} at time t.
    For each item type, store the set of storage vertices used.
    """
    type_to_vertices: Dict[ItemTypeId, Set[VertexId]] = field(default_factory=dict)

    def storage_vertices_for(self, type_id: ItemTypeId) -> Set[VertexId]:
        return self.type_to_vertices.get(type_id, set())

    def add_storage_vertex(self, type_id: ItemTypeId, vertex_id: VertexId) -> None:
        self.type_to_vertices.setdefault(type_id, set()).add(vertex_id)


@dataclass
class StoragePolicyState:
    """
    Combined state of placement p_t and policy s_t at time t.
    """
    placement: StoragePlacement
    snapshot: StoragePolicySnapshot


# ---------- Orders and MAPD tasks ----------

@dataclass
class Order:
    """
    Customer order o ⊆ Q (finite multiset of item units).
    """
    id: OrderId
    units: List[ItemUnitId]


@dataclass
class MAPDTask:
    """
    MAPD task τ = (q, v_pick, v_del).
    """
    id: TaskId
    unit_id: ItemUnitId
    pick_vertex: VertexId
    delivery_vertex: VertexId
    release_time: int  # discrete time t when task appears


# ---------- Agents and agent state ----------

class LoadStatus(Enum):
    EMPTY = auto()
    CARRYING = auto()


@dataclass
class AgentInternalState:
    """
    Σ_a: internal variables such as load, battery level, mode.
    """
    load_status: LoadStatus = LoadStatus.EMPTY
    carried_unit_id: Optional[ItemUnitId] = None
    battery_level: float = 1.0
    mode: str = "IDLE"


@dataclass
class AgentState:
    """
    X_a = V × Σ_a for agent a.
    """
    agent_id: AgentId
    vertex_id: VertexId
    internal: AgentInternalState

    @property
    def pos(self) -> VertexId:
        """Projection pos_a : X_a → V."""
        return self.vertex_id


@dataclass
class JointSystemState:
    """
    X_t = ∏_{a∈A} X_a at time t.
    """
    agents: Dict[AgentId, AgentState] = field(default_factory=dict)


# ---------- Local observation graph for RL-GNN ----------

@dataclass
class NodeFeatures:
    """
    Features for a vertex in a local observation graph:
    congestion, queues, etc.
    """
    congestion: float = 0.0
    queue_length: int = 0


@dataclass
class EdgeFeatures:
    """
    Features for an edge in a local observation graph:
    occupancy, effective travel time, etc.
    """
    occupancy: int = 0
    travel_time: float = 0.0


@dataclass
class LocalObservationGraph:
    """
    G_a^t: local observation graph for agent a at time t.
    Includes vertices and edges within a fixed radius and messages.
    """
    center_vertex: VertexId
    vertices: Dict[VertexId, NodeFeatures] = field(default_factory=dict)
    edges: Dict[Tuple[VertexId, VertexId], EdgeFeatures] = field(default_factory=dict)
    messages: Dict[AgentId, Dict[str, float]] = field(default_factory=dict)


# ---------- Controller architectures and routing policy protocol ----------

class ControllerArchitecture(Enum):
    CENTRALISED = auto()
    SECTION_BASED = auto()
    DISTRIBUTED = auto()


@dataclass
class MAPDControllerConfig:
    """
    Describe controller architecture and sectioning of the warehouse.
    """
    architecture: ControllerArchitecture
    # For section-based controllers: map section label to vertices in that section.
    sections: Dict[str, Set[VertexId]] = field(default_factory=dict)


class RoutingPolicy(Protocol):
    """
    Protocol for routing policies; RLlib policies can conform to this
    by wrapping compute_actions into 'act'.
    """

    def act(
        self,
        agent_state: AgentState,
        task: Optional[MAPDTask],
        obs_graph: Optional[LocalObservationGraph] = None,
    ) -> Any:
        """
        Decide the next action (e.g., move to neighbour or wait).
        Return type Any so RLlib's action format can be used directly.
        """
        ...


# ---------- Transport and congestion history ----------

@dataclass
class TransportHistory:
    """
    H_t: history of observed trajectories, tasks, and congestion statistics.
    """
    edge_flows: Dict[Tuple[VertexId, VertexId], int] = field(default_factory=dict)
    edge_travel_times: Dict[Tuple[VertexId, VertexId], List[float]] = field(default_factory=dict)
    queue_lengths: Dict[VertexId, List[int]] = field(default_factory=dict)

    def record_edge_traversal(self, src: VertexId, dst: VertexId, travel_time: float) -> None:
        key = (src, dst)
        self.edge_flows[key] = self.edge_flows.get(key, 0) + 1
        self.edge_travel_times.setdefault(key, []).append(travel_time)

    def record_queue_length(self, v: VertexId, length: int) -> None:
        self.queue_lengths.setdefault(v, []).append(length)


# ---------- Storage feedback function and coupled/decoupled policies ----------

class StorageFeedbackFunction(Protocol):
    """
    F: storage policy feedback function.
    Updates s_t and p_t based on history H_t.
    """

    def update(
        self,
        current: StoragePolicyState,
        history: TransportHistory,
    ) -> StoragePolicyState:
        ...


@dataclass
class PolicyPair:
    """
    (s, π) pair representing either a decoupled or a closed-loop coupled policy.
    - If 'coupled' is False, storage updates do not depend on realised flows.
    - If 'coupled' is True, storage_feedback implements s_{t+1} = F(s_t, H_t).
    """
    storage_feedback: StorageFeedbackFunction
    routing_policy: RoutingPolicy
    coupled: bool