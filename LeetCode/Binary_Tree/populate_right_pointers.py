from collections import deque


class Node(object):
    def __init__(self, val=0, left=None, right=None, next=None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


# ---------- Helpers ----------

def build_tree(values):
    """Build a binary tree from a level-order list (LeetCode format).
       `next` pointers are NOT set — that's the job of the solution."""
    if not values:
        return None
    root = Node(values[0])
    queue = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values):
            if values[i] is not None:
                node.left = Node(values[i])
                queue.append(node.left)
            i += 1
        if i < len(values):
            if values[i] is not None:
                node.right = Node(values[i])
                queue.append(node.right)
            i += 1
    return root


def print_tree_structure(root, label=""):
    """Pretty-print the tree level by level (just structure, no next pointers)."""
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


def serialize_via_next(root):
    """
    Walk the tree using ONLY left-child + next pointers, producing the
    LeetCode-style output: each level's values, then '#' for end-of-level.
    This is what actually verifies the solution worked.
    """
    if root is None:
        return []
    out = []
    level_head = root
    while level_head is not None:
        # Walk this level using `next`
        cur = level_head
        while cur is not None:
            out.append(cur.val)
            cur = cur.next
        out.append("#")
        # Find the first node on the next level. Could be left or right of
        # any node on the current level.
        next_head = None
        cur = level_head
        while cur is not None:
            if cur.left is not None:
                next_head = cur.left
                break
            if cur.right is not None:
                next_head = cur.right
                break
            cur = cur.next
        level_head = next_head
    return out


def get_next_chains(root):
    """For debugging: return a list of strings showing the next-pointer chain at each level."""
    if root is None:
        return []
    chains = []
    level_head = root
    while level_head is not None:
        chain = []
        cur = level_head
        while cur is not None:
            chain.append(str(cur.val))
            cur = cur.next
        chains.append(" -> ".join(chain) + " -> #")
        # Find next level head
        next_head = None
        cur = level_head
        while cur is not None:
            if cur.left is not None:
                next_head = cur.left
                break
            if cur.right is not None:
                next_head = cur.right
                break
            cur = cur.next
        level_head = next_head
    return chains


# ---------- Your solution ----------

class Solution(object):
    def connect(self, root):
        
        if root == None:
            return root

        current = [root]

        while current:

            next_level = []
            for node in current:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)

            for idx,node in enumerate(next_level[:-1]):
                node.next = next_level[idx+1]
            
            current = next_level


        


        

        


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_level_order, expected_serialization)
        ([1, 2, 3, 4, 5, None, 7], [1, "#", 2, 3, "#", 4, 5, 7, "#"]),     # example 1
        ([], []),                                                            # example 2: empty
        ([1], [1, "#"]),                                                     # single node
        ([1, 2], [1, "#", 2, "#"]),                                          # root + left only
        ([1, None, 2], [1, "#", 2, "#"]),                                    # root + right only
        ([1, 2, 3], [1, "#", 2, 3, "#"]),                                    # perfect depth 2
        ([1, 2, 3, 4, 5, 6, 7], [1, "#", 2, 3, "#", 4, 5, 6, 7, "#"]),       # perfect depth 3
        ([1, 2, 3, 4, None, None, 7],
         [1, "#", 2, 3, "#", 4, 7, "#"]),                                    # gap between 4 and 7
        ([1, 2, 3, None, 5, 6, None],
         [1, "#", 2, 3, "#", 5, 6, "#"]),                                    # 5 must connect to 6 across parents
        ([1, 2, 3, None, None, 6, None],
         [1, "#", 2, 3, "#", 6, "#"]),                                       # only one node on bottom
        ([1, 2, 3, 4, None, None, 5, 6, None, None, 7],
         [1, "#", 2, 3, "#", 4, 5, "#", 6, 7, "#"]),                         # asymmetric depth 4
        ([0], [0, "#"]),                                                     # value 0
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         [1, "#", 2, 3, "#", 4, 5, 6, 7, "#", 8, 9, 10, 11, 12, 13, 14, 15, "#"]),  # full depth 4
        ([1, 2, None, 3, None, 4, None, 5],
         [1, "#", 2, "#", 3, "#", 4, "#", 5, "#"]),                          # left-skewed
        ([1, None, 2, None, 3, None, 4, None, 5],
         [1, "#", 2, "#", 3, "#", 4, "#", 5, "#"]),                          # right-skewed
        ([2, 1, 3, 0, 7, 9, 1, 2, None, 1, 0, None, None, 8, 8, None, None,
          None, None, 7],
         [2, "#", 1, 3, "#", 0, 7, 9, 1, "#", 2, 1, 0, 8, 8, "#", 7, "#"]),  # complex (LeetCode-style stress)
    ]

    passed = 0
    failed = 0

    for i, (vals, expected) in enumerate(test_cases):
        root = build_tree(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}")
        print_tree_structure(root, "Tree (before connect)")
        print(f"Expected: {expected}")

        try:
            Solution().connect(root)
            result = serialize_via_next(root)
            chains = get_next_chains(root)
            print("Next-pointer chains:")
            for c in chains:
                print(f"  {c}")
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