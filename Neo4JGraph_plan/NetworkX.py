"""
Formula 1 Knowledge Graph Builder, Neo4j Exporter & PNG Visualizer
====================================================================
Constructs the property graph (MultiDiGraph) from Gold tier parquet data,
exports GraphML and GEXF formats, and renders a high-resolution PNG visualization.

Author: Manohar Zalki & Project Group
Course: Data Management Winter 2026/27
"""

import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


def build_f1_knowledge_graph(gold_dir="../data/gold"):
    """Builds a NetworkX MultiDiGraph representing the F1 championship ecosystem
    by reading directly from the project's Gold tier parquet folders.
    """
    print("[INFO] Loading Gold tier datasets...")

    try:
        results_df = pd.read_parquet(os.path.join(gold_dir, "fact_session_results", "fact_session_results.parquet"))
        drivers_df = pd.read_parquet(os.path.join(gold_dir, "dim_drivers", "dim_drivers.parquet"))
        constructors_df = pd.read_parquet(os.path.join(gold_dir, "dim_constructors", "dim_constructors.parquet"))
        races_df = pd.read_parquet(os.path.join(gold_dir, "dim_races", "dim_races.parquet"))
    except Exception as e:
        print(f"[ERROR] Failed to load parquet files from {gold_dir}: {e}")
        return None

    G = nx.MultiDiGraph(name="F1_Championship_Knowledge_Graph")

    print("[INFO] Adding :Driver nodes...")
    for _, row in drivers_df.iterrows():
        G.add_node(
            f"Driver:{row['driver_id']}",
            labels="Driver",
            full_name=str(row.get('full_name', '')),
            dob=str(row.get('date_of_birth', '')),
            nationality=str(row.get('nationality', '')),
            wikidata_qid=str(row.get('wikidata_qid', ''))
        )

    print("[INFO] Adding :Constructor nodes...")
    for _, row in constructors_df.iterrows():
        G.add_node(
            f"Constructor:{row['constructor_id']}",
            labels="Constructor",
            name=str(row.get('constructor_name', '')),
            nationality=str(row.get('nationality', ''))
        )

    print("[INFO] Adding :Race and :Circuit nodes...")
    for _, row in races_df.iterrows():
        race_key = f"Race:{row['season']}_{row['round']}"
        G.add_node(
            race_key,
            labels="Race",
            season=int(row.get('season', 0)),
            round=int(row.get('round', 0)),
            race_name=str(row.get('race_name', '')),
            date=str(row.get('race_date', ''))
        )
        if 'circuit_id' in row and pd.notna(row['circuit_id']):
            circuit_node = f"Circuit:{row['circuit_id']}"
            if not G.has_node(circuit_node):
                G.add_node(circuit_node, labels="Circuit")
            G.add_edge(race_key, circuit_node, relation="HELD_AT")

    print("[INFO] Adding transaction fact edges (RACED_IN, DROVE_FOR)...")
    for _, row in results_df.iterrows():
        driver_node = f"Driver:{row['driver_id']}"
        constructor_node = f"Constructor:{row['constructor_id']}"
        race_node = f"Race:{row['season']}_{row['round']}"

        if G.has_node(driver_node) and G.has_node(race_node):
            G.add_edge(
                driver_node,
                race_node,
                relation="RACED_IN",
                grid_position=int(row['grid_position']) if pd.notna(row.get('grid_position')) else 0,
                final_position=int(row['final_position']) if pd.notna(row.get('final_position')) else 0,
                points=float(row['points']) if pd.notna(row.get('points')) else 0.0,
                status=str(row.get('status', ''))
            )

        if G.has_node(driver_node) and G.has_node(constructor_node):
            G.add_edge(
                driver_node,
                constructor_node,
                relation="DROVE_FOR",
                season=int(row['season'])
            )

    print(f"[SUCCESS] Graph constructed successfully! Total Nodes: {G.number_of_nodes()}, Total Edges: {G.number_of_edges()}")
    return G


def export_graph_and_render_png(G, output_dir="../Neo4JGraph_plan"):
    """Exports NetworkX graph into GraphML, GEXF, and renders a high-resolution PNG plot."""
    os.makedirs(output_dir, exist_ok=True)
    
    # GraphML Export
    graphml_path = os.path.join(output_dir, "f1_graph.graphml")
    nx.write_graphml(G, graphml_path)
    print(f"[EXPORT] GraphML written to {graphml_path}")

    # GEXF Export
    gexf_path = os.path.join(output_dir, "f1_graph.gexf")
    nx.write_gexf(G, gexf_path)
    print(f"[EXPORT] GEXF written to {gexf_path}")

    # PNG Visualization Render (taking a sampled or core component for clear plotting)
    print("[INFO] Rendering high-resolution PNG visualization...")
    plt.figure(figsize=(14, 10), dpi=300)
    
    # To keep the visualization readable, sample a connected component or top degree nodes if graph is very large
    # Here we create a sub-graph of drivers and constructors for clean aesthetic rendering
    sample_nodes = [n for n, d in G.nodes(data=True) if d.get('labels') in ['Driver', 'Constructor']][:300]
    sub_g = G.subgraph(sample_nodes)

    pos = nx.spring_layout(sub_g, seed=42, k=0.15)
    
    node_colors = []
    for node in sub_g.nodes():
        if "Driver" in node:
            node_colors.append('#1f77b4')  # Blue for drivers
        elif "Constructor" in node:
            node_colors.append('#ff7f0e')  # Orange for constructors
        else:
            node_colors.append('#2ca02c')  # Green for others

    nx.draw_networkx_nodes(sub_g, pos, node_size=40, node_color=node_colors, alpha=0.8)
    nx.draw_networkx_edges(sub_g, pos, alpha=0.2, edge_color='#888888', width=0.5)

    plt.title("Formula 1 Knowledge Graph Sample (Drivers & Constructors)", fontsize=16, fontweight='bold', color='navy')
    plt.axis('off')
    
    png_path = os.path.join(output_dir, "f1_knowledge_graph.png")
    plt.tight_layout()
    plt.savefig(png_path, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[EXPORT] High-res PNG rendered and saved to {png_path}")


if __name__ == "__main__":
    f1_graph = build_f1_knowledge_graph()
    if f1_graph:
        export_graph_and_render_png(f1_graph)