# AI Building Permit Manager

AI 건축 인허가 매니저는 사용자가 주소, 지번, 좌표, 지도 클릭으로 특정 필지나 건축물을 선택하고, 해당 대상지에서 수행하려는 건축 행위를 입력하면 공공데이터, 룰엔진, RAG, LLM 문서 생성을 결합해 인허가 사전검토 결과를 제공하는 웹 서비스입니다.

현재 프로젝트는 다음 방향으로 개발합니다.

- 주소 문자열이 아니라 `PNU`, 필지 Geometry, Parcel Profile, Building Profile, Action JSON을 기준으로 판단합니다.
- 인허가 판단의 1차 골격은 LLM이 아니라 룰엔진이 만듭니다.
- RAG는 법령, 조례, 지구단위계획, 별표, 서식 근거를 찾고 Evidence Trace로 연결합니다.
- LLM은 판단자가 아니라 체크리스트, 사전협의 질문, 보고서 문장 생성 보조자로 사용합니다.
- 모든 결과에는 Rule Trace, Evidence Trace, 데이터 기준일자, 수집 시각을 남기는 것을 목표로 합니다.
- 실제 인허가 가능 여부는 관할 행정청의 최종 판단 대상이며, 본 서비스는 사전진단 참고자료를 제공합니다.

---

## 1. 기술 스택

### Frontend

- Node.js 20 LTS+
- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- OpenLayers, VWorld 지도 연동 예정

### Backend

- Python 3.11+
- FastAPI
- Pydantic / pydantic-settings
- Uvicorn
- PostgreSQL + PostGIS
- Redis, background worker 예정

### AI / Data Pipeline

- YAML/JSON 기반 Rule Set
- Python Rule Engine
- Qdrant vector database
- BGE-M3 embedding 예정
- BM25 keyword retrieval 예정
- bge-reranker-v2-m3 reranker 예정
- GPT 계열 LLM structured output 예정
- DOCX/PDF report generation 예정

### Infrastructure

- Docker Desktop
- Docker Compose
- PostgreSQL/PostGIS
- Redis
- Qdrant

---

## 2. 폴더 구조

```text
ai-building-permit-manager/
  apps/
    web/                         Vue 3 + TypeScript 프론트엔드
      src/
        app/                     앱 진입점, 라우터
        pages/                   페이지 컴포넌트
        features/                5단계 진단 기능 단위
        components/              공통 UI, 지도, 폼, 근거 표시 컴포넌트
        api/                     프론트 API client
        stores/                  Pinia store
        types/                   프론트 타입
        utils/                   포맷터, 검증 함수

    api/                         FastAPI 백엔드
      app/
        api/v1/                  HTTP API router
        core/                    보안, 로깅, 상수, 상태값
        db/                      DB session, migration, repository
        models/                  DB model 예정
        schemas/                 API DTO / Pydantic schema
        services/                백엔드 application service
        clients/                 외부 API client
        workers/                 장시간 작업 worker 예정

  packages/
    shared-types/                공통 계약, JSON Schema, 타입 생성 예정
    ui-specs/                    화면 정책, 폼 스키마, Wizard 단계 정의

  services/
    location/                    주소, 좌표, PNU, 필지 Polygon 처리
    public-data/                 건축물대장, 토지이용계획, VWorld 연계
    rule-engine/                 룰 로딩, 조건 평가, Rule Trace
    rag/                         법령 문서 수집, 청킹, 검색, reranking
    llm/                         체크리스트, 질문, 보고서 생성
    document-generator/          DOCX/PDF 생성

  data/
    rules/                       버전별 룰셋
    legal-docs/                  법령, 조례, 지구단위계획 원문/청크/메타데이터
    seed/                        초기 DB 시드
    samples/                     샘플 주소, 필지, 건축행위 케이스

  infra/                         Docker, DB, nginx, 배포 보조 파일
  docs/                          기획서, 아키텍처, API 명세, ADR
  tests/                         E2E, fixture, RAG/룰엔진 평가
  scripts/                       문서 수집, DB 시드, 평가 실행 스크립트
```

