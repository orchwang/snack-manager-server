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

## Auth APIs

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

# Stack

## Backend

- Python==3.11.7
- Django==4.2.9

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
  - sign-up api
- Sign in
  - sign-in api
- User list
  - user-list api
  - update-user api
  - user-leave api

## Order App

### requirements

- `이름, 이미지, 구매 URL, 설명` 을 입력할 수 있는 게시판
- 목록만 에서 모든 필드와 상태 확인 가능
- 관리자는 게시판에서 주문상태 변경
- 주문상태 변경할 시 예상 사용 일시 입력해야 함
- 월별 별도 목록 필요
- 한번 등록된 간식은 추후 선택 가능 (간식 요청 모델과 간식 모델의 관계 지정을 통한 구현 필요)
- 대기중 일 때만 수정 가능
- 같은 간식을 중복 신청할 수 없다. 
- 신청된 간식에 좋아요/싫어요를 선택 가능
- 좋아요/싫어요 비율에 따라 우선순위 조정
- 싫어요가 좋아요보다 많으면, 간식신청의 주문상태를 주문완료로 바꿀 수 없다.

> 간식을 구별하는 유일값은 간식의 이름이다.

### UIs

- Order list
  - order-list api
  - update-order api
- Snack list
  - snack-list api
- Order snack
  - create-order api

# Business Processes 

본 프로젝트에서 사용되는 Business Processes 를 정의합니다.

## 새로운 간식 주문

```mermaid
flowchart TD
    A[로그인 페이지] --> |로그인 성공| B[간식 주문 테이블]
    B[간식 주문 테이블] --> |간식 주문 버튼 클릭| C[주문서 작성 폼]
    C[주문서 작성 폼] --> |주문서 작성 후 주문| D{간식 주문 프로세스 실행}
    D{간식 주문 프로세스 실행} --> |주문 성공| B[간식 주문 테이블]
    D{간식 주문 프로세스 실행} --> |주문 실패| C[주문서 작성 폼]
```

## 기존에 존재하는 간식 주문

```mermaid
flowchart TD
  A[로그인 페이지] --> |로그인 성공| B[간식 주문 테이블]
  B[간식 주문 테이블] --> |간식 주문 버튼 클릭| C[주문서 작성 폼]
  C[주문서 작성 폼] --> |간식 목록에서 선택 후 주문| D{간식 주문 프로세스 실행}
  D{간식 주문 프로세스 실행} --> |주문 성공| B[간식 주문 테이블]
  D{간식 주문 프로세스 실행} --> |주문 실패| C[주문서 작성 폼]
```

# Model

```mermaid
---
title: 간식창고 ERD
---
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ CART: contains 
    SNACK }|--|{ CART: include

    USER {
        int id PK
        string name
        enum type
        boolean is_deleted
    }
    ORDER {
        int id PK
        int user_id FK
        int quantity
    }
    CART {
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

# TODOs

- 요구사항에 근거해 API 설계
- Permission 세팅
- Serializer 구현
- APIView 구현
- drf-spectacular 이용해 APIView, Serializer 와 병합하여 SwaggerUI 페이지 서빙
- djangorestframework-simplejwt 를 이용해 인증 API 구현
