from collections import deque


class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ---------- Helpers ----------

def tree_to_level_order(root):
    """Convert a tree to LeetCode's level-order list format (trailing Nones stripped)."""
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
    while out and out[-1] is None:
        out.pop()
    return out


def get_preorder(root):
    """Compute the preorder traversal of a tree (for verification)."""
    if root is None:
        return []
    return [root.val] + get_preorder(root.left) + get_preorder(root.right)


def get_inorder(root):
    """Compute the inorder traversal of a tree (for verification)."""
    if root is None:
        return []
    return get_inorder(root.left) + [root.val] + get_inorder(root.right)


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
    def buildTree(self, preorder, inorder):

        if not preorder:
            return None
        
        
        root_val = preorder[0]
        root = TreeNode(root_val)


        mid = inorder.index(root_val)
        left_inorder = inorder[:mid]
        right_inorder = inorder[mid+1:]

        left_preorder  = preorder[1 : 1 + len(left_inorder)]
        right_preorder = preorder[1 + len(left_inorder):]

        root.left  = self.buildTree(left_preorder, left_inorder)
        root.right = self.buildTree(right_preorder, right_inorder)

        return root


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (preorder, inorder, expected_level_order)
        ([3, 9, 20, 15, 7], [9, 3, 15, 20, 7], [3, 9, 20, None, None, 15, 7]),    # example 1
        ([-1], [-1], [-1]),                                                       # example 2
        ([1], [1], [1]),                                                          # single node
        ([1, 2], [2, 1], [1, 2]),                                                 # only left child
        ([1, 2], [1, 2], [1, None, 2]),                                           # only right child
        ([1, 2, 3], [2, 1, 3], [1, 2, 3]),                                        # balanced
        ([1, 2, 3, 4], [4, 3, 2, 1], [1, 2, None, 3, None, 4]),                   # left-skewed
        ([1, 2, 3, 4], [1, 2, 3, 4], [1, None, 2, None, 3, None, 4]),             # right-skewed
        ([1, 2, 4, 5, 3, 6, 7], [4, 2, 5, 1, 6, 3, 7], [1, 2, 3, 4, 5, 6, 7]),    # full tree depth 3
        ([3, 1, 2, 4], [1, 2, 3, 4], [3, 1, 4, None, 2]),                         # asymmetric
        ([5, 4, 3, 2, 1], [1, 2, 3, 4, 5], [5, 4, None, 3, None, 2, None, 1]),    # left-skewed deep
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, None, 2, None, 3, None, 4, None, 5]),  # right-skewed deep
        ([0], [0], [0]),                                                           # value 0
        ([-1, -2, -3], [-2, -1, -3], [-1, -2, -3]),                                # negatives
    ]

    passed = 0
    failed = 0

    for i, (preorder, inorder, expected) in enumerate(test_cases):
        print(f"========== Test {i} ==========")
        print(f"Preorder: {preorder}")
        print(f"Inorder:  {inorder}")
        print(f"Expected: {expected}")

        try:
            root = Solution().buildTree(preorder, inorder)
            result = tree_to_level_order(root)
            print_tree(root, "Built tree")
            print(f"Got:      {result}")

            # Sanity: traversals of the built tree should match the inputs
            actual_pre = get_preorder(root)
            actual_in = get_inorder(root)
            if actual_pre != preorder:
                print(f"⚠️  Preorder mismatch: built tree gives {actual_pre}")
            if actual_in != inorder:
                print(f"⚠️  Inorder mismatch:  built tree gives {actual_in}")

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