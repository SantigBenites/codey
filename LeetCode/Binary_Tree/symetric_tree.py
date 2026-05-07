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
    def isSymmetric(self, root:TreeNode):

        if root is None:
            return True
        # Kick off the helper with the two subtrees that should mirror each other
        return self.isMirror(root.left, root.right)


    def isMirror(self, a:TreeNode, b:TreeNode):
        if a is None and b is None:
            return True
        
        if a is None or b is None:
            return False
        
        return a.val == b.val and self.isMirror(a.left, b.right) and self.isMirror(a.right, b.left)

# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_level_order, expected)
        ([1, 2, 2, 3, 4, 4, 3], True),                # example 1: symmetric
        ([1, 2, 2, None, 3, None, 3], False),         # example 2: same vals, asymmetric structure
        ([1], True),                                   # single node: trivially symmetric
        ([1, 2, 2], True),                             # symmetric, depth 2
        ([1, 2, 3], False),                            # asymmetric values
        ([1, 2, 2, 3, None, None, 3], True),           # symmetric with mirrored Nones
        ([1, 2, 2, None, 3, 3, None], True),          # symmetric with inner Nones
        ([1, 2, 2, 3, None, 3, None], False),          # looks similar but NOT symmetric (both 3s on left side of their parents)
        ([1, 2, 2, 2, None, 2], False),                # asymmetric structure even with same vals
        ([1, 0, 0], True),                             # value 0 (truthiness trap)
        ([0, 0, 0, 0, 0, 0, 0], True),                 # all zeros, perfect tree
        ([1, 2, 2, 3, 4, 4, 5], False),                # almost symmetric, last leaf differs
        ([5, 4, 4, 3, 2, 2, 3], True),                 # symmetric with arbitrary values
        ([1, 2, 3, 4, 5, 6, 7], False),                # full tree, all unique values
        ([-1, -2, -2, -3, -4, -4, -3], True),          # negatives, symmetric
        ([1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 6, 5], True),  # deeper symmetric tree
        ([1, 2, 2, 3, 4, 4, 3, 5, 6, 7, 8, 8, 7, 6, 4], False), # deeper, last leaf wrong
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
            result = Solution().isSymmetric(root)
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