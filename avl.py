_rotation_count = 0

def reset_rotation_count():
    global _rotation_count
    _rotation_count = 0

def get_rotation_count():
    return _rotation_count

class AvlNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

def _node_height(node):
    return 0 if node is None else node.height

def _update_height(node):
    node.height = 1 + max(_node_height(node.left), _node_height(node.right))

def _balance_factor(node):
    return _node_height(node.left) - _node_height(node.right)

def _rotate_right(y):
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

def _rotate_left(x):
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

def insert(root, key):
    if root is None:
        return AvlNode(key)

    if key < root.key:
        root.left = insert(root.left, key)
    elif key > root.key:
        root.right = insert(root.right, key)
    else:
        return root

    _update_height(root)
    balance = _balance_factor(root)

    if balance > 1 and key < root.left.key:
        return _rotate_right(root)

    if balance < -1 and key > root.right.key:
        return _rotate_left(root)

    if balance > 1 and key > root.left.key:
        root.left = _rotate_left(root.left)
        return _rotate_right(root)

    if balance < -1 and key < root.right.key:
        root.right = _rotate_right(root.right)
        return _rotate_left(root)

    return root

def _find_min(node):
    while node.left is not None:
        node = node.left
    return node

def delete(root, key):
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

def search(root, key):
    current = root
    while current:
        if key == current.key:
            return current
        elif key < current.key:
            current = current.left
        else:
            current = current.right
    return None

def height(root):
    return _node_height(root)

def inorder_traversal(root):
    if root is None:
        return []
    return inorder_traversal(root.left) + [root.key] + inorder_traversal(root.right)

def is_bst(root, min_key=None, max_key=None):
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

def print_tree(node, level=0, prefix=""):
    if node is not None:
        print_tree(node.right, level + 1, "    ")
        print(prefix * level + str(node.key))
        print_tree(node.left, level + 1, "    ")

if __name__ == "__main__":
    valores = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
    raiz = None
    reset_rotation_count()

    for v in valores:
        raiz = insert(raiz, v)

    print("Valores em ordem:", inorder_traversal(raiz))
    print("Altura AVL :", height(raiz))
    print("É árvore de busca?", is_bst(raiz))
    print("Rotações nas inserções:", get_rotation_count())

    print("\nÁrvore AVL após inserções:")
    print_tree(raiz)

    for chave in [20, 30, 50]:
        raiz = delete(raiz, chave)

    print("\nValores em ordem após remoções:", inorder_traversal(raiz))
    print("\nÁrvore AVL após deleções:")
    print_tree(raiz)
    print("Altura final:", height(raiz))
    print("ABB/AVL válida?", is_bst(raiz))