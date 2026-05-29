# Magic Square 4x4 - Dual-Track TDD & Clean Architecture 설계 보고서

## 문서 메타
- 프로젝트: Magic Square (4x4)
- 목적: 알고리즘 난이도보다 레이어 분리, 계약 기반 테스트, 리팩토링 훈련
- 범위: 설계/계약/테스트/통합 계획만 포함 (구현 코드 제외)

---

# 1) Logic Layer (Domain Layer) 설계
## 1.1 도메인 개념
- **Entity: `MagicSquareCandidate`**
  - 책임: 4x4 행렬 상태를 보유하고 도메인 검증 대상 제공
- **Value Object: `CellPosition`**
  - 책임: 1-index 좌표 표현 (`row`, `col`) 및 동일성 비교
- **Value Object: `MissingPair`**
  - 책임: 누락 숫자 2개를 오름차순(`small`, `large`)으로 보관
- **Value Object: `CompletionPlan`**
  - 책임: 최종 출력 `[r1,c1,n1,r2,c2,n2]` 전달
- **Domain Service: `MatrixInvariantValidator`**
  - 책임: 입력 계약(크기/범위/중복/빈칸 개수) 검증
- **Domain Service: `BlankLocator`**
  - 책임: 0 위치 2개를 row-major 순으로 추출
- **Domain Service: `MissingNumberFinder`**
  - 책임: 1~16 기준 누락 숫자 2개 계산
- **Domain Service: `MagicSquareJudge`**
  - 책임: 완성 행렬의 마방진 성립 여부 판정
- **Domain Service: `CompletionResolver`**
  - 책임: 두 조합(A/B)을 시도해 계약에 맞는 출력 순서 결정

## 1.2 도메인 불변조건(Invariants)
- 행렬 크기는 항상 4x4이다.
- 값 범위는 0 또는 1~16이다.
- 0의 개수는 정확히 2개다.
- 0을 제외한 값은 중복되지 않는다.
- 완성 후보는 1~16을 정확히 1회씩 포함해야 한다.
- 마방진 성립 조건: 모든 행/열/대각선 합이 34이다.
- 출력 길이는 항상 6이며 좌표는 1-index다.
- 두 빈칸 좌표 순서는 row-major로 고정한다.
- 숫자 순서 규칙:
  - A 조합: `small -> blank1`, `large -> blank2`가 성립하면 채택
  - 아니면 B 조합: `large -> blank1`, `small -> blank2` 채택
  - 둘 다 실패하면 `ERR_UNSOLVABLE`

## 1.3 핵심 유스케이스(도메인 관점)
- 입력 검증
- 빈칸 찾기
- 누락 숫자 찾기
- 마방진 판정
- 두 조합 시도 후 출력 결정

## 1.4 Domain API(내부 계약)
- `validateInput(matrix) -> ValidationResult`
  - 입력: `int[4][4]`
  - 출력: `{isValid:boolean, errorCode?:string}`
  - 실패조건: 크기/범위/중복/빈칸 개수 위반
- `locateBlanks(matrix) -> [CellPosition, CellPosition]`
  - 출력: row-major 기준 두 좌표
- `findMissingNumbers(matrix) -> MissingPair`
  - 출력: 오름차순 누락 숫자 2개
- `isMagicSquare(matrix) -> boolean`
  - 입력: 0이 없는 완성 행렬
- `resolveCompletion(matrix) -> CompletionPlan | DomainError`
  - 출력: `[r1,c1,n1,r2,c2,n2]`
  - 실패조건: A/B 모두 불성립

