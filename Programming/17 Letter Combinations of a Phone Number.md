# 17. Letter Combinations of a Phone Number

Status: done, in progress
Theme: recursive
Created time: December 7, 2023 5:10 PM
Last edited time: December 7, 2023 5:41 PM

- 잘 풀었다 🪇
    
    ```python
    class Solution:
        def letterCombinations(self, digits: str) -> List[str]:
          ans = []
          N = len(digits)
          if N == 0: return ans
    
          char_dict= {i:[] for i in range(2, 10)}
          start_unicode = 97
          for num in range(2, 7):
            num_unicode = 97 + 3 * (num-2)
            for i in range(3):
              char_dict[num].append(chr(num_unicode+i))
    
          char_dict[7] = ['p', 'q', 'r', 's']
          char_dict[8] = ['t', 'u', 'v']
          char_dict[9] = ['w', 'x', 'y', 'z']
    
          def recur(temp, idx):
            if len(temp) == N:
              ans.append("".join(temp[:]))
              return
    
            cur_num = int(digits[idx])
            for char in char_dict[cur_num]:
                temp.append(char)
                recur(temp, idx+1)
                temp.pop()
          
          recur([], 0)
          return ans
    ```