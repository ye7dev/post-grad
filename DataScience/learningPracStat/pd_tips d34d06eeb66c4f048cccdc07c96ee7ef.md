# pd_tips

- **`ax`**
    - Matplotlib에서 사용되는 축(Axes) 객체를 나타내는 변수명입니다.
    - 이 객체는 특정 하나의 그래프나 플롯에 대한 모든 요소와 설정을 포함
- `**kwargs`
    - keyword arguments
    
    ```python
    def record_data(**kwargs):
        for key, value in kwargs.items():
            print(f"{key}: {value}")
    
    # Calling the function with various keyword arguments
    record_data(name="Alice", age=25, job="Engineer")
    ```
    
- `ravel()`
    - 다차원 배열이나 DataFrame의 데이터를 1차원 배열로 변환
    - df column이나 agg 함수 적용한 결과에서 .values 하면 ndarray로 return 되고, nested array가 됨
        - 예
            
            ```sql
            array([[172.8],
                   [182.6],
                   [175.6],
                   [164.6]])
            ```
            
    - values까지 하고 뒤에 `ravel()` 붙이면 1차원 list로 return 해줌
- `df.copy()`
    - 기본적으로 딥카피(deep copy)를 수행
    - 이는 원본 DataFrame의 데이터를 모두 복사하여 새로운 객체를 생성하는 것입니다.
    - 원본 DataFrame과 복사된 DataFrame은 독립적으로 존재하며, 한쪽의 변경이 다른 쪽에 영향을 미치지 않습니다.
- `df.groupby('Page').mean().var()[0]`
    1. page 칼럼 값을 기준으로 그룹을 짓는다 
    2. 그룹별 평균을 낸다 → 이제 row는 그룹 개수
    3. 그룹 간 분산 수치를 구한다 
    4. var() method 실행 시 dtype이 같이 나오므로 앞의 수치만 가져온다 
- p값 구하기
    - `np.mean([var > observed_variance for var in perm_variance]))`
    - mean으로 주어진 list는 True, False 두 원소로 이루어져 있다
        - perm_variance의 원소 하나마다 `> observed_variance` 조건 체크
    - True는 1, False는 0이기 때문에 여기다가 mean을 내면 True가 나온 비율을 구할 수 있는 것
- statsmodels 패키지 라이브러리는 크게 두 개로 나뉨
    
    ```python
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    ```
    
    - `statsmodels.api` 기본 통계 모델링을 위한 함수와 클래스를 제공
        - NumPy 배열이나 Pandas 데이터프레임을 사용하여 모델을 정의
        - 다양한 데이터 구조에 유연하게 대응
    - `statsmodels.formula.api` R의 formula 인터페이스와 유사한 방식으로 통계 모델을 정의할 수 있는 기능을 제공합니다.
        - 가독성 중시, 데이터 프레임 많이 사용할 때
        - formula: 포뮬러는 종속 변수와 독립 변수 간의 관계를 문자열로 표현
            - 종속 변수 ~ 독립 변수1 + 독립 변수2 + …
            - `~` 기호: 종속 변수와 독립 변수 간의 관계
            - `+` 기호: 여러 독립 변수를 추가하는 데 사용
- `sm.OLS`(y, X)
    - OLS(Ordinary Least Squares) - 최소제곱법을 사용하여 선형 회귀 모델의 계수를 추정
    - 사용자가 상수 값을 가지는 칼럼(예: 값이 모두 1인 칼럼)을 추가하면, 그 칼럼의 계수를 절편으로 해석
    - 독립 변수 행렬에 절편 항을 명시적으로 추가해야 절편을 추정
        - `house[predictors].assign(const=1)`를 독립변수(두번째 parameter)로 준다고 하면, const 칼럼이 절편으로 들어감
        - 확실한지 모르겠으나 1을 주는 건 절편의 계수라서임. $\hat{b_0} \cdot 1$ 에서 1