## 1.5 Domain 단위 테스트 설계(RED 우선)
| ID | 테스트명 | 기대 결과 | 보호 Invariant |
|---|---|---|---|
| D-RED-01 | 크기 검증 실패 | `ERR_INVALID_SIZE` | 4x4 고정 |
| D-RED-02 | 빈칸 개수 실패 | `ERR_INVALID_BLANK_COUNT` | 빈칸 2개 |
| D-RED-03 | 값 범위 실패 | `ERR_OUT_OF_RANGE` | 값 범위 |
| D-RED-04 | 중복 실패 | `ERR_DUPLICATE_NON_ZERO` | 중복 금지 |
| D-RED-05 | 빈칸 순서 검증 | row-major 좌표 반환 | 좌표 결정성 |
| D-RED-06 | 누락 숫자 검증 | 오름차순 2개 반환 | 누락 계산 |
| D-RED-07 | A 조합 성공 | A 규칙대로 출력 | 순서 규칙 |
| D-RED-08 | B 조합 성공 | B 규칙대로 출력 | 순서 규칙 |
| D-RED-09 | 불가능 케이스 | `ERR_UNSOLVABLE` | 실패 명확성 |
| D-RED-10 | 마방진 판정 | true/false 정확 반환 | 합=34 규칙 |

---

# 2) Screen Layer (UI Layer) 설계 (Boundary Layer)
## 2.1 사용자/호출자 관점 시나리오
1. 호출자가 4x4 `int[][]` 입력
2. UI Boundary가 스키마 검증
3. 성공 시 Domain 유스케이스 호출
4. 결과를 `int[6]`으로 직렬화
5. 실패 시 표준 에러 스키마 반환

## 2.2 UI 계약(외부 계약)
- **Input schema**
  - 4x4 `int[][]`
  - 값: 0 또는 1~16
  - 0은 정확히 2개
  - 0 제외 중복 금지
- **Output schema**
  - `int[6]`
  - `[r1,c1,n1,r2,c2,n2]`
  - 좌표는 1-index
- **Error schema**
  - `error.code`, `error.message`, `error.details?`

## 2.3 UI 레벨 테스트(Contract-first, RED 우선)
| ID | 테스트명 | Domain Mock | 기대 결과 |
|---|---|---|---|
| UI-RED-01 | 크기 오류 | 호출 안 함 | `ERR_INVALID_SIZE` |
| UI-RED-02 | 빈칸 개수 오류 | 호출 안 함 | `ERR_INVALID_BLANK_COUNT` |
| UI-RED-03 | 범위 오류 | 호출 안 함 | `ERR_OUT_OF_RANGE` |
| UI-RED-04 | 중복 오류 | 호출 안 함 | `ERR_DUPLICATE_NON_ZERO` |
| UI-RED-05 | 성공 포맷 검증 | 성공 응답 | 길이 6, int, 1-index |
| UI-RED-06 | 도메인 실패 매핑 | `ERR_UNSOLVABLE` | Error schema 일치 |

## 2.4 UX/출력 규칙
- 에러 메시지는 코드별 고정 문구 사용
- 메시지 형식: `입력 오류: <원인>.`
- 표준 문구:
  - `ERR_INVALID_SIZE`: 입력 오류: 행렬 크기는 4x4여야 합니다.
  - `ERR_INVALID_BLANK_COUNT`: 입력 오류: 빈칸(0)은 정확히 2개여야 합니다.
  - `ERR_OUT_OF_RANGE`: 입력 오류: 값은 0 또는 1~16이어야 합니다.
  - `ERR_DUPLICATE_NON_ZERO`: 입력 오류: 0을 제외한 숫자는 중복될 수 없습니다.
  - `ERR_UNSOLVABLE`: 도메인 오류: 주어진 조건으로 마방진을 완성할 수 없습니다.

---

# 3) Data Layer 설계 (Data Layer)
## 3.1 목적 정의
- 학습용 저장/로드 인터페이스 분리 훈련
- 입력 행렬 저장/로드, 결과 저장/로드(선택)
- DB 도입 없이 교체 가능한 포트 기반 설계

## 3.2 인터페이스 계약
- `MatrixRepository.saveInput(matrix, runId) -> void | DataError`
- `MatrixRepository.loadInput(runId) -> matrix | DataError`
- `ResultRepository.saveResult(runId, result) -> void | DataError`
- `ResultRepository.loadResult(runId) -> result | DataError`
- 공통 오류 코드:
  - `ERR_DATA_NOT_FOUND`
  - `ERR_DATA_FORMAT_INVALID`
  - `ERR_DATA_IO_FAILURE`

