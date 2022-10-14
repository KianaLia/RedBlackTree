class Node(object):
    def __init__(self, data: int = 0):
        self.right = None
        self.left = None
        self.data = data
        self.parent = None


class RedBlackNode(Node):
    def __init__(self, data: int = 0):
        super().__init__(data)
        self.colour = True  # Red

    def change_colour(self):
        self.colour = not self.colour

    def get_colour(self):
        return "Red" if self.colour else "Black"
