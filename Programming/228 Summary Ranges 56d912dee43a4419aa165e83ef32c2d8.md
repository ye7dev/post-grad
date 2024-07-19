# 228. Summary Ranges

Status: done
Theme: array
Created time: November 16, 2023 5:45 PM
Last edited time: November 16, 2023 5:53 PM

- 머리 식히기 3
- 마지막 원소에서 arr 값이 update 된 다음 범위에 추가되지는 않는 상태로 for loop이 끝나기 때문에, 범위에 추가해주는 작업을 추가로 마지막에 for loop 밖에서 한번 더 해줘야 함
- 코드
    
    ```python
    class Solution:
        def summaryRanges(self, nums: List[int]) -> List[str]:
            if len(nums) == 0: return []
            if len(nums) == 1: return [str(nums[0])]
            
            range = []
            dep = nums[0]
            arr = nums[0]
            for n in nums[1:]:
                if n == arr + 1:
                    arr = n 
                else:
                    if dep == arr:
                        range.append(str(dep))
                    else:
                        range.append(f'{dep}->{arr}')
                    dep = n
                    arr = n 
    
            if dep == arr:
                range.append(str(dep))
            else:
                range.append(f'{dep}->{arr}')
    
            return range
    ```