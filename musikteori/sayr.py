import collections
import os
import pathlib
import sys

import numpy

if sys.platform == "win32":
    path = pathlib.Path(r"C:\Program Files\Graphviz\bin")
    if path.is_dir() and str(path) not in os.environ["PATH"]:
        os.environ["PATH"] += f";{path}"

import networkx
import maqamator
from typing import Dict, List


class Sayr:
    def __init__(
        self,
        ajnas: Dict[str, maqamator.Jins],
        bottom: str,
        bottom_pitch: int,
        bottom_degree: int,
        depth: int,
        topk: List[int] = None,
    ):
        self.ajnas = ajnas
        self.bottom = bottom
        self.bottom_tonic_pitch = bottom_pitch
        self.bottom_degree = bottom_degree
        self.depth = depth
        self.graph = networkx.DiGraph()
        self.topk = topk
        self._create_graph()

    def add_node(
        self,
        *,
        name: str,
        root_pitch: int,
        tonic_pitch: int,
        jins: maqamator.Jins,
        degree: int,
        similarity: float,
        depth: int,
    ):

        identity = f"{name} {degree} : {int(root_pitch)}/{int(tonic_pitch)}"
        self.graph.add_node(
            identity,
            name=name,
            root_pitch=root_pitch,
            tonic_pitch=tonic_pitch,
            jins=jins,
            degree=degree,
            similarity=similarity,
            depth=depth,
        )
        return identity

    def _create_graph(self):
        identity = self.add_node(
            name=self.bottom,
            root_pitch=self.bottom_tonic_pitch + min(self.ajnas[self.bottom].pitches),
            tonic_pitch=self.bottom_tonic_pitch,
            jins=self.ajnas[self.bottom],
            degree=self.bottom_degree,
            similarity=float("inf"),
            depth=0,
        )
        self._expand_graph(identity, 1)
        # nodes_to_remove = [
        #     node for node, in_deg in self.graph.in_degree() if in_deg <= 1 and self.graph.nodes[node]["depth"] > 1
        # ]
        # self.graph.remove_nodes_from(nodes_to_remove)
        nodes_to_remove = [
            node
            for node, out_deg in self.graph.out_degree()
            if out_deg <= 0 and self.graph.nodes[node]["depth"] < self.depth
        ]
        self.graph.remove_nodes_from(nodes_to_remove)

    def _similarity_score(self, source_pitches, dest_pitches, threshold=0.25):
        used_indices = []  # To keep track of used elements in dest_pitches

        # Iterate through each pitch in source_pitches
        for pitch in source_pitches:
            closest_distance = None
            closest_index = None

            for i, dest_pitch in enumerate(dest_pitches):
                if i not in used_indices:  # Avoid double counting
                    # Try some module octave stuff
                    distance = abs((pitch % 12.0) - (dest_pitch % 12.0))
                    if distance < threshold:
                        if (closest_distance is None) or (distance < closest_distance):
                            closest_distance = distance
                            closest_index = i

            if closest_index is not None:
                used_indices.append(closest_index)

        return len(used_indices)

    def _expand_graph(self, source_id, current_depth):
        if current_depth > self.depth:
            return

        source_name: str = self.graph.nodes[source_id]["name"]
        source_root_pitch: int = self.graph.nodes[source_id]["root_pitch"]
        source_jins: maqamator.Jins = self.graph.nodes[source_id]["jins"]
        source_degree: int = self.graph.nodes[source_id]["degree"]
        bestkwargslist = []
        for dest_name, dest_jins in self.ajnas.items():
            if source_name == dest_name:
                continue
            best_root_pitch = None
            best_tonic_pitch = None
            best_modulation = None
            best_similarity = 0
            for source_modulation in source_jins.modulation_pitches:
                for dest_modulation in dest_jins.modulation_pitches:
                    dest_tonic_pitch = source_root_pitch + source_modulation - dest_modulation
                    dest_root_pitch = dest_tonic_pitch + min(dest_jins.pitches)
                    if dest_root_pitch > source_root_pitch:
                        source_pitches = source_root_pitch + numpy.array(
                            source_jins.pitches + source_jins.extension_pitches
                        )
                        dest_pitches = dest_root_pitch + numpy.array(dest_jins.pitches + source_jins.extension_pitches)
                        similarity = self._similarity_score(source_pitches=source_pitches, dest_pitches=dest_pitches)
                        if similarity > best_similarity:
                            best_similarity = similarity
                            best_tonic_pitch = dest_tonic_pitch
                            best_root_pitch = dest_root_pitch
                            best_modulation = source_modulation
            if best_root_pitch is not None and best_tonic_pitch is not None and best_modulation is not None:
                bestkwargslist.append(
                    {
                        "name": dest_name,
                        "root_pitch": best_root_pitch,
                        "tonic_pitch": best_tonic_pitch,
                        "jins": dest_jins,
                        "degree": source_degree + source_jins.pitches.index(best_modulation),
                        "similarity": best_similarity,
                        "depth": current_depth,
                    }
                )
        bestkwargslist = sorted(bestkwargslist, key=lambda x: x["similarity"], reverse=True)
        for ix, bestkwargs in enumerate(bestkwargslist):
            if self.topk is None or ix < 1 + self.topk[current_depth]:
                dest_id = self.add_node(**bestkwargs)
                self.graph.add_edge(source_id, dest_id)
                self._expand_graph(dest_id, current_depth=current_depth + 1)
            else:
                pass

    def visualize(self, filename="sayr_graph.png"):
        A = networkx.nx_agraph.to_agraph(self.graph)
        A.graph_attr["rankdir"] = "LR"
        A.node_attr["shape"] = "rect"

        # Assign ranks based on tonic_pitch
        for node, data in self.graph.nodes(data=True):
            node_attr = A.get_node(node)
            tonic_pitch = data.get("tonic_pitch", 0)  # Default to 0 if tonic_pitch is missing
            node_attr.attr["rank"] = str(tonic_pitch)

            # Node styling
            if tonic_pitch == 0:
                node_attr.attr["fillcolor"] = "black"
                node_attr.attr["fontcolor"] = "white"
                node_attr.attr["style"] = "rounded,filled"
            else:
                node_attr.attr["fillcolor"] = "lightgray"
                node_attr.attr["style"] = "filled"

        # Edge labels (if applicable)
        for u, v, data in self.graph.edges(data=True):
            u_degree = self.graph.nodes[u]["degree"]
            v_degree = self.graph.nodes[v]["degree"]
            label = f"{u}->{v} ({u_degree + v_degree}) : {self.graph.nodes(data=True)[v]["similarity"]}"
            A.get_edge(u, v).attr["label"] = label

        # Draw the graph to the specified filename
        A.draw(filename, prog="dot", format="png", args="-GedgeLabelJust=cent")

        # Return the generated file path
        return filename


# My best effort to reproduce maqam zanjaran sayr
zanjaran = Sayr(
    {
        key: value
        for key, value in maqamator.arabic_ajnas.items()
        if key in {"Ajam3", "Ajam5", "Hijaz", "SabaDalanshin", "Nahawand", "Nikriz", "Hijazkar"}
    },
    bottom="Hijaz",
    bottom_pitch=0,
    bottom_degree=1,
    depth=2,
)
zanjaran.visualize("zanjaran.png")

iraq = Sayr(
    {
        key: value
        for key, value in maqamator.arabic_ajnas.items()
        if key in {"Rast", "Sikah", "Bayati", "Hijaz", "Saba", "Nahawand"}
    },
    bottom="Sikah",
    bottom_pitch=0,
    bottom_degree=1,
    depth=2,
)
iraq.visualize("iraq.png")

for source in maqamator.arabic_ajnas.keys():
    from_source = Sayr(maqamator.arabic_ajnas, bottom=source, bottom_pitch=0, bottom_degree=1, depth=1, topk=[1, 5])
    from_source.visualize(f"from_{source}.png")
