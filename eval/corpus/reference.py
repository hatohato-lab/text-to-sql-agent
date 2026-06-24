# 正例: 各お題に正しく答える SQL。これが結果の基準（お手本）になる。
QUERIES = {
    "q1": "SELECT COUNT(*) FROM employees",
    "q2": "SELECT name FROM employees WHERE dept='営業'",
    "q3": "SELECT dept, AVG(salary) FROM employees GROUP BY dept",
    "q4": "SELECT name FROM employees ORDER BY salary DESC LIMIT 1",
    "q5": "SELECT COUNT(*) FROM employees WHERE salary>=500000",
}
