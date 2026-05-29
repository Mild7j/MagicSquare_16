# PRD — Magic Square 4x4 TDD Practice

## 1. Executive Summary
Magic Square 4x4 프로젝트의 목표는 정답 탐색 자체가 아니라, 불변식 기반 사고와 계약 기반 개발을 훈련 가능한 방식으로 고정하는 것이다. 본 PRD는 구현 이전 기준 문서로서 입력/출력 계약, Boundary/Domain 분리, Dual-Track UI + Logic TDD, RED-GREEN-REFACTOR 절차, 그리고 Concept-to-Code Traceability를 명시한다. 모든 요구사항은 테스트 가능한 문장으로 정의하며, 본 문서의 요구사항 위반은 구현 완료 기준 미달로 판정한다.

---

## 2. Background
학습자는 마방진 문제를 풀 때 구현을 먼저 시작하고, 이후 테스트를 덧붙이는 방식으로 진행하는 경향이 있다. 이 접근은 판정 기준이 고정되지 않아 회귀 검증이 불가능해지고, Boundary와 Domain 책임이 혼합되어 변경 비용이 증가한다.  
본 프로젝트는 4x4 마방진을 대상으로 요구-계약-검증의 연결을 먼저 확정한다. 프로젝트는 UI/DB/Web 의존 없이 순수 로직 중심으로 진행하며, 테스트가 설계를 구속하는 방식으로 품질을 유지한다.

---

## 3. Problem Statement
문제는 “마방진을 만든다”가 아니다. 문제는 “4x4 입력에 대해 불변식을 판정하고, 판정 가능한 계약 결과를 일관되게 반환한다”이다.  
핵심은 다음 두 가지다.

1. 입력 계약 고정: 어떤 입력이 유효하고 어떤 입력이 거부되는지 사전에 고정한다.  
2. 출력 계약 고정: 어떤 순서와 형식으로 결과를 반환하며 어떤 실패 코드를 반환하는지 사전에 고정한다.

이 프로젝트는 완성된 격자 한 장을 목표로 하지 않고, **검증 가능한 기준의 재현성**을 목표로 한다.

---

## 4. Why Now / Why Chain
현재 학습 흐름에서 반복적으로 발생하는 문제는 다음과 같다.

- 구현 먼저 시작하여 테스트가 요구사항을 추적하지 못한다.
- 테스트 기준이 불명확하여 동일 입력의 기대 결과가 고정되지 않는다.
- Boundary와 Domain 책임이 섞여 리팩토링 시 계약이 손상된다.
- 리팩토링 이후 출력 형식과 오류 정책이 변경되어 회귀가 발생한다.

지금 이 프로젝트를 수행해야 하는 이유는 다음과 같다.

- 불변식(합 34, 값 집합, 구조 규칙)을 먼저 문서화하면 요구사항이 측정 가능해진다.
- 계약 기반 TDD를 적용하면 실패 원인과 수정 범위를 분리할 수 있다.
- Dual-Track 방식으로 UI 계약과 Domain 규칙을 병렬 관리하면 구조적 혼합을 방지할 수 있다.

---

## 5. Target Users
- TDD 학습자
- 코드 리뷰어
- Clean Architecture + ECB 분리를 훈련하는 개발자

사용 환경:
- 콘솔 실행 또는 테스트 실행 중심
- 실제 UI 화면, DB, Web/API 서버는 범위 밖

---

## 6. Vision & Epic Goal
**Vision:** 불변식 기반 사고를 실천 가능한 개발 습관으로 고정한다.  
**Epic Goal:** “불변식 기반 사고 훈련 시스템 구축”

Epic 성공 기준:
- Domain 규칙과 Boundary 계약이 분리된 상태로 유지된다.
- 핵심 불변식마다 검증 경로가 존재한다.
- 리팩토링 이후 외부 계약이 변경되지 않는다.
- Traceability(Concept → Rule → Use Case → Contract → Test → Component)가 문서에서 확인 가능하다.

---

## 7. Persona
### Persona A — TDD 학습 개발자
- 목표: 실패 테스트로 요구사항을 고정하고 최소 구현으로 통과시킨다.
- 어려움: 구현 선행으로 인해 Red 단계가 생략된다.

