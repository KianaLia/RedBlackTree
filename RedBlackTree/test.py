from RBT import RedBlackTree
from BST import BinarySearchTree
from Node import Node, RedBlackNode


def main():
    tree = RedBlackTree()
    tree.insert(5)
    tree.insert(105)
    tree.insert(26)
    tree.insert(19)
    tree.insert(43)
    tree.insert(56)
    tree.insert(120)
    tree.display()

    # Search of RBT Tree
    target = tree.search(tree.root, 43)
    print(f"Value, Colour : {target.data, target.colour}")

    tree.delete(26)
    tree.display()

    tree.insert(26)
    tree.display()


if __name__ == "__main__":
    main()
