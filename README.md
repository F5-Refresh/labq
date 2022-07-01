# Lab-Q Django 실무과제

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
 ![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)
## 팀원 소개
- ### 🍺🍺***이동연***
- ### 🔥🔥***김동규***
- ### 🤘🤘***조병민***
- ### 😎😎***남효정***
- ### 😻😻***전기원***
 
## 프로젝트 소개

 
 본 서비스는 `한국시간`을 기준으로 현재시간에서 `1시간 전`의 `하수관로의 평균 수위와 총 강우량수치`의 정보를 제공하는 서비스입니다.  
 원하시는 `구`의 데이터를 PathParameter로 취득하여 그 `구`에 대한 정보를 제공합니다.

## 요구사항 및 해결방안

- 서울 열린데이터 광장의 하수관로, 강우량 OpenApi을 사용하여 데이터를 수집
  - 서울 열린데이터 광장 회원가입 및 OpenApi Key 취득
  - SamPle 데이터를 활용하여 OpenApi Path 취득
  - OpenApi 데이터 조사

- Open Api의 두 데이터를 결합한 데이터를 활용하여 Api작성
  - 구를 PathParameter로 받아 key값으로 활용
  - 하수관로 강우량정버는 구의 정보를 가지고 있으므로 구별로 GroupBy
  - 하수관로 데이터를 총합하여 평균치 측정
  - 강우량 데이터를 우량계 별 GroupBy
  - 각 우량계별 데이터를 파싱
  
- 요청에대한 응답은 Json형식으로 할 것
  - Json형식으로 응답

## 주요 기능 및 이유

- 현재시간에서 1시간 전의 시간을 기준으로 데이터를 제공 ex: 현재시각이 12:38일 경우 11:00 ~ 11:59까지의 데이터를 제공합니다.
  - 아래와 같은 이유로 1시간 전의 데이터의 평균 수위 및 평균 강우량을 나타내는형식이 안정적이라고 생각하였습니다. 
    - 하수관로Api에서는 시간별 데이터를 응답
    - 강우량Api는 시간별 데이터를 응답하지않음 

- 총 하수관로 평균 수위 및 각 우량계 별 강우량 데이터를 제공

## 실행 방법

1. 서버
```
pip install -r requirements.txt
python manage.py runserver
```
2. 테스트코드
```
python manage.py test
```

## API호출
1. 호출URL 
```GET api/seoul/gu-search/<구 이름(한글)>```
2. Response Data Frame
```
data: {
    gu_name: string                                   # xx구의 이름을 나타냅니다. ex: 종로구, 강남구 
    avg_water_level: float                            # 하수관수위의 평균치
    raingauge_info: [                                 # 우량계 별 정보
            {
                raingauge_name: string                # 우량계의 이름
                sum_rain_fall: float                  # 우량계의 측정된 강우량 수치
            }
            {
                raingauge_name: string               
                sum_rain_fall: float                 
            }
        ]
    }
}
```
