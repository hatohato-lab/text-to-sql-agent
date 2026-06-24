# 陰性対照: q1 の SQL が壊れている（括弧の閉じ忘れ）。実行時にエラー → 実行不可で検出。
QUERIES = {
    "q1": "SELECT COUNT(* FROM employees",
    "q2": "SELECT name FROM employees WHERE dept='営業'",
    "q3": "SELECT dept, AVG(salary) FROM employees GROUP BY dept",
    "q4": "SELECT name FROM employees ORDER BY salary DESC LIMIT 1",
    "q5": "SELECT COUNT(*) FROM employees WHERE salary>=500000",
}