### Persona B — 아키텍처 분리 학습자
- 목표: Boundary와 Domain 책임을 분리한다.
- 어려움: 입력 검증과 도메인 판단 로직이 혼합된다.

### Persona C — 리뷰 중심 개발자
- 목표: 계약 위반을 빠르게 식별한다.
- 어려움: 요구사항 문서와 테스트 간 연결이 약하다.

---

## 8. User Journey Summary

| Stage | Pain Point | Learning Outcome |
|---|---|---|
| 문제 인식 | “정답 찾기”와 “검증 시스템 구축”이 혼합됨 | 프로젝트 목표를 검증 가능성으로 재정의 |
| 계약 정의 | 입력/출력/오류 형식이 합의되지 않음 | 고정 계약과 실패 정책을 명시 |
| 도메인 분리 | Boundary 검증과 Domain 판단이 섞임 | 레이어 책임과 의존 방향 고정 |
| Dual-Track TDD 진행 | UI 테스트와 로직 테스트가 순차적으로 밀림 | Track A/Track B 병렬 Red-Green 적용 |
| 회귀 보호 | 리팩토링 후 외부 계약이 변형됨 | 계약 테스트와 불변식 테스트로 회귀 차단 |

---

## 9. Scope

### 9.1 In-Scope
- 빈칸 좌표 탐색
- 누락 숫자 탐색
- 마방진 판정
- 두 조합 시도 후 결과 반환
- Boundary 계층 입력 검증
- 출력 계약 검증
- RED-GREEN-REFACTOR에 맞춘 테스트 가능 요구사항 정의

### 9.2 Out-of-Scope
- UI 화면 개발
- DB 저장/검색
- Web/API 서버 개발
- N×N 일반화
- 완전한 마방진 생성 알고리즘
- 사용자 인증/권한
- 네트워크 오류 처리
- QR 스캔
- 외부 서비스 연동

---

## 10. Functional Requirements

### FR-01 Input Verification (Boundary)
- Description: Boundary는 입력 행렬 계약을 검증한다.
- Layer: Boundary
- Input: `int[][] matrix`
- Processing Rules:
  - 행렬 크기는 4x4여야 한다.
  - `0`의 개수는 정확히 2개여야 한다.
  - 값은 `0` 또는 `1~16`이어야 한다.
  - `0`을 제외한 값은 중복되면 안 된다.
- Output:
  - 성공: 검증 통과 상태
  - 실패: 정의된 오류 코드와 메시지
- Acceptance Criteria:
  - AC-FR01-01: 4x4가 아닌 입력은 `ERR_INVALID_SIZE`를 반환한다.
  - AC-FR01-02: 빈칸 개수가 2개가 아니면 `ERR_INVALID_BLANK_COUNT`를 반환한다.
  - AC-FR01-03: 범위 위반 값이 있으면 `ERR_OUT_OF_RANGE`를 반환한다.
  - AC-FR01-04: 0 제외 중복 값이 있으면 `ERR_DUPLICATE_NON_ZERO`를 반환한다.
  - AC-FR01-05: FR-01 실패 시 Domain resolver를 호출하지 않는다.
- Error / Exception Policy: Boundary 오류 응답 반환
- Related Business Rules: BR-01, BR-02, BR-03, BR-04
- Related Test Direction: 계약 기반 입력 거부 테스트, resolver 미호출 테스트
- Component Candidate: `BoundaryValidator`

### FR-02 Blank Coordinate Discovery
- Description: Domain은 두 개의 빈칸 좌표를 row-major 순서로 탐색한다.
- Layer: Domain
- Input: FR-01 통과 행렬
- Processing Rules:
  - 0 위치 두 개를 탐색한다.
  - 좌표 순서는 row-major를 따른다.
- Output: `(r1, c1), (r2, c2)` (내부 표현)
- Acceptance Criteria:
  - AC-FR02-01: 첫 번째 좌표는 row-major 기준 첫 번째 0의 위치다.
  - AC-FR02-02: 두 번째 좌표는 row-major 기준 두 번째 0의 위치다.