---

## 3. 설치 전 준비

### 필수 설치 항목

아래 도구가 설치되어 있어야 합니다.

| 도구 | 권장 버전 | 확인 명령 |
|---|---:|---|
| Git | 최신 안정 버전 | `git --version` |
| Python | 3.11 이상 | `python --version` |
| Node.js | 20 LTS 이상 | `node --version` |
| npm | 10 이상 | `npm --version` |
| Docker Desktop | 최신 안정 버전 | `docker --version` |
| Docker Compose | v2 | `docker compose version` |

Windows PowerShell 기준으로 다음 명령을 실행해 버전을 확인합니다.

```powershell
git --version
python --version
node --version
npm --version
docker --version
docker compose version
```

### 선택 설치 항목

- PostgreSQL client 또는 DBeaver
- Postman, Insomnia, Bruno 같은 API client
- VS Code 확장: Python, Vue, Docker, YAML
- Qdrant REST 확인용 API client

---

## 4. 환경 파일 준비

프로젝트 루트에서 `.env.example`을 복사해 `.env`를 만듭니다.

```powershell
Copy-Item .env.example .env
```

루트 `.env` 주요 값:

```env
APP_ENV=local
API_HOST=0.0.0.0
API_PORT=8000
WEB_PORT=5173

DATABASE_URL=postgresql+psycopg://permit:permit@localhost:5432/permit
REDIS_URL=redis://localhost:6379/0
QDRANT_URL=http://localhost:6333

VWORLD_API_KEY=
ROAD_ADDRESS_API_KEY=
BUILDING_HUB_API_KEY=
LAW_OPEN_API_KEY=
OPENAI_API_KEY=
```

초기 스캐폴딩 단계에서는 외부 API 키가 비어 있어도 서버 실행 자체는 가능합니다. 위치/PNU 변환, 건축물대장, 법령 API, LLM 호출 기능을 실제로 붙일 때 각 키를 채웁니다.

### 프론트엔드 환경 파일

프론트엔드는 Vite 환경변수를 사용합니다. 아직 `apps/web/.env.example`은 없으므로 필요할 때 직접 생성합니다.

```powershell
cd apps\web
New-Item -ItemType File -Force .env
```

`apps/web/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Vite에서 브라우저 코드로 노출되는 환경변수는 반드시 `VITE_`로 시작해야 합니다.

---

## 5. 인프라 실행

PostgreSQL/PostGIS, Redis, Qdrant는 루트의 `docker-compose.yml`로 실행합니다.

프로젝트 루트에서 실행합니다.

```powershell
docker compose up -d
```

실행 상태 확인:

```powershell
docker compose ps
```

로그 확인:

```powershell
docker compose logs -f
```

특정 서비스 로그만 확인:

```powershell
docker compose logs -f postgres
docker compose logs -f redis
docker compose logs -f qdrant
```

중지:

```powershell
docker compose down
```

볼륨까지 삭제하고 완전히 초기화할 때만 사용합니다.

```powershell
docker compose down -v
```

기본 접속 정보:

| 서비스 | 주소/포트 | 비고 |
|---|---|---|
| PostgreSQL/PostGIS | `localhost:5432` | DB `permit`, user `permit`, password `permit` |
| Redis | `localhost:6379` | background job 예정 |
| Qdrant | `http://localhost:6333` | vector search 예정 |

Qdrant 상태 확인:

```powershell
curl http://localhost:6333/healthz
```

---

## 6. Backend 실행

새 터미널을 열고 프로젝트 루트에서 시작합니다.

