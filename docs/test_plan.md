# MagicSquare 테스트 계획서

## 1. 문서 메타

| 항목 | 내용 |
|---|---|
| **문서 ID** | TP-AC-FR01-01 |
| **버전** | 1.0 |
| **작성 역할** | 시니어 QA 리드 |
| **대상 기능** | FR-01 Input Verification (Boundary) — 크기 검증 |
| **기준 AC** | **AC-FR01-01** — 4×4가 아닌 입력은 `INVALID_SIZE`를 반환한다 |
| **연관 AC** | **AC-FR01-05** — FR-01 실패 시 Domain resolver를 호출하지 않는다 |
| **기준 문서** | `docs/PRD_MagicSquare.md` (§10 FR-01, §11 BR-01, §13, §16.2 TC-E-01) |
| **기술 스택** | Python 3.13, pytest, pydantic, unittest.mock |
| **샘플 예제** | `grid = None` → `{ code: "INVALID_SIZE", message: "Grid must be 4x4." }` |

---

## 2. 목적 및 범위

### 2.1 목적

본 계획서는 **AC-FR01-01**을 중심으로, Boundary 계층의 입력 크기 검증과 Domain resolver 진입점 격리를 pytest 기반 단위 테스트로 고정하기 위한 실행 계획이다. Dual-Track TDD의 **Track A (Boundary / Contract)** Red 단계 산출물로 사용한다.

### 2.2 In-Scope (본 계획 범위)

- Boundary 크기 검증 단위 테스트 (`BoundaryValidator` 또는 동등 컴포넌트)
- Control/Application 계층 오케스트레이션 테스트 (검증 실패 시 Domain 미호출)
- pydantic 기반 오류 응답 스키마 계약 검증
- `unittest.mock` 기반 Domain resolver 호출 횟수 검증
- pytest-cov 커버리지 측정 및 게이트 정의

### 2.3 Out-of-Scope (본 계획 범위 외)

- AC-FR01-02 ~ AC-FR01-04 (빈칸 개수, 값 범위, 중복) — 별도 테스트 계획에서 다룸
- FR-02 ~ FR-05 Domain 로직 — Track B 계획에서 다룸
- **4×4 정상 입력** — AC-FR01-01 범위 외이므로 본 계획의 경계값 목록에 **포함하지 않음**
- UI, DB, Web/API, 성능(50ms) 벤치마크

---

## 3. 추적성 (Traceability)

| Concept | Business Rule | Feature | AC | Test Case | Component |
|---|---|---|---|---|---|
| 4×4 입력 | BR-01 | FR-01 | AC-FR01-01 | TC-E-01 | `BoundaryValidator` |
| Domain 격리 | §13 정책 | FR-01 | AC-FR01-05 | TC-E-01 + spy | Control + `CompletionResolver` |
| Gherkin | — | FR-01 | AC-FR01-01, AC-FR01-05 | Scenario-G3 | — |

---

## 4. pytest 기반 단위 테스트 범위 및 우선순위

### 4.1 테스트 레이어 구분

| 레이어 | 대상 모듈 (예정) | 테스트 디렉터리 (예정) | 커버리지 목표 |
|---|---|---|---|
| **Boundary** | `src/boundary/validator.py`, `src/boundary/errors.py`, `src/boundary/schemas.py` | `tests/boundary/` | **≥ 85%** |
| **Control** | `src/control/magic_square_service.py` | `tests/control/` | Boundary 게이트에 포함 또는 별도 85% |
| **Domain** | `src/domain/completion_resolver.py` 등 | `tests/domain/` | **≥ 95%** (본 AC 범위 외, 전체 프로젝트 게이트) |

### 4.2 우선순위 매트릭스