- Error / Exception Policy: FR-01 사전 검증 전제
- Related Business Rules: BR-05
- Related Test Direction: 좌표 순서 결정성 테스트
- Component Candidate: `BlankFinder`

### FR-03 Missing Number Discovery
- Description: Domain은 누락된 숫자 2개를 계산하고 오름차순으로 반환한다.
- Layer: Domain
- Input: FR-01 통과 행렬
- Processing Rules:
  - 기준 집합은 `{1..16}`이다.
  - 입력 비영(0 제외) 집합의 보완집합을 계산한다.
  - 결과는 오름차순으로 정렬한다.
- Output: `small, large`
- Acceptance Criteria:
  - AC-FR03-01: 누락 숫자는 정확히 2개다.
  - AC-FR03-02: 반환 순서는 오름차순이다.
- Error / Exception Policy: FR-01 사전 검증 전제
- Related Business Rules: BR-06, BR-07
- Related Test Direction: 누락 숫자 계산 및 정렬 테스트
- Component Candidate: `MissingNumberFinder`

### FR-04 Magic Square Validation
- Description: Domain은 완성 후보가 마방진 불변식을 만족하는지 판정한다.
- Layer: Domain
- Input: 0이 없는 4x4 후보 행렬
- Processing Rules:
  - 모든 행 합은 34여야 한다.
  - 모든 열 합은 34여야 한다.
  - 두 대각선 합은 34여야 한다.
- Output: `true | false`
- Acceptance Criteria:
  - AC-FR04-01: 조건 만족 시 `true`를 반환한다.
  - AC-FR04-02: 하나라도 위반 시 `false`를 반환한다.
- Error / Exception Policy: 판정 결과 boolean 반환
- Related Business Rules: BR-08, BR-09
- Related Test Direction: 합 규칙 만족/위반 판정 테스트
- Component Candidate: `MagicSquareValidator`

### FR-05 Two-Combination Solver and Result Formatting
- Description: Domain은 두 조합을 순서대로 시도하고 성공 조합을 반환 형식으로 고정한다.
- Layer: Domain + Boundary Formatting
- Input: FR-01 통과 행렬
- Processing Rules:
  - Attempt 1: `small -> blank1`, `large -> blank2`
  - Attempt 2: Attempt 1 실패 시 `large -> blank1`, `small -> blank2`
  - 성공한 첫 조합의 순서로 결과를 구성한다.
- Output:
  - 성공: `int[6] = [r1, c1, n1, r2, c2, n2]` (1-index)
  - 실패: `ERR_UNSOLVABLE`
- Acceptance Criteria:
  - AC-FR05-01: Attempt 1 성공 시 Attempt 1 순서 결과를 반환한다.
  - AC-FR05-02: Attempt 1 실패, Attempt 2 성공 시 Attempt 2 순서 결과를 반환한다.
  - AC-FR05-03: 두 조합 모두 실패 시 `ERR_UNSOLVABLE`를 반환한다.
  - AC-FR05-04: 성공 결과 길이는 6이고 좌표는 1-index다.
- Error / Exception Policy:
  - **확정 정책:** 실패는 예외 throw가 아니라 표준 오류 응답(`ERR_UNSOLVABLE`)으로 반환한다.
- Related Business Rules: BR-10, BR-11, BR-12, BR-13
- Related Test Direction: 조합 우선순위, 실패 정책, 출력 포맷 테스트
- Component Candidate: `Solver`, `ResultFormatter`

---

## 11. Business Rules / Domain Rules

