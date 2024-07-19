# 638. Shopping Offers

Created time: May 21, 2024 5:37 PM
Last edited time: May 23, 2024 5:51 PM

- 문제가 무슨 소리인지 잘 모르겠다 예제를 보자
    
    ```
    Input: price = [2,5], special = [[3,0,5],[1,2,10]], needs = [3,2]
    Output: 14
    Explanation: There are two kinds of items, A and B. Their prices are $2 and $5 respectively.
    In special offer 1, you can pay $5 for 3A and 0B
    In special offer 2, you can pay $10 for 1A and 2B.
    You need to buy 3A and 2B, so you may pay $10 for 1A and 2B (special offer #2), and $4 for 2A.
    ```
    
    - needs[i]: 물건 i를 사야 하는 개수
    - price[i]: 물건 i의 개당 가격
    - special[idx]: idx번째 할인 판매 패키지
    - special[idx][-1]: package 전체 가격
    - special[idx][i]: 내가 사고 싶은 물건i가 idx번째 패키지에 몇 개 포함되어 있는지
    - 특정 항목들을 정확히 구매하는 데 지불해야 하는 최저 가격을 반환하세요. 이때 특별 할인 상품을 최적으로 활용할 수 있습니다. 필요한 항목보다 더 많이 구매하는 것은 허용되지 않습니다, 비록 그것이 전체 가격을 낮출 수 있더라도. 특별 할인 상품은 원하는 만큼 여러 번 사용할 수 있습니다.
- scratch
    - state가 보통은 물건 별로 있어야 하는데 물건이 최대 6개까지 나온다고 하면 6차원 dp를 만들어야 하나?
    - 그리고 memoization 쓰기에는 물건 별 남은 개수를 parameter로 쓸 건데 list를 dict의 key로 쓸수가 없다
    - package index로 가야 하지 않으려나?
        - 근데 package는 몇 번이고 쓸 수 있다는데
    - package i까지를 j번 사용했을 때까지의 치뤄야 하는 비용?
- AC 코드
    - Top-down solution
        
        ```python
        class Solution:
            def shoppingOffers(self, price: List[int], special: List[List[int]], needs: List[int]) -> int:
                n_items = len(needs)
                n_sale = len(special)
                memo = {}
        
                def get_full_price(items):
                    total = 0
                    for i in range(len(items)):
                        total += price[i] * items[i]
                    return total
        
                def recur(items_to_buy, sale_position):
        		        state = (tuple(items_to_buy), sale_position)
        		        if state in memo:
        			        return memo[state]
                    cur_min = get_full_price(items_to_buy)
                    for i in range(sale_position, n_sale):
                        cur_offer = special[i]
                        next_buy = []
                        for item_idx in range(n_items):
                            if cur_offer[item_idx] > items_to_buy[item_idx]:
                                next_buy = None 
                                break 
                            else:
                                # update the number of items to buy 
                                next_buy.append(items_to_buy[item_idx]-cur_offer[item_idx])
                                
                        if next_buy is not None:
                            cur_min = min(cur_min, cur_offer[-1] + recur(next_buy, i))
                            
                    memo[state] = cur_min
                    return memo[state]
                
                return recur(needs, 0)
        
                    
                
        ```