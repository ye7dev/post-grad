# 399. Evaluate Division

Status: in progress, with help, 🏋️‍♀️
Theme: graph
Created time: December 13, 2023 5:10 PM
Last edited time: December 14, 2023 11:51 AM

- Editorial
    - Path Search in Graph (BFS, DFS 관련 내용이라 나중에)
        - 새로운 등식을 도출하는 방법
            
            1) equation에서 주어진 분수의 역수 취하기 
            
            2) 주어진 분수들을 chaining up 하기 
            
        - equations들을 그래프 자료 구조로 전환
            - 각 변수가 node, 나눗셈 관계는 방향과 가중치가 있는 edge!
                - 방향: 어느게 분모고 어느게 분자인지
                - 가중치: 나눗셈 결과값 (value)
            - 그림
                
                ![Untitled](Untitled%2068.png)
                
        - 주어진 쿼리를 평가하는 것은 그래프 위에서 두 가지 task를 수행하는 것과 같음
            1. 쿼리를 구성하는 두 요소가 연결되어 있는지 확인
            2. 만약 연결되어 있으면 cumulative products along the paths를 구한다 
        - 알고리듬
            - BFS, DFS 사용-추후 공부할 것이기 때문에 우선 pass
    - Union-Find with Weights
        - 우선 확실히 알 수 있는 건 두 노드의 연결 여부 - connected method
        - Cumulative product along the path
            - 기존 Union find 자료 구조의 약간의 변형 필요
                
                ⇒ 그래프의 각 node마다 어떤 entry를 받아 저장하는 table 생성 
                
                - entry: `key -> (group_id, weight)`
                    
                    예) ‘a’ → (’a’, 1) : 두번째 ‘a’는 첫번째 ‘a’가 속한 그룹의 대표값을 의미 
                    
                    - 초기값은 (자기 자신, 1)
                    
                    ![Untitled](Untitled%2069.png)
                    
                - 위의 entry가 두 개 있을 때(`(a_group_id, a_weight)` and `(b_group_id, b_weight)`) 쿼리 (`a/b`) 답을 구하려면
                    
                    1) a, b의 그룹 아이디가 동일한지 확인 → 동일해야 둘 사이에 path가 있다는 뜻 
                    
                    2) a_weight / b_weight : dividing over the relative weights assigned to the variables
                    
        - 예시
            1. Union operation으로 a/b = 2 처리
                - union 하고 나면 각각 존재하던 a, b 그룹이 하나로 병합
                    - 분자인 a를 분모인 b에 갖다 붙임
                - group a의 relative weight를 update → to reflect the ratio between the two variables.
                    
                    ![Untitled](Untitled%2070.png)
                    
            2. Union operation으로 b/c = 3 처리 
                - 분자인 b를 c에 붙여주고, relative weights update
                    
                    ![Untitled](Untitled%2071.png)
                    
                - 이 상황에서의 inconsistency
                    - a의 group_id는 c로, relative weights는 group id인 c와의 관계이므로 6으로 update되어야 하는데 안되어 있음
                    - find operation으로 마법이 펼쳐진다~
                        
                        `find(a)` → chain reaction triggered 
                        
                        ![Untitled](Untitled%2072.png)
                        
                
        - 전체 풀이
            - equation을 돌면서 `union(분자, 분모, 몫)` → union-find 자료 구조 빌드
            - query 하나씩 처리
                - case1: query를 구성하는 두 변수 모두 equation에서 등장한 적이 없음 → return -1.0
                - case2: 두 변수 모두 equation에 등장 → `find(변수)` → 변수 별로 (group_id, weight) 얻기 → 만약 두 변수의 그룹이 서로 다른 것으로 밝혀지면 chain of division이 없다는 것 → return -1
                - case3: 두 변수 모두 valid & 같은 그룹에 있음 → 두 변수의 weight 사이의 나눗셈 수행
        - `group_weight[num_id] = (denom_id, denom_wt * value / num_wt)`이해하기
            - 원래 내가 생각한 node의 relative weight : node’s weight / root’s weight
            - 근데 문제에서의 relative weight: node부터 root까지 가는 과정에서 만나는 ratio의 곱
                
                In the union-find structure, especially in the context of this problem where we deal with equations, the weight of each node (variable) is defined relative to the root of its group. The key point here is that the weight of a node is not just a simple direct ratio to the root, but a cumulative product of ratios along the path from the node to the root.
                
                Here's a step-by-step explanation:
                
                1. **Initial Weights**: Initially, each variable (node) is in its own group with itself as the root. At this stage, the weight of each variable relative to its own root is 1 (since any variable divided by itself equals 1).
                2. **Combining Groups**: When we combine two variables (say, `A` and `B`) using an equation (like `A = 2 * B`), we are essentially saying that `A` is in the same group as `B` and its value is 2 times that of `B`. This relationship sets the weight of `A` relative to `B`.
                3. **Cumulative Product**: Suppose there's another variable `C` such that `B = 3 * C`. Now, `C` is the root of the group containing `A`, `B`, and `C`. The weight of `B` relative to `C` is 3, and the weight of `A` relative to `B` is 2. To find the weight of `A` relative to `C`, we multiply these weights: \( 2 \times 3 = 6 \). This means `A` is 6 times `C`.
                4. **Relative Weight to the Root**: The relative weight of any node to the root of its group is the cumulative product of weights along the path from the node to the root. This cumulative product tells us how the value of the node is related to the value of the root.
                5. **Why Cumulative Product?**: The cumulative product ensures that all the relationships (ratios from the equations) along the path from a node to the root are accounted for. This is crucial to maintain consistency in the relationships when groups are merged.
                
                In the context of your problem, when we talk about the relative weight of `dividend` to the root, it's the cumulative product of all the weights (ratios) from `dividend` to the root of its group. This cumulative weight is what's used in the formula `divisor_weight * value / dividend_weight` to correctly merge the groups while maintaining the integrity of the relationships defined by the equations.
                
            - 예) A = 2 * B, B = 3 * C → A가 C를 root로 삼는다고 하면, A → B → C 과정에서 만나는 ratio 2 * 3 = 6
            - num_wt, denom_wt는 find function을 각각 지나온 것이고, 그래서 chain of ratio를 곱한 결과임. 물론 식에서는 rel_wt * group_wt 지만 사실 group_wt에 여러 단계의 곱이 축적되어 있다고 생각
            - num을 denom에 합쳐야 하는 상태 → denom이 속한 chain에서 num을 붙인 뒤, 여기서 출발해서 denom의 root까지 가는 길에 만나는 ratio의 누적 곱이 새로운 weight가 되어야 함
                - 그런데 우리가 갖고 있는 정보는
                    
                    1) num/denom ratio
                    
                    2) num이 자기 chain을 거쳐서 root에 도달하기 까지 누적된 ratio
                    
                    3) denom이 자기 chain을 거쳐서 root에 도달하기까지 누적된 ratio 
                    
            - **`divisor_weight * value`**
                - calculates what the `dividend` would be if it were in the same group as `divisor`, directly compared to the root of `divisor`'s group. It's like re-scaling `dividend` to the scale of `divisor`'s group using the given equation.
                - For example, if `divisor_weight` is 4 (meaning `divisor` is 4 times the value of the root of its group), and `value` is 2 (from the equation `dividend / divisor = 2`), then `divisor_weight * value` is 8. This means if `dividend` were in the same group and directly compared to the `divisor`, it would be 8 times the root's value.
                
                ⇒ 분모가 자기 chain에서 갖는 상대적 가치 * 분자가 분모에 대해 상대적으로 갖는 가치 = 분자가 분모의 chain에 있다고 가정할 때 갖게 될 상대적 가치 
                
            - **`/dividend_weight`**
                - Suppose in the `divisor`'s group, the `divisor` is twice the value of the root (so `divisor_weight = 2`), and the equation says `dividend / divisor = 4` (so `value = 4`). This implies that in the context of `divisor`'s group, `dividend` should be 8 times the root (`divisor_weight * value = 8`).
                - However, if in the `dividend`'s group, the `dividend` is already 2 times the value of its root (`dividend_weight = 2`), dividing by `dividend_weight` adjusts this value back to 4 times the root of `divisor`'s group, which is the correct scale for merging.
                
                ⇒ 분자만 떼다가 분모의 그룹(체인, 집합 whatever)에 붙이는 것이 아니라, 분자가 속한 전체 체인을 분모의 체인에다가 합병시켜야 함. 따라서 분모의 그룹에서 분자 개인의 가치만 계산할 것이 아니라, 분자의 체인 위에서 분자가 가졌던 상대적 가치까지 같이 고려해야, 병합된 두 체인에서의 분자 개인의 가치가 정확하게 update 되는 것임 ;; 
                
            - chat gpt 추가 설명
                - To clarify why we divide by `dividend_weight`
                    
                    In the expression `divisor_weight * value / dividend_weight`, let's consider the process step by step:
                    
                    1. **Scaling in the Context of the Divisor's Group**: When we calculate `divisor_weight * value`, we're temporarily placing the `dividend` in the `divisor`'s group and scaling it according to the given ratio (the `value` from the equation). This gives us a new scaled value for the `dividend`, but this value is in the context of the `divisor`'s group.
                    2. **Need to Adjust Back to Dividend's Group**: However, the `dividend` originally belongs to its own group, where it has a certain established relationship (weight) with respect to its own group's root. This relationship is what `dividend_weight` represents.
                    3. **Why Divide by `Dividend_weight`**:
                        - The division by `dividend_weight` adjusts the scaled value of the `dividend` back to the context of its own original group.
                        - It effectively asks, "Given this new scaled value in the context of the `divisor`'s group, what would be the equivalent value in the `dividend`'s original group?"
                    4. **Merging the Groups with Consistent Scales**:
                        - The purpose of this operation is to merge the groups of `dividend` and `divisor` while maintaining the correct relative values as defined by the original equations.
                        - Without this adjustment (the division by `dividend_weight`), the scale of values would be inconsistent across the merged group. We need to ensure that after merging, the relative values of all variables in the newly formed group are still accurate according to the equations provided.
                    5. **An Illustration**:
                        - Suppose `dividend_weight = 2`, meaning in its original group, `dividend` is twice the value of its root.
                        - Now, in the context of `divisor`'s group, we find that `dividend` should be, say, 8 times the root of `divisor`'s group (from `divisor_weight * value`).
                        - Dividing this by `dividend_weight` (2) gives us 4. This means, to maintain the ratio consistent with the original equation when merging the groups, the `dividend` should be considered as 4 times the root of `divisor`'s group.
                    
                    In summary, dividing by `dividend_weight` is a necessary adjustment to ensure that when we merge the groups of `dividend` and `divisor`, the relative values of variables within these groups remain consistent and accurate. It's a re-scaling step to align the `dividend`'s value back to its original group's context before finalizing the merge.
                    
                - Merging entire groups
                    
                    In the union-find algorithm, especially in the context of the problem you're working with, we merge the entire chain (or group) of the `dividend` into the chain (or group) of the `divisor`, not just the `dividend` alone.
                    
                    Here's how it works:
                    
                    1. **Merging Entire Chains**: When a union operation is performed (as in the case of `union(dividend, divisor, value)`), it's not just about connecting the `dividend` and `divisor` directly. Instead, the whole group (or chain) that `dividend` belongs to is merged with the whole group that `divisor` belongs to.
                    2. **Adjusting Weights During Merging**: This merging process involves adjusting the weights of the variables in the `dividend`'s group to maintain the correct relative values as per the given equations. The expression `divisor_weight * value / dividend_weight` is crucial in this process. It helps recalculate the weights for the variables in the `dividend`'s group so that they are consistent with the ratios in the `divisor`'s group.
                    3. **Result of Merging**: After the merge, all variables in both the `dividend`'s and `divisor`'s groups will be part of a single, larger group. They will have a common root (the root of the `divisor`'s group), and their weights will be adjusted so that the equations (ratios) that defined their relationships are still valid in this new, combined group.
                    4. **Why Merge Entire Groups?**: Merging entire groups is essential because each variable (not just `dividend` and `divisor`) has established relationships with other variables in its group. To maintain the integrity of all these relationships, the entire groups need to be merged and recalibrated.
                    
                    In essence, the union operation in this algorithm is about integrating entire sets of relationships (chains or groups) rather than just connecting individual elements. This ensures that all the relationships (equations) between variables are preserved and remain consistent across the merged group.
                    
        
- AC 코드
    
    ```python
    class Solution:
        def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
            group_weight = {}
    
            def find(nid):
                # add node 
                if nid not in group_weight: 
                    group_weight[nid] = (nid, 1) # a/a = 1 
                # lookup
                group_id, rel_wt = group_weight[nid]
                # inconsistency -> chain update
                if group_id != nid: # root[x] != x
                    new_group_id, group_wt = find(group_id) # find(root[x])
                    group_weight[nid] =  (new_group_id, rel_wt * group_wt) # root[x] = find(root[x]) + α
                return group_weight[nid]
            
            def union(num, denom, value):
                # get numerator's info
                num_id, num_wt = find(num)
                # get denominator's info
                denom_id, denom_wt = find(denom)
                # merge two different groups
                if num_id != denom_id:
                    group_weight[num_id] = (denom_id, denom_wt * value / num_wt)
            
            # big picture (1) build groups from equations
            for i in range(len(equations)):
                num, denom = equations[i]
                value = values[i]
                union(num, denom, value)
            
            results = []
            # big picture (2) check queries 
            for num, denom in queries:
                # case 1. equation에 없던 node가 나올 때 
                if num not in group_weight or denom not in group_weight:
                    results.append(-1.0)
                else:
                    num_id, num_wt = find(num)
                    denom_id, denom_wt = find(denom)
                    if num_id != denom_id:
                        # case2. 두 node가 서로 다른 그룹에 위치 -> 서로의 상대적 가치를 알길이 없음(?)
                        results.append(-1.0)
                    else:
                        # case3. 같은 그룹이면 서로의 상대적 가치가 계산된 상태라서 나눗셈만 하면 된다
                        results.append(num_wt / denom_wt)
            return results
    ```