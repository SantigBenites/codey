class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None



def level_transverse(tree:Node):

    ret = []
    queue = [tree]


    while queue:

        current_level = []
        nodeCount = len(queue)

        for i in range(nodeCount):
            node = queue.pop(0)
            current_level.append(node.data)

            if node.left is not None:
                queue.append(node.left)
            if node.right is not None:
                queue.append(node.right)

        if current_level:
            ret.append(current_level)

    return ret


def reverse_tree(tree:Node):

    if tree == None:
        return
    tree.left, tree.right = tree.right, tree.left

    reverse_tree(tree.left)
    reverse_tree(tree.right)

root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.right = Node(6)

traversal = level_transverse(root)

for level in traversal:
    print(" ".join(map(str, level)))

reverse_tree(root)

traversal = level_transverse(root)

for level in traversal:
    print(" ".join(map(str, level)))