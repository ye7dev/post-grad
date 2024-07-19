# Sqrt

Status: done
Created time: November 1, 2023 3:11 PM
Last edited time: November 1, 2023 4:37 PM

- 나는 그냥 Math 모듈 써서 풀었다
- `mid = first + (last-first)/ 2`
    - 그냥 (first + last) / 2 하는 것보다 안정적이라고 함
- *rounded down to the nearest integer로 구해야 하기 때문에 몫으로 따짐*
- binary search

```python
def mySqrt(self, x: int) -> int:
        if x == 0: return 0 
        first, last = 1, x
        while first <= last:
            mid = first + (last-first) // 2
            if mid == x // mid: 
                return mid 
            elif mid > x // mid:
                last = mid - 1
            else:
                first = mid + 1 
        return last
```