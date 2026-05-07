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


def all_root_to_leaf_paths(root):
    """Helper for debugging: returns all root-to-leaf paths and their sums."""
    if root is None:
        return []
    paths = []

    def dfs(node, path):
        if node is None:
            return
        path = path + [node.val]
        if node.left is None and node.right is None:
            paths.append((path, sum(path)))
            return
        dfs(node.left, path)
        dfs(node.right, path)

    dfs(root, [])
    return paths


# ---------- Your solution ----------

class Solution(object):
    def hasPathSum(self, root:TreeNode, targetSum):
        
        if root == None:
            return False

        return self.regression_sum(root,0, targetSum)


    def regression_sum(self, root:TreeNode,current_sum, targetSum):

        if root == None:
            return False

        current_sum += root.val

        if current_sum == targetSum and root.left == None and root.right == None:
            return True
        
        return self.regression_sum(root.left,current_sum, targetSum) or self.regression_sum(root.right,current_sum, targetSum)




# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_level_order, targetSum, expected)
        ([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22, True),    # example 1
        ([1, 2, 3], 5, False),                                                  # example 2
        ([], 0, False),                                                          # example 3: empty
        ([], 1, False),                                                          # empty, nonzero target
        ([1], 1, True),                                                          # single node, matches
        ([1], 0, False),                                                         # single node, doesn't match (target ≠ val)
        ([0], 0, True),                                                          # single node 0, target 0
        ([1, 2], 3, True),                                                       # 1 + 2 = 3, leaf is 2
        ([1, 2], 1, False),                                                      # path is 1+2=3, NOT just root
        ([1, 2, 3], 4, True),                                                    # 1 + 3 = 4
        ([1, 2, 3], 3, True),                                                    # 1 + 2 = 3
        ([1, 2, 3], 1, False),                                                   # root alone is not a leaf path
        ([1, -2, -3, 1, 3, -2, None, -1], -1, True),                             # negatives, path 1 + -2 + 1 + -1 = -1
        ([-2, None, -3], -5, True),                                              # all negatives
        ([1, 2], 2, False),                                                      # 2 is not the root, path is 1+2
        ([1, None, 2, None, 3], 6, True),                                        # right-skewed, 1+2+3=6
        ([1, None, 2, None, 3], 3, False),                                       # not a complete root-to-leaf path
        ([1, 2, None, 3], 6, True),                                              # left-skewed, 1+2+3=6
        ([1, 2, 3, 4, 5], 7, True),                                              # 1+2+4=7
        ([1, 2, 3, 4, 5], 8, True),                                              # 1+2+5=8
        ([1, 2, 3, 4, 5], 4, True),                                             # internal-only sum
        ([0, 1, 1], 1, True),                                                    # 0 + 1 = 1
        ([0, 1, 1], 0, False),                                                   # no path sums to 0 (root alone not a leaf)
    ]

    passed = 0
    failed = 0

    for i, (vals, target, expected) in enumerate(test_cases):
        root = build_tree(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}, targetSum={target}")
        print_tree(root, "Tree")
        paths = all_root_to_leaf_paths(root)
        if paths:
            print("Root-to-leaf paths:")
            for p, s in paths:
                print(f"  {p} → sum={s}")
        else:
            print("Root-to-leaf paths: (none — empty tree)")
        print(f"Expected: {expected}")

        try:
            result = Solution().hasPathSum(root, target)
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