| 우선순위 | 테스트 ID | 대상 | 검증 내용 | AC |
|---|---|---|---|---|
| **P0** | `BND-UT-01` | `BoundaryValidator.validate_size` | `grid = None` → `INVALID_SIZE` + 메시지 | AC-FR01-01 |
| **P0** | `CTL-UT-01` | `MagicSquareService.solve` | `grid = None` 시 Domain resolver **0회** 호출 | AC-FR01-05 |
| **P0** | `BND-UT-02` | `BoundaryValidator.validate_size` | `grid = []` → `INVALID_SIZE` | AC-FR01-01 |
| **P0** | `BND-UT-03` | `BoundaryValidator.validate_size` | `grid = [[]] * 4` → `INVALID_SIZE` | AC-FR01-01 |
| **P1** | `BND-UT-04` ~ `BND-UT-06` | `BoundaryValidator.validate_size` | 3×4, 4×3, 5×5 → `INVALID_SIZE` | AC-FR01-01 |
| **P1** | `CTL-UT-02` ~ `CTL-UT-06` | `MagicSquareService.solve` | 위 P0/P1 입력 각각 Domain resolver **0회** | AC-FR01-05 |
| **P2** | `BND-UT-07` ~ `BND-UT-10` | Boundary + pydantic | 예외/특이 입력 거부 및 스키마 계약 | AC-FR01-01 |
| **P2** | `BND-UT-11` | `ErrorResponse` (pydantic) | `code`, `message` 필드 타입·필수성 | §12.2, §13 |

### 4.3 실행 순서 (TDD Red → Green)

1. **Red (P0):** `BND-UT-01`, `CTL-UT-01` — 샘플 예제(`grid = None`) 고정
2. **Red (P0):** 나머지 명시적 경계값 케이스 (`BND-UT-02`, `BND-UT-03`)
3. **Red (P1):** 크기 불일치 행렬 + Control spy 테스트
4. **Red (P2):** 예외/특이 케이스 및 pydantic 스키마 계약
5. **Green:** 최소 구현으로 P0 → P1 → P2 순 통과
6. **Refactor:** 검증 로직 추출, 상수 명명(NFR-08), mock fixture 공통화

### 4.4 테스트 작성 규칙

- **AAA 패턴** (Arrange → Act → Assert) 필수
- 모든 테스트 함수에 타입힌트 및 `@pytest.mark.parametrize` 활용 (동일 AC 다중 입력)
- `@pytest.fixture`로 공통 invalid grid 및 mock resolver 제공
- `print()` 디버깅, bare `except`, 테스트 약화/삭제 금지 (PRD §20)
- 마커 예시: `@pytest.mark.boundary`, `@pytest.mark.contract`, `@pytest.mark.priority_p0`

---

## 5. 경계값 케이스 목록 (AC-FR01-01)

> **제외:** 4×4 정상 입력은 AC-FR01-01 범위 외이므로 본 절에 포함하지 않는다.

### 5.1 케이스 정의

| TC ID | 입력 (`grid`) | 실패 원인 | 기대 `code` | 기대 `message` (영문 계약) | 우선순위 |
|---|---|---|---|---|---|
| **TC-E-01-None** | `None` | 행렬 자체 부재 | `INVALID_SIZE` | `Grid must be 4x4.` | P0 |
| **TC-E-01-Empty** | `[]` | 행 0개 | `INVALID_SIZE` | `Grid must be 4x4.` | P0 |
| **TC-E-01-EmptyRows** | `[[]] * 4` | 행 4개, 열 0개 | `INVALID_SIZE` | `Grid must be 4x4.` | P0 |
| **TC-E-01-3x4** | `3×4` 행렬 (아래 예시) | 행 3개 | `INVALID_SIZE` | `Grid must be 4x4.` | P1 |
| **TC-E-01-4x3** | `4×3` 행렬 (아래 예시) | 열 3개 | `INVALID_SIZE` | `Grid must be 4x4.` | P1 |
| **TC-E-01-5x5** | `5×5` 행렬 (아래 예시) | 행·열 5개 | `INVALID_SIZE` | `Grid must be 4x4.` | P1 |

### 5.2 구체 입력 예시

```python
# TC-E-01-None
grid = None

# TC-E-01-Empty
grid = []

# TC-E-01-EmptyRows — 행 존재, 열 없음
grid = [[]] * 4

# TC-E-01-3x4 — 행 3, 열 4
grid = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]

# TC-E-01-4x3 — 행 4, 열 3
grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12],
]

# TC-E-01-5x5 — 행 5, 열 5
grid = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 1, 2, 3, 4],
    [5, 6, 7, 8, 9],
]
```

### 5.3 공통 기대 결과 (Boundary 단위)

모든 TC-E-01-* 케이스에 대해 Boundary 검증 결과는 다음 계약을 만족해야 한다.

