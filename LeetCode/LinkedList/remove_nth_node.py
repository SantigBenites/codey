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
    def removeNthFromEnd(self, head, n):
        
        
        dummy = ListNode(0, head)

        idx = 0
        pointer = dummy
        while idx < n:
            pointer = pointer.next
            idx +=1

        n_behind = dummy

        while pointer.next != None:
            n_behind = n_behind.next
            pointer = pointer.next

        

        n_behind.next = n_behind.next.next
        return dummy.next


# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_list, n, expected_output)
        ([1, 2, 3, 4, 5], 2, [1, 2, 3, 5]),    # example 1: remove from middle-ish
        ([1], 1, []),                           # example 2: remove only node
        ([1, 2], 1, [1]),                       # example 3: remove tail of two
        ([1, 2], 2, [2]),                       # remove HEAD of two-node list
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4]),     # remove tail
        ([1, 2, 3, 4, 5], 5, [2, 3, 4, 5]),     # remove head (n == length)
        ([1, 2, 3, 4, 5], 3, [1, 2, 4, 5]),     # remove middle
        ([1, 2, 3], 2, [1, 3]),                 # remove middle of three
        ([1, 2, 3], 3, [2, 3]),                 # remove head of three
        ([1, 2, 3], 1, [1, 2]),                 # remove tail of three
        ([7, 7, 7, 7], 2, [7, 7, 7]),           # duplicate values
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4, [1, 2, 3, 4, 5, 6, 8, 9, 10]),  # longer
    ]

    passed = 0
    failed = 0

    for i, (vals, n, expected) in enumerate(test_cases):
        head = build_list(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}, n={n}")
        print(f"Expected: {expected}")

        result_head = Solution().removeNthFromEnd(head, n)
        result = to_list(result_head)
        print(f"Got:      {result}")

        if any(isinstance(x, str) for x in result):
            print("⚠️  Cycle detected in result!")

        if len(result) != len(vals) - 1:
            print(f"⚠️  Length wrong: got {len(result)}, expected {len(vals) - 1}")

        if result == expected:
            print("✅ PASS\n")
            passed += 1
        else:
            print("❌ FAIL\n")
            failed += 1


    print(f"========== Results ==========")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")