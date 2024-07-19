# 1238. [S/W 문제해결 기본] 10일차 - Contact

Created time: April 7, 2024 4:53 PM
Last edited time: April 7, 2024 9:35 PM

[https://careers.tridge.com/ko/jobs/464qFnv29jK2tA9NRpvsgnk42](https://careers.tridge.com/ko/jobs/464qFnv29jK2tA9NRpvsgnk42)

```python
from collections import deque
def get_latest(first, arr):
    # arr to graph
    graph = {}
    for i in range(0, len(arr), 2):
        f, t = arr[i], arr[i+1]
        if f not in graph:
            graph[f] = []
        if t not in graph:
            graph[t] = []
        if t not in graph[f]:
            graph[f].append(t)

    visited = [False] * 101
    visited[first] = True

    dq = deque([(first, 0)])
    max_contact = -1
    max_latest = -1
    while dq:
        for _ in range(len(dq)):
            x = dq.popleft()
            cur_node, num_contact = x
            if max_contact < num_contact:
                max_latest = cur_node
                max_contact = num_contact
            if max_contact == num_contact:
                max_latest = max(max_latest, cur_node)
            for next_node in graph[cur_node]:
                if not visited[next_node]:
                    visited[next_node] = True
                    dq.append((next_node, num_contact + 1))

    return max_latest

for tc in range(1, 1+1):
    len_data, start = map(int, input().split())
    data = list(map(int, input().split()))
    print(f'#{tc} {get_latest(start, data)}')
```