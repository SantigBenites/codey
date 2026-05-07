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
    def deleteDuplicates(self, head):
        
        dummy = ListNode(0, head)

        pointer = dummy

        while pointer.next != None and pointer.next.next != None:

            head = pointer

            while head.next and  head.next.next and head.next.val == head.next.next.val:
                head = head.next



            if pointer == head:
                pointer = pointer.next
            else:
                pointer.next = head.next.next


        
        return dummy.next



# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_list, expected_output)
        ([1, 2, 3, 3, 4, 4, 5], [1, 2, 5]),         # example 1: duplicates in middle
        ([1, 1, 1, 2, 3], [2, 3]),                   # example 2: duplicates at head
        ([], []),                                     # empty list
        ([1], [1]),                                   # single node
        ([1, 1], []),                                 # two duplicates, all removed
        ([1, 2], [1, 2]),                             # two distinct nodes
        ([1, 1, 2], [2]),                             # duplicate at head, single distinct after
        ([1, 2, 2], [1]),                             # distinct at head, duplicate at tail
        ([1, 1, 1], []),                              # all same value
        ([1, 1, 2, 2, 3, 3], []),                     # every value duplicated
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),           # no duplicates at all
        ([1, 1, 2, 3, 3, 4, 5, 5], [2, 4]),           # multiple duplicate runs, scattered
        ([1, 2, 2, 3, 4, 4, 5], [1, 3, 5]),           # alternating
        ([-3, -1, -1, 0, 0, 0, 2], [-3, 2]),          # negatives + zeros
        ([1, 1, 1, 1, 1, 2], [2]),                    # long run of duplicates at head
        ([1, 2, 3, 3, 3, 3], [1, 2]),                 # long run of duplicates at tail
        ([1, 1, 2, 3], [2, 3]),                       # leetcode-style edge: head dup of length 2
    ]

    passed = 0
    failed = 0

    for i, (vals, expected) in enumerate(test_cases):
        head = build_list(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}")
        print(f"Expected: {expected}")

        result_head = Solution().deleteDuplicates(head)
        result = to_list(result_head)
        print(f"Got:      {result}")

        if any(isinstance(x, str) for x in result):
            print("⚠️  Cycle detected in result!")

        if result == expected:
            print("✅ PASS\n")
            passed += 1
        else:
            print("❌ FAIL\n")
            failed += 1

    print(f"========== Results ==========")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")