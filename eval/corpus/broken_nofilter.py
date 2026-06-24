# 陰性対照: q5 の WHERE 条件を忘れる。全員を数えてしまい結果が変わる → 結果違いで検出。
QUERIES = {
    "q1": "SELECT COUNT(*) FROM employees",
    "q2": "SELECT name FROM employees WHERE dept='営業'",
    "q3": "SELECT dept, AVG(salary) FROM employees GROUP BY dept",
    "q4": "SELECT name FROM employees ORDER BY salary DESC LIMIT 1",
    "q5": "SELECT COUNT(*) FROM employees",
}
