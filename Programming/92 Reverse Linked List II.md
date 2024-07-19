# 92. Reverse Linked List II

Status: done, in progress
Theme: Linked list
Created time: February 28, 2024 12:02 PM
Last edited time: February 28, 2024 12:07 PM

- AC 코드
    - 바뀌는 건 next node다 !
    - 포인터 끊는 순서
        1. curr → next 를 끊는다 (next passing 하고 next의 next와 연결)
        2. next → next.next를 끊는다 (next는 sublist_head의 next, 현재 상태에서 sublist node 중 가장 앞에 있는 노드에 연결) 
        3. sublist_head → sublist_head.next 끊는다 (sublist_head 다음에는 next 노드가 오게 됨)
    
    ```python
    # Definition for singly-linked list.
    # class ListNode:
    #     def __init__(self, val=0, next=None):
    #         self.val = val
    #         self.next = next
    class Solution:
        def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
            dummy_head = sublist_head = ListNode(0, head)
            for _ in range(left-1):
                sublist_head = sublist_head.next
    
            curr = sublist_head.next 
            for _ in range(right-left):
                next_node = curr.next
                curr.next, next_node.next, sublist_head.next = next_node.next, sublist_head.next, next_node 
            return dummy_head.next
    ```