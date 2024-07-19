# 215. Kth Largest Element in an Array

Status: done, in progress
Theme: heap
Created time: November 1, 2023 5:58 PM
Last edited time: November 1, 2023 6:24 PM

- 나의 30분
    - heapq 써서 제일 작은 것부터 앞에 오게 하고, pop 하려고 했는데 그러면 pop 했을 때 가장 작은게 와야 하니까 제일 큰 게 앞에 와야함. 그러려면 heap에 push 할 때 음수로 넣어야. 음수로 넣으면 가장 작은 게 앞으로 가니까, 절대값이 가장 큰 게 앞으로 들어감
    - heapify는 heap으로 사용하려는 list에 이미 원소가 있을 때 사용. 근데 heapify 자체도 정렬에 해당하는 것인가? 다르다. 최소값을 맨 앞으로 보내주는 것은 맞는데 나머지 부분은 정렬되어 있지 않다
        - You're correct that if you start with an empty list and keep adding elements using **`heappush`**, you don't need to call **`heapify`**. The list will always maintain the heap property.
        - However, if you start with a populated list and you aren't sure if it satisfies the heap property, you should call **`heapify`** before doing any heap operations on it.
        - The resulting list has the property that the smallest element is at the root (index **`0`**), but the rest of the list is not sorted.
    - 문제를 잘못 읽었다 K번째 큰게 와야 한다
    - for문을 다 돌면서 heappush를 해도 list가 정렬되지 않는다 그냥 최소값이 맨 앞에 와있을 뿐
    - heappop을 사용하는게 나을 수도

```python
def findKthLargest(self, nums: List[int], k: int) -> int:
        heapq.heapify(nums)
        # 2번째로 큰 값 == 3번째로 작은 값
        for _ in range(len(nums)-k+1):
            val = heapq.heappop(nums)
        return val
```

- heapify를 해서 작은 값들을 먼저 빼내는 전략. 이 때 헷갈릴 수 있는 것이 K번째로 큰 값은 N-k번째로 작은 값. 그리고 range는 exclusive니까 마지막에 +1 하는 것 빼먹으면 안됨