- **BR-01:** 입력 행렬은 항상 4행 4열이어야 한다.
- **BR-02:** 입력 내 값 `0`의 개수는 항상 2개여야 한다.
- **BR-03:** 각 셀 값은 항상 `0` 또는 `1~16`이어야 한다.
- **BR-04:** `0`을 제외한 숫자는 항상 중복되면 안 된다.
- **BR-05:** 첫 번째 빈칸은 항상 row-major 순서에서 첫 번째 `0`의 좌표다.
- **BR-06:** 누락 숫자는 항상 정확히 2개여야 한다.
- **BR-07:** 누락 숫자 반환 순서는 항상 오름차순이어야 한다.
- **BR-08:** 마방진 상수는 항상 `34`다.
- **BR-09:** 완성 후보는 모든 행/열/대각선 합이 항상 `34`여야 한다.
- **BR-10:** Solver는 항상 Attempt 1을 먼저 평가해야 한다.
- **BR-11:** Attempt 1 실패 시 Solver는 항상 Attempt 2를 평가해야 한다.
- **BR-12:** 성공 출력 좌표는 항상 1-index여야 한다.
- **BR-13:** 성공 출력 형식은 항상 `int[6]`이며 `[r1,c1,n1,r2,c2,n2]` 순서를 유지해야 한다.

---

## 12. Input / Output Contract

### 12.1 Input Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code 또는 Failure Policy |
|---|---|---|---|---|---|
| matrix | `int[][]` | 크기 4x4 고정 | `[[16,2,0,13],[5,11,10,8],[9,7,6,0],[4,14,15,1]]` | `[[1,2],[3,4]]` | `ERR_INVALID_SIZE` |
| blank count | derived | `0` 개수는 2 | 위 valid 예시에서 `0` 2개 | `0`이 1개 또는 3개 | `ERR_INVALID_BLANK_COUNT` |
| value range | each cell | 값은 `0` 또는 `1~16` | `0`, `1`, `16` | `-1`, `17` | `ERR_OUT_OF_RANGE` |
| non-zero uniqueness | derived | `0` 제외 값 중복 금지 | 비영 값 모두 유일 | `5`가 두 번 등장 | `ERR_DUPLICATE_NON_ZERO` |
| first blank definition | derived | row-major 첫 번째 `0` | (1,3)이 첫 `0` | 임의 순서 선택 | 계약 위반(테스트 실패) |

### 12.2 Output Contract

| Field / Item | Type | Rule | Valid Example | Invalid Example | Related Error Code 또는 Failure Policy |
|---|---|---|---|---|---|
| result | `int[6]` | 길이 6 고정 | `[1,3,3,3,4,12]` | `[1,3,3]` | 계약 위반(테스트 실패) |
| coordinate index | `int` | 좌표는 1-index | `r=1,c=4` | `r=0,c=3` | 계약 위반(테스트 실패) |
| ordering | tuple order | `[r1,c1,n1,r2,c2,n2]` | `[1,1,16,4,4,1]` | `[n1,r1,c1,n2,r2,c2]` | 계약 위반(테스트 실패) |
| failure response | error object | 실패 시 표준 오류 코드 반환 | `{code:"ERR_UNSOLVABLE",...}` | 빈 배열 반환 | `ERR_UNSOLVABLE` |

---

## 13. Error / Failure Policy

| Case | Error Code | Message | Layer | Domain resolver 호출 여부 | Related Acceptance Criteria |
|---|---|---|---|---|---|
| 4x4 아님 | `ERR_INVALID_SIZE` | 입력 오류: 행렬 크기는 4x4여야 합니다. | Boundary | 호출 금지 | AC-FR01-01, AC-FR01-05 |
| 빈칸 개수 오류 | `ERR_INVALID_BLANK_COUNT` | 입력 오류: 빈칸(0)은 정확히 2개여야 합니다. | Boundary | 호출 금지 | AC-FR01-02, AC-FR01-05 |
| 값 범위 위반 | `ERR_OUT_OF_RANGE` | 입력 오류: 값은 0 또는 1~16이어야 합니다. | Boundary | 호출 금지 | AC-FR01-03, AC-FR01-05 |
| 0 제외 중복 | `ERR_DUPLICATE_NON_ZERO` | 입력 오류: 0을 제외한 숫자는 중복될 수 없습니다. | Boundary | 호출 금지 | AC-FR01-04, AC-FR01-05 |
| 두 조합 모두 실패 | `ERR_UNSOLVABLE` | 도메인 오류: 주어진 조건으로 마방진을 완성할 수 없습니다. | Domain 결과를 Boundary가 표준화 | 호출 필요(검증 통과 후) | AC-FR05-03 |

