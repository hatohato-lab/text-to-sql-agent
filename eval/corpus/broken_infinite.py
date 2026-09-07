# 陰性対照: q1 が停止条件の無い再帰 CTE。構文は正しいが計算が終わらない。
# 実行予算（oracle.py の STEP_BUDGET）が無いと採点自体が止まり、評価の反復が続けられない。
QUERIES = {
    "q1": "WITH RECURSIVE loop(x) AS (VALUES(1) UNION ALL SELECT x FROM loop) SELECT count(*) FROM loop",
    "q2": "SELECT name FROM employees WHERE dept='営業'",
    "q3": "SELECT dept, AVG(salary) FROM employees GROUP BY dept",
    "q4": "SELECT name FROM employees ORDER BY salary DESC LIMIT 1",
    "q5": "SELECT COUNT(*) FROM employees WHERE salary>=500000",
}
