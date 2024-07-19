# 149. Max Points on a Line

Status: done
Theme: math
Created time: November 1, 2023 5:19 PM
Last edited time: November 2, 2023 4:56 PM

- 나의 30분
    - 어느 점을 기준으로 잡고 갈 것인가-근데 max input이 300개인 것으로 보아 전체를 다 돌면서…?
    - union-find 알고리즘과 비슷할 것 같은데 같은 집합에 있다는 것을 어떻게 기록…
    - 각 점에 대해 각 점을 돌면서 x가 같거나, y가 같거나, x와 y의 차이가 같거나(대각선) 체크까지는 할 수 있을 것 같은데. x가 2 차이 나고 y가 1 차이나는 경우의 직선 이런 건 커버 안됨
- 남의 풀이
    - 포인트: 같은 직선 위에 있는 점들은 두 점 사이의 slope가 동일하다! y차이 / x차이
    - 주어진 점의 개수가 2개 이하면 그냥 그 자체로 직선이 되기 때문에 그대로 개수 return
    - pairwise (자기 자신과 그 뒤에 있는 모든 점을) 비교
    - 기울기 사전을 만들어서 각 기울기마다 해당되는 점이 몇 개인지 기록
        - 근데 x 좌표가 같은 경우 기울기를 계산할 수 없음 → key를 문자로 하나 해서 넣어줘야 겠다
            - ‘etc’라는 특수 경우를 하나만 만들면, 서로 다른 x 값을 가진 pair가 하나의 key 아래 모여서 에러
            - f‘etc_{x}’로 key를 따로 만들어줬지만, 또 에러
    
    ⚠️ 근데 생각해보면 같은 기울기라도…(0, 0)&(1, 1) vs. (1, 2)%(2, 3) 이 두 pair는 같은 기울기지만 같은 직선 위에 있지 않다 ⇒ **slope dictionary를 각 점마다 만들어준다!** 
    
    - 이렇게 하면 마지막에 가장 value를 많이 갖고 있는 key의 value length에 +1만 해줘도 된다 귀찮게 value를 set으로 만들고 add를 여러번 할 필요도 없음
    - 가장 큰 점 개수를 return
        - max 값 찾는 것은 inner loop 돌면서 사전에 값 추가하는 즉시 그때그때 비교하면 for loop 마지막에 또 안 돌아도 돼서 편리
    
    ```python
    class Solution:
        def maxPoints(self, points: List[List[int]]) -> int:
            if len(points) <= 2:
                return len(points)
            
            def find_slope(p1, p2):
                x1, y1 = p1
                x2, y2 = p2
                if x1-x2 == 0:
                    return inf
                return (y1-y2)/(x1-x2)
            
            ans = 1
            for i, p1 in enumerate(points):
                slopes = defaultdict(int)
                for j, p2 in enumerate(points[i+1:]):
                    slope = find_slope(p1, p2)
                    slopes[slope] += 1
                    ans = max(slopes[slope], ans)
            return ans+1
    ```