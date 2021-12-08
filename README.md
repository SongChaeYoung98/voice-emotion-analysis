# voice-emotion-analysis
목소리 속 감정을 파악하는 프로그램

## Language, Development tools
Python 3, Pycharm(Anaconda, Virtual Machine)

## Introduction
2020년 대한민국(남한)의 최저, 최고 기온 및 강수량을 기준으로 밀 경작 가능지를 판단 및 학습
기상청에서 공고한 미래의 기온 변화를 참고하여 2020년 기온에 ± α°C 를 하여 각각 2030, 2040년 기후 데이터 제작
2020년의 기상 데이터로 학습한 데이터를 2030, 2040년 데이터에 예측을 진행
(코드 구동에 필요한 데이터는 배포 권한이 없어 미 첨부)

## Configuration

- 기온 및 토양 분석 - 최종.ipynb : 2020 기준 학습 데이터 정확도 검증 및 테스트 / 2030, 2040 경작 가능지 최종 예측 (RandomForest 사용)
- 라벨링 - 강수량.ipynb : 시 군 단위로 나눈 지역 별 강수량 데이터를 기준으로 라벨링 진행
- 라벨링 - 기온.ipynb : 시 군 단위로 나눈 지역 별 최고, 최저 기온, 평균 기온 데이터를 기준으로 라벨링 진행
- 밀 재배지 예측-1.ipynb : 2020년 기준 밀 재배지 예측 및 학습된 데이터 구축
- 지역 별 데이터불러오기.ipynb : 지역 별로 나뉜 전국의 토양, 강수량, 기온 파일을 한 csv 파일로 가공 및 결측치 보정
- 최종 라벨링 : 각각 라벨링(재배 가능 여부 0, 1) 된 최저 최고 기온, 평균 기온, 강수량을 종합해 모든 라벨링 값을 더한 가중치 설정
(ex. 최저기온 부적절 = 0 / 최고기온 적절 = 1 / 평균기온 적절 = 1 / 강수량 적절 = 1 [최종 라벨링 : 3] // 숫자가 높을 수록 경작 가능지에 가까워짐)

##  Predictive accuracy
2020년 밀 재배 가능지 기준
- KNN : 0.9466521&nbsp;
- 교차검증 KNN : 0.9351228&nbsp;
- Decision Tree : 0.946652&nbsp;
- 교차검증 Decision Tree : 0.949659

## Result
- 2020년 밀 재배 가능지 학습용 최종 라벨링(가중치 적용) 결과
![2020년 가중 라벨링](https://user-images.githubusercontent.com/93585651/145029206-43a62ff8-31eb-4762-ada3-7e7f61b3531a.PNG)
![image](https://user-images.githubusercontent.com/93585651/145030093-7d4ef3a2-8def-45f6-8ffe-c87e51b7afe0.png)&nbsp;&nbsp;

- 2030년 밀 재배 가능지 예측 결과
![image](https://user-images.githubusercontent.com/93585651/145029704-3ead6aa3-8fd5-4598-baeb-468cda5e9558.png)
![image](https://user-images.githubusercontent.com/93585651/145029822-3c5beb4a-2039-4e0b-b875-baaa52b12746.png)&nbsp;&nbsp;

- 2040년 밀 재배 가능지 예측 결과 (부정확한 데이터 사용으로 신뢰도 낮음)
![image](https://user-images.githubusercontent.com/93585651/145030412-d3eb1c26-b2d7-4249-bc03-9f7f0795053c.png)
