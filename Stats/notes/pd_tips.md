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
    - get_dummies 전후 칼럼 수 어떻게 변하는지 확인하기
        1. 범주형 칼럼 개수 확인 
            
            `df.select_dtypes(include=['object', 'category']).columns`
            
        2. 범주형 칼럼마다  고유한 값의 개수를 계산 (요인 수준 개수 확인)
            
            `{col: test_df[col].nunique() for col in categorical_columns}`
            
            - 여기서 주의할 점! 다중공선성 문제 해결 위해 각 칼럼에서 파생되는 더미 칼럼 개수는 실제 요인 수준 개수 - 1임!!
        3. `원래 df의 칼럼 개수 - 범주형 칼럼 개수 + (범주형 칼럼의 요인 수준 개수 합 - 범주형 칼럼 개수)`가 get_dummies 이후의 칼럼 개수 
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
    df.loc[0:0, column_list] # 0번째 행만 특정 칼럼들
    ```
    
    - pandas의 df.loc에서 [a:b, :]를 사용할 때, a부터 b까지의 행은 둘 다 포함
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
- `colname.cat`
    - 범주형 칼럼인 경우 저 뒤에 다양한 method를 붙여서 범주에 대한 정보를 얻을 수 있다
- `from sklearn.linear_model import LogisticRegression`
    - 모델 클래스 하나 찍어내기 → fit(X, y)
    - → `modelname.predict_log_proba(X)`
        - 각 데이터 포인트에 대해 각 클래스에 속할 로그 확률을 반환
        - 확률이 매우 작을 때 로그 확률을 사용하면 계산 안정성이 증가
        - 0과 1 사이의 값을 가진 확률이 로그를 만나면 음수가 된다
    - [ ]  `predict_proba(X)`
        - [ ]  차원
    - `full_model.fit(X, y, sample_weight=wt)`
        - weight로 데이터별 가중치 조정
    - `predict(X)`
        - 이진분류모델이라 이름은 regression이지만 label을 예측한다
- Y 칼럼을 그냥 범주가 아닌 순서형 범주로 변환해야 하는 경우
    
    ```python
    from sklearn.preprocessing import OrdinalEncoder
    # 순서형 인코더 클래스 인스턴스 생성
    enc = OrdinalEncoder(categories=[['paid off', 'default']])
    # 위에서 찍어낸 인코더 이용해서 y 칼럼 변환 
    y_enc = enc.fit_transform(loan_data[[outcome]]).ravel()
    
    logit_reg_enc = LogisticRegression(penalty="l2", C=1e42, solver='liblinear')
    # 로지스틱 회귀 할 때도 변환된 y가 들어간다 
    logit_reg_enc.fit(X, y_enc)
    
    print('intercept ', logit_reg_enc.intercept_[0])
    print('classes', logit_reg_enc.classes_)
    pd.DataFrame({'coeff': logit_reg_enc.coef_[0]}, 
                 index=X.columns) 
    ```
    
- `colname.ravel()`
    - 다차원 배열을 1차원 배열로 변환
- `precision_recall_fscore_support(y, logit_reg.predict(X), labels=['default', 'paid_off'])`
    - 에러 발생
        
        ```
        /opt/anaconda3/envs/ml/lib/python3.9/site-packages/sklearn/metrics/_classification.py:1334: UndefinedMetricWarning: Precision and F-score are ill-defined and being set to 0.0 in labels with no predicted samples. Use `zero_division` parameter to control this behavior.
          _warn_prf(average, modifier, msg_start, len(result))
        ```
        
    - predict한 label이랑 parameter labels에 들어가 있는 것들이랑 같은지 확인
        - np.unique(pred)로 확인하고 labels 파라미터 수정해주면 에러 안남
- `from sklearn.metrics import roc_curve, accuracy_score, roc_auc_score`
    - [ ]  파라미터
- column indexing output 차이
    - df[col]: 시리즈 vs. df[ `[col]`] : 데이터 프레임
- [ ]  SMOTE 알고리즘 체크
    - [ ]  from imblearn.over_sampling import SMOTE, ADASYN
    - [ ]  X_resampled, y_resampled = SMOTE().fit_resample(X, y)
    - [ ]  ADASYN().fit_resample(X, y)
- `np.meshgrid(x, y)`
    - 두 개의 1차원 배열을 입력 받아 두 배열의 모든 조합을 포함하는 2차원 행렬을 반환
    - 주로 그리드 생성이나 표면 플롯에 사용
- `np.argmax`
    - 동일한 최대값이 여러 개 있을 경우, 가장 먼저 나타나는 인덱스를 반환
- 🪐 jupyter tip
    - 주피터 노트북 커널이 뭐뭐 있는지 확인
        - jupyter kernelspec list
    - 커널별 연동되어 있는 콘다 환경이 뭔지 확인
        - 위의 리스트에 나와있는 커널 경로로 이동
        - kernel.json 파일 확인 - argv에 나와 있는 python 실행 파일 경로 보고 확인 가능
    - /opt/anaconda3/share/jupyter/kernels → /opt/anaconda3/bin/python
        - conda base 환경에서 돌아간다는 커널 의미
    - conda  환경에 뭐 깔려고 하면 자꾸 unicode error 났음
        - 범인은 zsh theme 때문에 적용된 X 특수문자 마크 https://github.com/conda/conda/issues/3982#issuecomment-425672922
        
        ![Untitled](pd_tips%20d34d06eeb66c4f048cccdc07c96ee7ef/Untitled.png)
        
- `from sklearn import preprocessing`
    - `preprocessing.StandardScaler()`
        - `scaler.fit(X * 1.0)`
            - X의 모든 칼럼을 float 타입으로 바꿔서 계산의 정확도를 높이고자 함
            - 데이터의 평균과 표준 편차를 구하여 스케일러에 저장
        - `scaler.transform(X * 1.0)`
            - 여기서도 X의 모든 칼럼을 float으로 바꿈
            - fit 메서드에서 계산된 평균과 표준 편차를 사용하여 데이터를 변환
- `from sklearn.tree import DecisionTreeClassifier`
    - `loan_tree = DecisionTreeClassifier(random_state=1, criterion='entropy', min_impurity_decrease=0.003)`
        - random_state : 결과의 재현성을 위해 난수 시드를 설정
            - 트리의 특정 노드에서 여러 분할 후보가 동일한 불순도 감소를 제공할 때, 어느 분할을 선택할지 랜덤하게 결정되기 때문에
        - criterion: 노드 분할 기준 지표
            - gini 옵션도 선택 가능
        - min_impurity_decrease
    - tree 시각화 하려면 graphViz conda에 깔아야 함
        - `plotDecisionTree`
- `from sklearn.ensemble import RandomForestClassifier`
    - `rf = RandomForestClassifier(n_estimators=500, random_state=1, oob_score=True)`
        - n_estimators: 생성할 의사결정 트리의 개수를 지정
            - 커질 수록 성능, 계산 비용 증가
        - random_state
            - 여기서는 칼럼도 랜덤으로 선택하기 때문에 난수 고정 필요
        - oob_score
            - OOB(Out-Of-Bag) 샘플을 사용하여 모델을 평가할지 여부를 설정
                - 트리 모델을 만들 때 사용했던 학습 데이터에 속하지 않는 데이터
            - oob_score=True로 설정하면 모델이 학습된 후 OOB 샘플을 사용하여 성능 점수를 계산
            - c.f. 통계적으로, 원본 데이터셋의 약 63.2%의 샘플만이 부트스트랩 샘플에 포함되며, 나머지 약 36.8%의 샘플은 포함되지 않게 되어 OOB 샘플로 남습니다.
- ax = df.plot(kind = `barh` , x='feature', y='Accuracy decrease', legend=False, ax=axes[0])
    - x, y축이 바뀐다