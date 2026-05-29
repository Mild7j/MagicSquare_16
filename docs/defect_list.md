# MagicSquare 결함 목록 (Defect List)

## 문서 메타

| 항목 | 내용 |
|---|---|
| **문서 ID** | DL-AC-FR01-01 |
| **버전** | 1.0 |
| **기준 AC** | AC-FR-01-01, AC-FR-01-05 |
| **기준 테스트** | `tests/boundary/`, `tests/control/` |
| **최종 회귀 확인** | 2026-05-29 — `pytest tests/ -v` → **34 passed** |

---

## 결함 요약

| 상태 | 건수 |
|---|---|
| **Closed** | 4 |
| **Open** | 1 |

---

## 결함 상세

| ID | Severity | AC ID | 재현 절차 | 기대값 | 실제값 | 근본 원인 | 수정 요약 |
|---|---|---|---|---|---|---|---|
| DEF-001 | Critical | AC-FR-01-01 | 1. `src/boundary/` 미구현 상태에서<br>2. `python -m pytest tests/boundary tests/control -v` 실행 | 테스트 수집 후 `grid=None` → `code="INVALID_SIZE"`, `message="Grid must be 4x4."` | `ModuleNotFoundError: No module named 'src.boundary'` (`tests/boundary/conftest.py:7`) | RED 단계에서 Boundary/Control 최소 패키지·모듈 미작성으로 import 단계 실패 | `src/boundary/` (`schemas.py`, `validator.py`, `constants.py`), `src/control/magic_square_service.py`, `src/entity/completion_resolver.py` 최소 Green 구현 추가. **`[Closed]`** |
| DEF-002 | Major | AC-FR-01-01 | 1. venv 활성화 후 `pydantic` 미설치<br>2. `python -m pytest tests/boundary -v` 실행 | `ErrorResponse` pydantic 모델 로드 후 검증 실행 | `ModuleNotFoundError: No module named 'pydantic'` (`src/boundary/schemas.py:5`) | 개발 의존성(`pydantic`) 미설치·`requirements-dev.txt` 부재 | `python -m pip install pydantic pytest`. 로컬 venv에 설치 후 재실행. **`[Closed]`** |
| DEF-003 | Info | — | 1. Git Bash(MINGW64)에서<br>2. `py -3.13 -m venv .venv` 실행 | 가상환경 생성 성공 | `bash: py: command not found` | Git Bash PATH에 Windows `py` 런처 미포함 | `python -m venv .venv` 사용 (PowerShell도 동일). **`[Closed — 워크어라운드]`** |
| DEF-004 | Minor | AC-FR-01-01 | 1. Green 구현 후<br>2. `python -m pytest tests/boundary tests/control -v` 실행 | 경고 없이 테스트 통과 | `PytestUnknownMarkWarning: Unknown pytest.mark.boundary` / `.control` | `pytest.ini` / `pyproject.toml`에 커스텀 마커 미등록 | `pytest.ini`에 `markers = boundary, control` 등록 (선택). 기능 영향 없음. **`[Open]`** |
| DEF-005 | Info | AC-FR-01-01 | 1. `grid=None` 입력 시 Boundary가 `None` 반환하는 가정 구현<br>2. `test_none_grid_returns_exact_invalid_size_code` 실행 | `result.code == "INVALID_SIZE"` | `AttributeError: 'NoneType' object has no attribute 'code'` (잠재 결함 — RED 설계 리뷰 시 식별) | `validate_size()`가 invalid 입력에 `ErrorResponse` 대신 `None` 반환 가능성 | `_has_valid_dimensions()`에 `grid is None` 조기 거부 + invalid 시 `ErrorResponse` 반환 (`src/boundary/validator.py:25-29`, `35-36`). 실제 실행 중 미재현, 예방 수정. **`[Closed — 예방]`** |

---

## AC-FR-01-01 관련 재현 명령 (공통)

```bash
cd /c/DEV/MagicSquare_xx
source .venv/Scripts/activate
python -m pytest tests/boundary/test_ac_fr_01_01_invalid_size.py -v --tb=short
python -m pytest tests/control/test_ac_fr_01_01_resolve_isolation.py -v --tb=short
```

---

## 회귀 테스트 기록

| 일자 | 명령 | 결과 |
|---|---|---|
| 2026-05-29 | `pytest tests/boundary tests/control -v` | **27 passed**, 2 warnings (DEF-004) |
| 2026-05-29 | `pytest tests/ -v` | **34 passed**, 2 warnings (DEF-004) |

---

## 범위 외 (본 목록에 미포함)

다음은 AC-FR-01-01 범위 밖이므로 별도 결함·스프린트에서 다룸.

- AC-FR-01-02 ~ AC-FR-01-04 (빈칸 개수, 값 범위, 중복)
- FR-02 ~ FR-05 (Domain resolver 본 구현 — `CompletionResolver.resolve()`는 `NotImplementedError` 스텁)
- 커버리지 게이트 Domain 95%+ / TOTAL 90%+ 미달 시 별도 이슈 등록

---

## 변경 이력

| 버전 | 일자 | 변경 내용 |
|---|---|---|
| 1.0 | 2026-05-29 | RED/Green 과정에서 발견된 결함 5건 최초 등록 |
