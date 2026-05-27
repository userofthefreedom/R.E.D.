# AI Building Permit Manager

AI 건축 인허가 매니저는 사용자가 주소, 지번, 좌표, 지도 클릭으로 대상 필지나 건축물을 선택하고, 해당 대상지에서 수행하려는 건축 계획을 입력하면 공공데이터, 룰엔진, RAG, LLM 문서 생성을 결합해 인허가 사전진단 결과를 제공하는 웹 서비스입니다.

이 프로젝트의 판단 원칙은 단순합니다.

- 주소 문자열이 아니라 `PNU`, 필지 Geometry, Parcel Profile, Building Profile, Action JSON을 기준으로 판단합니다.
- 인허가 판단의 1차 골격은 LLM이 아니라 룰엔진이 만듭니다.
- RAG는 법령, 조례, 지구단위계획, 별표, 서식 근거를 찾고 Evidence Trace로 연결합니다.
- LLM은 판단자가 아니라 체크리스트, 사전협의 질문, 보고서 문장 생성 보조자로 사용합니다.
- 모든 결과에는 Rule Trace, Evidence Trace, 데이터 기준일자, 수집 시각을 남기는 것을 목표로 합니다.
- 실제 인허가 가능 여부는 관할 행정청의 최종 판단 대상이며, 본 서비스는 사전진단 참고자료를 제공합니다.

---

## 1. 현재 구현 상태

현재는 **프론트엔드 mockup + 백엔드 API 스캐폴딩** 단계입니다.

- Frontend: Vue 3 + TypeScript + Vite 기반 mockup 화면 구현
- Backend: FastAPI 라우터와 endpoint 스텁 구성
- Infrastructure: PostgreSQL/PostGIS, Redis, Qdrant Docker Compose 구성
- Data/AI: 룰엔진, RAG, LLM, 문서 생성 폴더 구조만 준비된 상태

프론트 mockup은 백엔드 연결 없이 화면 검토용으로 실행할 수 있습니다.

---

## 2. 기술 스택

### Frontend

- Node.js 20 LTS+
- npm 10+
- Vue 3
- TypeScript
- Vite
- Vue Router
- Pinia
- `@lucide/vue`

### Backend

- Python 3.11+
- FastAPI
- Pydantic / pydantic-settings
- Uvicorn
- PostgreSQL + PostGIS
- Redis
- Qdrant

### AI / Data Pipeline

- YAML/JSON 기반 Rule Set
- Python Rule Engine
- Qdrant vector database
- BGE-M3 embedding 예정
- BM25 keyword retrieval 예정
- bge-reranker-v2-m3 reranker 예정
- GPT 계열 LLM structured output 예정
- DOCX/PDF report generation 예정

---

## 3. 폴더 구조

```text
ai-building-permit-manager/
  apps/
    web/                         Vue 3 + TypeScript 프론트엔드
      src/
        app/                     앱 진입점, 라우터, mock 데이터, 전역 스타일
        pages/                   화면 단위 Vue 페이지
        features/                4단계 진단 기능과 대안 시나리오 서브 페이지
        components/              공통 UI, 지도, 근거, 보고서 컴포넌트
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

  services/                      location, public-data, rule-engine, rag, llm, document-generator
  data/                          rules, legal-docs, seed, samples
  infra/                         Docker, DB, nginx, 배포 보조 파일
  docs/                          planning, architecture, api, data, history
  tests/                         E2E, fixture, RAG/룰엔진 평가
  scripts/                       문서 수집, DB 시드, 평가 실행 스크립트
```

---

## 4. Bash 기준 실행 준비

이 README는 **Git Bash / Bash 기준**입니다.

Windows 경로 `C:\Users\mypc\Desktop\newpjt`는 Git Bash에서 보통 아래처럼 이동합니다.

```bash
cd /c/Users/mypc/Desktop/newpjt
```

현재 위치 확인:

```bash
pwd
```

---

## 5. 필수 도구 확인

```bash
git --version
python --version
node --version
npm.cmd --version
docker --version
docker compose version
```

Windows Git Bash에서 `npm`이 실행 정책 문제를 만나면 `npm.cmd`를 사용합니다.

---

## 6. 환경 파일 준비

루트에서 `.env.example`을 복사해 `.env`를 만듭니다.

```bash
cd /c/Users/mypc/Desktop/newpjt
cp .env.example .env
```

`.env` 주요 값:

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

프론트엔드는 현재 mockup이라 API 서버가 없어도 화면 확인이 가능합니다. 나중에 백엔드와 연결할 때 `apps/web/.env`를 만듭니다.

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/web
printf "VITE_API_BASE_URL=http://localhost:8000\n" > .env
```

API 키는 브라우저에 노출되면 안 됩니다. 외부 API 키는 루트 `.env`에만 둡니다.

---

## 7. 프론트엔드 mockup 실행

회의에서 화면만 확인하려면 이 단계만 해도 됩니다.

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/web
npm.cmd install
npm.cmd run dev
```

브라우저에서 접속:

```text
http://localhost:5173/
```

빌드 확인:

```bash
npm.cmd run build
```

현재 구현된 주요 mockup 화면:

- `/` 홈
- `/dashboard` 프로젝트 대시보드
- `/projects` 내 프로젝트 목록
- `/projects/new` 새 진단 시작
- `/projects/demo/diagnosis` 4단계 진단 Wizard
- `/projects/demo/diagnosis/alternatives` 대안 시나리오 서브 페이지
- `/projects/demo` 프로젝트 상세
- `/projects/demo/history` 진단 이력/버전 비교
- `/reports/demo` 보고서 미리보기
- `/support` 지원/예외 안내
- `/data-sources` 데이터 출처 및 면책 안내