**정책 확정:** 입력 검증 실패는 Boundary에서 종료한다. Domain resolver는 호출하지 않는다.

---

## 14. Non-Functional Requirements

- **NFR-01 Coverage (Domain):** Domain Logic 테스트 커버리지는 95% 이상이어야 한다.
- **NFR-02 Coverage (Boundary):** Boundary Validation 테스트 커버리지는 85% 이상이어야 한다.
- **NFR-03 Coverage (Project Gate):** 전체 프로젝트 커버리지는 80% 이상이어야 한다.
- **NFR-04 Determinism:** 동일 입력은 항상 동일 출력 또는 동일 오류 코드를 반환해야 한다.
- **NFR-05 No Side Effects:** 입력 행렬은 처리 전후 동일해야 하며 함수 외부 상태를 변경하면 안 된다.
- **NFR-06 Performance:** 4x4 단일 실행은 50ms 이내에 완료되어야 한다.
- **NFR-07 Maintainability:** Boundary와 Domain 책임을 분리해야 한다.
- **NFR-08 Maintainability:** 설명 없는 매직 넘버를 금지하고 명명된 상수를 사용해야 한다.

---

## 15. Dual-Track TDD Strategy

### 15.1 Track A — Boundary / UI Contract TDD
- 입력 검증 실패 케이스를 Red로 먼저 고정한다.
- 성공 경로의 출력 형식을 계약 테스트로 고정한다.
- 실패 응답 코드/메시지 고정 테스트를 포함한다.
- FR-01 실패 케이스에서 Domain resolver 미호출을 검증한다.

### 15.2 Track B — Domain / Logic TDD
- 빈칸 탐색 규칙(row-major)을 Red로 고정한다.
- 누락 숫자 계산 및 오름차순 반환을 Red로 고정한다.
- 마방진 판정 규칙(행/열/대각선, 상수 34)을 Red로 고정한다.
- Attempt 1 성공, Attempt 2 성공, 양쪽 실패를 각각 독립 테스트로 고정한다.

### 15.3 Parallel Progression Rules
- UI Red와 Logic Red를 분리한다.
- UI Green과 Logic Green은 각각 최소 구현만 허용한다.
- 구조 개선은 Refactor 단계에서만 수행한다.
- Domain 전량 구현 후 Boundary를 연결하는 일괄 방식은 금지한다.
- 테스트 삭제/완화로 통과시키는 행위는 금지한다.

---

## 16. Test Plan / QA

### 16.1 Normal Scenarios
- TC-N-01: small-first 성공
- TC-N-02: small-first 실패 후 reverse 성공

### 16.2 Exception Scenarios
- TC-E-01: invalid size
- TC-E-02: invalid blank count
- TC-E-03: invalid range
- TC-E-04: duplicate non-zero
- TC-E-05: both combinations fail (`ERR_UNSOLVABLE`)

### 16.3 Boundary Scenarios
- TC-B-01: 최소값 1 포함
- TC-B-02: 최대값 16 포함
- TC-B-03: 0은 빈칸으로만 해석
- TC-B-04: 출력 좌표 1-index
- TC-B-05: 반환 배열 길이 6

### 16.4 Representative Test Data

| Test Data ID | Purpose | Matrix (4x4) | Expected |
|---|---|---|---|
| TD-01 | small-first 성공 | `[[16,2,0,13],[5,11,10,8],[9,7,6,0],[4,14,15,1]]` | 성공, Attempt 1 경로 |
| TD-02 | reverse 성공 | `[[0,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,0]]` | 성공, Attempt 2 경로 |
| TD-03 | invalid size | `[[1,2],[3,4]]` | `ERR_INVALID_SIZE` |
| TD-04 | invalid blank count | `[[16,2,3,13],[5,11,10,8],[9,7,6,12],[4,14,15,1]]` | `ERR_INVALID_BLANK_COUNT` |
| TD-05 | duplicate value | `[[16,2,0,13],[5,11,10,8],[9,7,6,0],[4,14,15,16]]` | `ERR_DUPLICATE_NON_ZERO` |
| TD-06 | invalid range | `[[16,2,0,13],[5,11,10,8],[9,7,6,0],[4,14,15,17]]` | `ERR_OUT_OF_RANGE` |

