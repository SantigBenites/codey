from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------- Helpers ----------

def build_tree(values):
    """
    Build a binary tree from a level-order list (LeetCode format).
    `None` represents a missing node. Example: [3, 9, 20, None, None, 15, 7]
    """
    if not values:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        # left child
        if i < len(values):
            if values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
        # right child
        if i < len(values):
            if values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
    return root


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
        # stop if next level is all None
        if all(n is None for n in next_level):
            break
        level = next_level
        depth += 1


# ---------- Your solution ----------

class Solution(object):
    def maxDepth(self, root:TreeNode):

        if root == None:
            return 0

        if (root.right == None and root.left == None):
            return 1

        return 1 + max(self.maxDepth(root.left),self.maxDepth(root.right))


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_level_order, expected_depth)
        ([3, 9, 20, None, None, 15, 7], 3),     # example 1
        ([1, None, 2], 2),                       # example 2: only right child
        ([], 0),                                  # empty tree
        ([1], 1),                                 # single node
        ([1, 2], 2),                              # root + one left child
        ([1, None, 2], 2),                        # root + one right child (dup of ex 2 for clarity)
        ([1, 2, 3], 2),                           # root + two children
        ([1, 2, 3, 4, 5, 6, 7], 3),               # full tree of depth 3
        ([1, 2, None, 3, None, 4, None, 5], 5),   # left-skewed
        ([1, None, 2, None, 3, None, 4, None, 5], 5),  # right-skewed
        ([1, 2, 3, 4, None, None, 5, 6, None, None, 7], 4),  # asymmetric, deep on left
        ([1, 2, 3, None, None, 4, 5, None, None, 6, 7], 4),  # deep on right
        ([0], 1),                                 # single node with value 0 (truthiness trap)
        ([-1, -2, -3], 2),                        # negative values
    ]

    passed = 0
    failed = 0

    for i, (vals, expected) in enumerate(test_cases):
        root = build_tree(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}")
        print_tree(root, "Tree")
        print(f"Expected: {expected}")

        try:
            result = Solution().maxDepth(root)
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