---

## 8. 인프라 실행

PostgreSQL/PostGIS, Redis, Qdrant는 루트의 `docker-compose.yml`로 실행합니다.

```bash
cd /c/Users/mypc/Desktop/newpjt
docker compose up -d
docker compose ps
```

로그 확인:

```bash
docker compose logs -f
```

특정 서비스 로그:

```bash
docker compose logs -f postgres
docker compose logs -f redis
docker compose logs -f qdrant
```

중지:

```bash
docker compose down
```

볼륨까지 삭제하고 완전히 초기화할 때만 사용:

```bash
docker compose down -v
```

기본 접속 정보:

| 서비스 | 주소/포트 | 비고 |
|---|---|---|
| PostgreSQL/PostGIS | `localhost:5432` | DB `permit`, user `permit`, password `permit` |
| Redis | `localhost:6379` | background job 예정 |
| Qdrant | `http://localhost:6333` | vector search 예정 |

Qdrant 상태 확인:

```bash
curl http://localhost:6333/healthz
```

---

## 9. 백엔드 실행

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/api
python -m venv .venv
source .venv/Scripts/activate
python -m pip install --upgrade pip
pip install -e .
```

FastAPI 앱 import 확인:

```bash
python -c "from app.main import app; print(app.title)"
```

정상 출력:

```text
AI Building Permit Manager API
```

개발 서버 실행:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

확인 URL:

```text
http://localhost:8000/health
http://localhost:8000/docs
http://localhost:8000/api/v1/projects
```

헬스 체크:

```bash
curl http://localhost:8000/health
```

현재 API는 초기 스캐폴딩 상태라 대부분 `not_implemented` 또는 빈 배열을 반환합니다.

---

## 10. 권장 실행 순서

화면 mockup만 볼 때:

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/web
npm.cmd install
npm.cmd run dev
```

전체 로컬 환경을 켤 때는 터미널 3개를 사용합니다.

Terminal 1: Infrastructure

```bash
cd /c/Users/mypc/Desktop/newpjt
docker compose up -d
docker compose ps
```

Terminal 2: Backend

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/api
source .venv/Scripts/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Terminal 3: Frontend

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/web
npm.cmd run dev
```

확인 순서:

1. `docker compose ps`에서 `postgres`, `redis`, `qdrant` 실행 확인
2. `http://localhost:8000/health`에서 `{"status":"ok"}` 확인
3. `http://localhost:8000/docs`에서 FastAPI 문서 확인
4. `http://localhost:5173/`에서 Vue 화면 확인

---

## 11. 테스트와 검증

Python 문법 확인:

```bash
cd /c/Users/mypc/Desktop/newpjt
python -m compileall apps/api/app services scripts
```

Backend import 확인:

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/api
source .venv/Scripts/activate
python -c "from app.main import app; print(app.title)"
```

Frontend build 확인:

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/web
npm.cmd run build
```

---

## 12. 자주 나는 문제

### `python` 명령이 동작하지 않음

Windows Python Launcher를 확인합니다.

```bash
py --version
py -3.11 --version
```

필요하면 `python` 대신 `py -3.11`을 사용합니다.

```bash
py -3.11 -m venv .venv
```

### Bash에서 가상환경 활성화가 안 됨

Git Bash 기준:

```bash
source .venv/Scripts/activate
```

PowerShell 명령인 `.\.venv\Scripts\Activate.ps1`는 Bash에서 쓰지 않습니다.

### `ModuleNotFoundError: No module named 'fastapi'`

가상환경이 켜져 있지 않거나 패키지가 설치되지 않은 상태입니다.

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/api
source .venv/Scripts/activate
pip install -e .
```

### `ModuleNotFoundError: No module named 'app'`

`apps/api` 폴더 밖에서 Uvicorn을 실행했을 가능성이 큽니다.

```bash
cd /c/Users/mypc/Desktop/newpjt/apps/api
uvicorn app.main:app --reload
```

### Docker가 실행되지 않음

Docker Desktop이 켜져 있는지 확인합니다.

```bash
docker info
```

### 포트 충돌

사용 포트:

- PostgreSQL: `5432`
- Redis: `6379`
- Qdrant: `6333`
- Backend: `8000`
- Frontend: `5173`

필요하면 `docker-compose.yml` 또는 실행 명령의 포트를 바꿉니다.

### npm 취약점 경고

`npm.cmd install` 후 `npm audit`이 경고를 낼 수 있습니다. `npm audit fix --force`는 의존성을 크게 바꿀 수 있으므로, 회의용 mockup 확인 중에는 바로 실행하지 않는 것을 권장합니다.

---

## 13. 앞으로 구현할 주요 작업

1. 프론트 mockup 회의 피드백 반영
2. SQLAlchemy 모델과 Alembic migration 구성
3. PostgreSQL/PostGIS 연결
4. Project, Parcel, Building, Action 기본 CRUD
5. Location resolve 스텁을 실제 PNU 변환 흐름으로 확장
6. Action JSON schema 정의
7. 룰셋 YAML schema와 Rule Engine 최소 구현
8. 샘플 법령 chunk와 RAG 검색 스텁 구현
9. DiagnosisRun 비동기 실행 구조 추가
10. 체크리스트와 보고서 HTML/DOCX 생성

MVP 1차는 전국 실데이터 완성이 아니라, 샘플 필지와 샘플 법령 근거로 진단 플로우가 끝까지 도는 세로 흐름을 만드는 것을 목표로 합니다.