- `pd.get_dummies(dataframe, drop_first=True)`
    - 범주형, 불 변수 칼럼에 대해 정수값으로 변환 (0/1)
    - 실수형 칼럼은 알아서 pass
        - 그래서 input에 df 자체를 줄 수 있는 것
    - 범주형 변수 변환 예시
        - 원래: Property_type의 unique value는 3개(multiplex, single family, town house)
        - get_dummies 변환 이후: PropertyType_Single Family, PropertyType_Townhouse 두 가지 칼럼이 추가로 생겨나고, 원래의 property_type 칼럼은 사라짐
    - drop_first = True
        - 다중공선성을 방지하기 위한 옵션
        - 범주형 변수에서 첫번째 카테고리는 별도의 칼럼으로 배정되지 않고 drop
        - property type이 세 가지이지만, 추가된 칼럼은 2개뿐
            
            
            | pt_single_family | pt_townhouse | original value |
            | --- | --- | --- |
            | 0 | 0 | multiplex |
            | 0 | 1 | town_house |
            | 1 | 0 | single_family |
    - chatGPT는 범주형에도 적용된다고 하는데, 막상 주피터 노트북 보면 범주형에는 적용이 안되어 있어서
        - 칼럼의 데이터 타입 변환 (column.astype(’int’) 해서 assign 해주거나
            
            ```python
            house['NewConstruction'] = house['NewConstruction'].astype(int).values
            ```
            
        - 정수로 변환한 별도의 리스트를 칼럼에 넣어주거나 해야 하는듯
            
            ```python
            house['NewConstruction'] = [1 if nc else 0 for nc in X['NewConstruction']]                        
            ```
            
- `groupby` → `apply(lambda x: ...)`
    - 여기서 x는 그룹키가 아니라! 그룹 키로 묶인 subdataframe 전체다!
- `pandas.core.series.Series`
    - 1차원 배열 (values) + 인덱스(index)
        - 시리즈 이름.values, 시리즈 이름.index로 각각 호출 가능
    - values가 1차원 배열이지만, 각 원소 자체는 dict일수도 있음
        
        ```python
        array([{'ZipCode': 98001, 'count': 358, 'median_residual': -125549.1294836502},
               {'ZipCode': 98002, 'count': 180, 'median_residual': -60076.24485961301}], dtype=object)
        ```
        
    - pd.DataFrame([*시리즈 이름])
        - [*시리즈] : 시리즈의 각 값(요소)을 순서대로 하나씩 꺼내어 리스트에 담는다 → list of dictionary
        - pd.DataFrame(list of dictionary) : dict의 각 키가 하나의 칼럼이 된다
- `pd.qcut`
    - 데이터를 분할할 때 값의 분포를 기반으로 구간을 분할
    - 각 구간은 데이터의 동일한 수의 항목을 포함하는 것이 이상적
    - parameters
        - labels
            - 각 구간에 레이블을 붙일지 여부를 결정합니다. False로 설정하면, 레이블 대신 구간의 인덱스(0부터 시작하는 정수)가 반환
        - retbins
            - 각 구간에 레이블을 붙일지 여부를 결정합니다. False로 설정하면, 레이블 대신 구간의 인덱스(0부터 시작하는 정수)가 반환
- [ ]  왜 누적합이 균등 분할에 활용되는지 모르겠다
- data type: category
    - 순서가 없는 범주형 데이터 타입
    - c.f. 순서가 있는 범주형 데이터로 변환하고 싶으면
        
        ```sql
        df['level'] = pd.Categorical(df['level'], categories=['저', '중', '고'], ordered=True)
        ```
        
- `from sklearn.linear_model import LinearRegression`
    - 모델 인스턴스 생성(class로 찍어놓기) → fit(train) → predict(test)
- `dataframe.loc`
    
    ```python
    df.loc[0] # 특정 행 선택
    df.loc[0, 'Name'] # 특정 행의 특정 열 선택. cell 값 선택
    df.loc[0:2] # 행 슬라이싱
    df.loc[df['Age'] >= 30] # 행 조건부 선택
    df.loc[0, 'Age'] = 29 # cell 값 설정 
    ```
    
- OLSInfluence 모듈
    - `from statsmodels.stats.outliers_influence import OLSInfluence`
    - OLS 회귀 모델 피팅 후, 각 데이터 포인트가 회귀 모델에 얼마나 영향을 미치는지 평가할 수 있는 다양한 진단 통계를 제공
    - 제공하는 통계치
        
        1.	**잔차(residuals)**: 관측된 값과 예측된 값의 차이.
        
        2.	**리버리지(hat matrix diagonal)**: 각 관측치의 리버리지 값을 계산하여, 관측치가 회귀 모델에 얼마나 영향을 미치는지 평가.
        
        3.	**Cook’s Distance**: 각 관측치가 전체 회귀 모델에 얼마나 영향을 미치는지 측정.
        
        4.	**DFBETAS**: 특정 관측치가 각 회귀 계수에 얼마나 영향을 미치는지 평가.
        
        5.	**DFFITS**: 특정 관측치가 전체 예측 값에 얼마나 영향을 미치는지 평가.
        
        6.	**Studentized Residuals**: 각 잔차를 표준화하여 비교.
        
- `sm.add_constant(X)`
    - statsmodels 라이브러리에서 회귀 모델을 피팅할 때 독립 변수 행렬 X에 상수항(절편, intercept)을 추가
    - 회귀 분석에서는 종속 변수와 독립 변수 간의 관계를 설명하기 위해 상수항이 필요
        - 상수항은 회귀 직선이 데이터의 중심을 더 잘 맞출 수 있게 해줌
    - **왜 상수항이 필요한가?**
        - **절편의 의미**:
            - 상수항(절편)은 독립 변수들의 값이 모두 0일 때 종속 변수의 예상 값을 나타냄
            - 절편이 없으면 회귀 직선은 원점을 통과해야만 하므로, 데이터의 특성에 맞지 않는 모델이 될 수 있음
    - **sm.add_constant 함수의 역할**
        - 주어진 데이터프레임이나 배열에 상수항을 추가
        - 새로운 열을 추가하여 그 열의 모든 값이 1이 되도록 합니다. 이 열은 회귀 분석에서 절편을 추정하는 데 사용됨