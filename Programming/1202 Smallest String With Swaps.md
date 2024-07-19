# 1202. Smallest String With Swaps

Status: done, in progress, with help
Theme: graph
Created time: December 13, 2023 1:18 PM
Last edited time: December 13, 2023 5:09 PM

- 과정
    
    유니코드가 더 작은 알파벳이 더 앞에 오게끔 해야 함. root에는 비교해서 더 앞으로 간 글자의 index가 담기게 되는듯? 
    
    몇 번이고 swap 할 수 있다고 해도 일단 a, b 중에 앞에 있는 char이 더 lexicographically small value를 가졌으면 더 이상 바꿀 필요 없음 
    
    - 약간 수정해본 코드
        
        ```python
        class UnionFind:
            def __init__(self, input_str):
                self.rank = [ord(s) for s in input_str]
                self.root = [s for s in input_str]
            def find(self, x):
                if x != self.root[x]:
                    self.root[x] = self.find(self.root[x])
                return self.root[x]
            def union(self, x, y):
                # root_x, root_y = self.find(x), self.find(y)
                # if root_x != root_y:
                # 앞에 letter가 더 뒤에 나오는 알파벳
                # if self.rank[root_x] > self.rank[root_y]: 
                #     self.root[root_x], self.root[root_y] = root_y, root_x
                if self.rank[x] > self.rank[y]: 
                    self.root[x], self.root[y] = self.root[y], self.root[x]
                # elif self.rank[root_x] < self.rank[root_y]:
                #     self.root[root_y] = root_x
                # else: # same level
                #     self.root[root_y] = root_x
                #     self.rank[root_x] += 1
            def connected(self, x, y):
                return self.find(x) == self.find(y) 
        
        class Solution:
            def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
                uf = UnionFind(s)
                for a, b in pairs:
                    uf.union(a, b)
                    print(uf.root)
                return "". join(uf.root)
        ```
        
    - Editorial 보고 다시 짠 코드
        
        ```python
        class UnionFind:
            def __init__(self, size):
                self.root = [i for i in range(size)]
                self.rank = [1] * size
            def find(self, x):
                if self.root[x] != x:
                    self.root[x] = self.find(self.root[x])
                return self.root[x]
            def union(self, x, y):
                root_x, root_y = self.find(x), self.find(y)
                if root_x != root_y:
                    if self.rank[root_x] > self.rank[root_y]:
                        self.root[root_y] = root_x
                    elif self.rank[root_x] < self.rank[root_x]:
                        self.root[root_x] = root_y
                    else: # same level
                        self.root[root_y] = root_x
                        self.rank[root_x] += 1 
        
        class Solution:
            def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
                idx_dict = {i:s[i] for i in range(len(s))}
                UF = UnionFind(len(s))
                for a, b in pairs:
                    UF.union(a, b)
                # group by root
                group_dict = {}
                for i in range(len(s)):
                    cur_root = UF.root[i]
                    if cur_root not in group_dict:
                        group_dict[cur_root] = [i]
                    else:
                        group_dict[cur_root].append(i)
                # sort each group
                sub_strs = []
                for r in group_dict:
                    sub_str = []
                    for idx in group_dict[r]:
                        sub_str.append(idx_dict[idx])
                    sub_str.sort()
                    sub_strs.append("".join(sub_str))
                # assemble the sorted substring
                sub_strs.sort()
                return "".join(sub_strs)
        ```
        
