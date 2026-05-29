# Golden Master Approve Pattern — Magic Square Solver

## Purpose

GM-1/GM-2 회귀 테스트는 `UIBoundary.solve()`의 **실제 반환값**을 기준 파일과 비교한다.  
stdout이 아닌 **API Result 직렬화**(`ErrorResponse` / `list[int]` / 미처리 예외)를 사용한다.

## Artifacts

| Path | Role |
|------|------|
| `tests/golden_master_expected.txt` | 승인된 기준 출력 (버전 관리 대상) |
| `tests/golden_master/scenarios.py` | GM-TC 시나리오 격자 + 직렬화 |
| `tests/golden_master/contracts.py` | int[6]·row-major·Attempt 규칙 검증 |
| `tests/golden_master/approve.py` | approve/compare 로더 |
| `scripts/generate_golden_master.py` | 기준 파일 생성 CLI |
| `tests/boundary/test_golden_master_magic_square.py` | GM-2 pytest (`@pytest.mark.golden_master`) |

## Scenario Coverage (GM-TC)

| ID | Input intent | Observed outcome |
|----|--------------|------------------|
| `GM-TC-01` | Attempt 1 small-first (PRD TD-01) | `Output: [1,3,3,3,4,12]` |
| `GM-TC-02` | Attempt 2 reverse (PRD TD-02) | `Output: [1,1,16,4,4,1]` |
| `GM-TC-03` | 빈칸 3개 | `Error: INVALID_BLANK_COUNT` |
| `GM-TC-04` | non-zero 중복 (PRD TD-05) | `Error: ValueError` *(Boundary 미구현)* |
| `GM-TC-05` | 양쪽 Attempt 실패 | `Error: UNSOLVABLE` |

## Execution

```powershell
$env:PYTHONPATH='.'; python -m pytest -m golden_master -v
```

Approve (baseline 갱신):

```powershell
$env:PYTHONPATH='.'; $env:GOLDEN_MASTER_APPROVE='1'; python -m pytest -m golden_master -v
```

## Failure Output

불일치 시 unified diff:

```text
--- expected
+++ actual
@@ ...
________________________________________
```

## Contract Checks (GM-2)

| Rule | GM-TC |
|------|-------|
| `int[6]` 형식 | 01, 02 |
| row-major 빈칸 순서 | 01, 02 |
| 1-index 좌표 | 01, 02 |
| small-first (Attempt 1) | 01 |
| reverse fallback (Attempt 2) | 02 |
| Error contract | 03, 04, 05 |

## Approve Workflow

1. **기준 파일 없음** → 현재 출력으로 자동 생성
2. **기준 파일 있음** → `open(expected).read()` vs actual 문자열 비교
3. **불일치** → unified diff + `FAIL`
4. **`GOLDEN_MASTER_APPROVE=1`** → baseline 덮어쓰기 후 `PASS`

## Design Notes

1. **ECB 경계**: 시나리오 실행은 `UIBoundary.solve()` 단일 진입점.
2. **duplicate_number**: FR-01 duplicate 구현 후 approve로 `DUPLICATE_NON_ZERO` 갱신.
3. **GM-TC-01 vs GM-TC-02**: 각각 Attempt 1/2 전용 SSOT 격자 사용 (혼용 금지).
