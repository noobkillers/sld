import uuid
from typing import List

import networkx as nx

from app.models.schemas import Connectivity, DigitalTwin, Equipment, Rating


class DigitalTwinBuilder:
    def __init__(self) -> None:
        self.graph = nx.DiGraph()

    def add_equipment(self, name: str, equipment_type: str, rating: Rating) -> Equipment:
        equipment_id = str(uuid.uuid4())
        semantic_id = f"{equipment_type[:2].upper()}_{equipment_id.split('-')[0]}"
        equipment = Equipment(
            id=equipment_id,
            semantic_id=semantic_id,
            name=name,
            equipment_type=equipment_type,
            rating=rating,
            criticality=3,
        )
        self.graph.add_node(equipment.id, data=equipment)
        return equipment

    def connect(self, upstream: Equipment, downstream: Equipment, relation: str = "feeds") -> Connectivity:
        self.graph.add_edge(upstream.id, downstream.id, relation=relation)
        return Connectivity(from_id=upstream.id, to_id=downstream.id, relation=relation)

    def build(self) -> DigitalTwin:
        equipment = [self.graph.nodes[node]["data"] for node in self.graph.nodes]
        connectivity: List[Connectivity] = []
        for source, target, data in self.graph.edges(data=True):
            connectivity.append(
                Connectivity(from_id=source, to_id=target, relation=data.get("relation", "feeds"))
            )
        return DigitalTwin(equipment=equipment, connectivity=connectivity)
