# 295. Find Median from Data Stream

Status: done, in progress
Theme: heap
Created time: November 2, 2023 2:56 PM
Last edited time: November 2, 2023 4:45 PM

- 나의 30분
    - heappop을 하고 난 원소를 버리면 안되고 다시 Heap에 넣어줘야 함. 같은 Heap을 대상으로 이러저러한 연산을 수행하기 때문
    - self.temp을 사용해서 pop 한 원소들을 잠시 넣어놨다가 다시 Heap에 push 했는데 time error
    - addNum 할 때 차라리 다 뺐다가 다시 넣으면? 그래도 time error
    - 최선의 코드 (TLE)
        
        ```python
        import heapq
        
        class MedianFinder:
        
            def __init__(self):
                self.heap = []
                self.temp = [] 
                self.last_in = float('inf')
        
            def addNum(self, num: int) -> None:
                if not self.heap or num <= self.heap[0]:
                    heapq.heappush(self.heap, num)
                else:
                    while self.heap and self.heap[0] < num:
                        self.temp.append(heapq.heappop(self.heap))
                    self.temp.append(num)
                    while self.heap:
                        self.temp.append(heapq.heappop(self.heap))
                    self.heap = self.temp
                    self.temp = self.heap
        
            def findMedian(self) -> float:
                mid = len(self.heap) // 2
                if (len(self.heap) & 1) == 0: # even
                    return (self.heap[mid-1] + self.heap[mid]) / 2
                else:
                    return self.heap[mid]
        ```
        
- 남의 기막힌 아이디어
    - small, large 두 개의 heap 사용
    - small의 원소 수는 항상 n // 2, large는 n//2 +1 (홀수) or n//2 (짝수)
        
        → 이렇게 되면 mid 계산은
        
        - 홀수 array : large에서 smallest pop
        - 짝수 array : (small 에서 largest + large에서 smallest) / 2
    - small에서는 largest를 pop 해야 하기 때문에, 음수로 넣어줘야 min heap에서 pop 때렸을 때 가장 큰 수가 나옴
    - 새로운 원소가 들어올 때 small 음수로 넣고, 거기서 나오는 애를 large로 보내야 함 → heapq.heappushpop을 쓰면 더 빠르다고 함
- 남의 아이디어 내가 구현
    
    ```python
    import heapq
    class MedianFinder:
    
        def __init__(self):
            self.small = []
            self.large = []
            
    
        def addNum(self, num: int) -> None:
            if len(self.small) == len(self.large):
                temp = heapq.heappushpop(self.small, -num)
                heapq.heappush(self.large, -temp)
            elif len(self.small) < len(self.large): # send someone to small
                if num <= self.large[0]:
                    heapq.heappush(self.small, -num)
                else: 
                    temp = heapq.heappushpop(self.large, num)
                    heapq.heappush(self.small, -temp)
            else: # send someone to large
                if -num <= self.small[0]: # x is larger than largest in small
                    heapq.heappush(self.large, num)
                else: # send current largest in small to large 
                    temp = heapq.heappushpop(self.small, -num)
                    heapq.heappush(self.large, -temp)
            
    
        def findMedian(self) -> float:
            if len(self.large) != len(self.small): # odd
                return self.large[0]
            else:
                return (self.large[0]-self.small[0]) / 2
            
    
    # Your MedianFinder object will be instantiated and called as such:
    # obj = MedianFinder()
    # obj.addNum(num)
    # param_2 = obj.findMedian()
    ```
    
- 남의 아이디어 남이 구현
    - small, large 길이가 같으면 small에서 제일 큰 수를 꺼내서 large로
    - 같지 않으면(무조건 large가 더 기니까) large에서 제일 작은 수를 꺼내서 small로
    - 이 때 small에서 오고 가는 수는 음수, large에서 오고 가는 수는 양수임을 주의
    
    ```python
    from heapq import *
    
    class MedianFinder:
        def __init__(self):
            self.small = []  # the smaller half of the list, max heap (invert min-heap)
            self.large = []  # the larger half of the list, min heap
    
        def addNum(self, num):
            if len(self.small) == len(self.large):
                heappush(self.large, -heappushpop(self.small, -num))
            else:
                heappush(self.small, -heappushpop(self.large, num))
    
        def findMedian(self):
            if len(self.small) == len(self.large):
                return float(self.large[0] - self.small[0]) / 2.0
            else:
                return float(self.large[0])
    
    # 18 / 18 test cases passed.
    # Status: Accepted
    # Runtime: 388 ms
    ```