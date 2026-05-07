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
    # Cycle guard so an accidental loop doesn't hang forever
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
    """Pretty-print the list."""
    if label:
        print(f"{label}: {to_list(head)}")
    else:
        print(to_list(head))


def check_no_node_reuse_or_loss(original_values, result_head):
    """Sanity check: result should contain exactly the same node values, same multiset."""
    result = to_list(result_head)
    if any(isinstance(x, str) for x in result):  # cycle detected
        return False, "Cycle detected in result list"
    if sorted(result) != sorted(original_values):
        return False, f"Node set differs. Expected multiset {sorted(original_values)}, got {sorted(result)}"
    return True, "OK"


# ---------- Your solution ----------

class Solution(object):
    def reverseKGroup(self, head, k):
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # TODO 1: find the k-th node from group_prev (i.e., the last node of the next group).
            #         If there aren't k nodes left, break out of the loop.
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if kth is None:
                    break
            if kth is None:
                break  # exits the outer while True

            # TODO 2: identify the boundaries of the group you're about to reverse:
            #   - group_start: the first node of the group (it'll become the tail after reversal)
            #   - group_next:  the node AFTER the group (it'll be the head_after for stitching)
            group_start = group_prev.next
            group_next = kth.next

            # TODO 3: reverse the group [group_start ... kth].
            #         This is the same 4-line reversal pattern from reverseBetween.
            #         Initialize prev = group_next so the tail (group_start) ends up
            #         pointing at the right place automatically — no fix-up needed.
            prev = group_next
            curr = group_start
            while curr is not group_next:
                save = curr.next
                curr.next = prev
                prev = curr
                curr = save

            # TODO 4: stitch this reversed group to the previous group.
            #         After reversal, `kth` is the new head of this group (since it was the last,
            #         now it's the first). Connect group_prev to it.
            group_prev.next = kth

            # TODO 5: advance group_prev for the next iteration.
            #         It should become the new tail of the just-reversed group.
            group_prev = group_start

        return dummy.next





# ---------- Test cases ----------

if __name__ == "__main__":
    test_cases = [
        # (input_list, k, expected_output)
        ([1, 2, 3, 4, 5], 2, [2, 1, 4, 3, 5]),           # example 1: leftover at end
        ([1, 2, 3, 4, 5], 3, [3, 2, 1, 4, 5]),           # example 2: leftover at end
        ([1, 2, 3, 4, 5], 1, [1, 2, 3, 4, 5]),           # k=1, no change
        ([1, 2, 3, 4, 5], 5, [5, 4, 3, 2, 1]),           # k == length, full reverse
        ([1, 2, 3, 4, 5, 6], 2, [2, 1, 4, 3, 6, 5]),     # exact multiple, k=2
        ([1, 2, 3, 4, 5, 6], 3, [3, 2, 1, 6, 5, 4]),     # exact multiple, k=3
        ([1, 2, 3, 4, 5, 6], 6, [6, 5, 4, 3, 2, 1]),     # k == length even
        ([1], 1, [1]),                                    # single node, k=1
        ([1, 2], 2, [2, 1]),                              # two nodes
        ([1, 2], 1, [1, 2]),                              # two nodes, no change
        ([1, 2, 3], 4, [1, 2, 3]),                        # k > length: should be unchanged
        # ^ note: leetcode constraint says k <= n, but worth testing your code's behavior
        ([1, 2, 3, 4, 5, 6, 7], 3, [3, 2, 1, 6, 5, 4, 7]),  # leftover of 1
        ([1, 2, 3, 4, 5, 6, 7, 8], 3, [3, 2, 1, 6, 5, 4, 7, 8]),  # leftover of 2
        ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4, [4, 3, 2, 1, 8, 7, 6, 5, 9, 10]),  # longer
    ]

    passed = 0
    failed = 0

    for i, (vals, k, expected) in enumerate(test_cases):
        head = build_list(vals)
        print(f"========== Test {i} ==========")
        print(f"Input:    {vals}, k={k}")
        print(f"Expected: {expected}")


        result_head = Solution().reverseKGroup(head, k)
        result = to_list(result_head)
        print(f"Got:      {result}")

        ok, msg = check_no_node_reuse_or_loss(vals, result_head)
        if not ok:
            print(f"⚠️  Sanity check failed: {msg}")

        if result == expected:
            print("✅ PASS\n")
            passed += 1
        else:
            print("❌ FAIL\n")
            failed += 1


    print(f"========== Results ==========")
    print(f"Passed: {passed}/{len(test_cases)}")
    print(f"Failed: {failed}/{len(test_cases)}")