```json
{
  "code": "INVALID_SIZE",
  "message": "Grid must be 4x4."
}
```

- pydantic `ErrorResponse` 모델로 역직렬화 가능해야 한다.
- HTTP/예외 throw가 아닌 **표준 오류 응답 객체 반환** (PRD §13 정책).
- 동일 입력에 대해 **결정적** 동일 출력 (NFR-04).

### 5.4 PRD 오류 코드 매핑 (참고)

| 본 계획 code | PRD §13 code | PRD message (한국어) |
|---|---|---|
| `INVALID_SIZE` | `ERR_INVALID_SIZE` | 입력 오류: 행렬 크기는 4x4여야 합니다. |

> 구현 시 code/message 중 하나를 프로젝트 표준으로 확정하고, 테스트와 pydantic 스키마를 단일 소스로 유지한다.

---

## 6. 예외 / 특이 케이스 목록

AC-FR01-01 크기 검증 경로에서 Boundary가 **안전하게 거부**해야 하는 추가 케이스이다. Domain resolver는 모두 **호출 금지**(AC-FR01-05).

| TC ID | 입력 | 특이점 | 기대 동작 | 우선순위 |
|---|---|---|---|---|
| **TC-X-01** | `"not a grid"` (str) | 타입 불일치 | `INVALID_SIZE` 또는 명시적 타입 오류 정책* | P2 |
| **TC-X-02** | `42` (int) | 스칼라 입력 | `INVALID_SIZE` 또는 타입 오류* | P2 |
| **TC-X-03** | `[[1,2,3,4], [5,6,7], [9,10,11,12], [13,14,15,16]]` | **ragged array** (행별 열 길이 불일치) | `INVALID_SIZE` | P2 |
| **TC-X-04** | `[[None, 2, 3, 4], ...]` (4×4 형태) | 셀 값 `None` — 크기 통과 후 범위 검증 대상** | 본 AC 범위: 크기 4×4이면 AC-FR01-01 통과 가능 → **AC-FR01-03 범위로 이관** | — |
| **TC-X-05** | `[[]] * 4` 후 `grid[0].append(1)` | 가변 공유 참조 (`[[]]*4` 함정) | 여전히 `INVALID_SIZE` (열 길이 불균일 또는 4×4 미달) | P2 |
| **TC-X-06** | `[[1,2,3,4]] * 4` | 행 참조 공유 (shallow copy) | 크기 4×4로 **통과** — AC-FR01-01 범위 외; FR-01 후속 규칙에서 처리 | — |
| **TC-X-07** | 빈 튜플 `()` | falsy 비-matrix | `INVALID_SIZE` | P2 |
| **TC-X-08** | `grid = [[]]` | 행 1개, 열 0개 | `INVALID_SIZE` | P2 |

\* **Decision Needed:** 타입 오류를 `INVALID_SIZE`에 흡수할지, 별도 `ERR_INVALID_TYPE`을 둘지 PRD 확정 전까지 **기본 정책은 `INVALID_SIZE`로 통일**하여 Boundary에서 조기 종료한다.

\** AC-FR01-01은 **구조적 크기**만 검증한다. 값 유효성은 AC-FR01-03(범위)에서 다룬다.

---

## 7. Domain resolver 진입점 호출 횟수 검증 전략

### 7.1 검증 대상

| 항목 | 설명 |
|---|---|
| **Domain 진입점** | `CompletionResolver.resolve(matrix)` (또는 PRD §18 `Solver` / Design Report `resolveCompletion`) |
| **오케스트레이터** | Control 계층 `MagicSquareService.solve(grid)` |
| **격리 AC** | AC-FR01-05 — FR-01 실패 시 Domain resolver **호출 금지** |

### 7.2 Mock / Spy 전략

#### 전략 A — Control 통합 단위 테스트 (권장, P0)

Control 계층 테스트에서 Domain resolver를 **주입 가능한 의존성**으로 두고 `unittest.mock.Mock` 또는 `MagicMock`을 주입한다.

| 단계 | 내용 |
|---|---|
| Arrange | `mock_resolver = Mock(spec=CompletionResolver)` 또는 `create_autospec(CompletionResolver, instance=True)` |
| Arrange | `service = MagicSquareService(validator=BoundaryValidator(), resolver=mock_resolver)` |
| Act | `result = service.solve(grid=None)` |
| Assert (응답) | `result.code == "INVALID_SIZE"` |
| Assert (호출) | `mock_resolver.resolve.assert_not_called()` |
| Assert (횟수) | `mock_resolver.resolve.call_count == 0` |

