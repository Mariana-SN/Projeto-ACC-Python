from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Node:
    key: int
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def insert(root: Optional[Node], key: int) -> Node:

    if root is None:
        return Node(key=key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    return root


def search(root: Optional[Node], key: int) -> Optional[Node]:

    current = root
    while current is not None:
        if key == current.key:
            return current
        if key < current.key:
            current = current.left
        else:
            current = current.right
    return None


def _find_min(node: Node) -> Node:
    current = node
    while current.left is not None:
        current = current.left
    return current


def delete(root: Optional[Node], key: int) -> Optional[Node]:

    if root is None:
        return None

    if key < root.key:
        root.left = delete(root.left, key)
    elif key > root.key:
        root.right = delete(root.right, key)
    else:
        if root.left is None and root.right is None:
            return None

        if root.left is None:
            return root.right
        if root.right is None:
            return root.left

        successor = _find_min(root.right)
        root.key = successor.key
        root.right = delete(root.right, successor.key)

    return root


def height(root: Optional[Node]) -> int:

    if root is None:
        return 0
    return 1 + max(height(root.left), height(root.right))


def inorder_traversal(root: Optional[Node]) -> List[int]:
    if root is None:
        return []
    return inorder_traversal(root.left) + [root.key] + inorder_traversal(root.right)


def is_bst(
    root: Optional[Node],
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
    
    print("CENÁRIO 1 – Exemplo básico")
    valores1 = [50, 30, 70, 20, 40, 60, 80]
    raiz1: Optional[Node] = None
    for v in valores1:
        raiz1 = insert(raiz1, v)

    print("In-order:", inorder_traversal(raiz1))
    print("Altura:", height(raiz1))
    print("É ABB válida?", is_bst(raiz1))
    print("Busca 40:", search(raiz1, 40) is not None)
    print("Busca 100:", search(raiz1, 100) is not None)

    raiz1 = delete(raiz1, 70)
    print("In-order após remover 70:", inorder_traversal(raiz1))
    print("Altura após remoção:", height(raiz1))
    print("ABB válida após remoção?", is_bst(raiz1))
    print()

    
    print("CENÁRIO 2 – Inserção em ordem crescente (pior caso)")
    valores2 = [1, 2, 3, 4, 5, 6, 7]
    raiz2: Optional[Node] = None
    for v in valores2:
        raiz2 = insert(raiz2, v)

    print("In-order:", inorder_traversal(raiz2))
    print("Altura (esperado 7):", height(raiz2))
    print("É ABB válida?", is_bst(raiz2))
    print()

    print(" CENÁRIO 3 – Inserção de duplicatas")
    raiz3: Optional[Node] = None
    for v in [10, 10, 10, 10]:
        raiz3 = insert(raiz3, v)

    print("In-order (apenas um 10):", inorder_traversal(raiz3))
    print("Altura:", height(raiz3))
    print("É ABB válida?", is_bst(raiz3))
    print()

    print("CENÁRIO 4 – Remoção de folha, 1 filho e 2 filhos ===")
    valores4 = [50, 30, 70, 20, 40, 60, 80, 35]
    raiz4: Optional[Node] = None
    for v in valores4:
        raiz4 = insert(raiz4, v)
    print("In-order inicial:", inorder_traversal(raiz4))

    raiz4 = delete(raiz4, 20)
    print("Depois de remover 20:", inorder_traversal(raiz4), "| ABB válida?", is_bst(raiz4))

   
    raiz4 = delete(raiz4, 40)
    print("Depois de remover 40:", inorder_traversal(raiz4), "| ABB válida?", is_bst(raiz4))

    raiz4 = delete(raiz4, 50)
    print("Depois de remover 50:", inorder_traversal(raiz4), "| ABB válida?", is_bst(raiz4))

    print("Altura final:", height(raiz4))
