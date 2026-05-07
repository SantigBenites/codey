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


def get_preorder(root):
    """Compute the preorder traversal (for figuring out the expected output)."""
    if root is None:
        return []
    return [root.val] + get_preorder(root.left) + get_preorder(root.right)


def flattened_to_list(root):
    """
    Walk a flattened tree using ONLY .right pointers.
    Also asserts every .left is None — if not, returns an error string.
    """
    if root is None:
        return []
    out = []
    cur = root
    seen = set()
    while cur is not None:
        if id(cur) in seen:
            return f"<CYCLE detected at val={cur.val}>"
        seen.add(id(cur))
        if cur.left is not None:
            return f"<NON-NULL .left found at val={cur.val} pointing to val={cur.left.val}>"
        out.append(cur.val)
        cur = cur.right
    return out


# ---------- Your solution ----------

class Solution(object):

    def __init__(self):
        self.prev = None  # remembers the last visited node

    def flatten(self, root:TreeNode):
        if root is None:
            return

        self.flatten(root.right)

        self.flatten(root.left)


        root.right = self.prev      # what should this point to?
        root.left = None             # what should this be?
        self.prev = root            # update prev for the next iteration

        return root

        

# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_level_order, expected_flat_values)
        ([1, 2, 5, 3, 4, None, 6], [1, 2, 3, 4, 5, 6]),     # example 1
        ([], []),                                              # example 2: empty
        ([0], [0]),                                            # example 3: single node
        ([1], [1]),                                            # single non-zero
        ([1, 2], [1, 2]),                                      # only left child
        ([1, None, 2], [1, 2]),                                # only right child (already "flat")
        ([1, 2, 3], [1, 2, 3]),                                # simple split
        ([1, 2, 3, 4, 5, 6, 7], [1, 2, 4, 5, 3, 6, 7]),        # full tree depth 3
        ([1, 2, None, 3, None, 4], [1, 2, 3, 4]),              # left-skewed
        ([1, None, 2, None, 3, None, 4], [1, 2, 3, 4]),        # right-skewed (already flat)
        ([1, 2, 3, 4], [1, 2, 4, 3]),                          # left subtree has children
        ([1, 2, 3, None, 4, 5], [1, 2, 4, 3, 5]),              # right child of left, left child of right
        ([1, 2, 3, None, None, 4, 5], [1, 2, 3, 4, 5]),        # only right side has depth
        ([0, 0, 0], [0, 0, 0]),                                # all zeros
        ([-1, -2, -3, -4, -5], [-1, -2, -4, -5, -3]),          # negatives
    ]

    passed = 0
    failed = 0

    for i, (vals, expected) in enumerate(test_cases):
        root = build_tree(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}")
        print_tree(root, "Tree (before flatten)")
        if root is not None:
            print(f"Preorder: {get_preorder(root)}")
        print(f"Expected: {expected}")

        try:
            Solution().flatten(root)
            result = flattened_to_list(root)
            print(f"Got:      {result}")

            if isinstance(result, str):
                print(f"⚠️  Structural problem: {result}")
                failed += 1
                print("❌ FAIL\n")
                continue

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