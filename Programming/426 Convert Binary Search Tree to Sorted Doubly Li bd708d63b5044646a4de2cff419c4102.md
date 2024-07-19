# 426. Convert Binary Search Tree to Sorted Doubly Linked List

Status: in progress, with help
Theme: Divide & Conquer
Created time: December 6, 2023 3:18 PM
Last edited time: December 7, 2023 4:59 PM

- [ ]  재귀 안에서 언제 왼쪽이 연결되고 오른쪽이 연결되는지 곱씹어보면서 짜볼 것
- [x]  divide and conquer
- 과정
    - 쭉 왼쪽으로 내려가면서 부모 자식 관계를 사전에 저장해두기?
    - root가 손잡을 대상
        - 왼쪽 자식의 rightmost child
        - 오른쪽 자식의 leftmost child
    - 마지막으로 leftmost child와 rightmost child를 손잡게 만든다.
    - 중간 노드들에 대해서도 leftmost child, rightmost child를 얻게 하면 되지
    - 여기까지 짜보았다
        
        ```python
        """
        # Definition for a Node.
        class Node:
            def __init__(self, val, left=None, right=None):
                self.val = val
                self.left = left
                self.right = right
        """
        
        class Solution:
            def treeToDoublyList(self, root: 'Optional[Node]') -> 'Optional[Node]':
                head = Node()
                # conquer
                def transform(cur_node, is_left):
                    if not cur_node:
                        return None, None
                    # divide
                    left_leftmost, left_rightmost = transform(cur_node.left, True)
                    right_leftmost, right_rightmost = transform(cur_node.right, False)
                    # combine - cur_node
                    if left_rightmost:
                        cur_node.left = left_rightmost
                    else:
                        left_rightmost = 
                    left_rightmost.right = cur_node
                    cur_node.right = right_leftmost
                    right_leftmost.left = cur_node
                    
                    if is_left:
                        return left_leftmost, left_rightmost
                    return right_leftmost, right_rightmost
        
                # combine - total
                left_leftmost, left_rightmost = transform(root.left, True)
                right_leftmost, right_rightmost = transform(root.right, False)
                left_leftmost.left = right_rightmost
                right_rightmost.right = left_leftmost
                head.next = left_leftmost
                return head
        ```
        
- Editorial
    - standard inorder recursion: left → node → right
        - left, right는 재귀 호출의 일부
        - node : 모든 processing이 끝나는 부분
    - 우리 문제에서의 processing
        - 이전 node를 current node에 연결하는 것
        - 지금까지 만들어진 새로운 doubly linked list에서 가장 큰 node (`last`) node를 keep track 해야 함
        - 그림
            
            ![Untitled](Untitled%20141.png)
            
        - 또한 마지막에 doubly linked list의 ring을 완성하기 위해 가장 작은 값을 가진 node (`first`)도 추적해야 함
    - 알고리즘
        - first, last node를 Null(None)로 초기화
        - standard inorder recursion 호출 `helper(root)`
            - node가 None이 아니면
                - left subtree에 대해 recursive call `helper(node.left)`
                - last node가 None이 아니면 last node와 current node를 연결
                - last node가 None이면 first node를 초기화
                    - last node = None이다 → 아직까지 doubly linked list가 하나도 안만들어졌다 → cur node가 dll의 처음이다 → first node를 cur_node로 초기화하라는 뜻인듯
                - current node를 last node로 mark `last = node`
                - 오른쪽 subtree에 대한 recursion 호출
            - DLL ring을 완성하기 위해 first, last node를 연결
            - return first node
- Editorial 보고 짰는데 first node가 왜 still None?
    
    ```python
    """
    # Definition for a Node.
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right
    """
    
    class Solution:
        def treeToDoublyList(self, root: 'Optional[Node]') -> 'Optional[Node]':
    				first, last = None, None # subproblem의 solution이라고 할 수 있을 듯 
    				# base case
            if not root: return first
            def transform(node):
                # base case - conquer
                if not node: return 
                # left recursive call - divide
                transform(node.left)
                # cur node work - conquer & combine
                nonlocal first, last
                if last is not None:
    								last.right = node
                    ~~last.next = node~~
                    node.left = last 
                else:
                    first = node
                last = node 
                print(last.val)
    
                # right recursive call - divide
                transform(node.right)
    
            transform(root)
            # closing DLL ring - combine
            first.left = last
            last.right = first
            return first # 왜냐면 final solution이 first니까 
    ```
    
- 복습할 때 놓친 점
    - root가 None이면 따로 edge case 처리해줘야 함 - None을 return 해라