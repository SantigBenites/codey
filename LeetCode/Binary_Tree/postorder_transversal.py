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


def get_inorder(root):
    """Compute the inorder traversal of a tree (for verification)."""
    if root is None:
        return []
    return get_inorder(root.left) + [root.val] + get_inorder(root.right)


def get_postorder(root):
    """Compute the postorder traversal of a tree (for verification)."""
    if root is None:
        return []
    return get_postorder(root.left) + get_postorder(root.right) + [root.val]


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
    def buildTree(self, inorder, postorder):
        # TODO 1: base case — what should you return when there are no nodes
        #         left to build a subtree from?
        if not postorder:
            return None

        # TODO 2: find the root.
        #         In postorder, where does the root always sit?
        #         (Hint: it's the OPPOSITE end from preorder.)
        root_val = postorder[-1]
        root = TreeNode(root_val)

        # TODO 3: split inorder using the root's position.
        #         Same trick as problem 105 — find root_val in inorder,
        #         everything before it is the left subtree's inorder,
        #         everything after it is the right subtree's inorder.
        mid = inorder.index(root_val)
        left_inorder = inorder[:mid]
        right_inorder = inorder[mid+1:]

        # TODO 4: split postorder.
        #         Postorder layout is: [...left subtree..., ...right subtree..., root]
        #         Use the SIZE of left_inorder to decide where the split goes.
        #         Be careful: the very last element of postorder is the root,
        #         so it shouldn't end up in either subtree's slice.
        left_postorder  = postorder[: len(left_inorder)]
        right_postorder = postorder[len(left_inorder):-1]

        # TODO 5: recurse and assign children.
        root.left  = self.buildTree(left_inorder, left_postorder)
        root.right = self.buildTree(right_inorder, right_postorder)

        return root


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (inorder, postorder, expected_level_order)
        ([9, 3, 15, 20, 7], [9, 15, 7, 20, 3], [3, 9, 20, None, None, 15, 7]),  # example 1
        ([-1], [-1], [-1]),                                                       # example 2
        ([1], [1], [1]),                                                          # single node
        ([2, 1], [2, 1], [1, 2]),                                                 # only left child
        ([1, 2], [2, 1], [1, None, 2]),                                           # only right child
        ([2, 1, 3], [2, 3, 1], [1, 2, 3]),                                        # balanced depth 2
        ([4, 3, 2, 1], [4, 3, 2, 1], [1, 2, None, 3, None, 4]),                   # right-skewed
        ([1, 2, 3, 4], [4, 3, 2, 1], [1, None, 2, None, 3, None, 4]),             # right-skewed (different vals)
        ([4, 3, 2, 1], [1, 2, 3, 4], None),  # placeholder; replaced below
        ([4, 2, 5, 1, 6, 3, 7], [4, 5, 2, 6, 7, 3, 1], [1, 2, 3, 4, 5, 6, 7]),    # full tree depth 3
        ([1, 2, 3, 4], [1, 2, 3, 4], [4, 3, None, 2, None, 1]),                   # left-skewed
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [5, 4, None, 3, None, 2, None, 1]),    # left-skewed deep
        ([0], [0], [0]),                                                           # value 0
        ([-2, -1, -3], [-2, -3, -1], [-1, -2, -3]),                                # negatives
        ([1, 3, 2, 4], [1, 2, 4, 3], [3, 1, 4, None, None, 2]),                          # asymmetric
    ]

    # Drop the placeholder entry (test 8 is bogus — postorder [1,2,3,4] is the same
    # as the right-skewed case, ambiguous if values differ from inorder)
    test_cases = [tc for tc in test_cases if tc[2] is not None]

    passed = 0
    failed = 0

    for i, (inorder, postorder, expected) in enumerate(test_cases):
        print(f"========== Test {i} ==========")
        print(f"Inorder:   {inorder}")
        print(f"Postorder: {postorder}")
        print(f"Expected:  {expected}")

        try:
            root = Solution().buildTree(inorder, postorder)
            result = tree_to_level_order(root)
            print_tree(root, "Built tree")
            print(f"Got:       {result}")

            # Sanity: traversals of the built tree should match the inputs
            actual_in = get_inorder(root)
            actual_post = get_postorder(root)
            if actual_in != inorder:
                print(f"⚠️  Inorder mismatch:   built tree gives {actual_in}")
            if actual_post != postorder:
                print(f"⚠️  Postorder mismatch: built tree gives {actual_post}")

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