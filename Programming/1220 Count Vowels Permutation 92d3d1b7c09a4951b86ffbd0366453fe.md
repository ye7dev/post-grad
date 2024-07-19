# 1220. Count Vowels Permutation

Status: done, in progress
Theme: DP
Created time: January 15, 2024 4:06 PM
Last edited time: January 15, 2024 4:42 PM

- Progress
    - invert dict function
        
        ```python
        def invert_dict(precedence_dict):
            successor_dict = {}
            for precedence, successors in precedence_dict.items():
                for successor in successors:
                    if successor not in successor_dict:
                        successor_dict[successor] = []
                    successor_dict[successor].append(precedence)
            return successor_dict
        ```
        
- AC 코드
    - by myself Bottom-up
        - 굳이 사전을 안만들고 그냥 바로 index로 선후 관계 만들면 더 빨리 할 수 있는 듯
        
        ```python
        class Solution:
            def countVowelPermutation(self, n: int) -> int:
                mod = 10 ** 9 + 7
                vowel_list = ['a', 'e', 'i', 'o', 'u']
                vowel_dict = {}
                # first, second
                vowel_dict['a'] = ['e']
                vowel_dict['e'] = ['a', 'i']
                vowel_dict['i'] = ['a', 'e', 'o', 'u']
                vowel_dict['o'] = ['i', 'u']
                vowel_dict['u'] = ['a']
        
                # invert dict 
                order_dict = {}
                for first, second_list in vowel_dict.items():
                    for second in second_list:
                        second_idx = vowel_list.index(second)
                        first_idx = vowel_list.index(first)
                        if second_idx not in order_dict:
                            order_dict[second_idx] = []
                        order_dict[second_idx].append(first_idx)
                
                # array
                dp = [[0] * 5 for _ in range(n)]
                # base case
                for j in range(5):
                    dp[0][j] = 1 
        
                for i in range(1, n):
                    for j in range(5):
                        for first_idx in order_dict[j]:
                            dp[i][j] += dp[i-1][first_idx]
        
                return sum(dp[-1]) % mod
        ```