---

## 17. Architecture Overview, High-Level

### Boundary Layer
- 입력 검증 수행
- 오류 응답 표준화
- 성공 출력 형식 변환

### Domain Layer
- 빈칸 탐색
- 누락 숫자 계산
- 마방진 판정
- 두 조합 시도 및 성공 경로 결정

### Control / Application Layer
- Boundary와 Domain 호출 흐름 조정
- 요청/응답 수명주기 오케스트레이션

의존 방향:
- Boundary → Control → Domain
- Domain은 Boundary를 참조하지 않는다.
- Domain은 UI, DB, Web, 파일 시스템에 의존하지 않는다.

---

## 18. Component Candidates

| Component | Responsibility | Layer | Input | Output | Related FR | Related Test |
|---|---|---|---|---|---|---|
| `BoundaryValidator` | 입력 계약 검증 및 사전 거부 | Boundary | `int[][]` | 검증 통과/오류코드 | FR-01 | TC-E-01~04 |
| `BlankFinder` | row-major 빈칸 2개 좌표 탐색 | Domain | 검증 통과 행렬 | 빈칸 좌표 2개 | FR-02 | TC-B-03, TC-N-01 |
| `MissingNumberFinder` | 누락 숫자 2개 계산 및 정렬 | Domain | 검증 통과 행렬 | `small, large` | FR-03 | TC-N-01, TC-N-02 |
| `MagicSquareValidator` | 합 34 불변식 판정 | Domain | 완성 후보 행렬 | `true/false` | FR-04 | TC-N-01, TC-N-02, TC-E-05 |
| `Solver` | Attempt 1/2 순서 시도 및 경로 선택 | Domain | 검증 통과 행렬 | 성공 결과 또는 `ERR_UNSOLVABLE` | FR-05 | TC-N-01, TC-N-02, TC-E-05 |
| `ResultFormatter` | `int[6]`, 1-index 출력 계약 고정 | Boundary | 성공 경로 결과 | `[r1,c1,n1,r2,c2,n2]` | FR-05 | TC-B-04, TC-B-05 |

---

## 19. Risks & Ambiguities

| Risk | Impact | Decision / Mitigation |
|---|---|---|
| 1-index/0-index 혼동 | 출력 계약 위반 | BR-12 고정, TC-B-04 필수 |
| row-major 첫 빈칸 정의 누락 | Solver 결과 순서 불일치 | BR-05 고정, FR-02 AC 필수 |
| small-first/reverse 데이터 혼동 | 테스트 오검출 | TD-01/TD-02 고정, 케이스 분리 |
| 입력 행렬 변경 여부 불명확 | 부작용 회귀 발생 | NFR-05 고정(입력 불변) |
| 두 조합 실패 정책 누락 | 실패 처리 분기 붕괴 | `ERR_UNSOLVABLE` 반환으로 확정 |
| 상수 34 하드코딩 남용 | 변경 취약성과 가독성 저하 | BR-08 + NFR-08로 상수 명명 고정 |
| Boundary/Domain 책임 혼합 | 계층 의존 위반 | 아키텍처 규칙 및 FR 레이어 고정 |

---

## 20. Engineering Principles

- Python 3.10+ 기준
- PEP8 준수
- 모든 함수에 타입힌트 명시
- public 함수/메서드 docstring 관리
- `pytest` 사용
- AAA 패턴 사용
- Coverage 목표 준수(95/85/80)
- ECB 계층 분리 준수
- RED-GREEN-REFACTOR 순서 준수
- `print()` 디버깅 금지
- bare `except` 금지
- 테스트 약화/삭제 금지
- 설명 없는 magic number 금지

---

## 21. Traceability Matrix

