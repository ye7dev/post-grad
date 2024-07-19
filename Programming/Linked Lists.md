# Linked Lists

- Top-tips
    - inserting, deleting → O(1)
    - kth element 가져오기 → O(n)
    - dummy head 사용하면 empty list 확인해야 하는 걸 피할 수 있다 ?
    - head랑 tail의 next, prev update 하는 것 잊지 말라
    - singly linked list의 경우 두 개의 iterator 사용하면 유용
        - 하나를 다른 하나보다 한 칸 더 앞에 있게끔

### 7.1 Merge two sorted list

- dummy head를 시작점으로 두고, 그 다음 노드가 실제 정렬된 list의 head가 됨
- 둘 중 더 작은 쪽의 노드를 가져올 때는 tail.next로.
    - 노드를 보낸 쪽에서는 head node를 그 다음 노드로 바꿔야 함
- 노드 붙이고 나서는 tail이 tail.next로 한칸 이동

### 7.2 Reverse a single sublist

- input: s, f, L → L의 s번째 노드부터 f번째 노드까지를 reverse 해라

### 7.3 Test for cyclicity

- cycle이 있으면 cycle의 시작점을, 없으면 null return
- two iterators 사용
- 완전히 이해는 안가지만 이게 핵심
    - 느린 포인터와 빠른 포인터가 사이클 내에서 만나면, 느린 포인터를 리스트의 시작으로 옮기고 두 포인터를 같은 속도로 이동시킵니다. 이 때, 그들이 만나는 지점은 사이클의 시작 지점입니다.
1. slow, fast 만날 때까지 전진(fast는 두 칸씩)
2. 만난 지점에서 cycle 길이 구함 - 다시 제자리로 돌아오는데 필요한 steps 수
3. head에서 시작해서 cycle 길이만큼 포인터 하나 보내 놓음
4. 다시 head에서 시작해서 3이랑 같이 한 칸씩 전진하다가 만나는 지점 return 

### 7.4 Test for overlapping lists - lists are cycle free

- 두 개의 singly linked list 주어질 때, 두 리스트가 공유하는 노드가 있을 수도 있음
- 공유하는 노드가 있는지 없는지 확인
- 일단 어떤 노드 공유한다고 하면 tail 노드가 같아진다는 점에 주목
    - 왜냐면 공유하는 노드에서 서로 다른 next를 가질리 없기 때문에
1. 각 리스트의 길이 구한다
2. 더 긴 쪽에서 두 리스트 길이 차이만큼 전진한다 
3. 하나는 시작점에서 하나는 2에서 한 칸씩 전진하다가 두 노드가 같아지는 지점 있으면 return 

### 7.7 Remove the kth last element from a list

- 링크드 리스트 길이를 저장할 수 없는 상황에서 맨 마지막에서 K번째 요소 삭제하기
1. 포인터 하나를 첫번째 노드에서 시작해서 k만큼 앞으로 전진 시켜 둔다 
    
    → k+1번째 노드에 도착한 상태 
    
2. 두번째 포인터는 dummy(첫번째 노드보다 앞에서 시작)로 초기화
3. 1이 None에 도달할 때까지 1, 2를 한 칸씩 전진시킨다 
    
    → 전체 노드 개수가 n이면, n-(k+1)+1 = n-k-1+1 = n-k 이동 가능
    
    → 두번째 포인터는 dummy에서 시작했기 때문에 n-k 노드에 도착한 상태 
    
4. 3을 마치고 나면 포인터 2의 위치는 (k+1)이 되기 때문에 바로 다음 노드를 삭제하면 된다
    
    → kth last 노드는 앞에서 세면 n-k+1번째 노드 
    
    → 두번째 포인터의 바로 다음 노드가 삭제 대상인 노드
    
5. 2.next를 그 다음 다음 이웃으로 연결 
- 헷갈리는 점
    
    ```python
    while node:
    		node = node.next 
    ```
    
    - node는 null까지 도달해야 전진을 멈추게 된다
    - 어떤 노드에서 두번 이동하면 그 노드보다 두번째 뒤에 있는 노드에 도달하게 된다
    - 노드 간 값이 1씩 증가하는 링크드 리스트에서
        - 시작점이 1일 때, k번 이동하면, 도착 노드는 k+1이다
            - 1 → 2 : 우선 한번 이동하면 도착노드는 1+1 = 2
        - 시작점이 0일 때, k번 이동하면, 도착 노드는 k
            - 0 → 1 : 한번 이동하면 0+1 =1
- 전체 노드 개수가 \(n\)이고, 뒤에서 \(k\)번째 노드를 찾으려 할 때, 앞에서부터 세었을 때의 위치를 알고 싶다면, 해당 노드는 앞에서 \(n - k + 1\)번째 노드입니다.
    - 예를 들어, 전체 노드가 5개 있고(\(n = 5\)), 뒤에서 2번째(\(k = 2\)) 노드를 찾으려 한다면, 앞에서부터 세었을 때 그 노드는 \(5 - 2 + 1 = 4\)번째 노드입니다.

### 7.10 Implement even-odd merge