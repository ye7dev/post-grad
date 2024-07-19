# 918. Maximum Sum Circular Subarray

Status: done, in progress
Theme: DP
Created time: January 12, 2024 1:58 PM
Last edited time: January 12, 2024 4:24 PM

class Solution:
def maxProfit(self, prices: List[int]) -> int:
min_price = float('inf')
max_profit = 0
for i in range(len(prices)):
if prices[i] < min_price:
min_price = prices[i]
elif prices[i] - min_price > max_profit:
max_profit = prices[i] - min_price

```
    return max_profit

```

- 문제 이해
    
    kadane’s algorithm에 index로 장난을 친 것 같구만 
    
    아 근데 원소가 똑같은 애들이 둘 있음. 그리고 원소는 음수로 나올 수 있음 
    
    근데 왜 그냥 카데인만 쓰면 안되는 거지? 어차피 input nums 자체는 그냥 array인 것 같고만 
    
    아하 subsequence가 아니라 subarray네. subarray는 예를 들어 [1, -2, 3, -2]에서 [1, 3]만 가져올 수 없다. [3]만 가져오거나 [1, -2, 3]을 통째로 다 가져와야 함 
    
    그리고 여기서 circular 제약이 발동되는 것. 왜냐면 nums에 끝이 없기 때문에…
    
    [5, -3, 5]의 경우 [5, 5]가 나올 수 있다. 왜냐면 끝이 맞닿아 있는 형태기 때문에. 
    
    → 다시 보면 5, -3, 5, 5, -3, 5, 5, … 가 무한히 있을 때 여기서 max sum이면서 원소가 한번씩만 들어 있는 subarray를 구하는 것이 문제 
    
    nums[2]의 next element: nums[(2+1)%3)] = nums[0]
    
    - dictionary를 써야 하나? 각 원소가 한번씩 쓰였다는 것을 어떻게 체크?
    - 마지막 원소 한번만 붙이면 될 것 같은데…
        - 그니까 얘를들어 [5, -3, 5] 랑 [-3, 5, 5] 두 개 가져다가 쓰면 될 것 같다.
        - 난 천재인가 후후
- subarray는 contiguous
    - subsequence는 순서 바꾸는 거 없이 중간 원소 몇 개 빼서 만들 수 있는 경우. not contiguous
- 누적 합 vs. 현재 원소
    - 누적 합 + 현재 원소가 제일 큰 경우 → subarray에 현재 원소 추가
    - 누적 합이 제일 큰 경우 → 변화 없음
    - 현재 원소가 제일 큰 경우 → subarray에 현재 원소만 넣음
- Trial
    - 96/111 TLE
        
        ```python
        class Solution:
            def maxSubarraySumCircular(self, nums: List[int]) -> int:
                n = len(nums)
                
                def kadane(arr):
                    cum_sum = []
                    cur_sum = 0
                    for i in range(len(arr)):
                        cur_sum += arr[i]
                        cum_sum.append(cur_sum)
                    
                    best = arr[0]
                    prev = arr[0]
                    for i in range(1, len(arr)):
                        prev = max(prev+arr[i], arr[i])
                        best = max(best, prev)                
                    return best  
                
                
                max_sum = -float('inf')
                for i in range(n):
                    new_nums = nums[i:] + nums[:i]
                    temp_sum = kadane(new_nums)
                    max_sum = max(max_sum, temp_sum)
                return max_sum
        ```
        
    - 예제 2/5
        
        ```python
        class Solution:
            def maxSubarraySumCircular(self, nums: List[int]) -> int:
                n = len(nums)
                if n == 1:
                    return nums[0]
        
                # cum_sum list 
                cum_sum = [nums[0]]
                for i in range(1, n):
                    cum_sum.append(cum_sum[i-1] + nums[i])
        
                # define two differnt kadane function
                def max_kadane(arr):
                    current = 0
                    best = -float('inf')
                    for i in range(n):
                        # same value for the first element
                        current = max(cum_sum[i], nums[i])
                        best = max(best, current)
                    return best 
                
                def min_kadane(arr):
                    current = 0
                    best = float('inf')
                    for i in range(n):
                        current = min(cum_sum[i], nums[i])
                        best = min(best, current)
                    return best 
                
                # circular case 
                if max(nums) < 0:
                    # non-circular case
                    max_sum = max_kadane(nums)
                else:
                    max_sum = sum(nums) - min_kadane(nums)
                
                return max_sum
        ```
        
    
