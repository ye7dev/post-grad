# 1964. Find the Longest Valid Obstacle Course at Each Position

Status: done, in progress
Theme: DP, Longest Increasing Subsequence
Created time: January 22, 2024 11:31 AM
Last edited time: January 22, 2024 3:45 PM

- Trial
    - 예제 통과 60/78에서 TLE
        
        ```python
        from bisect import bisect_right
        class Solution:
            def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
                n = len(obstacles)
                ans = [1] * n
        
                for i in range(n):
                    for j in range(i):
                        if obstacles[i] >= obstacles[j]:
                            ans[i] = max(ans[j]+1, ans[i])
                
                return ans
        ```
        
- AC 코드
    
    ```python
    from bisect import bisect_right
    class Solution:
        def longestObstacleCourseAtEachPosition(self, obstacles: List[int]) -> List[int]:
            n = len(obstacles)
            ans = [1] * n
            # base case 
            lis = [obstacles[0]]
    
            for i in range(1, n):
                h = obstacles[i]
                lis_idx = bisect_right(lis, h)
                if lis_idx == len(lis):
                    lis.append(h)
                else:
                    lis[lis_idx] = h
                ans[i] += lis_idx
            return ans
    ```
    
    - `lis = [obstacles[0]]`
        - 길이가 1인 subsequence 중 아직까지 본 건 첫번째 원소뿐이라 초기화. 만약 obstacles[0]보다 작은 값을 가진 원소가 더 뒤에 나오면 lis[0]은 대체되게 될 것. 왜냐면 늘 길이 i+1의 shortest ending height가 list[i]이기 때문에
    - `lis_idx == len(lis)`
        - 아직 current height보다 큰 값이 한 번도 안 나온 경우
        - lis의 마지막 원소: 인덱스가 len(lis)-1이므로 길이는 len(lis)인 subsequence 들 중 shortest ending height
            
            → 근데 이 값보다 현재 height가 더 크다고 하면, 현재 height를 길이가 len(lis)인 subsequence 뒤에 붙일 수 있다는 의미 
            
            ⇒ 따라서 현재 index 자리에서 가질 수 있는 longest course 길이는 len(lis+1) = lis_idx +1
            
    - `lis[lis_idx] = h`
        - current height보다 큰 값을 shortest ending height로 갖는 길이가 더 긴 subsequence가 존재
        - 현재 height가 속할 수 있는 곳은 길이가 lis_idx+1인 어떤 subarray. 근데  여기에 append 되는 건 아니고, shortest ending을 h로 대체하는 것
        
        ⇒ 현재 index에서 가질 수 있는 Longest course 길이는 lis_idx +1
        
- Editorial
    - 10**5까지 input 길이가 길어지면 O(n^2) solution들은 TLE 난다고 봐야 함
    - **Approach: Greedy + Binary Search**
        - Intuition
            - i에서의 longest course를 구하기 위해 필요한 것
                1. obstacles[i]: mandatory
                2. i보다 앞에 나오면서 obstacles[i]와 같거나 그보다 작은 값을 가진 원소의 longest course 
            - i보다 앞선 원소들의 obstacle course를 조정해야 → i에 왔을 때 앞선 원소의 course 마지막 값이 obstacles[i]보다 작거나 같은 경우에, obstacles[i]를 append → longest course at i
                - 조건을 만족하는 previous course 중 가장 긴 것을 greedily choose
            - 문제 - 길이가 같은 sequence도 여럿일 수 있어서 각각을 다 저장하는 건 비효율 → shortest ends를 가진 course에 주목
                - 그리고 sequence 자체를 저장할 필요 없고 길이만 저장하면 됨
            
            ⇒ `lis[i]` 
            
            - 길이가 i+1
            - shortest ending obstacle - 마지막 원소 길이가 가장 작은 subseq
            - 마지막 원소의 길이
            - 예) lis[4] = 7
                - 길이가 5인 subseq 중 마지막 원소가 가장 작은 크기를 갖는 subseq의 마지막 원소 값
            - i th iteration step - 현재 obstacle로 끝나는 longest course를 찾아야
                - 찾고 나면 현재 원소 append만 하면 됨
                - lis에 binary search 적용
                    - find the rightmost insertion position of current obstacle value to lis
                - 예(그림)
                    - current obstacle h = 6인 경우, lis에서 6이 낄 수 있는 rightmost 자리는 index 4
                    
                    → 6 바로 앞의 lis[3] 의 longest course 길이가 4라는 의미 → 여기에 6을 마지막에 붙이기만 하면 6에 대한 Longest course = 4 +1 = 5
                    
                
                ![Untitled](Untitled%20214.png)
                
                - obstacle, answer, lis의 index 의미 구분
                    
                    ![Untitled](Untitled%20215.png)
                    
                    - obstacles[i] : 주어진 array에서 i번째 위치의 height
                    - answer[i]: i 위치에서 조건 만족하는 Longest course의 길이
                    - lis[i]: 길이가 i+1인 increasing subseqences 중, 마지막 원소의 길이가 가장 짧은 subsequence의, 마지막 원소 길이