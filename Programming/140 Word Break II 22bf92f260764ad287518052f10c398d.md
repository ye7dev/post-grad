# 140. Word Break II

Status: done, in progress
Theme: DP
Created time: March 11, 2024 11:16 AM
Last edited time: March 11, 2024 11:50 AM

- Trial
    - Top-down → 24/27
        
        ```python
        from collections import defaultdict
        class Solution:
            def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
                ans = []
                memo = defaultdict(list)
                n = len(s)
                min_len = min([len(x) for x in wordDict])
                def recur(start):
                    # return 
                    if start in memo:
                        return memo[start]
                    # base case 
                    if s[start:n] in wordDict:
                        return [s[start:n]]
                    if n-start < min_len:
                        return 
                    # recursive case
                    for end in range(start, n):
                        if s[start:end+1] in wordDict:
                            temp = recur(end+1)
                            if temp is not None:
                                for sent in temp:
                                    new_sent = s[start:end+1] + " " + sent
                                    memo[start].append(new_sent)
                    return memo[start]
        
                return recur(0)
        ```
        
- AC 코드
    - Top-down(🪇🐢)
        
        ```python
        from collections import defaultdict
        class Solution:
            def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
                ans = []
                memo = defaultdict(list)
                n = len(s)
                min_len = min([len(x) for x in wordDict])
                def recur(start):
                    # return 
                    if start in memo:
                        return memo[start]
                    # base case 
                    if start == n:
                        return [""]
                    if n-start < min_len:
                        return 
                    # recursive case
                    for end in range(start, n):
                        if s[start:end+1] in wordDict:
                            temp = recur(end+1)
                            if temp is not None:
                                for sent in temp:
                                    new_sent = s[start:end+1] + " " + sent
                                    memo[start].append(new_sent)
                    return memo[start]
                sents = recur(0)
                return [sent[:-1] for sent in sents]
        ```
        
    - DFS(⚡️)
        - path를 list로 관리하고, 마지막에 “ “.join으로 최종 답에 넣어주는 게 포인트
        
        ```python
        from collections import defaultdict
        class Solution:
            def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
                ans = []
                n = len(s)
                def dfs(start, path):
                    # base case
                    if start == n:
                        ans.append(" ".join(path))
                    # recursive case
                    for end in range(start+1, n+1):
                        if s[start:end] in wordDict:
                            dfs(end, path + [s[start:end]])          
        
                dfs(0, [])
                return ans
        ```