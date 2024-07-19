# 213. House Robber II

Created time: May 21, 2024 5:29 PM
Last edited time: May 21, 2024 5:36 PM

[[**1388. Pizza With 3n Slices**](https://leetcode.com/problems/pizza-with-3n-slices/description/?envType=problem-list-v2&envId=50vif4uc)](1388%20Pizza%20With%203n%20Slices%20b12943b3ac6c40a3a2dbdc5b88e9b5db.md) 문제에서 circular case 어떻게 푸는지 알게 되어서 금방 풀었다

다만 base case 주의. 원소가 1개인 경우는 가장 앞 원소 빼거나 뒷 원소 빼면 남는 원소가 없기 때문. 바로 return nums[0]으로 처리해줘야 함 

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        # circular -> no [-1, 0]
        def get_max(arr):
            n = len(arr)
            dp = [0] * (n+1)
            # base case
            dp[1] = arr[0]
            # iterative
            for i in range(2, n+1):
                dp[i] = max(dp[i-1], dp[i-2]+ arr[i-1])
            return dp[-1]
        return max(get_max(nums[:-1]), get_max(nums[1:]))

        
```