```powershell
cd apps\api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

FastAPI 앱이 import 되는지 먼저 확인합니다.

```powershell
python -c "from app.main import app; print(app.title)"
```

개발 서버 실행:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

확인 URL:

```text
http://localhost:8000/health
http://localhost:8000/docs
http://localhost:8000/api/v1/projects
```

헬스 체크:

```powershell
curl http://localhost:8000/health
```

현재 API는 초기 스캐폴딩 상태라 대부분 `not_implemented` 또는 빈 배열을 반환합니다. 서버 실행, 라우터 구조, API 문서 확인이 목적입니다.

### Backend 주요 엔드포인트

| Method | Endpoint | 현재 상태 |
|---|---|---|
| GET | `/health` | 동작 |
| GET | `/api/v1/auth/me` | 임시 응답 |
| POST | `/api/v1/projects` | 스텁 |
| GET | `/api/v1/projects` | 빈 목록 |
| GET | `/api/v1/projects/{project_id}` | 임시 응답 |
| POST | `/api/v1/locations/resolve` | 스텁 |
| POST | `/api/v1/locations/parcel-profile` | 스텁 |
| POST | `/api/v1/actions/normalize` | 스텁 |
| POST | `/api/v1/diagnosis/runs` | 스텁 |
| GET | `/api/v1/diagnosis/runs/{run_id}/status` | 임시 상태 |
| GET | `/api/v1/diagnosis/runs/{run_id}/result` | 임시 응답 |
| GET | `/api/v1/diagnosis/runs/{run_id}/evidence` | 빈 목록 |
| GET | `/api/v1/diagnosis/runs/{run_id}/trace` | 빈 목록 |
| POST | `/api/v1/reports` | 스텁 |
| GET | `/api/v1/reports/{report_id}` | 임시 응답 |

---

## 7. Frontend 실행

새 터미널을 열고 프로젝트 루트에서 시작합니다.

```powershell
cd apps\web
npm install
npm run dev
```

확인 URL:

```text
http://localhost:5173/
```

프론트엔드는 기본적으로 `http://localhost:8000`을 API 서버로 사용합니다. API 주소를 바꾸려면 `apps/web/.env`의 `VITE_API_BASE_URL`을 수정한 뒤 프론트 서버를 재시작합니다.

Windows PowerShell에서 `npm` 실행이 막히면 `npm.cmd`를 사용합니다.

```powershell
npm.cmd install
npm.cmd run dev
```

프론트 빌드 확인:

```powershell
npm run build
```

---

## 8. 권장 실행 순서

처음 실행할 때는 터미널을 3개로 나누는 것을 권장합니다.

### Terminal 1: Infrastructure

```powershell
docker compose up -d
docker compose ps
```

### Terminal 2: Backend

```powershell
cd apps\api
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

가상환경을 아직 만들지 않았다면 6번 Backend 실행 단계를 먼저 진행합니다.

### Terminal 3: Frontend

```powershell
cd apps\web
npm run dev
```

실행 확인 순서:

1. `docker compose ps`에서 `postgres`, `redis`, `qdrant`가 실행 중인지 확인
2. `http://localhost:8000/health`에서 `{"status":"ok"}` 확인
3. `http://localhost:8000/docs`에서 FastAPI 문서 확인
4. `http://localhost:5173/`에서 Vue 화면 확인

---

## 9. 테스트와 검증

현재는 초기 스캐폴딩 단계이므로 정식 테스트 스위트는 아직 없습니다. 대신 아래 명령으로 기본 상태를 확인합니다.

### Python 문법 확인

프로젝트 루트에서 실행합니다.

```powershell
python -m compileall apps services scripts
```

### Backend import 확인

```powershell
cd apps\api
.\.venv\Scripts\Activate.ps1
python -c "from app.main import app; print(app.title)"
```

### Frontend build 확인

```powershell
cd apps\web
npm run build
```

---

## 10. 개발 원칙

### 판단 파이프라인

서비스의 핵심 흐름은 다음 순서로 구현합니다.

```text
위치 입력
→ 주소/PNU/필지 Polygon 식별
→ 공공데이터 수집
→ Parcel Profile / Building Profile 구성
→ 사용자 건축행위 입력
→ Action JSON 정규화
→ 룰엔진 실행
→ Rule Trace 저장
→ Evidence Query 생성
→ RAG 검색 및 reranking
→ Evidence Trace 저장
→ 체크리스트/질문/보고서 생성
→ 검증 및 단정표현 완화
```

