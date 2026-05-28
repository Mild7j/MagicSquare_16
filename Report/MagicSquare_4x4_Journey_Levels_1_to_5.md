# Magic Square 4x4 — Journey Levels 1 to 5 Report

## 문서 메타
- Project: Magic Square 4x4 TDD Practice
- Scope: Level 1(Epic) ~ Level 5(Verification) 정리
- 작성 목적: 불변식 기반 학습 설계의 일관성 검증 및 다음 단계 준비
- 제약: 구현 코드 없음, 테스트 코드 없음, Task 상세 구현 없음

---

## Level 1: Epic — Business Goal

### Epic Title
- 불변식 기반 사고 훈련 시스템 구축

### Business Goal
- 4x4 Magic Square 문제를 통해 정답 중심 구현이 아닌 불변식/계약 중심 설계 습관을 훈련한다.

### Learning Goal
- 불변식 중심 설계 사고
- Dual-Track(UI + Logic) TDD 적용
- 입력/출력 계약 명시
- 설계 -> 테스트 -> 구현 -> 리팩토링 흐름 학습
- Concept -> Invariant -> Contract -> Test 추적성 확보

### Success Criteria
- Domain Logic 테스트 커버리지 95% 이상
- Boundary 입력 검증 계약 테스트 100% 통과
- 설명 없는 매직 넘버 금지
- 명명된 상수 사용(`GRID_SIZE`, `MAX_VALUE`, `MAGIC_CONSTANT`)
- 정답 하드코딩 금지
- 주요 Invariant별 최소 1개 테스트 추적 가능
- 리팩토링 이후 외부 I/O 계약 불변

---

## Level 2: User Journey

### Persona
- TDD 학습 개발자
- Clean Architecture 계층 분리 학습자
- 설계/계약/테스트/리팩토링 흐름 훈련 지향 학습자

### Journey Goal
- 불변식 중심 문제 인식
- 계약 선정의
- Domain/Boundary 책임 분리
- Dual-Track TDD 체험
- 회귀 보호 중심 품질 유지

### 5-Stage Journey
1. Problem Recognition
2. Contract Definition
3. Domain Separation
4. Dual-Track TDD Progress
5. Regression Protection

각 Stage는 Action/Thinking/Emotion/Pain Point/Opportunity와 불변식 또는 계약 연결을 포함하도록 정의되었다.

---

## Level 3: User Stories

### Story Set
- Story 1 (Boundary): 입력 검증
- Story 2 (Domain): 빈칸 좌표 탐색
- Story 3 (Domain): 누락 숫자 탐색
- Story 4 (Domain): 마방진 검증
- Story 5 (Domain + Boundary Output): 두 가지 조합 시도

### Story 작성 원칙
- Acceptance Criteria는 테스트 가능한 문장으로만 작성
- Boundary Story와 Domain Story 분리
- Story별 보호 Contract/Invariant 명시
- Task 분해는 보류(후속 단계)

---

## Level 4: Technical Scenarios

### 정의된 시나리오
- SC-DOM-SOL-001: small-first 실패 후 reverse 조합 성공
- SC-BND-VAL-001: 빈칸 개수 오류
- SC-BND-VAL-002: 0 제외 중복 오류
- SC-BND-VAL-003: 값 범위 오류

### 시나리오 특성
- Given-When-Then 구조 명시
- Layer 명시(Domain/Solver, Boundary)
- 보호 Invariant/Contract 연결
- Future RED Test ID / Implementation Task Candidate 연결

---

## Level 5: Scenario Verification and Summary

### Overall Judgment
- 적합성 점수: 7.2/10
- 현재 상태: 일부 수정 필요

### 강점
- Epic -> Journey -> Story 연결 논리 명확
- Boundary/Domain 책임 분리 방향 일관
- 핵심 불변식과 계약이 Story 수준까지 명시됨

### 보완 필요 항목
- Story 대비 Technical Scenario 커버리지 보강 필요
- 누락 시나리오 추가 필요:
  - 4x4 형상 오류
  - small-first 즉시 성공
  - 두 조합 모두 실패
  - BlankFinder/MissingNumberFinder/MagicSquareValidator 전용 시나리오

### 진행 가능성
- 조건부 진행 가능
- 누락 시나리오 보강 후 Level 6(RED Test Specification) 진행 권장

---

## Traceability Summary

### Epic -> Journey
- 학습 목표(불변식/계약/Dual-Track/회귀 보호)가 Journey Stage에 반영됨

### Journey -> Story
- Stage별 기능적 Story로 분해 가능
- Acceptance Criteria가 측정 가능한 검증 단위로 작성됨

### Story -> Scenario
- 일부 AC는 시나리오 매핑 완료
- 일부 AC는 시나리오 추가 필요(커버리지 갭 존재)

### Invariant Coverage 상태
- 입력 범위/중복/빈칸 2개/합 34/출력 형식/1-index는 대부분 연결됨
- 누락 숫자 2개/오름차순, 4x4 형상 검증은 기술 시나리오 보강 필요

---

## Final Summary
- 본 문서는 Level 1~5의 산출물을 통합해 일관성을 검증한 결과를 정리한다.
- 현재 구조는 학습 목표와 추적성 관점에서 유효하다.
- 다만 Story -> Scenario 커버리지 갭을 해소해야 다음 단계 분해의 품질이 확보된다.
- 우선적으로 누락된 Domain/Boundary 시나리오를 보강한 후 RED Test ID 체계를 확장하는 것이 권장된다.
