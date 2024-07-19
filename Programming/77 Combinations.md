# 77. Combinations

Status: done, in progress, incomplete
Theme: backtracking
Created time: November 27, 2023 2:56 PM
Last edited time: December 5, 2023 5:42 PM

[[**2930. Number of Strings Which Can Be Rearranged to Contain Substring**](https://leetcode.com/problems/number-of-strings-which-can-be-rearranged-to-contain-substring/description/)](2930%20Number%20of%20Strings%20Which%20Can%20Be%20Rearranged%20to%20%20a744f35e8c4b4a408407e3abea0031bf.md) 엮은 문제로 풀러옴 

- [x]  모범답안 코드로 다시 한번 풀어보기
- [x]  need, remain, available, [first_num, first_num + available+1] range 그림으로 표현하고 여기 올려두기→backtracking 공부했더니 필요 없다
- 코드
    
    ```python
    class Solution:
        def combine(self, n: int, k: int) -> List[List[int]]:
            combis = [] 
            def make_combi(temp_arr, last_idx):
                if len(temp_arr) == k:
                    combis.append(temp_arr)
                else:
                    cnt = 1 
                    for i in range(last_idx, n+1):
                        make_combi(temp_arr + [i], last_idx+cnt)
                        cnt += 1 
            make_combi([], 1)
            return combis
    ```
    
- backtracking 개념 공부
    - 기본
        - low bound를 주면서 all of something을 찾으라고 하면 대부분 backtracking으로 풀미
        - 한 번에 하나의 element를 가지고 solution 생성
        - `curr` current something(이 문제에서는 combination) we are building
        - 첫번째 element로 1을 더하고, locking → find all of something that starts with [1] → 두번째 element로 2를 더하고, locking → find all of something that starts with [1, 2] … → length k에 도달할 때까지 반복
        - [1, 2]로 시작하는 모든 조합을 찾은 뒤에는, backtrack by removing 2 and now we have curr = [1] again …
        - [1]로 시작하는 모든 조합을 찾은 뒤에는, backtrack by removing 1 and now we have curr = [2] for the first time
    - modeling it as a tree
        - root: []
        - traversing → root에서 curr까지 가는 모든 path가 curr에 담긴다
        - depth k의 node에서의 curr이 우리가 찾는 답
        - each call=a node in the tree
            - current node의 value보다 큰 값에 대해 iterate
        - parent → child 갈 때는 curr에 원소 하나 추가 ↔ child → parent 다시 올라갈 때는 curr에서 원소 하나 제거
    - 코드
        
        ```python
        def combine(n, k):
            ans = []
            def backtrack(curr, first_num):
                if len(curr) == k:
                    ans.append(curr[:])
                    return 
        
                need = k - len(curr)  # curr에 더 채워야 하는 숫자
                remain = n - first_num + 1  # 아직 안 살펴본 숫자 개수
                available = remain - need
        
                for num in range(first_num, first_num + available +1):
                    curr.append(num)
                    backtrack(curr, num+1)
                    curr.pop() 
        
            combine([], 1)
            return ans
        ```
        
        n = 4, k = 2 
        
        | curr | first_num | need | remain | available | range |
        | --- | --- | --- | --- | --- | --- |
        | [] | 1 | 2 | 4 | 4-2=2 | [1, 4] ⇒ 1, 2, 3 |
        | [1] | 2 | 1 | 4-2+1=3 | 3-1=2 | [2, 5] ⇒ 2, 3, 4 |
    - backtracking 공부해서 스스로 답변도 잘 만들어냄-시간은 좀 느리지만 잘했당 🪇
        
        ```python
        class Solution:
            def combine(self, n: int, k: int) -> List[List[int]]:
                ans = []
                def backtrack_combi(temp_arr, last_num):
                    # base case 
                    if len(temp_arr) == k:
                        ans.append(temp_arr[:])
                        return 
                    # candidate iteration 
                    for num in range(last_num+1, n+1):
                        # validity check
                        if len(temp_arr) < k:
                            if num not in temp_arr:
                                temp_arr.append(num) # place
                                backtrack_combi(temp_arr, num) # go forward
                                # solution 여부는 체크할 필요 없음. 뭘 return 할 값이 없고 그냥 list에 추가만 하면 되는 것이어서 
                                temp_arr.pop() # remove 
                            # else 필요 없을 듯 그냥 다음 후보로 넘어가면 될 듯 
                
                backtrack_combi([], 0)
                return ans
        ```