#### 전략 B — `patch` 데코레이터 (대안)

Control 내부 import 경로에 `@patch("src.control.magic_square_service.CompletionResolver")` 적용.

- **주의:** patch 대상은 **사용처 모듈**의 import 경로 (`where it's used`, not where it's defined).
- `assert_not_called()`로 AC-FR01-05 충족.

#### 전략 C — Spy (wraps) 패턴

실제 resolver 인스턴스를 유지하되 `resolve` 메서드만 spy.

```python
resolver = CompletionResolver()
with patch.object(resolver, "resolve", wraps=resolver.resolve) as spy:
    service = MagicSquareService(validator=validator, resolver=resolver)
    service.solve(grid=None)
    spy.assert_not_called()
```

- 크기 검증 실패 경로에서는 spy가 **한 번도 호출되지 않음**을 확인.
- Domain 단위 테스트(Track B)에서는 spy로 **정상 호출 1회**를 별도 검증.

### 7.3 테스트 ID ↔ Spy 매핑

| Control Test ID | grid 입력 | `resolve.call_count` 기대 |
|---|---|---|
| `CTL-UT-01` | `None` | **0** |
| `CTL-UT-02` | `[]` | **0** |
| `CTL-UT-03` | `[[]] * 4` | **0** |
| `CTL-UT-04` | 3×4 | **0** |
| `CTL-UT-05` | 4×3 | **0** |
| `CTL-UT-06` | 5×5 | **0** |

### 7.4 Mock 품질 규칙

- `spec=` 또는 `autospec=True`로 resolver API 표면만 노출 (오타 메서드 조기 발견).
- Boundary 테스트(`tests/boundary/`)에서는 Domain mock **사용하지 않음** — 순수 크기 검증만.
- Control 테스트(`tests/control/`)에서만 mock/spy 적용 — **레이어 책임 분리** 유지.
- `@pytest.fixture` `mock_resolver`를 `conftest.py`에 정의하여 P0~P1 테스트 재사용.

---

## 8. pydantic 스키마 계약 검증

Boundary 오류 응답은 pydantic 모델로 고정한다 (Track A Contract).

| 모델 (예정) | 필드 | 검증 |
|---|---|---|
| `ErrorResponse` | `code: str`, `message: str` | 필수, non-empty |
| `ErrorResponse` | `details: dict \| None` | 선택 (§12.2) |

**테스트 (`BND-UT-11`):**

- `ErrorResponse.model_validate({"code": "INVALID_SIZE", "message": "Grid must be 4x4."})` 성공
- `code` 누락, `message` 빈 문자열 → `ValidationError`

---

## 9. 커버리지 목표

PRD §14 NFR 기준:

| 대상 | 목표 | 측정 범위 (예정) |
|---|---|---|
| **Domain Logic** | **≥ 95%** | `src/domain/` |
| **Boundary Validation** | **≥ 85%** | `src/boundary/`, `src/control/` (검증·오케스트레이션) |
| **Project 전체** | **≥ 80%** | `src/` |

### 9.1 본 AC(FR-01-01) 최소 커버리지 기준

| 모듈 | 본 AC 완료 시 최소 line coverage |
|---|---|
| `boundary/validator.py` — `validate_size` 분기 | 100% (None, empty, wrong dims) |
| `control/magic_square_service.py` — early return 경로 | 100% (invalid size → no resolve) |

---

## 10. pytest-cov 측정 전략

### 10.1 설치

```bash
pip install pytest-cov
```

### 10.2 기본 실행 (전체)

```bash
pytest --cov=src --cov-report=term-missing
```

- `term-missing`: 미커버 라인을 터미널에 출력하여 Red → Green 루프에서 즉시 확인.

### 10.3 레이어별 실행 (권장)

```bash
# Boundary + Control (Track A — 본 계획)
pytest tests/boundary tests/control \
  --cov=src/boundary --cov=src/control \
  --cov-report=term-missing \
  --cov-fail-under=85

# Domain (Track B — 전체 게이트)
pytest tests/domain \
  --cov=src/domain \
  --cov-report=term-missing \
  --cov-fail-under=95
```

### 10.4 CI / 로컬 게이트 (권장 설정)

`pyproject.toml` 또는 `pytest.ini` (추가 예정):

```ini
[pytest]
testpaths = tests
markers =
    boundary: Boundary contract tests
    control: Control orchestration tests
    priority_p0: Must-pass gate

[coverage.run]
source = src
branch = true

[coverage.report]
fail_under = 80
show_missing = true
```

### 10.5 측정 시 주의사항

- **Boundary 테스트만 실행**할 때 Domain 95%는 달성되지 않음 — 레이어별 `--cov` 경로 분리 필수.
- mock/spy 테스트는 Control의 **분기 커버리지**에 기여; Domain resolver **실행 경로**는 Track B 테스트로 커버.
- `[[]] * 4` 등 특수 케이스는 **branch coverage**까지 확인 (`branch = true`).
- 커버리지 100%가 AC 충족을 대체하지 않음 — AC-FR01-05 mock assertion은 반드시 유지.

---

## 11. 테스트 데이터 및 Fixture 설계

### 11.1 공통 Fixture (`tests/conftest.py`)

| Fixture | 반환 | 용도 |
|---|---|---|
| `invalid_size_grids` | `list[None \| list]` | parametrize 소스 (§5.1 전체) |
| `expected_invalid_size_error` | `ErrorResponse` | 기대값 단일화 |
| `mock_resolver` | `Mock` | AC-FR01-05 호출 횟수 검증 |
| `boundary_validator` | `BoundaryValidator` | Boundary 단위 테스트 |

### 11.2 Parametrize 예시 (개념)

```python
@pytest.mark.parametrize(
    "grid",
    [None, [], [[]] * 4, grid_3x4, grid_4x3, grid_5x5],
    ids=["none", "empty", "empty_rows", "3x4", "4x3", "5x5"],
)
def test_invalid_size_returns_error(grid: object) -> None: ...
```

---

## 12. 완료 기준 (Exit Criteria)

| # | 기준 |
|---|---|
| 1 | §5 경계값 케이스 **전부** `INVALID_SIZE` 반환 (4×4 정상 입력 제외) |
| 2 | 각 invalid size 케이스에 대해 Domain `resolve` **call_count == 0** |
| 3 | pydantic `ErrorResponse` 계약 테스트 통과 |
| 4 | Boundary/Control `--cov-fail-under=85` 통과 |
| 5 | Traceability: AC-FR01-01, AC-FR01-05 ↔ 테스트 ID 매핑 문서화 완료 |
| 6 | Red → Green → Refactor 순서 준수, 테스트 삭제/약화 없음 |

---

## 13. 리스크 및 완화

| 리스크 | 영향 | 완화 |
|---|---|---|
| `[[]]*4` 가변성 함정 | false pass/ fail | TC-X-05 별도 검증 |
| code 표기 불일치 (`INVALID_SIZE` vs `ERR_INVALID_SIZE`) | 계약 drift | §5.4 매핑 테이블 + 단일 enum 상수 |
| patch 경로 오류 | spy 미작동 | import 경로 리뷰, `spec=` mock |
| 4×4 정상 입력 혼입 | AC 범위 오염 | 본 계획 §5 명시적 제외, 코드 리뷰 체크리스트 |

---

## 14. 부록 — Gherkin 시나리오 (Scenario-G3)

```gherkin
Feature: FR-01 Input Verification — Invalid Size

  Scenario: grid is None
    Given the input grid is None
    When the Boundary validator performs size verification
    Then the response code is "INVALID_SIZE"
    And the response message is "Grid must be 4x4."
    And the Domain resolver is not invoked

  Scenario Outline: grid dimensions are not 4x4
    Given the input grid is <grid_description>
    When the application receives a solve request
    Then the response code is "INVALID_SIZE"
    And the Domain resolver call count is 0

    Examples:
      | grid_description      |
      | empty list            |
      | four empty rows       |
      | 3 rows by 4 columns   |
      | 4 rows by 3 columns |
      | 5 rows by 5 columns |
```

---

## 15. 변경 이력

| 버전 | 일자 | 변경 내용 |
|---|---|---|
| 1.0 | 2026-05-29 | AC-FR01-01 샘플 예제 기반 초안 작성 |
