
# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

def addTwoNumbers(l1:ListNode, l2:ListNode):

    head = ListNode()
    tail = head
    total = 0
    carry = 0
    while l1 or l2 or carry:

        total = carry

        if l1:
            total += l1.val
            l1 = l1.next
        if l2:
            total += l2.val
            l2 = l2.next
        
        value = total % 10
        carry = total // 10
        tail.next = ListNode(value)
        tail = tail.next

    return head.next


l1 = [2,4,3]
l2 = [5,6,4]

node_l1_1 = ListNode(2)
node_l1_2 = ListNode(4)
node_l1_1.next = node_l1_2
node_l1_3 = ListNode(3)
node_l1_2.next = node_l1_3


node_l2_1 = ListNode(5)
node_l2_2 = ListNode(6)
node_l2_1.next = node_l2_2
node_l2_3 = ListNode(4)
node_l2_2.next = node_l2_3

res = addTwoNumbers(node_l1_1,node_l2_1)
while res != None:
    print(res.val)
    res = res.next