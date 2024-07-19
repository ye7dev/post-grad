# 1048. Longest String Chain

Status: done, in progress
Theme: DP
Created time: February 2, 2024 5:23 PM
Last edited time: February 2, 2024 9:55 PM

- Progress
    - 문제 이해
        - array `words` : 각 원소는 소문자 단어
        - word_a는 word_b의 전임자
            - word_a의 순서 유지하면서 letter 하나를 아무 자리에 끼워넣었을 때 word_b가 되면
            - 예) abc → abac OK / cba에는 d를 맨 뒤에 넣어도 원래 cba의 순서를 바꾸지 않고는 bcad가 될 ㅜㅅ 없다
        - word chain
            - sequence of words. 순서상 앞에 온 단어가 다음 단어의 전임자가 되는 관계가 처음부터 끝가지 지속
        - 주어진 words list에서 단어를 뽑아서 word chain을 만들 때, 가장 길게 만들 수 있는 길이를 return 해라
- Trial
    - Bottom-up → 37/86
        - 마지막 값이 아니라 max 값을 데리고 와야 했음
        
        ```python
        class Solution:
            def longestStrChain(self, words: List[str]) -> int:
                n = len(words)
                words.sort(key=lambda x: len(x))
                dp = [1] * n
        
                for i in range(n):
                    cur_word = words[i]
                    for j in range(len(cur_word)):
                        new_word = cur_word[:j] + cur_word[j+1:]
                        for k in range(i-1, -1, -1):
                            if words[k] == new_word:
                                dp[i] = max(dp[i], 1 + dp[k])
                            if len(words[k]) < len(new_word):
                                break
                            
                return dp[-1]
        ```
        
- AC 코드
    - Top-down (🐌🪇)
        
        ```python
        class Solution:
            def longestStrChain(self, words: List[str]) -> int:
                n = len(words)
                words.sort(key=lambda x: len(x))
                memo = {}
        
                def recur(start):
                    # check memo
                    if start in memo:
                        return memo[start]
                    # base case
                    if start == 0:
                        return 1
                    # recurrence relation
                    cur_word = words[start]
        
                    temp_ans = 1
                    for i in range(len(cur_word)): # remove a letter
                        new_word = cur_word[:i] + cur_word[i+1:]
                        for j in range(start, -1, -1):
                            if words[j] == new_word:
                                temp_ans = max(temp_ans, 1 + recur(j))
                            if len(words[j]) < len(new_word):
                                break 
                    memo[start] = temp_ans
                    return memo[start]
        
                max_len = 1
                for i in range(1, n):
                    ans = recur(i)
                    max_len = max(ans, max_len)
                return max_len
        ```
        
    - editorial top-down (🐢)
        - 단어 자체로 해서 정렬도 필요 없고 인덱스도 필요 없다
        
        ```python
        class Solution:
            def longestStrChain(self, words: List[str]) -> int:
                n = len(words)
                #words.sort(key=lambda x: len(x))
                memo = {}
        
                def recur(cur_word):
                    # check memo
                    if cur_word in memo:
                        return memo[cur_word]
                    
                    # no base case?
                    # recurrence relation
                    ans = 1 
                    for i in range(len(cur_word)): # remove a letter
                        new_word = cur_word[:i] + cur_word[i+1:]
                        if new_word in words:
                            ans = max(ans, 1 + recur(new_word))
        
                    memo[cur_word] = ans
                    return memo[cur_word]
        
                max_len = 1
                for w in words:
                    ans = recur(w)
                    max_len = max(ans, max_len)
                return max_len
        ```
        
    - bottom-up (🐌)
        
        ```python
        class Solution:
            def longestStrChain(self, words: List[str]) -> int:
                n = len(words)
                words.sort(key=lambda x: len(x))
                dp = [1] * n
        
                for i in range(n):
                    cur_word = words[i]
                    for j in range(len(cur_word)):
                        new_word = cur_word[:j] + cur_word[j+1:]
                        for k in range(i-1, -1, -1):
                            if words[k] == new_word:
                                dp[i] = max(dp[i], 1 + dp[k])
                            if len(words[k]) < len(new_word):
                                break
                            
                return max(dp)
        ```
        
    - editorial bottom-up (⚡️)
        - char 하나 빼서 새로 만든 단어가 list 안에 있는지 확인하기 위해서는 index가 아니라 사전을 쓰는게 더 빠름
        
        ```python
        class Solution:
            def longestStrChain(self, words: List[str]) -> int:
                n = len(words)
                words.sort(key=lambda x: len(x))
        
                dp = {}
                for i in range(n):
                    cur_word = words[i]
                    dp[cur_word] = 1 
                    for j in range(len(cur_word)):
                        new_word = cur_word[:j] + cur_word[j+1:]
                        if new_word in dp:
                            dp[cur_word] = max(dp[cur_word], 1 + dp[new_word])
                            
                return max(dp.values())
        ```