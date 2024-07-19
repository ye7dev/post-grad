# 458. Poor Pigs

Status: done, in progress
Theme: DP
Created time: March 12, 2024 1:37 PM
Last edited time: March 15, 2024 1:40 PM

- 문제 이해
    - N개의 양동이가 있을 때 하나만 유독성 물질을 담고 있음
    - 돼지들한테 먹여보고 유독성 테스트 하는데, 단 테스트 시간은 제한 - minutesToTest
    - 테스트 방법
        1. 살아 있는 돼지를 고른다
        2. 각 돼지에게 어떤 양동이를 먹일지 고른다. 돼지 한 마리에게 먹일 양동이가 여러 개인 경우에도 시간이 더 걸리지 않는다(?) 
            - 돼지 한 마리는 몇 개의 양동이를 먹어도 상관 없고, 각 양동이는 몇 번이고 돼지의 먹이가 될 수 있음
        3. minutesToDie 만큼 시간을 기다리면서 다른 돼지를 먹이지 않고 있는다
        4. minutesToDie의 시간이 지나고 나면, 독이 든 양동이로부터 먹이를 먹은 돼지는 죽을 것이고, 아닌 애들은 살아 있을 것
        5. minutesToTest를 다 쓸 때까지 실험을 반복한다 
    - 주어진 시간 내에 어떤 양동이가 유독한지 알기 위해 필요한 최소 돼지 수를 구하라
- Editorial
    - 돼지 한 마리가 가질 수 있는 state의 수: (minTest/minDie) + 1
    - x마리의 돼지로 test 할 수 있는 bucket의 수: (num_states) ** x
    - (num_states) ** x  ≥ buckets 를 만족하는 최소 x = log(buckets, base: num_states)
    - math ceil function 사용해서 정수로 구한다