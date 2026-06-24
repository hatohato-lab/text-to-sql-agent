# 陰性対照: q2 の部署を取り違える（営業→開発）。実行結果がお手本と変わる → 結果違いで検出。
QUERIES = {
    "q1": "SELECT COUNT(*) FROM employees",
    "q2": "SELECT name FROM employees WHERE dept='開発'",
    "q3": "SELECT dept, AVG(salary) FROM employees GROUP BY dept",
    "q4": "SELECT name FROM employees ORDER BY salary DESC LIMIT 1",
    "q5": "SELECT COUNT(*) FROM employees WHERE salary>=500000",
}
