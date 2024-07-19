# 740. Delete and Earn

Status: done, in progress, 👀1
Theme: DP
Created time: November 12, 2023 4:48 PM
Last edited time: February 28, 2024 12:11 PM

<aside>
⭐ 복습 포인트
- dp table은 숫자 0부터 주어진 array에서 가장 큰 값까지 모두 고려한다-중간 값들이 array에 나오던 말던
- 점화식에서 현재 값을 누적하는 대상은 이전 상태가 아니라 전전 상태 즉 i-2번째 값임

</aside>

- 코드
    
    ```python
    class Solution:
        def deleteAndEarn(self, nums: List[int]) -> int:
            if len(nums) == 0: return nums[0]
    
            freq = [0] * (max(nums) + 1) # idx: 0~max(nums)
    
            for n in nums:
                freq[n] += n
            
            dp = [0] * len(freq)
    				# dp[i]: nums에서 i번째 index가 아니라 literally 값 i에 관한 정보 
    				# 그래서 base case에서 dp[0]=0이고 dp[1]=freq[1]
            dp[1] = freq[1]
    
            for i in range(2, len(freq)):
                dp[i] = max(freq[i] + dp[i-2], dp[i-1])
    
            return dp[len(freq)-1]
    ```
    
- [[**198. House Robber**](https://leetcode.com/problems/house-robber/solutions/846002/python-dynamic-programming-easy-solution-faster-than-95/?envType=study-plan-v2&envId=dynamic-programming)](198%20House%20Robber%20d44dfd89aff84bde8814b45e00a22820.md) 랑 비슷한 문제로 귀결됨
    - 1) 직전 상태 유지 vs. 2) 전전 상태 + 현재 줄 수 있는 변화 중 max 선택
- 선택의 결과로 못 얻는 점수에 집중하지 말고, 선택의 결과로 얻게 되는 점수에 집중
    
    2-1) 이번 숫자를 선택함으로써 얻을 수 있는 점수는 이번 숫자 + 전전 숫자를 선택해서 얻은 점수 
    
    - 자연히 이번 직전 숫자는 선택하지 못하게 되므로 얻을 수 있는 점수에서 제외됨
    - 문제로 따지면 이번 숫자를 선택한 뒤, 다음 숫자를 제거 하는 것과 동일
    - 왜냐면 이번 숫자를 선택했을 때 다음으로 올 숫자는 다다음 숫자일 수 밖에 없기 때문에
    
    2-2) 이번 다음 숫자를 선택함으로써 얻을 수 있는 점수 = 이번 다음 숫자 + 이번 전 숫자 
    
    - 이번 직전 숫자로 얻을 수 있는 점수는 이번 다음 숫자를 선택하면서 고려됨
- kick: 사전 생성 (freq)
    - 각 숫자를 통해 얻을 수 있는 점수를 기록(value: 횟수가 아닌 점수 그 자체)
    - 쓰임새: 점화식에서 해당 숫자를 선택하는 경우 얻을 수 있는 점수를 바로 retrieval
- 4 steps
    - state
        - dp[n] : 숫자 n까지 봤을 때 얻을 수 있는 최대 점수
            - n이 nums에 있는 숫자가 아니더라도 값이 생김. 왜냐면 그 중간값이 있어야 최종 구하려는 값을 구할 수 있기 때문
    - transition
        - 점화식을 만들려면 0부터 nums의 최대값까지 모든 숫자 사이의 관계가 나와야 함
            - nums 원소 숫자가 아니라는 점, nums index와도 관련 없다는 점
        - i : 2 → max(nums)+1
            - dp[i] = max(dp[i-2] + freq[i], dp[i-1])
    - base case
        - dp[0] = 0, dp[1] = freq[1]
    - end
        - return dp[-1] = dp[max(nums)] # 0부터 시작해서 max(nums)까지 (length는 max(nums)+1)
- 예: [1, 2, 2, 4, 5]
    - freq = {1:1, 2:4, 4:4, 5:5}
        - value가 횟수가 아니라는 점~!
        - [x]  사전에 없는 원소는 0이 되게끔 초기에 설정해주는 게 좋을 듯?
            
            → 더 좋은 방식은 [0] * (max(nums)+1) 해서 0부터 max(nums)를 index로 삼는 array 생성 
            
    - dp = [0] * 6
    - dp[1] = freq[1] = 1
    - dp[2] = max(dp[0]+freq[2], dp[1])  = max(0+4, 1) = 4
    - dp[3] = max(dp[1]+freq[3], dp[2]) = max(1+0, 4) = 4
    - dp[4] = max(dp[2]+freq[4], dp[3]) = max(4+4, 4) = 8
    - dp[5] = max(dp[3] + freq[5], dp[4]) = max(4+5, 8) = 9
    - 답은 9
        - 5 터뜨리면 4 out → [1, 2, 2], score = 5
        - 2 터뜨리면 1 out → [2], score = 5 + 2 = 7
        - 2 터뜨리면 → [], score = 5 + 2 + 2 = 9