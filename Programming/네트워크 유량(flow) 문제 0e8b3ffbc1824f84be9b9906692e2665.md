# 네트워크 유량(flow) 문제

Created time: May 25, 2024 9:30 PM
Last edited time: May 26, 2024 4:33 PM

- 시작점(src) → 도착점(sink)로 동시에 보낼 수 있는 데이터나 사물의 최대 양을 구하는 알고리즘
- 네트워크의 bandwidth로 생각하면 좋음
- 용어 정리
    
    capacity(a, b): a→b edge를 통해 소화 가능한 (남은) 용량 값 
    
    flow(a, b): a→b edge에 대한 capacity 에서 이미 사용하고 있는 용량 = 유량 값 
    
- 유량의 대칭
    - a→b edge가 있고, 그 capacity가 5라면, b→a라는 가상의 edge가 있고, 해당 edge의 capacity는 0
    - f(a, b) = -f(b, a)
- 포드-풀커슨 알고리즘
    1. source → sink로 가는 경로를 찾는다 
        - 해당 경로는 c(a, b) - f(a, b) > 0이어야
    2. 찾아낸 경로에 보낼 수 있는 최대 flow를 찾는다 
        - 경로에 남은 capacity의 최소값
    3. 찾아낸 경로에 찾아낸 최대 flow를 흘려보낸다
        - 전체 경로에 f(a, b) += flow
        - 유링의 대칭 조건에 따라서 역방향으로도 음수값 flow를 흘려 보낸다
            - f(b, a) -= flow
            - 가상의 역방향 edge의 capacity는 사실 0이고, 해당 capacity에 음수 값으로 flow를 흘려도 용량의 제한을 넘지 않음
            - f(b, a) -= 1 → -1(flow)/0(capacity) → capacity(b,a) - f(b,a) = 0-(-1) = 1 이고 > 0 이라서 조건 만족
    4. 1번에 해당하는 경로 찾기가 실패하기 전까지 1~3번 반복 
    - 예
        - 역방향 edge가 없는 상황 → total: 9
            
            ![Untitled](Untitled%2014.png)
            
            ![Untitled](Untitled%2015.png)
            
            ![Untitled](Untitled%2016.png)
            
            → 3 + 2 + 4 = 9가 나옴 
            
        - 해당 그래프로 S → T 동시에 보낼 수 있는 최대 유량은 10
        - 역방향 edge가 있는 상황
            
            ![Untitled](Untitled%2017.png)
            
            → 3+2+5 = 10 
            
        - 두 상황 나란히 비교
            
            ![Untitled](Untitled%2018.png)
            
            - 차이가 나는 부분은 A→E가 3이 아니라 2, A→D가 0이 아니라 1
            - S→A→E→T로 3을 보내고 나면 S→A→D→T로는 보낼 수 있는게 없음
        - 역방향 edge가 있게 되면
            
            ![Untitled](Untitled%2019.png)
            
            - 마지막 S→C→F까지 5를 보낼 수 있음
            - F→T 로 4를 보내고, F→E를 1로 보낼 수 있음
            - 그리고 A→E 가면서 역방향으로 -3(flow)/0(capacity)인 상황인데
                - 여기서 remain capacity를 구해보면 c(a,e)-f(a,e) = 0-(-3) = 3
            - 여기다가 1을 보내면
                - E→A는 -3+(1) = -2 < 0
                - 역방향으로 A→E는 3-(1) = 2 < 3(A-E의 capacity)
                    
                    [https://www.notion.so](https://www.notion.so)
                    
                - A에서 1이 남게 되기 때문에 A→D→T로 1을 보낼 수 있게 됨
- 추가
    - [https://velog.io/@cjkangme/알고리즘-네트워크-유량-Network-Flow-파이썬](https://velog.io/@cjkangme/%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC-%EC%9C%A0%EB%9F%89-Network-Flow-%ED%8C%8C%EC%9D%B4%EC%8D%AC)

📌 정리

1. given state: source, sink, capacity[a][b]
    - a-b edge로 흐를 수 있는 용량
2. changing state: flow[a][b]
    - a-b edge로 이미 흐르고 있는 유량
3. 큰 그림 
    1. bfs해서 어떤 경로를 찾는다
    2. 해당 경로에 흘려보낼 수 있는 최소 유량을 찾는다
    3. 경로로 흘려보낸다
    4. 상태를 update 한다 
4. bfs 
    - visited는 매 bfs에서 renewal 되지만
    - valid next node에 대한 조건이
        1. visited
        2. capacity[cur][next]-flow[cur][next] > 0 
        
        으로 두 가지이고, capa는 일단 주어지면 고정이지만, flow array는 매 bfs 이후에 update 되기 때문에 bfs의 결과가 턴 마다 달라지게 된다 
        
    - 늘 source에서 시작하고, next_node로 sink를 만나면 return True
        - prev array를 통해 source와 sink 사이의 경로가 완성된 상태
        - sink → prev[sink] → another prev → … → source
            - linked list 역방향으로 움직이는 것 생각하면 됨
    - 다 돌고도 - flow가 이미 최대치로 흐르고 있어서 더 이상 valid next node가 없는 경우 - next_node로 sink를 만나지 못한 채 dq가 다 비어버리면 return False
5. 하나의 경로에서 흘릴 수 있는 최소 유량 찾기 
    - 흘릴 수 있는 유량이니까 capacity - flow
    - sink에서 시작, source로 거슬러 올라가면서 capacity[prev][cur]-flow[prev][cur]이랑 min_flow랑 비교해서 작은 쪽으로 update
6. 하나의 경로로 최소 유량 흘려보내기 
    - sink에서 source로 거슬러 올라가면서 순방향으로는 양수 min_flow를 더해주고, 역방향으로는 음수 min_flow를 더해주면 됨
    - flow[prev][cur]이 순방향, flow[cur][prev]가 역방향
7. res에 한 경로에 대한 min_flow 더해줌 
    - while bfs인 한 res에 계속 더 해져서 최종적으로 해당 그래프에 src→sink로 동시에 흘릴 수 있는 유량이 나오게 됨