- Editorial (chat GPT)
    - circular array의 참된 의미
        - allows for more combinations of subarrays that are not possible in a standard linear array
        - [A, B, C] → [B, C, A], [C, A, B]
    - 기본 아이디어
        1. 일반적인 kadane 알고 써서 구하는 maximum subarray sum 
            - Linear case cover (non-circular scenario)
            - 근데 왜 필요하냐
                - 주어진 array가 음수로만 구성된 경우
                    - min sum은 모든 원소를 다 더하는 경우에 구해짐
                    - 그럼 total sum - min sum = 0
                    - 그러나 문제에서 non-empty subarray라고 명시해둠
                    - 예) [-1, -2, -3]의 경우 max sum subarray는 [-1]
                    
                    → 따라서 standard kadane도 필요 
                    
        2. 약간 변형한 kadane 알고리즘 써서 구하는 minimum subarray sum
            - Total sum - 최소 합 빼면 = 최대 합
            - circular scenario
            - 최소 합: sum of the smallest contiguous subarray
            - 예) [a, b, c, d, e]에서 [b, c]가 minimum sum subarray인 경우
                - Non-circular scenario에서는 [a, ###, d, e]가 남아 있는데, 얘네는 contiguous 하지 않으므로 답은 max(a, sum(d, e))
                - 그러나 circular scenario에서는 [d, e, a]도 contiguous 하다고 보기 때문에 얘네 셋이 max sum subarray가 된다
                - 그러니까 앞부분-최소합-뒷부분이 Linear 상태에서 존재할 때, circular로 보면 최소합-뒷부분-앞부분이 될 수 있으니까 결국 뒷부분, 앞부분이 max sum이 되는 것
        - 하나의 input array에 대해 1. 2. 접근법 둘 다 사용해야 circular / non-circular scenario를 모두 다루는 것
            - The key takeaway is that in a circular array problem, you need to consider both possibilities: the maximum sum that can be achieved without wrapping around (using standard Kadane's algorithm) and the maximum sum that can be achieved with wrapping around (using the **`total - min_sum`** approach). Comparing these two will give you the correct answer for the maximum subarray sum in a circular array.
        - cumsum은 필요 없다
            - 왜냐면 cumsum의 시작점은 무조건 0인데
            - max subarray는 중간에서 시작해서 중간에서 끝날 수도 있잖슴~
            - 그리고 애초에 kadane’s algo는 Max sum subarray에 대한 것이지 subsequence에 대한게 아니라서 맘 놓고 써도 됨~
- AC 코드
    - kadane이 subarray를 무조건 보장한다는 사실을 이해하는 데 오래 걸림
        - key point: current는 best subarray에 해당 원소가 들어가든 안 들어가든, 그 원소까지 포함한 누적합이 그 원소 단독 값보다 크면 무조건 그 원소를 포함시킨 누적합을 들고 간다.
    
    ```python
    class Solution:
        def maxSubarraySumCircular(self, nums: List[int]) -> int:
            n = len(nums)
            if n == 1:
                return nums[0]
    
            # define two differnt kadane function
            def max_kadane(arr):
                current = 0
                best = -float('inf')
                for i in range(0, n):
                    # same value for the first element
                    current = max(current+nums[i], nums[i])
                    best = max(best, current)
                return best 
            
            def min_kadane(arr):
                current = 0
                best = float('inf')
                for i in range(n):
                    current = min(current+nums[i], nums[i])
                    best = min(best, current)
                return best 
            
            linear_max_sum = max_kadane(nums)
            circular_max_sum = sum(nums) - min_kadane(nums)
            
            if max(nums) >= 0:
                return max(linear_max_sum, circular_max_sum)
            else:
                return linear_max_sum
    ```