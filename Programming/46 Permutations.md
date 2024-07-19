# 46. Permutations

Status: done, in progress
Theme: recursive
Created time: December 7, 2023 5:00 PM
Last edited time: December 7, 2023 5:10 PM

- 코드
    
    느리지만 한번에 풀었다 🪇→ return 하나로 빨라짐 
    
    ```python
    class Solution:
        def permute(self, nums: List[int]) -> List[List[int]]:
            N = len(nums)
            ans = []
            def populate(temp):
                if len(temp) == N:
                    ans.append(temp[:])
    								return 
                for n in nums:
                  if n in temp:
                    continue
                  temp.append(n)
                  populate(temp)
                  temp.pop()
            populate([])
            return ans
    ```