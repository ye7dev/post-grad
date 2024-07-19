# 354. Russian Doll Envelopes

Status: done, in progress
Theme: DP, Longest Increasing Subsequence
Created time: January 19, 2024 11:46 AM
Last edited time: January 19, 2024 4:53 PM

- Process
    - array 원소 순서가 유지되어야 하는가 → 아니다
        
        ```
        Input: envelopes = [[5,4],[6,4],[6,7],[2,3]]
        Output: 3
        Explanation: The maximum number of envelopes you can Russian doll is3 ([2,3] => [5,4] => [6,7]).
        ```
        
    - default는 1인듯
        
        ```
        Input: envelopes = [[1,1],[1,1],[1,1]]
        Output: 1
        ```
        
    - 왠지 pair length랑 비슷한 듯 [[**646. Maximum Length of Pair Chain**](https://leetcode.com/problems/maximum-length-of-pair-chain/description/?envType=study-plan-v2&envId=dynamic-programming)](646%20Maximum%20Length%20of%20Pair%20Chain%2015e5932c32624cbd8be56ca5c2bc50fd.md)
    - 정렬 없이 구할 수 있는 방법은 뭐가 있을까
        - 정렬을 빼도 TLE가 나온다
        - `1 <= envelopes.length <= 10**5`
    - 원소가 두 개일 때 bisect_left의 동작
        
        ```python
        from bisect import bisect_left
        
        data = [(1, 'apple'), (3, 'banana'), (4, 'cherry'), (6, 'date')]
        new_element = (6, 'zebra')
        position = bisect_left(data, new_element)
        
        ```
        
        - position은 3. 저 자리에 zebra가 대체하게 된다.
    - 원소의 하위 원소가 2개씩 있고, 두 원소의 첫번째 하위원소들의 값이 같은 경우, array.sort()의 동작 → The comparison is made based on these second values.
    - 근데 그럼 width만 더 크고, height가 더 작은 원소도 subsequence 뒤에 올 수 있는거 아닌가? → 맞다
        
        ```python
        >>> x = [(1, 3)]
        >>> bisect_left(x, (2, 4))
        1
        >>> bisect_left(x, (2, 1))
        1
        >>>
        ```
        
- Trial
    - 정렬 후 pair comparison → 예제는 통과하지만 TLE
        - [[**646. Maximum Length of Pair Chain**](https://leetcode.com/problems/maximum-length-of-pair-chain/description/?envType=study-plan-v2&envId=dynamic-programming)](646%20Maximum%20Length%20of%20Pair%20Chain%2015e5932c32624cbd8be56ca5c2bc50fd.md) 와 유사한 풀이
        
        ```python
        class Solution:
            def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
                n = len(envelopes)
                # array
                dp = [1] * n
                envelopes.sort() # sort by width 
        
                for i in range(n):
                    for j in range(i):
                        a, b = envelopes[j]
                        c, d = envelopes[i]
                        if a < c and b < d:
                            dp[i] = max(dp[i], dp[j]+1)
        
                return max(dp)
        ```
        
    - bisect 모듈 도입 → 30/87
        
        ```python
        from bisect import bisect_left
        class Solution:
            def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
                n = len(envelopes)
                # array
                subseq = []
                envelopes.sort() # sort by width. for same width sort by height
        
                for env in envelopes:
                    i = bisect_left(subseq, env) # check width
                    
                    if i == len(subseq):
                        if not subseq or subseq[-1][1] < env[1]: # check height
                            subseq.append(env)
                    else:
                        # same width will always replaced with the latter element
                        if subseq[i-1][1] < env[1]: # check height
                            subseq[i] = env
                        
        
                return len(subseq)
        ```
        
    - w increasing, h decreasing 정렬 도입 → 14/87
        
        ```python
        from bisect import bisect_left
        class Solution:
            def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
                n = len(envelopes)
                # array
                subseq = []
                # increasing sort for w, decreasing sort for h
                envelopes.sort(key=lambda x: (x[0], -x[1])) 
        
                for env in envelopes:
                    i = bisect_left(subseq, env) # check width
                    
                    if i == len(subseq):
                        # increasing w, largest h among same w 
                        subseq.append(env)
        
                    else:
                        # same width will always replaced with the latter element
                        # latter element always has smaller height
                        ## this lead to higher possibility of longer subsequence?
                        subseq[i] = env
                        
        
                return len(subseq)
        ```
        
- [x]  [LIS 문제 O(NlogN)으로 bisect 모듈 이용해서 풀기](https://leetcode.com/problems/longest-increasing-subsequence/editorial/)
- AC 코드 (⚡️)
    
    ```python
    from bisect import bisect_left
    class Solution:
        def maxEnvelopes(self, envelopes: List[List[int]]) -> int:
            n = len(envelopes)
            # array
            subseq = []
            # increasing sort for w, decreasing sort for h
            envelopes.sort(key=lambda x: (x[0], -x[1])) 
    
            for w, h in envelopes:
                i = bisect_left(subseq, h) # check width
                
                if i == len(subseq):
                    # increasing w, largest h among same w 
                    subseq.append(h)
    
                else:
                    # same width will always replaced with the latter element
                    # latter element always has smaller height
                    ## this lead to higher possibility of longer subsequence
                    subseq[i] = h
                    
    
            return len(subseq)
    ```
    
- Editorial
    - **Approach 1: Sort + Longest Increasing Subsequence**
        - Algorithm
            - sort on width → find the length of the LIS on height
                - edge case - same width different height
                    - 예) `[[1, 3], [1, 4], [1, 5], [2, 3]]`
                        - sort by w → extract h 하면 [3, 4, 5, 3] → russian doll 3개 가능?
                            - No. 앞에 3, 4, 5의 w가 모두 동일하고, [1, 3]-[2, 3]은 서로 h가 같기 때문에 russion doll 불가능
                            - 결국 가능한 최대 russian doll 개수는 1개
            
            ⇒ w에 대해서 increasing sort만 할 뿐만 아니라, h에 대해 decreasing sort 
            
            - 이렇게 하면 w가 같은 두 개의 봉투는 절대 increasing subsequence에 있을 수 없음
            - 위의 예시를 다시 정렬하면 [[1, 5], [1, 4], [1, 3], [2, 3]]
                - w가 같은 세 개의 봉투는 [5, 4, 3] 순이라 불가하고
                - [1, 3], [2, 3]도 height가 같아서 불가
            - 마지막에 LIS는 두번째 차원-h-에 대해서만 한다
                - LIS 알고리즘은 1차원 sequence를 해결하기 위해 만들어짐
                - 예를 들어 (6, 2)는 우리 문제의 제약에 따르면 subsequence에 포함되어서는 안됨 → 근데 bisect_left method에 tuple을 통째로 넣으면 subsequence를 연장하게 됨
                    
                    ```python
                    >>> x = [(3, 4)]
                    >>> bisect_left(x, (6, 2))
                    1
                    ```
                    
                - 이 경우 h만 가지고 bisect_left method를 돌리면 4보다 2가 더 작기 때문에 0이 나온다 → (3, 4)를 (6,2)로 대체하게 됨
            - 왜 두번째 차원에 대해서만 LIS를 해도 되는가?
                - 같은 width를 가질 경우, 더 작은 height를 갖는 봉투가 더 뒤에 나오고, 앞의 봉투를 대체하게 됨
            - 왜 두번째 차원이 더 작은 봉투가 LIS에 포함되도록 하는가?
                - By placing shorter envelopes later in the sorted list for the same width, they have a higher chance of being part of the increasing height sequence.
                - If a taller envelope is included in the LIS, it would prevent the inclusion of any other envelope of the same width due to the height sorting order.