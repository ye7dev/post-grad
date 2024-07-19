# 21. Merge Two Sorted Lists

Status: done, in progress
Theme: Linked list
Created time: November 22, 2023 1:55 PM
Last edited time: November 22, 2023 2:03 PM

몸풀기 easy 잘했다요 원타임 원킬

splice 잇다

- 코드
    
    ```python
    class Solution:
        def mergeTwoLists(self, node1: Optional[ListNode], node2: Optional[ListNode]) -> Optional[ListNode]:
            head = ListNode()
            start = head 
            while node1 is not None and node2 is not None:
                if node1.val > node2.val:
                    head.next = node2
                    node2 = node2.next # 여기서 None에 대한 조건문 안달아도 될런지? 
                else:
                    head.next = node1
                    node1 = node1.next 
                head = head.next 
            if node1 is not None:
                head.next = node1 
            if node2 is not None:
                head.next = node2
            return start.next
    ```