from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------- Helpers ----------

def build_tree(values):
    """Build a binary tree from a level-order list (LeetCode format)."""
    if not values:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


def tree_to_level_order(root):
    """
    Convert a tree back to its level-order list representation,
    matching LeetCode's format (trailing Nones stripped).
    """
    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            out.append(None)
        else:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    # Strip trailing Nones (LeetCode convention)
    while out and out[-1] is None:
        out.pop()
    return out


def print_tree(root, label=""):
    """Pretty-print the tree level by level."""
    if label:
        print(f"--- {label} ---")
    if root is None:
        print("  (empty)")
        return
    level = [root]
    depth = 0
    while level:
        vals = [str(n.val) if n else "None" for n in level]
        print(f"  depth {depth}: {' '.join(vals)}")
        next_level = []
        for n in level:
            if n is not None:
                next_level.append(n.left)
                next_level.append(n.right)
        if all(n is None for n in next_level):
            break
        level = next_level
        depth += 1


# ---------- Your solution ----------

class Solution(object):
    def invertTree(self, root:TreeNode):

        if root == None:
            return

        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)

        return root


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_level_order, expected_level_order)
        ([4, 2, 7, 1, 3, 6, 9], [4, 7, 2, 9, 6, 3, 1]),     # example 1
        ([2, 1, 3], [2, 3, 1]),                              # example 2
        ([], []),                                             # example 3: empty
        ([1], [1]),                                           # single node
        ([1, 2], [1, None, 2]),                               # only left child becomes only right
        ([1, None, 2], [1, 2]),                               # only right child becomes only left
        ([1, 2, 3], [1, 3, 2]),                               # simple swap
        ([1, 2, None, 3], [1, None, 2, None, 3]),             # left-skewed becomes right-skewed
        ([1, None, 2, None, 3], [1, 2, None, 3]),             # right-skewed becomes left-skewed
        ([1, 2, 3, 4, 5, 6, 7], [1, 3, 2, 7, 6, 5, 4]),       # full tree of depth 3
        ([1, 2, 2, 3, 3, 3, 3], [1, 2, 2, 3, 3, 3, 3]),       # symmetric tree: invert == original
        ([0], [0]),                                           # zero-value node
        ([1, 2, 3, None, 4, None, 5], [1, 3, 2, 5, None, 4]), # asymmetric
        ([-1, -2, -3], [-1, -3, -2]),                         # negatives
    ]

    passed = 0
    failed = 0

    for i, (vals, expected) in enumerate(test_cases):
        root = build_tree(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}")
        print_tree(root, "Before")
        print(f"Expected: {expected}")

        try:
            result_root = Solution().invertTree(root)
            result = tree_to_level_order(result_root)
            print_tree(result_root, "After")
            print(f"Got:      {result}")

            if result == expected:
                print("✅ PASS\n")
                passed += 1
            else:
                print("❌ FAIL\n")
                failed += 1
        except RecursionError:
            print("❌ ERROR: RecursionError\n")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {type(e).__name__}: {e}\n")
            failed += 1

    print(f"========== Results ==========")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")