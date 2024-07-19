# bisect 모듈

Status: done, tools🛠️
Created time: January 19, 2024 12:03 PM
Last edited time: January 22, 2024 2:18 PM

- python 표준 라이브러리. 원소 추가할 때마다 list를 정렬하지 않고도 updated list를 정렬된 상태로 유지해주는 기능
    - 정렬된 sequence에서 원소 삽입, 검색이 잦을 때 유용
- Key functions
    1. `bisect.bisect_left(list, item, lo=0, hi=len(list))`
        - list의 정렬된 상태를 유지되도록 원소 item을 어디에 추가하면 되는지 추가 지점을 알려줌
        - low, high는 탐색 대상인 subsequence를 지정
        - return value: index i
            - `list[lo:i]` 구간에 위치한 원소들은 모두 item보다 크기가 작고
            - `list[i:hi]` 구간에 있는 원소들은 모두 item보다 크거나 같다
            - low-item(i)-hi
        - item이 들어가게 될 자리 i는 들어갈 수 있는 자리 중 가장 왼쪽을 의미
            - item과 크기가 같은 요소들은 모두 i의 오른쪽에 위치
    2. `bisect.bisect_right(list, item, lo=0, hi=len(list))`
        - item이 들어가게 될 자리 i는 들어갈 수 있는 자리 중 가장 오른쪽
            - item과 크기가 같은 요소들은 모두 i의 왼쪽에 위치
        - return value: index i
            - `list[lo:i]` 구간에 있는 원소들은 모두 item보다 크거나 같고
            - `list[i:hi]` 구간에 있는 원소들은 모두 item보다 크다
            - low-item(i)-hi
- bisect 모듈 활용한 LIS solution
    - `i = bisect_left(sub, num)`
        - sub라는 list의 정렬 상태를 유지하면서 num을 추가할 수 있는 자리 중, 가장 왼쪽의 index가 i
    - 순서가 상관 없을 때 원소를 다 붙여서 LIS를 만드는 게 아닐까 했지만 아니었음
        - 왜냐면 `sub[i] = num` 에 도달하는 경우 기존 원소를 replace 해버리기 때문
    - 전체 코드 흐름
        - longest increasing subsequence를 실제로 만든 다음 그것의 길이를 구한다
        - 원소를 앞에서부터 하나씩 돌면서
            - 제일 큰 원소라서 increasing subsequence를 연장할 수 있는 경우, 현재 subsequence에 마지막으로 붙이고
            - 아닌 경우 그것이 위치해야 하는 자리에 있던 다른 원소를 지금 원소로 대체한다
        - [1, 2, 3, 9, 5, 6, 7]의 경우, 9가 [1, 2, 3] 뒤에 오고 난 이후로 5, 6, 7이 못 들어가서 length of LIS가 6까지 나올 수 있는데 4에서 가로막히는 게 아닌가? → 아니다
            - [1, 2, 3, 9]인 상태에서 5를 만나면 bisect module은 3을 내놓을 것 → 5가 9를 대체하게 되고, 그래서 [1, 2, 3, 5] 가 된 이후로는 [6, 7]이 추가로 뒤에 올 수 있기 때문에 length of LIS는 6이 된다
    
    ```python
    class Solution:
        def lengthOfLIS(self, nums: List[int]) -> int:
            subseq = []
            for num in nums:
                i = bisect_left(subseq, num)
    
                # If num is greater than any element in sub
                if i == len(subseq):
                    subseq.append(num)
                
                # Otherwise, replace the first element in sub greater than or equal to num
                else:
                    sub[i] = num
            
            return len(subseq)
    ```
    
- bisect module 이용해서 return value i 자리에 원소 넣기
    
    ```python
    # insert method
    >>> my_list = [1, 2, 3, 5]
    >>> # Inserting an element (4) at index 3
    >>> my_list.insert(3, 4)  # Now the list will be [1, 2, 3, 4, 5]
    >>> print(my_list)
    [1, 2, 3, 4, 5]
    # concatenation
    >>> my_list = [1, 2, 3, 5]
    >>> my_list[:3] + [4] + my_list[3:]
    [1, 2, 3, 4, 5]
    ```
    
- LIS solution에 bisect_right를 쓰면 안되는 이유
    
    ```python
    >>> from bisect import bisect_left, bisect_right
    >>> x = [2]
    >>> bisect_left(x, 2)
    0
    >>> bisect_right(x, 2)
    1
    ```
    
    - 같은 값의 원소를 또 만날 경우, LIS 는 strictly increasing 해야 subsequence를 연장할 수 있기 때문에, subsequence에 그 원소를 추가할 수 없음
    - bisect_left를 주면 늘 제일 왼쪽 자리를 return 할 것이고, 이미 원소가 있기 때문에 동일한 값으로 원소가 대체될 뿐 subsequence가 길어지지 않음
    - 그러나 bisect_right를 쓰면 늘 제일 오른쪽 자리를 return 하기 때문에 원소를 추가하게끔 만듦
    - 반드시 반드시 bisect_left를 써야 함
- LIS solution 주의
    - 길이를 맞게 구할 수 있지만, subseq 자체가 valid는 아니라고 함
        - It's important to note that **`subseq`** does not necessarily represent a true subsequence found in the original list in its original order. Instead, it's a tool used to keep track of the lengths of potential increasing subsequences as the algorithm processes each element of the input list. The key idea here is that the length of **`subseq`** at the end of the algorithm equals the length of the LIS in the input list, even though the actual elements in **`subseq`** might not be a valid subsequence of the input list in terms of their original order.
    - 구체적인 예제
        
        To determine the Longest Increasing Subsequence (LIS) length using the provided method and the given array `[3, 1, 5, 6, 4, 2]`, we can follow the algorithm step by step:
        
        1. Initialize an empty list `subseq`.
        2. Process each element in the array `[3, 1, 5, 6, 4, 2]`:
            - Start with `3`: `subseq` becomes `[3]`.
            - Next, `1`: Replace `3` with `1` in `subseq`, so `subseq` becomes `[1]`.
            - Then, `5`: Append `5` to `subseq`, making it `[1, 5]`.
            - Next, `6`: Append `6` to `subseq`, making it `[1, 5, 6]`.
            - Then, `4`: Replace `5` with `4` in `subseq`, so `subseq` becomes `[1, 4, 6]`.
            - Finally, `2`: Replace `4` with `2` in `subseq`, so `subseq` becomes `[1, 2, 6]`.
        3. The final `subseq` is `[1, 2, 6]`. The length of this list, which is `3`, is the length of the longest increasing subsequence in the given array.
        
        It's important to note that the actual elements in `subseq` (`[1, 2, 6]`) do not represent a valid increasing subsequence in the original array in terms of their original order. However, the length of this list (which is `3`) accurately represents the length of the LIS in the input array. The actual LIS in the given array could be `[1, 5, 6]`, `[1, 4, 6]`, or any other increasing sequence of length `3`.