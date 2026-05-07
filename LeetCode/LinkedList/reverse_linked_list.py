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
    """Convert a linked list back to a Python list."""
    out = []
    cur = head
    while cur:
        out.append(cur.val)
        cur = cur.next
    return out


def print_list(head, label=""):
    """Pretty-print the list."""
    if label:
        print(f"{label}: {to_list(head)}")
    else:
        print(to_list(head))


# ---------- Your solution ----------

class Solution(object):
    def reverseBetween(self, head:ListNode, left, right):
        
        dummy = ListNode(0, head)
        res = dummy
        idx = 0
        while idx < left - 1:
            res = res.next
            idx += 1
        head_before = res

        reverse_start = res.next
        prev = None
        curr = reverse_start
        steps = right - left + 1
        for _ in range(steps):
            save = curr.next
            curr.next = prev
            prev = curr
            curr = save
        
        head_before.next = prev
        reverse_start.next = curr
        
        print_list(head, "before reverse")
        

        return dummy.next



# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_list, left, right, expected_output)
        ([1, 2, 3, 4, 5], 2, 4, [1, 4, 3, 2, 5]),   # example 1: middle reversal
        ([5], 1, 1, [5]),                            # example 2: single node
        ([1, 2, 3, 4, 5], 1, 5, [5, 4, 3, 2, 1]),    # reverse entire list
        ([1, 2, 3, 4, 5], 1, 1, [1, 2, 3, 4, 5]),    # left == right at head, no change
        ([1, 2, 3, 4, 5], 3, 3, [1, 2, 3, 4, 5]),    # left == right in middle, no change
        ([1, 2, 3, 4, 5], 1, 3, [3, 2, 1, 4, 5]),    # reverse from head
        ([1, 2, 3, 4, 5], 3, 5, [1, 2, 5, 4, 3]),    # reverse to tail
        ([1, 2], 1, 2, [2, 1]),                       # two nodes, full reverse
        ([1, 2], 1, 1, [1, 2]),                       # two nodes, no change
        ([1, 2, 3], 2, 3, [1, 3, 2]),                 # three nodes, reverse last two
        ([1, 2, 3], 1, 2, [2, 1, 3]),                 # three nodes, reverse first two
        ([3, 5], 1, 2, [5, 3]),                       # leetcode-style edge case
        ([1, 2, 3, 4, 5, 6, 7], 2, 6, [1, 6, 5, 4, 3, 2, 7]),  # longer middle reversal
    ]

    passed = 0
    failed = 0

    for i, (vals, left, right, expected) in enumerate(test_cases):
        head = build_list(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}, left={left}, right={right}")
        print(f"Expected: {expected}")

        result_head = Solution().reverseBetween(head, left, right)
        result = to_list(result_head)
        print(f"Got:      {result}")

        if result == expected:
            print("✅ PASS\n")
            passed += 1
        else:
            print("❌ FAIL\n")
            failed += 1


    print(f"========== Results ==========")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")