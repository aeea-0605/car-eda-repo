# 수입중고차 EDA Project
---
## 1. 개요
<br/>

### 1-1. 프로젝트 목적
수입중고차 판매, 네이버 트랜드, TV광고 시청률 데이터를 통해 광고주 및 퍼블러셔에게 브랜드 및 모델에 대한 소비자의 선호도 및 광고 cost 대비 시청률 등에 대한 정보를 제공해 중고차 모델 선정 및 효과적인 디지털 마케팅을 할 수 있게 합니다.

### 1-2. 프로젝트 목표
데이터를 DB를 통해 관리하고 SQL을 통해 분석에 필요한 format의 데이터셋을 추출하여 EDA를 진행합니다. <br/>
디지털 마케팅에서 사용되는 시각화 방법들을 사용해 광고주를 타게팅한 데이터 분석을 진행합니다.

### 1-3. 기술적 목표
- 모듈파일을 통한 함수 코드 관리 및 코드의 효율성 추구
- data.ini 파일을 통한 hide variable
- SqlAlchemy를 통해 데이터 추출 및 적재
- Input data로 특정 브랜드를 입력하면 해당 브랜드에 대한 Visualization Report 작성

### 1-4. 데이터셋 및 설명
- 데이터셋 : 프로젝트 진행 기준 2021년 5월까지의 데이터만 존재
    - 수입중고차 판매 데이터 : [한국 수입자동차 협회](https://www.kaida.co.kr/)
    - 네이버 트랜드 : [네이버 검색어 트랜드](https://datalab.naver.com/keyword/trendSearch.naver)
    - TV광고 시청률 데이터 : 특정 기업 제공 데이터

<br/>

---
---

## 2. 결과

### 특정 타겟 (Mercedes-Benz) 에 대한 종합적인 해석 및 결과
```
- 벤츠에 대한 대중들의 관심도가 전년대비 증가하고 판매량, GRP 관점에서 바라봤을 때 벤츠의 성장성은 꾸준히 증가하고 있다.

- 벤츠의 인기 모델은 E250, E350, GLE450이며 주요 고객층은 30대 남성(16%), 40대 여성(13.3%)이다.

- 주요 고객층의 차종 선호도는 세단이며, 선호 Segment는 준대형이다. 

- 벤츠의 광고 시청률은 남성보다 여성이 높으며 세부적으로는 50대 여성, 40대 여성, 60대 남성 순으로 많이 시청한다. 
  ABC 분석을 통해 40-60대의 연령층이 전체 시청률의 80%를 차지한다는 것을 알 수 있다.

```
**시청률과 판매량에 대한 전환율 기준으로 바라보았을 때 벤츠 광고주는 30-40대를 타게팅하여 광고를 제작해야하며, 시청률이 높은 40-60대 연령층을 어떻게 하면 주요 고객으로 이끌지에 대한 마케팅적인 고민을 해야한다.**

<br/>

### **Visualization**
****
<img width="330" alt="스크린샷 2021-07-28 오후 10 07 19" src="https://user-images.githubusercontent.com/80459520/127327421-bd0df3bf-ea72-4e5f-9686-6c0e92e3ed6a.png">

벤츠는 4월 기준 두번째로 시장점유율이 높은 해외 브랜드임을 알 수 있다.

<br/>

**<Page 1>**
<img width="1144" alt="car_view_1" src="https://user-images.githubusercontent.com/80459520/125198348-83445080-e29c-11eb-9653-3ad1922b8ac0.png">

- 당월 벤츠는 E250, E350, GLE450 모델이 가장 많이 팔렸다.
- 구매자 성비는 남자, 여자, 법인이 각각 45.1%, 41.8%, 13.1%로 남성, 여성 고르게 선호한다고 볼 수 있으며 30-50대의 연령대가 주로 구매한다.
- 차종 선호도에 있어 40대 여성은 세단, 30대 남성 또한 세단을 주로 선호한다고 볼 수 있다.

**인사이트 : 벤츠에서 인기 있는 모델은 E250, E350, GLE450이며, 주요 고객은 30대 남성(16%), 40대 여성(13.3%)이다. 차종 선호도는 주요 고객 모두 세단이라고 할 수 있다.**

<br/>

**<Page 2>**
<img width="1147" alt="car_view_2" src="https://user-images.githubusercontent.com/80459520/125198385-99eaa780-e29c-11eb-9ba3-2f52ee473ea9.png">

- 성별의 연령대별 선호 segment를 통해 주요 고객들은 모두 준대형을 선호한다.
- 벤츠의 z-chart를 통해 최근 1년간 특별한 이슈없이 무난한 성장을 보이고 있다는 것을 알 수 있다.
- TV 시청률 Audience GRP를 보면 시청자들의 벤츠 선호도가 매년 증가한다는 것을 알 수 있다.
- 전년동기 전월 및 전년대비의 네이버 검색량을 보면 3월보다 감소했지만 작년보단 증가했다는 것을 알 수 있다.

**인사이트 : 주요 고객층은 벤츠의 준대형 차종을 선호한다. 판매량, GRP관점에서 벤츠의 성장성은 꾸준히 증가한다는 것을 알 수 있다. 네이터 검색량을 통한 벤츠에 대한 고객들의 관심도 또한 전월대비는 감소했다고 볼 수 있지만 작년과 비교했을 때에는 증가했다고 볼 수 있다.**

<br/>

**<Page 3>**
<img width="1145" alt="car_view_3" src="https://user-images.githubusercontent.com/80459520/125198393-a4a53c80-e29c-11eb-80e3-aefb6016e73c.png">

- 나이/성별에 따른 시청자의 구성은 대체적으로 모든 연령대에서 여성을 비율이 높으며 40-50대가 많은 시청을 한다는 것을 알 수 있다.
- 그 중 50대 여성, 40대 여성, 60대 남성 순으로 시청률이 높다는 것을 알 수 있다.
- 연령대 기준 ABC Chart를 통해 40-60대의 연령층이 시청률의 80%를 담당한다는 것을 알 수 있다.

**인사이트 : 여성들의 벤츠 광고를 많이 보며 개별적으로는 50대, 40대 여성, 60대 남성 순으로 많이 시청한다는 것을 알 수 있다. 또한 40-60대의 연령층이 전체 시청률의 80%를 담당한다는 것을 알 수 있다.**

<br/>

---
---

## 3. 과정

### 3-1. 분석에 필요한 데이터셋 추출 후 csv 파일로 저장
!["extract_data.png"](https://user-images.githubusercontent.com/80459520/125197082-47f35300-e297-11eb-8dde-f1beda0bb3de.png)
- data.ini 파일을 통한 hide variable
- SqlAlchemy로 DB와 세션 연결 후 pandas를 통해 데이터프레임화
- 분석하기 위해 csv파일로 변환

<br/>

### 3-2 분석할 타겟 브랜드 설명 및 모듈 import
```
from EDA_module import *

# 타겟 브랜드의 한글명, 영문명 정의
target_brand_eng = "Mercedes-Benz"
target_brand_kor = "메르세데스벤츠코리아"
```

<br/>

### 3-3 Visualization Code Summary
```
# target brand에 대한 시각화 코드
# 4월 등록(판매)대수
sales_month(target_brand_eng, "2021-04")

# 상위 5개 브랜드의 시장 점유율 pie chart
pie_major(2021,4,)

# 4월 상위 3개 모델 bar chart
month_top3(2021, 4, target_brand_eng)

# 4월 소비자 성비 pie chart
sales_type(target_brand_eng,'2021-04')

# 4월 성별 연령대별 소비자 비율 bar chart
sales_age(target_brand_eng,'2021-04')

# 2021년 주요 고객 연령층(남-40, 여-30)의 차종 선호도 비율 bar chart
segment_preference(target_brand_eng,2021,40,'개인-여자')
segment_preference(target_brand_eng,2021,30,'개인-남자')

# 주요 고객층의 선호 segment 비율 bar chart
customer_preference(target_brand_eng,'개인-남자','segment',categorical)
customer_preference(target_brand_eng,'개인-여자','segment',categorical)

# 최근 12개월에 대한 Z-chart
make_z_chart(target_brand_eng, "2021-05")

# 4월 기준 전월대비, 전년대비 네이터 검색어 트랜드 bar chart
query_compare(2021, 4, target_brand_eng)

# Audience, GRP 추이 그래프
yearly_plot(target_brand_kor)

# 나이/성별에 따른 시청자 성비 bar chart
aud_ratio(target_brand_kor)

# 연령대 기준 Audience ABC chart
aud_ABC(target_brand_kor)
```

<br/>

---
---

<br/>

# 💡 제언
- 분석 대상에 대한 명확한 분석 목표를 갖고 목표지향적으로 집요하게 데이터를 바라보고 분석하는 습관이 중요하다는 것을 알았습니다.
- 분석결과에 대해 사용자 관점에서 어떠한 성과를 낼 수 있는지 끊임 없는 고민이 필요하다는 것을 알 수 있었고, 결과에 대한 오류가 존재하여 잘못된 해석을 하진 않았는지에 대한 계속된 고찰이 중요한 부분이라는 것을 느꼈습니다.

<br/>

# Code Explanation

> 특정 타겟에 대한 Visualization Note : [RESULT_REPORT.ipynb](https://github.com/aeea-0605/car-eda-repo/blob/main/RESULT_REPORT.ipynb)

> 시각화를 위한 변수 및 함수가 있는 모듈파일 : [EDA_module.py](https://github.com/aeea-0605/car-eda-repo/blob/main/EDA_module.py)

> SqlAlchemy와 pandas를 이용한 분석을 위한 데이터 추출 : [extract_data.py](https://github.com/aeea-0605/car-eda-repo/blob/main/extract_data.py)