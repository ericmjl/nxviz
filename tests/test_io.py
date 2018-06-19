from nxviz.io import graph_from_dataframe
import pandas as pd

from random import choice, seed

seed(123)
n_nodes = 100

headers = ["a_num", "a_string", "ten_things", "color", "group", "location"]
data_generator = (
    (
        i,
        str(i),
        i % 10,
        choice(["red", "green", "blue"]),
        choice(["A", "B"]),
        choice(
            ["New York", "San Francisco", "Chicago", "LA", "Austin", "Boston"]
        ),
    )
    for i in range(0, n_nodes)
)

test_dataframe = pd.DataFrame(data_generator, columns=headers)


def test_basic_import():

    g = graph_from_dataframe(test_dataframe)

    assert g.number_of_nodes() == 21
    assert g.number_of_edges() == 129
    assert g.nodes["A"] == {"type": "group"}
    assert g["blue"]["New York"] == {"type": "color_location", "weight": 6.0}


def test_percent_threshold():

    g = graph_from_dataframe(test_dataframe, threshold_by_percent_unique=0.08)

    assert g.number_of_nodes() == 11
    assert g.number_of_edges() == 36
    assert g.nodes["A"] == {"type": "group"}
    assert g["blue"]["B"] == {"type": "color_group", "weight": 20.0}


def test_count_threshold():

    g = graph_from_dataframe(test_dataframe, threshold_by_count_unique=3)

    assert g.number_of_nodes() == 5
    assert g.number_of_edges() == 6
    assert g.nodes["A"] == {"type": "group"}
    assert g["blue"]["B"] == {"type": "color_group", "weight": 20.0}


def test_node_properties():
    g = graph_from_dataframe(
        test_dataframe,
        threshold_by_count_unique=3,
        node_property_columns=["ten_things"],
    )

    assert g.number_of_nodes() == 5
    assert g.number_of_edges() == 6
    assert g.nodes["A"] == {
        "ten_things": "4|6|7|8|0|1|2|3|5|9",
        "type": "group",
    }


def test_edge_properties():
    g = graph_from_dataframe(
        test_dataframe, edge_property_columns=["ten_things", "a_string"]
    )

    assert g.number_of_nodes() == 21
    assert g.number_of_edges() == 129
    assert g["blue"]["B"] == {
        "a_string": "96",
        "ten_things": 6,
        "type": "color_group",
        "weight": 20.0,
    }
