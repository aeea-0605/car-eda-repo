# 수입중고차 EDA Project


### data.ini를 통해 정보 숨김 및 DB와 세션 연결후 데이터 추출 > csv파일로 저장
!["extract_data.png"](https://user-images.githubusercontent.com/80459520/125197082-47f35300-e297-11eb-8dde-f1beda0bb3de.png)

### 타겟 브랜드 설정 및 모듈 불러오기

```
from EDA_module import *


target_brand_eng = "Mercedes-Benz"
target_brand_kor = "메르세데스벤츠코리아"
```

### 특정 타겟에 대한 Visualization

<img width="1144" alt="car_view_1" src="https://user-images.githubusercontent.com/80459520/125198348-83445080-e29c-11eb-9653-3ad1922b8ac0.png">

<img width="1147" alt="car_view_2" src="https://user-images.githubusercontent.com/80459520/125198385-99eaa780-e29c-11eb-9ba3-2f52ee473ea9.png">

<img width="1145" alt="car_view_3" src="https://user-images.githubusercontent.com/80459520/125198393-a4a53c80-e29c-11eb-80e3-aefb6016e73c.png">


<br/>

자세한 EDA 과정 : [RESULT_REPORT.ipynb](https://github.com/aeea-0605/car-eda-repo/blob/main/RESULT_REPORT.ipynb)

전처리 함수 및 시각화 함수, 데이터셋 관리 모듈 : [EDA_module.py](https://github.com/aeea-0605/car-eda-repo/blob/main/EDA_module.py)
