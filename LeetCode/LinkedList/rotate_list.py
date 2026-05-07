class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ---------- Helpers ----------

def build_list(values):
    """Build a linked list from a Python list."""
    dummy = ListNode(0)
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    """Convert a linked list back to a Python list, with cycle guard."""
    out = []
    cur = head
    seen = set()
    while cur:
        if id(cur) in seen:
            out.append(f"<CYCLE back to val={cur.val}>")
            break
        seen.add(id(cur))
        out.append(cur.val)
        cur = cur.next
    return out


def print_list(head, label=""):
    if label:
        print(f"{label}: {to_list(head)}")
    else:
        print(to_list(head))


# ---------- Your solution ----------

class Solution(object):
    def rotateRight(self, head, k):

        if k == 0 or head == None:
            return head
        
        dummy = head
        tail = dummy
        size = 1

        while tail.next != None:
            tail = tail.next
            size +=1
        
        if k%size == 0:
            return head

        new_tail = dummy
        for _ in range(size - (k % size) - 1):
            new_tail = new_tail.next
        new_head = new_tail.next
        tail.next = dummy
        new_tail.next = None


        return new_head


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_list, k, expected_output)
        ([1, 2, 3, 4, 5], 2, [4, 5, 1, 2, 3]),       # canonical example
        ([0, 1, 2], 4, [2, 0, 1]),                    # k > length: should use k % length
        ([], 0, []),                                   # empty list, k=0
        ([], 5, []),                                   # empty list, any k
        ([1], 0, [1]),                                 # single node, k=0
        ([1], 1, [1]),                                 # single node, k=1 (no-op)
        ([1], 99, [1]),                                # single node, large k
        ([1, 2], 0, [1, 2]),                           # k=0, no rotation
        ([1, 2], 1, [2, 1]),                           # rotate two-node list
        ([1, 2], 2, [1, 2]),                           # k == length, full cycle = no-op
        ([1, 2], 3, [2, 1]),                           # k > length, two-node
        ([1, 2, 3, 4, 5], 0, [1, 2, 3, 4, 5]),         # k=0
        ([1, 2, 3, 4, 5], 5, [1, 2, 3, 4, 5]),         # k == length
        ([1, 2, 3, 4, 5], 1, [5, 1, 2, 3, 4]),         # rotate by 1
        ([1, 2, 3, 4, 5], 4, [2, 3, 4, 5, 1]),         # rotate by length-1
        ([1, 2, 3, 4, 5], 7, [4, 5, 1, 2, 3]),         # k > length, equiv to k=2
        ([1, 2, 3, 4, 5], 10, [1, 2, 3, 4, 5]),        # k = 2 * length, no-op
        ([1, 2, 3], 1, [3, 1, 2]),                     # three nodes, k=1
        ([1, 2, 3], 2, [2, 3, 1]),                     # three nodes, k=2
        ([1, 2, 3, 4, 5, 6], 100, [3, 4, 5, 6, 1, 2]), # large k, length 6 → 100 % 6 = 4
    ]

    passed = 0
    failed = 0

    for i, (vals, k, expected) in enumerate(test_cases):
        head = build_list(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}, k={k}")
        print(f"Expected: {expected}")


        result_head = Solution().rotateRight(head, k)
        result = to_list(result_head)
        print(f"Got:      {result}")

        if any(isinstance(x, str) for x in result):
            print("⚠️  Cycle detected in result!")

        if len(result) != len(vals):
            print(f"⚠️  Length wrong: got {len(result)}, expected {len(vals)}")

        if result == expected:
            print("✅ PASS\n")
            passed += 1
        else:
            print("❌ FAIL\n")
            failed += 1


    print(f"========== Results ==========")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")