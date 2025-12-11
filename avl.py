from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List

_rotation_count: int = 0


def reset_rotation_count() -> None:
    global _rotation_count
    _rotation_count = 0


def get_rotation_count() -> int:
    return _rotation_count


@dataclass
class AvlNode:
    key: int
    left: Optional["AvlNode"] = None
    right: Optional["AvlNode"] = None
    height: int = 1


def _node_height(node: Optional[AvlNode]) -> int:
    if node is None:
        return 0
    return node.height


def _update_height(node: AvlNode) -> None:
    node.height = 1 + max(_node_height(node.left), _node_height(node.right))


def _balance_factor(node: Optional[AvlNode]) -> int:
    if node is None:
        return 0
    return _node_height(node.left) - _node_height(node.right)


def _rotate_right(y: AvlNode) -> AvlNode:
    global _rotation_count

    x = y.left
    t2 = x.right if x else None

    if x is None:
        return y 

    x.right = y
    y.left = t2

    _update_height(y)
    _update_height(x)

    _rotation_count += 1
    return x


def _rotate_left(x: AvlNode) -> AvlNode:
    global _rotation_count

    y = x.right
    t2 = y.left if y else None

    if y is None:
        return x 

    y.left = x
    x.right = t2

    _update_height(x)
    _update_height(y)

    _rotation_count += 1
    return y


def insert(root: Optional[AvlNode], key: int) -> AvlNode:
    if root is None:
        return AvlNode(key=key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    _update_height(root)
    balance = _balance_factor(root)

    if balance > 1 and key < (root.left.key if root.left else key):
        return _rotate_right(root)

    if balance < -1 and key > (root.right.key if root.right else key):
        return _rotate_left(root)

    if balance > 1 and key > (root.left.key if root.left else key):
        root.left = _rotate_left(root.left) 
        return _rotate_right(root)

    if balance < -1 and key < (root.right.key if root.right else key):
        root.right = _rotate_right(root.right)
        return _rotate_left(root)

    return root


def _find_min(node: AvlNode) -> AvlNode:
    current = node
    while current.left is not None:
        current = current.left
    return current


def delete(root: Optional[AvlNode], key: int) -> Optional[AvlNode]:
    if root is None:
        return None

    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left

        temp = _find_min(root.right)
        root.key = temp.key
        root.right = delete(root.right, temp.key)

    _update_height(root)
    balance = _balance_factor(root)

    if balance > 1 and _balance_factor(root.left) >= 0:
        return _rotate_right(root)

    if balance > 1 and _balance_factor(root.left) < 0:
        root.left = _rotate_left(root.left)
        return _rotate_right(root)

    if balance < -1 and _balance_factor(root.right) <= 0:
        return _rotate_left(root)

    if balance < -1 and _balance_factor(root.right) > 0:
        root.right = _rotate_right(root.right)
        return _rotate_left(root)

    return root


def search(root: Optional[AvlNode], key: int) -> Optional[AvlNode]:
    current = root
    while current is not None:
        if key == current.key:
            return current
        if key < current.key:
            current = current.left
        else:
            current = current.right
    return None


def height(root: Optional[AvlNode]) -> int:
    return _node_height(root)


def inorder_traversal(root: Optional[AvlNode]) -> List[int]:
    if root is None:
        return []
    return inorder_traversal(root.left) + [root.key] + inorder_traversal(root.right)


def is_bst(
    root: Optional[AvlNode],
    min_key: Optional[int] = None,
    max_key: Optional[int] = None,
) -> bool:
    if root is None:
        return True

    if min_key is not None and root.key <= min_key:
        return False
    if max_key is not None and root.key >= max_key:
        return False

    return (
        is_bst(root.left, min_key, root.key)
        and is_bst(root.right, root.key, max_key)
    )


if __name__ == "__main__":
    valores = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    raiz: Optional[AvlNode] = None
    reset_rotation_count()

    for v in valores:
        raiz = insert(raiz, v)

    print("In-order AVL:", inorder_traversal(raiz))
    print("Altura AVL :", height(raiz))
    print("É árvore de busca?", is_bst(raiz))
    print("Rotações nas inserções:", get_rotation_count())

    for chave in [20, 30, 50]:
        raiz = delete(raiz, chave)

    print("Após remoções:", inorder_traversal(raiz))
    print("Altura final:", height(raiz))
    print("ABB/AVL válida?", is_bst(raiz))
