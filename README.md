# Python Graphviz wrapper

## Installation

* `pip install git+https://github.com/mavnt/pygraph.git` 

## Requirements

* `dot` 

## Examples

``` python
def test_digraph():
    g = Graph()  # dot_path=dot and type_=digraph options
    g.set_vertex_color(1, "red")
    g.add_edge(1, 2)
    g.add_edge(1, 3, label="test")
    g.add_edge(3, 2, color="blue")
    g.add_edge(3, 4)
    g.add_edge(4, 2, color="red", label="_test")
    g.add_edge("1", 2)
    g.add_edge(4, 1)
    print(g.get_source())
    g.view()  # this opens your pdf viewer
```

