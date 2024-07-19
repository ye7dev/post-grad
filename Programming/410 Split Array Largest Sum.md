# 410. Split Array Largest Sum

Status: done, in progress, incomplete, 🏋️‍♀️
Theme: DP
Created time: November 23, 2023 3:47 PM
Last edited time: November 23, 2023 10:34 PM

- [ ]  유사문제-1011
- [ ]  유사문제-2064
- [ ]  유사문제-875
- [x]  최적화-binary search solution 보기
- [ ]  binary search solution으로 풀어보기
- 과정
    
    [11/18 시험 문제 ](11%2018%20%E1%84%89%E1%85%B5%E1%84%92%E1%85%A5%E1%86%B7%20%E1%84%86%E1%85%AE%E1%86%AB%E1%84%8C%E1%85%A6%20a407cc1253004b84949e241f61477dde.md) 생각난다 근데 까먹음 ;; 30분 동안 고민해보고 그래도 생각 안나면 pass 하자 
    
    생각 안나서 시험 문제 다시 봤는데 완죠니 비슷한 문제다 
    
    여기까지 짜서 24/31했는데 시간 오바남 ;;
    
    ```python
    class Solution:
        def splitArray(self, nums: List[int], k: int) -> int:
            # edge cases
            if k == 1:
                return sum(nums)
            if k == len(nums):
                return max(nums)
    
            n = len(nums)
            dp = [[-float('inf')] * (k+1) for _ in range(n+1)]
            #dp[0][0] = 0 # no split -> sum = 0 
            for i in range(1, n+1):
                dp[i][1] = sum(nums[:i])
    
            for i in range(1, n+1): # array range from 0:1 to 0:n # i: exclusive boundary
                for j in range(2, min(i, k)+1): # num_split starts from 1 not zero 
                    for l in range(1, i):
                        cur_min = max(dp[l][j-1], sum(nums[l:i]))
                        if dp[i][j] == -float('inf'):
                            dp[i][j] = cur_min
                        else:
                            dp[i][j] = min(dp[i][j], cur_min)
    
            return dp[n][k]
    ```
    
- 코드
    
    prefix sum 도입해서 시간 오바는 간신히 면했는데 binary search 도입 등 더 최적화할 부분이 많다 
    
    ```python
    class Solution:
        def splitArray(self, nums: List[int], k: int) -> int:
            # edge cases
            if k == 1:
                return sum(nums)
            if k == len(nums):
                return max(nums)
    
            n = len(nums)
            dp = [[float('inf')] * (k+1) for _ in range(n+1)]
            dp[0][0] = 0 # no split -> sum = 0 
    
            prefix_sums = [0]*(n+1)
            for i in range(1, n+1):
                prefix_sums[i] = prefix_sums[i-1] + nums[i-1]
    
            for i in range(1, n+1):
                dp[i][1] = prefix_sums[i]
    
            for i in range(1, n+1): # array range from 0:1 to 0:n # i: exclusive boundary
                for j in range(2, min(i, k)+1): # num_split starts from 1 not zero 
                    for l in range(1, i):
                        cur_min = max(dp[l][j-1], prefix_sums[i]-prefix_sums[l])
                        dp[i][j] = min(dp[i][j], cur_min)
    
            return dp[n][k]
    ```
    
- binary sea
    
    ```python
    def splitArray(nums, m):
    		l, r = 0, 0
    		n = len(nums)
    		l, r = max(nums), sum(nums)
    
        while l < r:
          mid = (l+r)//2 # mid를 조정하다 보면 subarray 개수가 조정됨 
          temp_sum, num_split = 0, 1 # num_split: subarray 합이 mid랑 같거나 그보다 조금 큰 subarray 개수
          for num in nums:
              if temp_sum + num <=mid: 
                  temp_sum += num
              else:
                  temp_sum = num # new split
                  num_split += 1 
    
          if num_split > m: # mid보다 더 큰 합을 가진 subarray가 너무 많다-> mid를 더 키워서 덜 쪼개도 되게끔 
    					l = mid+1
          else: # mid보다 더 큰 합을 가진 subarray가 몇 안된다 -> mid를 줄여서 더 쪼갤 수 있도록 
    					r = mid # num_split == m일 때도 포함하기 때문에 mid-1이 아니고 그냥 mid
          return r
    ```
    
    - find the minimum element which is larger than the target
        - 사실 등호가 핵심임. 더 큰 수 중에 최소를 찾고 싶으면 등호일 때 left를 mid+1로 밀고, 더 작은 수 중에 최대를 찾고 싶으면 등호일 right를 mid-1로 당긴다
        
        ```python
        def min_larger_than_bs(arr, target):
            left, right = 0, len(arr)-1
        
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] <= target:
                    left = mid + 1
                else:
                    right = mid - 1
        
            if left < len(arr):
                return arr[left]
            else:
                return 'None'
        
        def max_less_than_bs(arr, target):
            left, right = 0, len(arr)-1
        
            while left <= right:
                mid = (left + right) // 2
                if arr[mid] >= target:
                    right = mid - 1
                else:
                    left = mid + 1
        		
        		# right가 left보다 더 앞으로 가면서(더 작은 수를 가리키며) while loop 종료하니까
            if right < len(arr):
                return arr[right]
            else:
                return 'None'
        
        x = [2, 5, 7, 8, 10]
        target = 7
        print(min_larger_than_bs(x, target)) # 8
        print(max_less_than_bs(x, target)) # 5
        ```