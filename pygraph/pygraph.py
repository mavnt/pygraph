import os

from .logging_utils import logging
from .utils import *


class Graph(object):
    def __init__(self, type_: str = "digraph", dot_path="dot"):
        super(Graph, self).__init__()
        self.type_: str = type_
        self.edges = list()
        if self.type_ == "digraph":
            self.link = "->"
        elif self.type_ == "graph":
            self.link = "--"
        else:
            logging.critical("Unknown type of graph !!!")
            raise ValueError
        self.header = self.type_ + " {"
        self.rd = "TB"
        self.vertexes_options = list()
        self.dot_path = dot_path

    def __str__(self):
        return "{} with {} __edges__.".format(self.type_, len(self.edges))

    def is_digraph(self) -> bool:
        return self.type_ == "digraph"

    def is_graph(self) -> bool:
        return self.type_ == "graph"

    def get_type(self) -> str:
        return self.type_

    def get_source(self) -> str:
        return (
            "\n".join(
                [self.header]
                + ["rankdir={}".format(quote(self.rd))]
                + self.vertexes_options
            )
            + "\n"
            + "\n".join(self.edges + ["}"])
        )

    def write_source(self, name=None) -> None:
        name_txt = get_tmp_name(name, "txt")
        with open(name_txt, "w") as f:
            f.writelines(self.get_source())

    def write(self, name=None, file_type: str = "pdf"):
        name = get_tmp_name(name, file_type)
        name_txt = get_tmp_name(None, "txt")

        with open(name_txt, "w") as f:
            f.writelines(self.get_source())
        os.system("{} -T {} {} > {}".format(self.dot_path, file_type, name_txt, name))
        try:
            os.remove(name_txt)
        except (FileNotFoundError, PermissionError):
            logging.warning("Could not remove {}.".format(name_txt))
        return name

    def view(self, name=None, file_type: str = "pdf"):
        platform = get_platform()
        if platform == "Windows":
            name = get_tmp_name(name, file_type)
            self.write(name, file_type=file_type)
            os.system(name)
        elif platform == "OS X":
            logging.critical("Not implemented. Use write method instead.")
            return
        elif platform == "Linux":
            name = get_tmp_name(name, file_type)
            self.write(name, file_type=file_type)
            os.system("evince " + name)
        try:
            os.remove(name)
        except (FileNotFoundError, PermissionError):
            logging.warning("Could not remove {}.".format(name))

    def __get_edge__(self, vertex1, vertex2, label, color):
        vertex1, vertex2, label, color = make_strings(vertex1, vertex2, label, color)
        edge = quote(vertex1) + self.link + quote(vertex2)
        edge = add_edge_options(label, color, edge)
        return edge

    def add_edge(self, vertex1, vertex2, label="", color="", unique_edge=True):
        edge = self.__get_edge__(vertex1, vertex2, label, color)
        if self.is_digraph():
            if edge not in self.edges:
                self.edges.append(edge)
            else:
                logging.warn("Edge {} already present.".format(edge))
                if not unique_edge:
                    self.edges.append(edge)
                    logging.warn("Adding anyway.".format(edge))
        else:
            tmp = self.__get_edge__(vertex2, vertex1, label, color)
            if edge not in self.edges and tmp not in self.edges:
                self.edges.append(edge)
            else:
                logging.warn("Edge {} already present.".format(edge))
                if not unique_edge:
                    self.edges.append(edge)
                    logging.warn("Adding anyway.".format(edge))

    def del_edge(self, vertex1, vertex2, label="", color=""):
        edge = self.__get_edge__(vertex1, vertex2, label, color)
        if self.is_digraph():
            if edge in self.edges:
                self.edges.remove(edge)
            else:
                logging.warn("Edge {} not present.".format(edge))
        else:
            tmp = self.__get_edge__(vertex2, vertex1, label, color)
            if edge in self.edges:
                self.edges.remove(edge)
            elif tmp in self.edges:
                self.edges.remove(tmp)
            else:
                logging.warn("Edge {} not present.".format(edge))

    def set_vertex_shape(self, vertex, shape: str):
        if shape not in shapes:
            logging.warning("Invalid shape: {}.".format(shape))
        else:
            if '"{}"[shape="{}"]'.format(vertex, shape) not in self.vertexes_options:
                self.vertexes_options.append('"{}"[shape="{}"]'.format(vertex, shape))
            else:
                logging.warn(
                    'Shape "{}" already present for vertex {}.'.format(shape, vertex)
                )

    def del_vertex_shape(self, vertex, shape):
        try:
            self.vertexes_options.remove('"{}"[shape="{}"]'.format(vertex, shape))
        except ValueError:
            logging.warn('Shape "{}" not found for vertex {}.'.format(shape, vertex))

    def set_vertex_color(self, vertex, color: str):
        if color not in colors:
            logging.warning("Invalid color: {}.".format(color))
        else:
            tmp = '"{}"[color="{}"]'.format(vertex, color)
            if tmp not in self.vertexes_options:
                self.vertexes_options.append(tmp)
            else:
                logging.warn(
                    'Color "{}" already present for vertex {}.'.format(color, vertex)
                )

    def del_vertex_color(self, vertex, color):
        try:
            self.vertexes_options.remove('"{}"[color="{}"]'.format(vertex, color))
        except ValueError:
            logging.warn('Color "{}" not found for vertex {}.'.format(color, vertex))

    def set_rank_dir(self, rd: str):
        if rd not in ["TB", "LR", "BT", "RL"]:
            logging.warning("Invalid direction.")
        else:
            self.rd = rd