- Editorial
    - Overview
        - 잘 이해는 안가지만 `(a, b)` and `(b, c)` 같은 pair가 있으면 `(a, c)` 간의 swap도 가능한 것이라고 함
            1. If you can swap characters at positions a and b, and also b and c, you can indirectly swap characters at a and c.
            2. To swap a and c, first swap a with b, then swap the new character at b with c.
            3. This method allows rearranging characters a, b, and c in any order, despite not having a direct a-c swap pair.
        - 그래프 문제로 가져오기
            - 각 index를 vertex로, pair를 edge로 생각
            - pair가 있다 = edge가 있다 =swap 할 수 있다
            - 한 pair에 속한 두 vertices가 같은 path 위에 존재하면, 그들 사이의 path 위에 존하는 다른 vertices들과 반복적으로 교환될 수 있다 (??)
            - 그림 요약: same connected component 안에서는 어떤 vertices 쌍도 swap 가능 = connected component에 속한 어떤 알파벳 끼리도 재정렬 가능
                - pair 쌍 중에 (0, 7)이 없어도 0과 7에 위치한 알파벳을 swap 가능
                
                ![Untitled](Untitled%20144.png)
                
                [https://www.notion.so](https://www.notion.so)
                
                ↳ pair - (7, 2) 
                
                ![Untitled](Untitled%20145.png)
                
                ↳ pair - (2, 3) : 원래 2의 자리에 3이 있고, 3의 자리에 7이 있음 
                
                ![Untitled](Untitled%20146.png)
                
                ↳ pair - (0, 3) : 원래 3의 자리에 7이 있음 
                
                ![Untitled](Untitled%20147.png)
                
        - To find the lexicographically smallest string
            - 각 index에 대응하는 알파벳을 오름차순으로 정렬
            
            → ith 알파벳을 ith 자리에 놓는다 (??)
            
        - solution은 크게 네 단계
            1. 주어진 pair 가지고 그래프 생성 
            2. connected components 찾기
            3. 각 connected components에서 알파벳 오름차순으로 정렬
            4. smallest string 빌드 
        - 가장 큰 난제
            - infinite swap 가능한 상황에서 connected component에 속한 모든 알파벳을 정렬된 순서로 배치
            
            → 어떤 index들이 같은 connected component에 속할 수 있는지? 
            
    - 코드 짜면서 발견한 차이
        - union-find로 connected component 끼리 그룹 짓고, 거기서 정렬한 것까지는 동일
        - 그러나 마지막에, 나는 각각 정렬된 상태의 subgroup을 그대로 concatenate 한 반면,
        - editorial 코드에서는 `The final string, with characters sorted within their groups but in original positions` 이라고 함. 무슨 말이지?
            - 상세 설명
                
                **Place Back in Original Positions**:
                
                - Now, we place the sorted characters back into their original positions in the string **`s`**.
                - The character 'b' (sorted from the first group) goes to index **`0`** (original position of 'd').
                - The character 'a' (sorted from the second group) goes to index **`1`** (original position of 'c').
                - The character 'c' goes to index **`2`**, and 'd' goes to index **`3`**
        
        ⇒ {d,b} 그룹이 {b,d}로 정렬된다고 해서, 바로 최종 string에 bd로 붙는 게 아니고, 원래 d 자리에 b를, b 자리에 d를 넣어준다는 뜻 
        
        smallest_string = list(s)
        for indices in root_to_component.values():
        characters = sorted(smallest_string[i] for i in indices)
        for i, char in zip(indices, characters):
        smallest_string[i] = char
        
        ```
            return ''.join(smallest_string)
        
        ```
        
    - 그룹별 정렬 후 마지막 최종 string 만들기
        - 그룹별 정렬하면 얻게 되는 결과물: 정렬된 substring & 각 char의 원래 자리 index
        
        ```python
        
                # sort each group
                arranged = [''] * len(s)
                for r in group_dict:
                    sub_str = []
                    for idx in group_dict[r]:
                        sub_str.append(s[idx])
                    sub_str.sort() # what we have : sorted substring
                    for idx, char in zip(group_dict[r], sub_str):
                        arranged[idx] = char
                return "".join(arranged)
        ```
        
- AC 코드
    
    ```python
    class UnionFind:
        def __init__(self, size):
            self.root = [i for i in range(size)]
            self.rank = [1] * size
        def find(self, x):
            if self.root[x] != x:
                self.root[x] = self.find(self.root[x])
            return self.root[x]
        def union(self, x, y):
            root_x, root_y = self.find(x), self.find(y)
            if root_x != root_y:
                if self.rank[root_x] > self.rank[root_y]:
                    self.root[root_y] = root_x
                elif self.rank[root_x] < self.rank[root_x]:
                    self.root[root_x] = root_y
                else: # same level
                    self.root[root_y] = root_x
                    self.rank[root_x] += 1 
    
    class Solution:
        def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
            char_dict = {i:s[i] for i in range(len(s))}
            idx_dict = {s[i]:i for i in range(len(s))}
            UF = UnionFind(len(s))
            for a, b in pairs:
                UF.union(a, b)
            # group by root
            group_dict = {}
            for i in range(len(s)):
                cur_root = UF.find(i) # not root[i]
                if cur_root not in group_dict:
                    group_dict[cur_root] = [i]
                else:
                    group_dict[cur_root].append(i)
            # sort each group
            arranged = [''] * len(s)
            for r in group_dict:
                sub_str = []
                for idx in group_dict[r]:
                    sub_str.append(char_dict[idx])
                sub_str.sort()
                for i in range(len(sub_str)):
                    arranged[group_dict[r][i]] = sub_str[i]
            return "".join(arranged)
    ```