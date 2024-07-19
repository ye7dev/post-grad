# 188. Best Time to Buy and Sell Stock IV

Status: done, incomplete, 👀1
Theme: DP
Created time: November 17, 2023 4:56 PM
Last edited time: November 21, 2023 12:19 AM

- 왜 그런지 모르겠지만 row 선언 시에는 무조건 list comprehension 사용해야. columns 처럼 * length 하면 안된다고 함
    
    I**mproper Initialization of `dp` Array**: In your code, the **`dp`** array is initialized in a way that makes each row a reference to the same array. This happens due to the use of the **`*`** operator for list multiplication in Python, which does not create distinct inner lists but references to the same list. This will cause unexpected behavior as modifying one element in any row will affect all other rows in the same column.
    
- 코드
    
    ```python
    def maxProfit(self, k: int, prices: List[int]) -> int:
            # i: trx, j: day
            dp = [[-float('inf')] * len(prices) for _ in range(k+1)] 
    
            dp[0][0] = 0
            
            for j in range(1, len(prices)): # no trx 
                dp[0][j] = 0
            for i in range(1, k+1): # first day: buying or do nothing
                dp[i][0] = 0 
    
            for i in range(1, k+1):
                max_diff = -prices[0]
                for j in range(1, len(prices)):
                    dp[i][j] = max(dp[i][j-1], max_diff + prices[j])
                    max_diff = max(max_diff, dp[i-1][j-1]-prices[j])
    
            return dp[-1][-1]
    ```
    
- dp[i][j] : day j까지 고려했을 때(inclusive), 최대 i번의 거래(inclusive)를 통해 얻을 수 있는 최대 이익
    - base case
        - i = 0 → 거래가 0번이면 이익도 0
        - j = 0 → 첫날에 할 수 있는 것: 주식 사기 / 안 사기 → 둘 다 얻게 되는 이익은 0
        - **이전 상태**
            - 주식을 오늘 가격에 파는 경우에만 불러와서 사용됨
            - 오늘 팔게 되는 주식을 과거 어느 시점에 샀을 텐데, 그 때 나의 금전 상태를 의미
            - 초기값: -prices[0]
    - transition
        - dp[i][j] update
            
            오늘 아무 거래도 하지 않고 어제 상태 유지 vs.  **이전 상태** + 오늘 주식 팔아서 얻은 이익 
            
        - 이전 상태 update
            
            다음 언젠가에 팔게 될 주식을 오늘 산다고 할 때 
            
            기존의 이전 상태 vs. 어제 직전 거래까지 마친 상태 - 오늘 주식 사는데 든 비용 (=오늘은 사기만 한 경우) (dp[i-1][j-1] - prices[j])
            
- max_diff에 관한 고찰
    
    ```python
     for i in range(1, k+1):
        max_diff = -prices[0]
        for j in range(1, len(prices)):
            dp[i][j] = max(dp[i][j-1], max_diff + prices[j])
            max_diff = max(max_diff, dp[i-1][j-1]-prices[j])
    ```
    
    - `dp[i][j] = max(dp[i][j-1], max_diff + prices[j])`
        - `dp[i][j-1]` 오늘 아무것도 안하고 전날의 이익 유지
        - `max_diff + prices[j]` 과거에 어느 시점에 어떤 가격으로 주식을 사고 난 상태의 이윤 + 오늘 가격으로 주식을 팔고 얻은 이윤
    - 거래 횟수가 하나 올라갈 때, max_diff는 왜 또 첫날 가격으로 주식을 사는 경우의 비용으로 기준점을 잡는가? 여전히 이해 안감…
        - 예를 들어 i=2라고 하자, 그럼 앞에서 사고 팔고 한번은 한건데 어떻게 첫날 가격을 기준점으로 삼을 수가…
        - 근데 또 그렇게 다지면 애초에 k ≥ 2 이면 첫째날 둘째날은 채우지도 말아야 할텐데
        - j도 어차피 1(둘째날)에서부터 시작함.
- 좋은 해설
    
    Easy to understand explanation for the above solution
    
    `dp[i][j] = maximum profit from at most i transactions using prices[0..j]`
    
    A transaction is defined as one buy + sell.
    
    Now on day j, we have two options
    
    1. Do nothing (or buy) which doesn't change the acquired profit : `dp[i][j] = dp[i][j-1]`
    2. Sell the stock: In order to sell the stock, you must've bought it on a day `t=[0..j-1]`. Maximum profit that can be attained is `t:0->j-1 max(prices[j]-prices[t]+dp[i-1][t-1])` where `prices[j]-prices[t]` is the profit from buying on day `t` and selling on day `j`. `dp[i-1][t-1]` is the maximum profit that can be made with at most `i-1` transactions with prices `prices[0..t-1]`.
    
    Time complexity of this approach is O(n^2k).
    
    In order to reduce it to O(nk), we must find `t:0->j-1 max(prices[j]-prices[t]+dp[i-1][t-1])`this expression in constant time. If you see carefully,
    
    `t:0->j-1 max(prices[j]-prices[t]+dp[i-1][t-1])` is same as
    
    `prices[j] + t:0->j-1 max(dp[i-1][t-1]-prices[t])`
    
    Second part of the above expression `maxTemp = t:0->j-1 max(dp[i-1][t-1]-prices[t])` can be included in the dp loop by keeping track of the maximum value till `j-1`.
    
    Base case:
    
    `dp[0][j] = 0; dp[i][0] = 0`
    
    DP loop:
    
    `for i : 1 -> kmaxTemp = -prices[0];for j : 1 -> n-1dp[i][j] = max(dp[i][j-1], prices[j]+maxTemp);maxTemp = max(maxTemp, dp[i-1][j-1]-prices[j]);return dp[k][n-1];`
    

## 또 다른 풀이

- k ≥ n/2 이면 거래 회수가 날짜 수의 절반 보다 크다. 예를 들어 날짜 수가 4일인데 거래 횟수가 8번까지 가능 → 그럼 무조건 전날에 산 가격보다 높기만 하면 바로 팔아서 이익을 조금이라도 많이 남겨야
    - 한 번의 거래는 사고/팔고로 이루어지는데 각각 하루가 필요하다고 해도, 공백기를 하루도 두지 않고 어제 사고 오늘 팔고를 계속 해도 된다는 뜻이라고 함
    
    ```python
    if k >= n/2:
    	max_pro = 0
    	for i in range(1, n):
    		if (prices[i] > prices[i-1]):
    			max_pro += prices[i] - prices[i-1]
    	return max_pro		
    ```
    
    예) 날짜 [10, 1, 2, 3, 20], 거래횟수: 8 
    
    - 직관적으로 보면 1에 사서 20에 팔면 1번의 거래로 19 얻을 수 있어서 최대일 것도 같지만…
    - 1에 사서 2에 판매: +1 → 2에 사서 3에 판매: +1 → 3에 사서 20에 판매 : +17
        
        ⇒ 1+1+17 = 19
        
        이렇게 해도 최대가 나온다 
        
- k < n/2 인 경우
    
    ```python
    dp = [[0]*n for _ in range(k+1)]
    for i in range(1, k+1):
    	local_max = dp[i-1][0] - prices[0] #어차피 0-prices[0] = -prices[0]
    	for j in range(1, n):
    		dp[i][j] = max(dp[i][j-1], local_max+prices[j])
    		local_max = max(local_max, dp[i-1][j] - prices[j]) 
    
    return dp[k][n-1]
    ```