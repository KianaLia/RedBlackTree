from Node import Node


class BinarySearchTree(object):
    def __init__(self, root: Node):
        self.root = root

    def insert(self, root, data):
        if root.data:
            if data < root.data:
                if root.left is None:
                    root.left = Node(data)
                    root.left.parent = root
                else:
                    self.insert(root.left, data)

            elif data > root.data:
                if root.right is None:
                    root.right = Node(data)
                    root.right.parent = root
                else:
                    self.insert(root.right, data)

        else:
            self.root.data = data

    def search(self, root, val):
        if root.data == val or (root.right is None and root.left is None):
            return root

        else:
            if val < root.data:
                return self.search(root.left, val)
            else:
                return self.search(root.right, val)

    def traversal(self, root, kind: str = None):
        if kind is None:
            kind = "inorder"
        res = []

        if kind == "inorder":
            if root:
                res = self.traversal(root.left, kind)
                res.append(root.data)
                res += self.traversal(root.right, kind)
        if kind == "preorder":
            if root:
                res.append(root.data)
                res += self.traversal(root.left, kind)
                res += self.traversal(root.right, kind)
        if kind == "postorder":
            if root:
                res = self.traversal(root.right, kind)
                res += self.traversal(root.left, kind)
                res.append(root.data)

        return res

    def display(self):
        print("\n" + "*" * 30 + " Display the Tree " + "*" * 30)
        lines, *_ = self._display_aux(self.root)
        for line in lines:
            print(line)

        print(f"inorder : {self.traversal(self.root, kind='inorder')}")
        print(f"preorder : {self.traversal(self.root, kind='preorder')}")
        print(f"postorder : {self.traversal(self.root, kind='postorder')}")
        print("*" * 78 + "\n")

    def _display_aux(self, root):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if root.right is None and root.left is None:
            line = "%s" % root.data
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if root.right is None:
            lines, n, p, x = self._display_aux(root.left)
            s = "%s" % root.data
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "
            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if root.left is None:
            lines, n, p, x = self._display_aux(root.right)
            s = "%s" % root.data
            u = len(s)
            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(root.left)
        right, m, q, y = self._display_aux(root.right)
        s = "%s" % root.data
        u = len(s)
        first_line = (x + 1) * " " + (n - x - 1) * "_" + s + y * "_" + (m - y) * " "
        second_line = (
            x * " " + "/" + (n - x - 1 + u + y) * " " + "\\" + (m - y - 1) * " "
        )
        if p < q:
            left += [n * " "] * (q - p)
        elif q < p:
            right += [m * " "] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * " " + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
