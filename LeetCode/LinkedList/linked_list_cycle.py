

# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


def hasCycle(head):
    fast_head:ListNode = head

    while fast_head and fast_head.next:
        head = head.next
        fast_head = fast_head.next.next
        if head is fast_head:
            return True
    return False


head = [3,2,0,-4]
node1 = ListNode(-4)
node2 = ListNode(0)
node3 = ListNode(2)
node4 = ListNode(3)
node1.next = node3
node2.next = node1
node3.next = node2
node4.next = node3

print(hasCycle(node4))