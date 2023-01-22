#################################################################
# FILE : Q7_find_path.py
# WRITER : David Ruppin, ruppin, 322296336
# EXERCISE : intro2cs exTest 2022-2023
#################################################################
from dataclasses import dataclass
from typing import Any, List


@dataclass
class Node:
    data: int
    left: Any = None
    right: Any = None

tree = Node(1, Node(2, Node(8), Node(0, Node(9))), Node(-7, Node(5, Node(0),Node(9)), Node(4, Node(-3))))
# tree = Node(1, Node(2, Node(8)), Node(0, Node(9)), Node(-7, Node(5, Node(0), Node(9)), Node(4, None, Node(-3))))


def find_path(root, k):
    return find_path_helper(root, k, [])

def find_path_helper(root: Node, k: int, path: List[Node]):
    path.append(root.data)
    if sum(path) == k:
        return path

    l, r = None, None
    if root.left:
        l = find_path_helper(root.left, k, path)
    if root.right:
        r = find_path_helper(root.right, k, path)

    if l:
        return l
    elif r:
        return r

    path.pop()
    
print(find_path(tree, 8))