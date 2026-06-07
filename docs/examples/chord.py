# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo>=0.23.8",
#     "matplotlib>=3.3.3",
#     "networkx==3.6.1",
#     "nxviz[plotly]==0.8.0",
# ]
# [tool.uv.sources]
# nxviz = { path = "../..", editable = true }
# ///

import marimo

__generated_with = "0.23.9"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Chord Diagram

    The chord diagram aggregates nodes into arc segments and edges into ribbons,
    showing **aggregate flow between groups** rather than individual connections.

    This is ideal for visualizing migration patterns, trade flows,
    information exchange, or any network where you want to see
    how much moves between categories rather than individual links.

    In this notebook we use synthetic **population migration data** between continents.
    """)
    return


@app.cell
def _():
    import networkx as nx

    import nxviz as nv

    return nv, nx


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build the Graph

    Each node is a country with a `continent` attribute.
    Each edge is a migration flow with a `flow` weight.
    """)
    return


@app.cell
def _(nx):
    G = nx.DiGraph()

    continents = {
        "Nigeria": "Africa",
        "Egypt": "Africa",
        "South Africa": "Africa",
        "China": "Asia",
        "India": "Asia",
        "Japan": "Asia",
        "Germany": "Europe",
        "France": "Europe",
        "UK": "Europe",
        "USA": "N. America",
        "Canada": "N. America",
        "Mexico": "N. America",
        "Brazil": "S. America",
        "Argentina": "S. America",
        "Australia": "Oceania",
        "New Zealand": "Oceania",
    }

    for country, continent in continents.items():
        G.add_node(country, continent=continent)

    flows = [
        ("India", "UK", 500000),
        ("India", "USA", 800000),
        ("Mexico", "USA", 1200000),
        ("China", "USA", 400000),
        ("Nigeria", "UK", 300000),
        ("France", "UK", 200000),
        ("Brazil", "USA", 300000),
        ("UK", "Australia", 250000),
        ("Germany", "USA", 200000),
        ("Egypt", "France", 150000),
        ("South Africa", "UK", 200000),
        ("China", "Australia", 350000),
        ("India", "Canada", 250000),
    ]

    for src, tgt, flow in flows:
        G.add_edge(src, tgt, flow=flow)

    print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
    return (G,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Basic Chord Diagram

    The `group_by` parameter is required — it tells nxviz which node attribute
    defines the groups. The `weight_by` parameter specifies the edge attribute
    to aggregate (ribbon width will be proportional to total flow).
    """)
    return


@app.cell
def _(G, nv):
    nv.chord(G, group_by="continent", weight_by="flow")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading the Diagram

    - **Arc segments** around the circle represent groups (continents).
      Arc width is proportional to the number of nodes in each group.
    - **Ribbons** connect arc segments. Each ribbon shows aggregate flow
      from one group to another.
    - **Ribbon color** matches the source group, so you can see directionality.
    - **Ribbon width** at each end is proportional to the flow volume.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Customizing Appearance

    Use `alpha` to control ribbon transparency.
    """)
    return


@app.cell
def _(G, nv):
    nv.chord(
        G,
        group_by="continent",
        weight_by="flow",
        alpha=0.6,
    )
    return


@app.cell
def _(G, nv):
    nv.chord(
        G,
        group_by="continent",
        weight_by="flow",
        alpha=0.6,
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Unweighted Chord Diagram

    If `weight_by` is omitted, each edge counts equally.
    This is useful when you only care about the **number of connections**
    between groups, not the volume.
    """)
    return


@app.cell
def _(G, nv):
    nv.chord(G, group_by="continent")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Interactive Chord Diagram (Plotly Backend)

    Switch to the plotly backend for hover tooltips, zoom, and pan.
    Hover over a ribbon to highlight it — the hovered ribbon goes fully opaque
    while the others fade out, making it easy to isolate individual flows.
    """)
    return


@app.cell
def _(G, mo, nv):
    fig = nv.chord(
        G,
        group_by="continent",
        weight_by="flow",
        backend="plotly",
    )
    mo.iframe(nv.chord_hover_html(fig), height="600px")
    return


if __name__ == "__main__":
    app.run()
