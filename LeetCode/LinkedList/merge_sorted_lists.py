

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def mergeTwoLists(list1:ListNode, list2:ListNode):

    head = ListNode()
    tail = head
    while list1 is not None and list2 is not None:
        if list1.val < list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 if list1 else list2

    return head.next

def build_list(values):
    dummy = ListNode()
    tail = dummy
    for x in values:
        tail.next = ListNode(x)
        tail = tail.next
    return dummy.next  # skip dummy

def print_list(head, label=None):
    """Print a linked list inline, e.g. 1 -> 2 -> 4 -> None"""
    parts = []
    node = head
    while node is not None:
        parts.append(str(node.val))
        node = node.next
    line = " -> ".join(parts) + " -> None"
    if label:
        line = f"{label}: {line}"
    print(line)

head_l1 = build_list([1, 2, 4])
head_l2 = build_list([1, 3, 4])

print_list(head_l1, "l1")               # 1 -> 2 -> 4 -> 0 -> None
print_list(head_l2, "l2")         # l2: 1 -> 3 -> 4 -> 0 -> None


merged = mergeTwoLists(head_l1,head_l2)
print_list(merged, "merged")      # merged: 1 -> 1 -> 2 -> 3 -> 4 -> 4 -> 0 -> 0 -> None

