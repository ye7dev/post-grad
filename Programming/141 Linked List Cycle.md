# 141. Linked List Cycle

Status: done, in progress
Theme: Linked list
Created time: November 16, 2023 6:01 PM
Last edited time: November 16, 2023 6:28 PM

- 머리 식히기 6
- 과정
    
    ![Untitled](Untitled%20133.png)
    
    - slow, fast pointer 두 개 쓰면 됐던 것 같은데 한번 해보자
        
        
        | slow | fast |
        | --- | --- |
        | 3 | 3 |
        | 2 | 0 |
        | 0 | 2 |
        | -4 | -4 |
    
    ![Untitled](Untitled%20134.png)
    
    | slow | fast |
    | --- | --- |
    | 1 | 1 |
    | 2 | 1 |
    | 1 | 1 |
    - value 만 가지고 했더니 value가 같은 node가 두 개 이상 나오기도 한다
        
        `[-21,10,17,8,4,26,5,35,33,-7,-16,27,-12,6,29,-12,5,9,20,14,14,2,13,-24,21,23,-21,5]`
        
    - 두 노드가 같아 지는 걸 while loop exit 조건으로 하고 loop 밖으로 나오면 return True
        - 안에서 둘 중에 하나라도 None이 나올 때 바로 return False 하면 되는데 문제는 update를 어떻게 에러 없이 하느냐…
- None check의 지저분함…
    - edge case에서 head, head.next, head.next.next까지 None 체크
    - while loop 안에서 slow.next, fast.next, fast.next.next까지 None 체크
    
    ⇒ 결론은 while loop 안에서 fast랑 fast.next의 None만 체크하면 위의 여섯개 다 필요 없음. 다만 시간은 더 걸림 
    
- 코드
    
    ```python
    class Solution:
        def hasCycle(self, head: Optional[ListNode]) -> bool:
            if head is None or head.next is None or head.next.next is None:
                return False 
            slow, fast = head.next, head.next.next
            while slow != fast:
                if slow.next is None:
                    return False 
                slow = slow.next
                if fast.next is None or fast.next.next is None:
                    return False
                fast = fast.next.next
    
            return True
    ```
    
    - 더 간결한 방식
        - 생각해보면 error message는 NoneType object는 next를 갖고 있지 않다는 뜻
        - 더 느리긴 하다
    
    ```python
    def hasCycle(self, head: Optional[ListNode]) -> bool:
            slow, fast = head, head
            while fast is not None and fast.next is not None:
                slow = slow.next
                fast = fast.next.next
    
                if fast == slow: return True 
    
            return False
    ```