| Concept / Invariant | Business Rule | Feature ID | Acceptance Criteria | Test Case Candidate | Component |
|---|---|---|---|---|---|
| 4x4 입력 | BR-01 | FR-01 | AC-FR01-01 | TC-E-01 | BoundaryValidator |
| 빈칸 2개 | BR-02 | FR-01 | AC-FR01-02 | TC-E-02 | BoundaryValidator |
| 값 범위 0 또는 1~16 | BR-03 | FR-01 | AC-FR01-03 | TC-E-03 | BoundaryValidator |
| 중복 금지(0 제외) | BR-04 | FR-01 | AC-FR01-04 | TC-E-04 | BoundaryValidator |
| row-major 첫 번째 빈칸 | BR-05 | FR-02 | AC-FR02-01 | TC-N-01 | BlankFinder |
| 누락 숫자 2개 | BR-06 | FR-03 | AC-FR03-01 | TC-N-01 | MissingNumberFinder |
| 누락 숫자 오름차순 | BR-07 | FR-03 | AC-FR03-02 | TC-N-01, TC-N-02 | MissingNumberFinder |
| 마방진 상수 34 | BR-08 | FR-04 | AC-FR04-01 | TC-N-01, TC-N-02 | MagicSquareValidator |
| 행/열/대각선 합 | BR-09 | FR-04 | AC-FR04-02 | TC-E-05 | MagicSquareValidator |
| small-first 시도 | BR-10 | FR-05 | AC-FR05-01 | TC-N-01 | Solver |
| reverse 시도 | BR-11 | FR-05 | AC-FR05-02 | TC-N-02 | Solver |
| int[6] 반환 | BR-13 | FR-05 | AC-FR05-04 | TC-B-05 | ResultFormatter |
| 1-index 좌표 | BR-12 | FR-05 | AC-FR05-04 | TC-B-04 | ResultFormatter |

---

## 22. Open Questions / Decision Needed

- **Decision Needed 01:** 문서 참조명 정규화 필요  
  - 현재 실파일명과 참조 문서 번호 체계(1~4)가 다르다. PRD 본문의 공식 참조 표기 규칙을 확정해야 한다.
- **Decision Needed 02:** 커버리지 게이트 우선순위 확정 필요  
  - 레이어별 목표(95/85)와 프로젝트 최소(80) 중 CI 차단 기준을 어떤 레벨로 적용할지 확정해야 한다.
- **Decision Needed 03:** 성능 측정 기준 확정 필요  
  - 50ms 기준 측정 환경(로컬 단일 스레드, 반복 횟수, warm-up 여부)을 QA 기준으로 확정해야 한다.

---

## 23. Appendix

### 23.1 참고 문서 목록
- `Report/Problem-Definition-Report.md`
- `Report/MagicSquare_4x4_Journey_Levels_1_to_5.md`
- `Report/MagicSquare_4x4_TDD_Design_Report.md`
- `Report/CursorRules_UserEntity_Work_Report.md`
- `.cursorrules`
- `.cursor/rules/*.mdc`

### 23.2 Cursor Rules 요약
- ECB 계층 분리 및 의존 방향 고정
- TDD 단계 준수(Red → Green → Refactor)
- pytest + AAA 사용
- 타입힌트/문서화 규칙 준수
- 금지 패턴(`print()`, bare except, 설명 없는 매직 넘버) 차단

### 23.3 대표 Gherkin Scenario 요약
- Scenario-G1: Given 유효 입력, When small-first 성립, Then Attempt 1 순서 결과 반환
- Scenario-G2: Given 유효 입력, When small-first 불성립 and reverse 성립, Then Attempt 2 순서 결과 반환
- Scenario-G3: Given invalid size, When 검증 수행, Then `ERR_INVALID_SIZE` 반환 및 Domain 미호출
- Scenario-G4: Given 유효 입력, When 두 조합 모두 불성립, Then `ERR_UNSOLVABLE` 반환

### 23.4 향후 RED Test ID 후보
- RED-BND-01 size 검증 실패
- RED-BND-02 blank count 검증 실패
- RED-BND-03 range 검증 실패
- RED-BND-04 duplicate 검증 실패
- RED-BND-05 resolver 미호출 검증
- RED-DOM-01 row-major blank 탐색
- RED-DOM-02 missing numbers 오름차순
- RED-DOM-03 magic sum 판정
- RED-DOM-04 small-first 성공
- RED-DOM-05 reverse 성공
- RED-DOM-06 unsolvable 실패 정책
