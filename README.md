# Snack Server

데이터메이커 구성원이 사용하는 간식 주문 App 을 위한 Backend API Server

# Project Settings

해당 프로젝트는 [Poetry](https://python-poetry.org/) 를 사용하여 패키징 되었다. 하기 Docker Container 에서도 poetry 를 그대로 사용한다. 모든 세팅은 `pyproject.toml` 에 기록되어 있으며 poetry 로 initialize 할 수 있다.

```shell
> poetry install
```

또한 별도 가상환경을 사용하지 않고 poetry 가 제공하는 가상환경을 사용하게 되는데 `activate` 방법은 아래와 같다.

```shell
> poetry shell
```

Python 을 통해 실행하는 모든 명령어는 가상환경을 activate 하지 않아도 아래와 같이 사용 가능하다.

```shell
> poetry run pytest --pdb
```

# Installation

아래의 과정을 통해 로컬 환경을 세팅합니다.

## .env

`.env.docker-compose.template` 파일을 복사해 `.env.docker-compose` 파일을 생성한 후 아래 내용을 작성합니다.

```
DB_VERSION=16.1
DB_DATABASE_NAME=snack
DB_USERNAME=snack
DB_PASSWORD=
DB_DIR=
```

- DB_DIR: postgres 컨테이너를 사용 시 컨테이너를 삭제하면 DB 내용이 삭제됩니다. 이에 local volume 과 연결하여 데이터 파일을 별도 저장하면 컨테이너가 삭제 되더라도 데이터를 유지할 수 있습니다.

## Docker Compose

개발환경은 Docker 및 Docker Compose 를 이용해 구성했습니다. 아래의 과정을 통해 이미지를 빌드하고 Docker container 를 실행합니다. 자세한 내용은 Makefile 을 살펴보면 조회할 수 있습니다.

### 빌드 및 실행

최초 실행 혹은 requirements 에 패키지가 추가된 경우 재빌드 합니다.

```
> make build
> make logs
```

### 단순 실행

보통의 경우 컨테이너를 단순 실행하여 개발서버를 구동합니다.

```
> make up
> make logs
```

### 컨테이너 재실행

컨테이너 재실행이 필요한 경우 아래와 같이 수행합니다. 전체 컨테이너 재실행이 필요한 경우 아래와 같습니다.

```
> make down
> make up
```

특정 컨테이너만 재실행 할 경우 아래와 같습니다.

```
> make restart CONTAINER=snack-server
```

# RESTAPI Convention

RESTful 개념은 이미 논문 제시된 개념이며, 이를 해석하여 Convention 들이 제시되고 있다. 그 중 아래의 Best Practice 를 참고할까 한다. 

REST API 의 Best Practice 는 프로젝트 마다 다양하게 변형될 수 있으며, 원 창안자가 제시한 개념을 단일 Best Practice 가 모두 담기도 어렵다. 

- 활발하게 discussion 및 revise 가 이루어 지고 있으며
- 반응이 비교적 좋은 Practice 라고 판단되는 아래 내용을 참조하려 한다.
- [Lokesh Gupta's Convention](https://restfulapi.net/resource-naming/)
- `Do not use trailing slash` 같은 rule 은 Django 에 적용할 수 없으니 무시한다.
- 모든 API 는 Endpoint 까지만 정의하고 나머지는 drf-spectacular 의 문서를 활용한다.

## Simple JWT

### Get Access Token

```text
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "davidattenborough", "password": "boatymcboatface"}' \
  http://localhost:8000/auth/token/

...
{
  "access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNDU2LCJqdGkiOiJmZDJmOWQ1ZTFhN2M0MmU4OTQ5MzVlMzYyYmNhOGJjYSJ9.NHlztMGER7UADHZJlxNG0WSi22a2KaYSfd1S-AuT7lU",
  "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"
}
```

### Refresh Access Token

```text
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImNvbGRfc3R1ZmYiOiLimIMiLCJleHAiOjIzNDU2NywianRpIjoiZGUxMmY0ZTY3MDY4NDI3ODg5ZjE1YWMyNzcwZGEwNTEifQ.aEoAYkSJjoWH1boshQAaTkf8G3yn0kapko6HFRt7Rh4"}' \
  http://localhost:8000/auth/token/refresh/

...
{"access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3BrIjoxLCJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiY29sZF9zdHVmZiI6IuKYgyIsImV4cCI6MTIzNTY3LCJqdGkiOiJjNzE4ZTVkNjgzZWQ0NTQyYTU0NWJkM2VmMGI0ZGQ0ZSJ9.ekxRxgb9OKmHkfy-zs1Ro_xs1eMLXiR17dIDBVxeT-w"}
```

## Order APIs

간식 주문 관련 APIs

### GET 간식 주문 목록

```text
GET /orders/
```

### PUT 간식 주문 상태 업데이트

```text
GET /order/<str:order_uid>/
```

### POST 간식 주문

```text
POST /order/
```

## Snack APIs

간식 관련 APIs

### GET 간식 목록

```text
GET /snacks/
```

# Permission

시스템 사용자의 권한을 설정하고 역할 별 제한사항을 설정합니다.

## 구성요소

Permission 구성 요소는 아래와 같습니다. 등급 별 권한이 상이합니다.

- 일반회원 (member)
- 관리자 (admin)

## member permissions

- 선택 가능한 간식 목록 조회
- 주문 목록 조회
- 간식 주문

## manager permissions

- member 의 모든 권한
- 주문 상태 변경

# Stack

## Backend

- Python==3.11.7
- Django==4.2.9
- Postgres==16.1

## Frontend

- Vue3

# Spec

## APIs

### requirements

- DRF 를 사용해 RESTAPI 를 제공한다.
- drf-spectacular 를 이용해 OpenAPI format 과 SwaggerUI 로 API 문서를 제공한다.

## Authentication

### requirements

- 회원가입할 때 `이메일(아이디), 비밀번호, 이름` 만 받습니다 .
- 회원은 일반 회원과 관리자로 나뉩니다.
- 관리자가 회원을 관리하는 목록이 존재하고, 회원을 관리자로 변경이 가능합니다.
- 회원 탈퇴가 가능하고, 가입할 때 탈퇴한 회원의 이메일로는 가입할 수 없습니다.

### UIs 

- Sign up 
- Sign in
- User list

## Order App

### requirements

- `이름, 이미지, 구매 URL, 설명` 을 입력할 수 있는 게시판
- 목록만 에서 모든 필드와 상태 확인 가능
- 관리자는 게시판에서 주문상태 변경
- 주문상태 변경할 시 예상 사용 일시 입력해야 함 (어떤 예상 사용 일시? 실제 소비할 수 있는 날자?)
- 월별 별도 목록 필요
- 한번 등록된 간식은 추후 선택 가능 (간식 요청 모델과 간식 모델의 관계 지정을 통한 구현 필요)
- 대기중 일 때만 수정 가능 - 배송 대기중? 주문 대기중? 생성 후 주문 전 (before status ordered)
- 같은 간식을 중복 신청할 수 없다. - 기준은? 한번 주문할 때
- 신청된 간식에 좋아요/싫어요를 선택 가능
- 좋아요/싫어요 비율에 따라 우선순위 조정
- 싫어요가 좋아요보다 많으면, 간식신청의 주문상태를 주문완료로 바꿀 수 없다.

> 간식을 구별하는 유일값은 간식의 이름이다.

### UIs

- Order list
- Snack list
- Order snack

# Business Processes 

본 프로젝트에서 사용되는 Business Processes 를 정의합니다.

## 페이지 목록

- 회원 가입 페이지
- 로그인 페이지
- 주문 목록 페이지
- 간식 목록 페이지
  - 관리자는 간식 상태 변경
- 통계 페이지

## Authentication Flow

```mermaid
---
title: 프로젝트 Business Process Flow
---
flowchart TD
  signup[회원 가입 페이지]
  login[로그인 페이지]
  orderlist[주문 목록 페이지]

  signup --> |가입 성공| login
  signup --> |가입 실패| signup
  login --> |로그인 성공| orderlist
  orderlist --> |로그아웃 성공| login
```

## Snack Management Flow

```mermaid
---
title: 프로젝트 Business Process Flow
---
flowchart TD
    orderlist[주문 목록 페이지]
    snacklist[간식 목록 페이지]
    registersnack[간식 등록 페이지 or 모달]
    registerprocess{간식 등록 프로세스 실행}
    
    orderlist --> |등록된 간식 목록 조회| snacklist
    snacklist --> |주문 목록 조회| orderlist
    snacklist --> |신규 간식 등록|registersnack
    registersnack --> |간식 정보 submit|registerprocess
    registerprocess --> |등록 성공| snacklist
    registerprocess --> |등록 실패| registersnack
```

## Order Management Flow

```mermaid
---
title: 프로젝트 Business Process Flow
---
flowchart TD
    orderlist[주문 목록 페이지]
    orderdetail[주문 상세 페이지]
    ordersnack[간식 주문 페이지 or 모달]
    orderprocess{간식 주문 프로세스 실행}
    
    orderlist --> |특정 주문 상세정보 확인| orderdetail
    orderdetail --> |주문 목록 조회| orderlist
    orderlist --> |간식 주문 버튼 클릭| ordersnack
    ordersnack --> |원하는 간식 및 수량 등을 선택 후 주문| orderprocess
    orderprocess --> |주문 성공| orderdetail
    orderprocess --> |주문 실패| ordersnack
```

## Resign Management

- 사용자는 시스템을 탈퇴할 수 있다.
- 탈퇴 버튼 위치는 sign-out 우측이다.
- 탈퇴 시 정말 탈퇴할지 한번 더 확인한다.
- 탈퇴에 성공하게 되면 시스템의 store.auth 를 비운다.
- 탈퇴 시 서버에서는 사용자 정보를 지우지 않고 is_deleted flag 만 True 처리 한다.
- 이후 재가입 시도 시 탈퇴한 사용자는 재가입이 불가능하다고 안내한다.
- 시스템에 ADMIN 이 본인 1명밖에 없으면 탈퇴할 수 없다.

## Order Status Flow

주문 상태의 구성과 플로우는 아래와 같다.

- created:생성됨
- ordered:주문 완료
- canceled:취소됨
- approved:승인됨
- shipping:배송중
- completed:완료

```mermaid
---
title: 주문 상태 Flow
---
flowchart TD
  created[created]
  ordered[ordered]
  canceled[canceled]
  approved[approved]
  shipping[shipping]
  completed[completed]
  
  approved --> |주문 작성 완료 및 주문| ordered 
  created --> |간식 승인| approved
  ordered --> |배송 시작 처리, 예상 도착 일시 입력| shipping
  shipping--> |간식 배송 완료| completed
  created --> |주문 취소| canceled
  approved --> |주문 취소| canceled
```

### 주문 생성 시 제약조건

- 주문 대기중 상태에서만 주문 수정 가능
- 아직 주문되지 않은 간식 중 신청된 간식이 있는 경우 중복 신청 할 수 없다.
- `싫어요가 좋아요보다 많으면, 간식신청의 주문상태를 주문완료로 바꿀 수 없다.` -> 이 항목은 아래와 같이 유의 해석함.
  - like_ratio < 1
  - 관리자가 해당 주문을 승인하고 주문함
  - 따라서 승인 시점에 좋아요/싫어요 비율을 측정하는 것이 `선호도가 낮은 간식은 주문하지 않는다` 라는 전제를 가장 만족한다고 본다.
  - 승인 이후 주문됨, 배송중, 완료 시점에는 이미 되돌릴 수 없기 때문이다.
   
### Strict State Flow 구현

말그대로 Flow 는 단계를 건너뛰거나 다음 단계로 갈 수 없는 등 오류가 없어야 한다. 더 적은 코드로 적은 오류를 발생시키고 고가용성을 발휘하도록 상태 흐름을 구현한다.

- Order models 의 Mixin 을 별도로 추가하고 상태를 변경하는 메소드를 지원한다.
- 이외 `직접 업데이트` 등의 방법으로 상태 변경을 금지한다.

### 주문 상태 별 변경 조건 체크

- 예상 도착 일시는 ordered, shipping 에서만 필요하며 업데이트 된다.
- created -> approved, approved -> ordered 변경 시 주문에 포함된 간식 중 `hate > like` 인 간식이 한개라도 있다면 변경 실패처리 한다.
- 현재 신청하려는 간식 중 아직 주문 (배송중 이상) 되지 않은 간식이 있다면 신청할 수 없다.

### UI

- Order List Page 에서 상태를 변경하도록 한다. -> 필드를 추가하고 status dropdown, arrive_estimate_date 를 위한 input 도 추가한다.
- 변경 시 예상 도착일 (예상 사용일) 을 같이 입력하도록 UI 를 구성한다.

## Reaction Management

### 정책 

- 개별 Snack model 은 ForeignKey 연결된 SnackReaction Model 에 like, hate 반응을 기록한다.
- 사용자는 단일 Snack 에 1개의 reaction 을 남길 수 있다.
  - 1번 사용자는 A 스낵에 like 를 남길 수 있다.
  - 1번 사용자는 A 스낵에 like 과 hate 를 동시에 남길 수 없다.
- 사용자는 자신이 남긴 reaction 을 취소할 수 있다.
  - 1번 사용자는 A 스낵에 남긴 hate 를 남긴 후 like 로 변경하고자 한다.
  - 이때 1번 사용자가 A 스낵의 hate 를 누르면 "중복해서 reaction 을 남길 수 없다." 는 메시지를 보게 된다.
  - 1번 사용자는 A 스낵의 like 를 누른다. 
  - snack, user 에 대응하는 reation 을 get_or_create 하여 get 인 경우 해당 type 으로 업데이트 한다.
  - Front 에서 업데이트 할 수 있도록 수량을 제공한다.
- 간식 별 수량 집계가 수월해야 한다.
  - type 별 수량
  - type 간 비율

### 설계 주의점

- 수량 및 비율 집계는 SQL Query 집계 시 온전한 성능을 발휘하기 어렵다.
  - 최대한 즉각 반영 되면서 중복문제가 없도록 구현 필요
  - 수량, 비율 등 집계 지표로 정렬이 가능해야 한다.
  - 1차: Celery 연동으로 통계용 필드 업데이트 담당(Order 의 통계용 필드들), 즉각 response 해야하는 부분은 바로 db 참조 (SnackReaction)
  - 2차: Redis cache 를 사용하여 업데이트 -> 속도 증가 차원

### 제약조건

- 간식 목록은 좋아요/싫어요 비율이 정렬의 기준이 된다. 해설하면 아래와 같다.
  - 전제: 싫어요 대비 좋아요 비율을 기준으로 상위 노출되어야 한다.
  - 좋아요/싫어요 개수가 7/3 인 간식 A와
  - 60/40 인 간식 B가 있을 때
  - A 의 비율은 7/3 = 2.3333
  - B 의 비율은 60/40 = 1.5
  - 이므로 A 가 B 보다 상위노출 되어야 한다.

### 아키텍처

```mermaid
---
title: Reaction 집계 Flow with One2Many Table
---
flowchart TD
  user[User]
  reaction_api[Reaction API]
  reaction_db[Reaction Table]
 
  user --> |좋아요 클릭| reaction_api
  reaction_api --> |Reaction 기록 get and update or create| reaction_db
  reaction_api --> |Reaction 반영 결과 제공| user
```

```mermaid
---
title: Reaction 집계 Flow with Celery Worker 
---
flowchart TD
  user[User]
  reaction_api[Reaction API]
  snack_api[Snack API]
  statistics_api[Statistics API]
  statistics_db[Order Table Statistics Field]
  reaction_db[Reaction Table]
  celery_task[Celery Reaction Task]
  celery_redis[Celery Worker with Redis]

  user --> |좋아요 클릭| reaction_api
  reaction_api --> |통계 테이블 업데이트 요청| celery_task
  celery_task --> |큐를 거쳐 통계 수치 계산| celery_redis
  celery_redis --> |통계 수치 업데이트| statistics_db
  user --> |통계 수치 요청| statistics_api
  statistics_api --> |통계 수치 쿼리| statistics_db
  statistics_db --> |통계 수치 제공| statistics_api
  statistics_api --> |통계 수치 응답| user
  snack_api --> |통계 수치 쿼리| statistics_db
  statistics_db --> |통계 수치 제공| snack_api
  user --> |간식 정보 요청| snack_api
  snack_api --> |통계 수치 포함된 간식 정보 응답| user
```

## Snacks in Order Management

현재 Order 에 속한 Snacks (주문에 포함된 간식) 의 Reaction, 수량 등 다양한 수치가 존재한다. Order 와 연관되어 관리해야하는 로직이 다양하게 발생할 수 있다. 관련된 정책은 아래와 같다.

- 현재 신청하려는 간식 중 `기존 주문 중` 아직 주문 (배송중 이상) 되지 않은 간식이 있다면 신청할 수 없다.

이를 원활하게 처리하기위해 아래의 방안을 고려한다. 

- Order 에 담긴 Snacks 처리 용 Model Mixin
- Order 에 담긴 Snacks 필터링 용 Model Queryset(Manager)
- Order 별 Snack 을 별도 API 로 제공

### 현재 신청하려는 간식 중 `기존 주문 중` 아직 주문 (배송중 이상) 되지 않은 간식이 있다면 신청할 수 없다.

- Create Order API Request
- not_delivered order 에 속한 간식 탐색
- 현재 신청한 간식 중 위와 중복되는 간식이 존재한다면
- 주문 반려

```mermaid
---
title: 간식 주문 시 중복 간식 검사 시퀀스
---
sequenceDiagram
    participant U as User
    participant COA as Create Order API View
    participant S as Order Write Serializer
    participant DB as Database
    
    U->>COA: 신청할 간식 uid, quantity 와 함께 주문
    COA->>S: 신청한 간식 목록 데이터 전달
    S->>DB: 아직 주문이 완료되지 않은 주문(not_delivered) 에 속한 간식 목록 쿼리
    DB-->>S: not_delivered 주문에 속한 간식 목록 응답
    S-->>S: 신청 간식 목록과 기 존재 간식 목록 비교
    Note over S,DB: 중복 주문된 간식이 존재하지 않도록 벨리데이션
    S->>DB: 주문(Order) 생성 및 간식 주문 데이터(Purchase) 생성 쿼리
    S-->>COA: 주문 생성 완료 처리
    COA-->>U: 주문 완료 Response
```

## Statistics

주문, 간식 관련 다양한 통계를 제공할 수 있다. 아래의 지표를 통계로 제공한다.

1. 상세 목록
    - 주기별 주문 목록
    - 주기별 간식 목록
2. 지표별 수치
    - 주기별 주문 수량
    - 주기별 간식 수량
    - 주기별 주문 금액

### 주기 정의

- 주기는 연, 월, 일 단위로 제공한다.
- 일 단위 range 형태로 필터링 할 수 있다.
    - 2024-1-1 ~ 2024-1-14
- 특정 주기는 별도 인터페이스 를 제공할 수 있다. 
    - 2024년 1월 1번째주
    - 2023년 3월

### 주기별 주문 목록

Order List 를 주기별로 가져올 수 있어야 한다.

- DatetimeField 에 대한 filtering 으로 주기별 목록을 필터링 할 수 있지만, 프론트에서 연동이 복잡해진다.
    - EX: Front 에서 지난 2023년 3월 을 지정해 불러오고자 할 때 2023-03-01T00:00:00, 2023-04-01T00:00:00 을 계산하 range 처리해야 한다.
- 백엔드에서 주문 혹은 간식을 등록할 때 year, month, day 값을 별도 field 로 저장 후 filter 에 활용할 수 있다.
    - ?year=2023&month=3
- 후자가 활용 면에서 좋고 Read performance 가 좋지만
- 전자는 3개의 필드가 추가되어 데이터가 방대한 경우 많은 손해를 볼 수 있다.

### 주기별 신청한 간식 목록

Order 와 연결된 Snack List 를 주기별로 가져올 수 있어야 한다.

- 신청한 간식은 Order 와 연결되어 있으며 Order 의 created_at 을 기준으로 가져오도록 한다.

### 주기별 주문 수량

주기별 주문의 합계 수량을 제공한다.

### 주기별 간식 수량

주기별 주문한 간식의 합계 수량을 계산한다.

### 주기별 주문 금액

주기별 주문 금액 합계를 계산하여 제공한다.

# Cache

Cache 는 하드디스크, 메모리 등 빠른 I/O 를 이용한 DB 혹은 시스템에 저장 후 활용하는 방식으로 용도에 맞게 사용하면 성능 및 리소스 효율성을 극대화 할 수 있다.

## 간식 좋아요 합계

```mermaid
---
title: Redis 를 이용한 통계 계산 시퀀스
---
sequenceDiagram
    participant U as User
    participant TRA as Toggle Reaction API
    participant STA as Statistics API
    participant S as Toggle Reaction Serializer
    participant DB as Database
    participant CC as Redis Cache
    participant SCHD as Celery Scheduler
    
    U->>TRA: 특정 간식에 좋아요 클릭하여 API 요청
    TRA->>S: 좋아요 클릭한 간식 uid, reaction_type 전달
    S->>CC: snack_uid 정보 기반으로 캐싱
    S->>CC: 현재 기준 리액션 수량 요청
    CC-->>S: 현재 기준 리액션 수량 제공
    Note over S,CC: 리액션 반영 정보 (snack_uid -> INCR like_count, DECR hate_count)
    S-->>TRA: 리액션 반영 완료 처리
    TRA-->>U: 리액션 반영 완료 Response
    SCHD->>CC: 일정 기간에 업데이트 된 리액션 수량 요청
    CC-->>SCHD: 일정 기간에 업데이트 된 리액션 수량 제공
    SCHD->>DB: 일정 기간에 업데이트 된 리액션 수량 업데이트
    Note over SCHD,DB: 일정 기간 업데이트된 리액션 수량을 DB 에 반영
    U->>STA: 통계 수치 요청
    STA->>DB: 통계 수치 쿼리
    DB-->>STA: 통계 수치 제공
    STA-->>U: 통계 수치 Response
    Note over U,STA: Scheduler 에 의해 합산된 통계를 프론트에서 활용
```

# Model

아래의 ERD 는 초기 설계용 이며, 개발이 진행되면서 추가 혹은 삭제되는 요소가 있을 수 있습니다.

```mermaid
---
title: 간식창고 ERD
---
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ PURCHASE: contains 
    SNACK }|--|{ PURCHASE: include
    SNACK ||--o{ SNACKREACTION: include

    USER {
        int id PK
        string name
        enum type
        boolean is_deleted
    }
    ORDER {
        int id PK
        int user_id FK
    }
    PURCHASE {
        int id PK
        int order_id FK
        int snack_id FK
        int quantity
    }
    SNACK {
        int id PK
        string name
        string url
        text desc 
        file image
        enum currency
        float price
    }
    SNACKREACTION {
        int id PK
        int snack_id FK
        int user_id FK
        enum type 
    }
```

# Structure

```
.
├── snack
│   ├── core
│   └── order
└── tests
```

## core app

- 사용자 인증 관련 기능
- 서버의 필수 기능 (middleware 등)
- 유틸리티(ex: response json 처리 유틸리티 등)

## order app

- 간식 주문 관련 기능
- 간식 관리 기능
