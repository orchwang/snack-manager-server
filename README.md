# Snack Server

데이터메이커 구성원이 사용하는 간식 주문 App 을 위한 Backend API Server

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
- 간식 목록 페이지
  - 관리자는 간식 상태 변경
- 통계 페이지

## 모달 목록

- 간식 주문 모달
- 주문 상태 변경 모달

## Business Process Flow

### Authentication Flow

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

### Snack Management Flow

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

### Order Management Flow

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

### Reaction Management

- 개별 Snack model 은 ForeignKey 연결된 SnackReaction Model 에 like, hate 반응을 기록한다.
- 사용자는 단일 Snack 에 1개의 reaction 을 남길 수 있다.
  - 1번 사용자는 A 스낵에 like 를 남길 수 있다.
  - 1번 사용자는 A 스낵에 like 과 hate 를 동시에 남길 수 없다.
- 사용자는 자신이 남긴 reaction 을 취소할 수 있다.
  - 1번 사용자는 A 스낵에 남긴 hate 를 남긴 후 like 로 변경하고자 한다.
  - 이때 1번 사용자가 A 스낵의 hate 를 누르면 "중복해서 reaction 을 남길 수 없다." 는 메시지를 보게 된다.
  - 1번 사용자는 A 스낵의 like 를 누른다. 이 때 서버에서 like reaction 을 등록하고 hate reaction 을 삭제한다.


### Resign Management

- 사용자는 시스템을 탈퇴할 수 있다.
- 탈퇴 버튼 위치는 sign-out 우측이다.
- 탈퇴 시 정말 탈퇴할지 한번 더 확인한다.
- 탈퇴에 성공하게 되면 시스템의 store.auth 를 비운다.
- 탈퇴 시 서버에서는 사용자 정보를 지우지 않고 is_deleted flag 만 True 처리 한다.
- 이후 재가입 시도 시 탈퇴한 사용자는 재가입이 불가능하다고 안내한다.
- 시스템에 ADMIN 이 본인 1명밖에 없으면 탈퇴할 수 없다.

## 필요한 API 목록

- 회원 가입
- JWT 발급 (로그인)
- JWT 리프레시
- 주문 목록
- 주문 상세
- 주문 상태 변경
- 등록된 간식 목록
- 간식 작성
- 월별 주문량 통계

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
```

- created -> ordered 변경 시 주문에 포함된 간식 중 `hate > like` 인 간식이 한개라도 있다면 변경 실패처리 한다. -> 주문 시 필터링 하도록 구현했다.

### UI

- Order List Page 에서 상태를 변경하도록 한다. -> 필드를 추가하고 status dropdown, arrive_estimate_date 를 위한 input 도 추가한다.
- 변경 시 예상 도착일 (예상 사용일) 을 같이 입력하도록 UI 를 구성한다.

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
    SNACKREACTION ||--|| USER: include

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