### 중요한 규칙

- LLM이 인허가 가능/불가를 직접 단정하지 않습니다.
- 룰엔진 결과에 없는 절차를 LLM이 임의로 추가하지 않습니다.
- 법령, 조례, 지구단위계획 설명은 Evidence Trace와 연결되어야 합니다.
- 공공 API 실패, 데이터 최신성 미확인, 입력 누락이 있으면 `추가정보 필요` 또는 `관할부서 확인 필요`로 표시합니다.
- 보고서에는 확정 표현보다 보수적 표현을 사용합니다.

---

## 11. 앞으로 구현할 주요 작업

초기 구조 이후 우선순위는 다음과 같습니다.

1. SQLAlchemy 모델과 Alembic migration 구성
2. PostgreSQL/PostGIS 연결
3. Project, Parcel, Building, Action 기본 CRUD
4. Location resolve 스텁을 실제 PNU 변환 흐름으로 확장
5. Action JSON schema 정의
6. 룰셋 YAML schema와 Rule Engine 최소 구현
7. 샘플 법령 chunk와 RAG 검색 스텁 구현
8. DiagnosisRun 비동기 실행 구조 추가
9. 결과 화면 5단계 Wizard 구현
10. 체크리스트와 보고서 HTML/DOCX 생성

MVP 1차는 전국 실데이터 완성이 아니라, 샘플 필지와 샘플 법령 근거로 진단 플로우가 끝까지 도는 세로 흐름을 만드는 것을 목표로 합니다.

---

## 12. 자주 나는 문제

### `python` 명령이 동작하지 않음

Python이 설치되지 않았거나 PATH에 등록되지 않은 상태입니다.

```powershell
py --version
py -3.11 --version
```

`python` 대신 `py -3.11`을 사용할 수 있습니다.

```powershell
py -3.11 -m venv .venv
```

### PowerShell에서 가상환경 활성화가 막힘

실행 정책 문제일 수 있습니다. 현재 사용자 범위에서 실행 정책을 완화합니다.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

그 다음 다시 실행합니다.

```powershell
.\.venv\Scripts\Activate.ps1
```

### `ModuleNotFoundError: No module named 'fastapi'`

가상환경이 켜져 있지 않거나 패키지가 설치되지 않은 상태입니다.

```powershell
cd apps\api
.\.venv\Scripts\Activate.ps1
pip install -e .
```

### `ModuleNotFoundError: No module named 'app'`

`apps/api` 폴더 밖에서 Uvicorn을 실행했을 가능성이 큽니다.

```powershell
cd apps\api
uvicorn app.main:app --reload
```

### Docker가 실행되지 않음

Docker Desktop이 켜져 있는지 확인합니다.

```powershell
docker info
```

`docker info`가 실패하면 Docker Desktop을 실행한 뒤 다시 시도합니다.

### `docker compose up`에서 포트 충돌이 발생함

이미 같은 포트를 사용하는 프로세스가 있을 수 있습니다.

사용 포트:

- PostgreSQL: `5432`
- Redis: `6379`
- Qdrant: `6333`
- Backend: `8000`
- Frontend: `5173`

필요하면 `docker-compose.yml` 또는 실행 명령의 포트를 바꿉니다.

### PowerShell에서 `npm` 실행이 막힘

`npm.cmd`를 사용합니다.

```powershell
npm.cmd install
npm.cmd run dev
```

### 프론트 화면은 뜨지만 API 호출이 실패함

확인할 것:

- FastAPI 서버가 `http://localhost:8000`에서 실행 중인지
- `http://localhost:8000/health`가 정상 응답하는지
- `apps/web/.env`의 `VITE_API_BASE_URL`이 맞는지
- `.env` 수정 후 프론트 서버를 재시작했는지

### 한글이 깨져 보임

파일 인코딩을 UTF-8로 저장합니다. VS Code 오른쪽 아래 인코딩 표시를 확인하고 `Save with Encoding`에서 `UTF-8`을 선택합니다.

