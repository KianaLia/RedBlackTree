from re import X
from Node import Node, RedBlackNode
from BST import BinarySearchTree


class RedBlackTree(BinarySearchTree):
    def __init__(self):
        self.TNULL = RedBlackNode(0)
        self.TNULL.colour = False  # Every NIL point is Black
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def traversal(self, root, kind: str = None):
        if kind is None:
            kind = "inorder"
        res = []

        if kind == "inorder":
            if root != self.TNULL:
                res = self.traversal(root.left, kind)
                res.append(root.data)
                res += self.traversal(root.right, kind)
        if kind == "preorder":
            if root != self.TNULL:
                res.append(root.data)
                res += self.traversal(root.left, kind)
                res += self.traversal(root.right, kind)
        if kind == "postorder":
            if root != self.TNULL:
                res = self.traversal(root.right, kind)
                res += self.traversal(root.left, kind)
                res.append(root.data)

        return res

    def rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y

    def rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def insert(self, data):

        z = RedBlackNode(data)
        z.left = self.TNULL
        z.right = self.TNULL

        y = None
        x = self.root

        while x != self.TNULL:
            y = x

            if z.data < x.data:
                x = x.left
            else:
                x = x.right

        z.parent = y

        if y == None:
            self.root = z

        elif z.data < y.data:
            y.left = z
        else:
            y.right = z

        if z.parent == None:
            z.colour = False
            return

        if z.parent.parent == None:
            return

        self._insert_fix_up(z)

    def _insert_fix_up(self, z: RedBlackNode):
        while z.parent.colour:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.colour:
                    z.parent.colour = False  # Black
                    y.colour = False
                    z.parent.parent.colour = True
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        _ = self.rotate_left(z)
                    z.parent.colour = False
                    z.parent.parent.colour = True
                    _ = self.rotate_right(z.parent.parent)

            else:
                y = z.parent.parent.left
                if y.colour:
                    z.parent.colour = False  # Black
                    y.colour = False
                    z.parent.parent.colour = True
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        _ = self.rotate_right(z)
                    z.parent.colour = False
                    z.parent.parent.colour = True
                    _ = self.rotate_left(z.parent.parent)
            if z == self.root:
                break
        self.root.colour = False

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def delete(self, val):
        z = self.search(self.root, val)
        y = z
        y_original_colour = y.colour

        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_colour = y.colour
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.colour = z.colour
        if not y_original_colour:
            self._delete_fix(x)

    def _delete_fix(self, x):
        while x != self.root and not x.colour:
            if x == x.parent.left:
                s = x.parent.right
                if s.colour:
                    s.colour = False
                    x.parent.colour = True
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if not s.left.colour and not s.right.colour:
                    s.colour = True
                    x = x.parent
                else:
                    if not s.right.colour:
                        s.left.colour = False
                        s.colour = True
                        self.right_rotate(s)
                        s = x.parent.right

                    s.colour = x.parent.colour
                    x.parent.colour = False
                    s.right.colour = False
                    self.rotate_left(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.colour:
                    s.colour = False
                    x.parent.colour = True
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if not s.right.colour and not s.right.colour:
                    s.colour = True
                    x = x.parent
                else:
                    if not s.left.colour:
                        s.right.colour = False
                        s.colour = True
                        self.rotate_left(s)
                        s = x.parent.left

                    s.colour = x.parent.colour
                    x.parent.colour = False
                    s.left.colour = False
                    self.rotate_right(x.parent)
                    x = self.root
        x.colour = False

    def _display_aux(self, root):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if root.right is None and root.left is None:
            line = "(%s, %s)" % (root.data, root.get_colour())
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if root.right is None:
            lines, n, p, x = self._display_aux(root.left)
            s = "(%s, %s)" % (root.data, root.get_colour())
            u = len(s)
            first_line = (x + 1) * " " + (n - x - 1) * "_" + s
            second_line = x * " " + "/" + (n - x - 1 + u) * " "
            shifted_lines = [line + u * " " for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if root.left is None:
            lines, n, p, x = self._display_aux(root.right)
            s = "(%s, %s)" % (root.data, root.get_colour())
            u = len(s)
            first_line = s + x * "_" + (n - x) * " "
            second_line = (u + x) * " " + "\\" + (n - x - 1) * " "
            shifted_lines = [u * " " + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self._display_aux(root.left)
        right, m, q, y = self._display_aux(root.right)
        s = "(%s, %s)" % (root.data, root.get_colour())
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
