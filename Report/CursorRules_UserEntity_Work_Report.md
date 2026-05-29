# MagicSquare `.cursorrules` 및 User 엔티티 작업 보고서

## 1. 작업 목적

본 보고서는 MagicSquare 프로젝트에서 수행한 `.cursorrules` 정비와 ECB 기반 `User` 엔티티 구현 작업을 기록한다.

## 2. 수행 범위

- `.cursorrules` YAML 뼈대 생성
- `tdd_rules` 섹션 보강 및 파일 반영
- `.cursorrules` 전체 섹션 완성 (project, code_style, architecture, tdd_rules, testing, forbidden, file_structure, ai_behavior)
- ECB `entity` 레이어에 `User` 엔티티 구현
- `pytest` 기반 단위 테스트 작성 및 실행 검증

## 3. 산출물

### 3.1 규칙/정책 파일

- `.cursorrules`
  - Python 3.10+, PEP8, 타입힌트/Google docstring 규칙 명시
  - ECB 레이어 책임과 의존 방향 정의
  - TDD 3단계(red/green/refactor) 세부 규칙 정의
  - 테스트 전략(pytest, AAA, coverage 80% 이상) 정의
  - 금지 패턴(`print()`, 하드코딩 상수, `except` 단독) 정의
  - AI 행동 규칙(코드 작성 전/중/후) 정의

### 3.2 소스 코드

- `src/__init__.py`
- `src/entity/__init__.py`
- `src/entity/user.py`
  - 불변 데이터 클래스(`@dataclass(frozen=True, slots=True)`) 적용
  - 도메인 검증 규칙:
    - `user_id > 0`
    - 이름 공백 금지, 길이 제한
    - 이메일 형식 검증
  - public 메서드:
    - `create(...)`
    - `rename(...)`
    - `change_email(...)`
    - `to_dict(...)`

### 3.3 테스트 코드

- `tests/entity/test_user.py`
  - `pytest` 기반 테스트
  - AAA 패턴 적용
  - `test_` 네이밍 규칙 준수
  - 정상/예외/불변성 검증 테스트 포함

## 4. 검증 결과

- 실행 명령: `python -m pytest`
- 결과: `7 passed`
- 린트 점검: 신규 파일 기준 이슈 없음

## 5. 주요 의사결정

- ECB 경계 준수를 위해 `User`는 `entity` 레이어에 배치
- `print()` 사용 대신 검증 실패는 `ValueError` 예외로 일관 처리
- 리팩터링 용이성을 위해 데이터 불변 모델 채택

## 6. 후속 권장 작업

- `boundary`/`control` 레이어의 사용자 유스케이스 연결
- 입력 계약 기반 통합 테스트(`tests/integration`) 추가
- 커버리지 리포트 자동화(예: `pytest --cov`) 파이프라인 연동
