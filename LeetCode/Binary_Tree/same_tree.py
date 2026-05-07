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
    `None` represents a missing node.
    """
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
    def isSameTree(self, p:TreeNode, q:TreeNode):

        if p is None and q is None:
            return True

        if p is None or q is None:   # exactly one is None
            return False

        return p.val  == q.val and self.isSameTree(p.left, q.left) and self.isSameTree(p.right, q.right)
    


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (p_values, q_values, expected)
        ([1, 2, 3], [1, 2, 3], True),                       # example 1: identical
        ([1, 2], [1, None, 2], False),                       # example 2: same vals, diff structure
        ([1, 2, 1], [1, 1, 2], False),                       # example 3: different values
        ([], [], True),                                       # both empty
        ([1], [], False),                                     # one empty
        ([], [1], False),                                     # the other empty
        ([1], [1], True),                                     # single node match
        ([1], [2], False),                                    # single node mismatch
        ([1, 2, 3], [1, 2, 4], False),                        # leaf value differs
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], True),             # deeper identical
        ([1, 2, 3, 4, 5], [1, 2, 3, 5, 4], False),            # subtree children swapped
        ([1, 2, 3, None, 4], [1, 2, 3, 4], False),            # 4 as right child of 2 vs left child
        ([0], [0], True),                                     # value 0 (truthiness trap)
        ([0, None, 0], [0, 0], False),                        # zeros, different structure
        ([-1, -2, -3], [-1, -2, -3], True),                   # negatives
        ([1, 2, 3], [1, 3, 2], False),                        # left/right children swapped
        ([1, None, 2, None, 3], [1, None, 2, None, 3], True), # right-skewed identical
        ([1, 2, None, 3], [1, 2, None, 3], True),             # left-skewed identical
        ([1, 2, None, 3], [1, 2, 3], False),                  # left-skewed vs balanced
    ]

    passed = 0
    failed = 0

    for i, (p_vals, q_vals, expected) in enumerate(test_cases):
        p = build_tree(p_vals)
        q = build_tree(q_vals)
        print(f"========== Test {i} ==========")
        print(f"p input: {p_vals}")
        print_tree(p, "p")
        print(f"q input: {q_vals}")
        print_tree(q, "q")
        print(f"Expected: {expected}")

        try:
            result = Solution().isSameTree(p, q)
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