## 3.3 구현 옵션 비교(메모리/파일)
| 옵션 | 장점 | 단점 | 적합도 |
|---|---|---|---|
| A. InMemory | 빠른 테스트, 설정 불필요 | 프로세스 종료 시 소실 | TDD 초기 학습 |
| B. File(JSON/CSV) | 실행 간 보존 | I/O/형식 오류 처리 필요 | 통합 검증 단계 |

- 추천안: **A. InMemory**
  - RED-GREEN 루프를 짧게 유지
  - 외부 환경 변수 최소화
  - 이후 File 구현으로 교체해 DIP 학습 가능

## 3.4 Data 레이어 테스트
| ID | 테스트명 | 기대 결과 |
|---|---|---|
| DATA-01 | 입력 저장/로드 정합성 | 동일 데이터 반환 |
| DATA-02 | 결과 저장/로드 정합성 | 동일 데이터 반환 |
| DATA-03 | 없는 키 조회 | `ERR_DATA_NOT_FOUND` |
| DATA-04 | 형식 오류(File) | `ERR_DATA_FORMAT_INVALID` |
| DATA-05 | 4x4 위반 저장 거부 | 실패 코드 반환 |

---

# 4) Integration & Verification (통합 및 검증)
## 4.1 통합 경로 정의
- 흐름: `UI -> Application(선택) -> Domain -> Data`
- 의존성 방향:
  - UI는 Application/Domain 인터페이스 의존
  - Domain은 UI/Data 구현체 의존 금지
  - Data는 Domain 계약을 직렬화해 보관

## 4.2 통합 테스트 시나리오
| ID | 유형 | 시나리오 | 기대 결과 |
|---|---|---|---|
| INT-OK-01 | 정상 | 조합 A 성립 입력 | 성공 + 규약 출력 |
| INT-OK-02 | 정상 | 조합 B만 성립 입력 | 성공 + B 순서 출력 |
| INT-FAIL-01 | 실패(입력) | 4x4 아님 | UI 검증 실패 |
| INT-FAIL-02 | 실패(도메인) | 두 조합 모두 실패 | `ERR_UNSOLVABLE` |
| INT-FAIL-03 | 실패(데이터) | 저장소 I/O 실패 | `ERR_DATA_IO_FAILURE` |

## 4.3 회귀 보호 규칙
- RED 테스트 삭제 금지
- 계약 테스트 실패 시 병합 금지
- 출력 포맷 `[r1,c1,n1,r2,c2,n2]` 변경 금지
- 좌표 1-index 규칙 변경 금지
- 에러 코드 문자열 변경 시 하위호환 검토 문서 필수

## 4.4 커버리지 목표
- Domain Logic: 95% 이상
- UI Boundary: 85% 이상
- Data Layer: 80% 이상

## 4.5 Traceability Matrix (필수)
| Concept(Invariant) | Rule | Use Case | Contract | Test | Component |
|---|---|---|---|---|---|
| 4x4 고정 | 행=4, 열=4 | 입력 검증 | Input size | D-RED-01, UI-RED-01 | Validator |
| 빈칸 2개 | 0 count=2 | 입력 검증/빈칸 탐지 | Input blank rule | D-RED-02, UI-RED-02 | Validator, BlankLocator |
| 값 범위 | 0 or 1~16 | 입력 검증 | Input range | D-RED-03, UI-RED-03 | Validator |
| 중복 금지 | non-zero unique | 입력 검증 | Input uniqueness | D-RED-04, UI-RED-04 | Validator |
| 누락 숫자 | 보완집합 2개 | 누락 계산 | Domain internal contract | D-RED-06 | MissingNumberFinder |
| 마방진 성립 | 행/열/대각=34 | 판정 | Judge contract | D-RED-10 | MagicSquareJudge |
| 출력 순서 | A 우선, 아니면 B | 조합 해석 | Output contract | D-RED-07, D-RED-08 | CompletionResolver |
| 불가능 처리 | 해 없음 명시 | 조합 해석 | Error contract | D-RED-09, UI-RED-06 | Resolver, UI Mapper |
| 저장 정합성 | 입력/결과 보존 | 저장/로드 | Repository contract | DATA-01, DATA-02 | Repositories |
