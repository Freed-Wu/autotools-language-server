r"""Diagnostics
===============
"""
import os
from typing import Callable

from tree_sitter import Node, Tree


def traverse_tree(
    node: Node,
    func: Callable[[Node], bool],
    condition: Callable[[Node], bool] | None = None,
    nodes: list[Node] | None = None,
) -> list[Node]:
    r"""Traverse tree.

    :param node:
    :type node: Node
    :param func:
    :type func: Callable[[Node], bool]
    :param condition:
    :type condition: Callable[[Node], bool] | None
    :param nodes:
    :type nodes: list[Node] | None
    :rtype: list[Node]
    """
    if nodes is None:
        nodes = []
    if condition is None:
        condition = lambda _: True
    for n in node.children:
        if func(n):
            nodes.append(n)
        if condition(n):
            traverse_tree(n, func, condition, nodes)
    return nodes


def get_missing_nodes(tree: Tree) -> list[Node]:
    r"""Get missing nodes.

    :param tree:
    :type tree: Tree
    :rtype: list[Node]
    """
    return traverse_tree(tree.root_node, lambda n: n.is_missing)


def get_error_nodes(tree: Tree) -> list[Node]:
    r"""Get error nodes.

    :param tree:
    :type tree: Tree
    :rtype: list[Node]
    """
    return traverse_tree(tree.root_node, lambda n: n.has_error)


def get_non_existent_include_directives(tree: Tree, cwd: str) -> list[Node]:
    r"""Get non existent include directives.

    :param tree:
    :type tree: Tree
    :param cwd:
    :type cwd: str
    :rtype: list[Node]
    """
    return traverse_tree(
        tree.root_node,
        lambda n: n.parent is not None
        and n.parent.type == "include_directive"
        and n == n.parent.children[1]
        and n.parent.children[0].type == "include"
        and not os.path.exists(os.path.join(cwd, n.text.decode())),
    )


def get_ignored_rules(tree: Tree) -> list[Node]:
    r"""Get ignored rules.

    :param tree:
    :type tree: Tree
    :rtype: list[Node]
    """
    targets = []
    nodes = []
    children = tree.root_node.children
    children.reverse()
    for n in children:
        if n.type != "rule":
            continue
        if n.children[0].text not in targets:
            targets += [n.children[0].text]
        elif not n.children[0].text.decode().startswith("."):
            nodes += [n.children[0]]
    return nodes


def diagnostic(tree: Tree, cwd: str) -> list[tuple[Node, str, str]]:
    r"""Diagnostic.

    :param tree:
    :type tree: Tree
    :param cwd:
    :type cwd: str
    :rtype: list[tuple[Node, str, str]]
    """
    results = []
    results += [(node, "missing", "Error") for node in get_missing_nodes(tree)]
    results += [(node, "error", "Error") for node in get_error_nodes(tree)]
    results += [
        (node, "file not found", "Error")
        for node in get_non_existent_include_directives(tree, cwd)
    ]
    results += [
        (node, "ignored by repeated rules", "Warning")
        for node in get_ignored_rules(tree)
    ]
    return results
