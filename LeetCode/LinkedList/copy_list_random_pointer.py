"""
# Definition for a Node.
class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Node:
    def __init__(self, x, next=None, random=None):
        self.val = int(x)
        self.next = next
        self.random = random


# ---------- Helpers to build/inspect lists ----------

def build_list(pairs):
    """Build a linked list from [[val, random_index], ...] format."""
    if not pairs:
        return None
    nodes = [Node(val) for val, _ in pairs]
    for i, (_, rand_idx) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if rand_idx is not None:
            nodes[i].random = nodes[rand_idx]
    return nodes[0]


def to_pairs(head):
    """Convert linked list back to [[val, random_index], ...] format."""
    nodes = []
    cur = head
    while cur:
        nodes.append(cur)
        cur = cur.next
    index_of = {id(n): i for i, n in enumerate(nodes)}
    return [
        [n.val, index_of[id(n.random)] if n.random else None]
        for n in nodes
    ]


def print_list(head, label=""):
    """Pretty-print the list with node identities for debugging."""
    if label:
        print(f"--- {label} ---")
    cur = head
    nodes = []
    while cur:
        nodes.append(cur)
        cur = cur.next
    for i, n in enumerate(nodes):
        rand = "None"
        if n.random is not None:
            try:
                rand_idx = nodes.index(n.random)
                rand = f"idx={rand_idx} (val={n.random.val})"
            except ValueError:
                rand = f"EXTERNAL NODE! val={n.random.val} id={id(n.random)}"
        print(f"  [{i}] val={n.val}  id={id(n)}  next={'->' if n.next else 'None'}  random={rand}")
    print()


def assert_deep_copy(original_head, copied_head):
    """Verify the copy is structurally identical AND uses no original nodes."""
    orig_nodes, copy_nodes = [], []
    a, b = original_head, copied_head
    while a or b:
        assert a is not None and b is not None, "Length mismatch"
        orig_nodes.append(a)
        copy_nodes.append(b)
        a, b = a.next, b.next

    orig_ids = {id(n) for n in orig_nodes}
    for i, (o, c) in enumerate(zip(orig_nodes, copy_nodes)):
        assert o.val == c.val, f"Value mismatch at {i}: {o.val} vs {c.val}"
        assert id(c) not in orig_ids, f"Node {i} in copy IS an original node!"
        if c.random is not None:
            assert id(c.random) not in orig_ids, f"random of node {i} points to ORIGINAL list!"
        # Check random points to the structurally correct node
        if o.random is None:
            assert c.random is None, f"random mismatch at {i}: should be None"
        else:
            o_idx = orig_nodes.index(o.random)
            c_idx = copy_nodes.index(c.random)
            assert o_idx == c_idx, f"random index mismatch at {i}: {o_idx} vs {c_idx}"
    print("✅ Deep copy verified.\n")


# ---------- Your solution ----------

class Solution(object):
    def copyRandomList(self, head:Node):

        res = Node(0) 
        res_tail = res
        nodes = {}
        tail = head

        # Generate Nodes
        while tail != None:
            new_node = Node(tail.val)
            res_tail.next = new_node
            res_tail = res_tail.next
            nodes[tail] = new_node
            tail = tail.next

        # Fill in randoms
        res_tail = res.next
        tail = head
        while res_tail != None:
 
            res_tail.random = nodes[tail.random] if tail.random != None else None
            tail = tail.next
            res_tail = res_tail.next

        return res.next


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
        [[1, 1], [2, 1]],
        [[3, None], [3, 0], [3, None]],
        [],                    # empty list
        [[1, None]],           # single node, no random
        [[1, 0]],              # single node pointing to itself
    ]

    for i, tc in enumerate(test_cases):
        print(f"========== Test {i} ==========")
        head = build_list(tc)
        print_list(head, "Original BEFORE")

        copied = Solution().copyRandomList(head)

        print_list(head, "Original AFTER (should be unchanged structurally)")
        print_list(copied, "Copy")

        try:
            assert_deep_copy(head, copied)
            result = to_pairs(copied)
            print(f"Output pairs: {result}")
            print(f"Expected:     {tc}")
            print(f"Match: {result == tc}\n")
        except AssertionError as e:
            print(f"❌ {e}\n")