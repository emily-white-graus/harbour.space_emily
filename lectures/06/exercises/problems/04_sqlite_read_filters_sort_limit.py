"""Problem 04: Practice WHERE, ORDER BY, LIMIT.

Task:
1. Get students with age >= 22
2. Sort students by age DESC
3. Return only top 3 oldest students
4. Get backend students younger than 23

Use parameterized queries for filter values.
"""

import sqlite3

DB_PATH = "school.db"


def main() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # TODO 1: age >= 22
    cur.execute("SELECT * FROM students WHERE age >= ?", (22,))
    students_22_plus = cur.fetchall()
    print("Students aged 22 and older:")
    for student in students_22_plus:
        print(student)

    # TODO 2 + 3: order by age desc, limit 3
    cur.execute("SELECT * FROM students WHERE age >= ? ORDER BY age DESC LIMIT ?", (22, 3))
    oldest_students = cur.fetchall()
    print("\nTop 3 oldest students:")
    for student in oldest_students:
        print(student)

    # TODO 4: track='backend' and age < 23
    cur.execute("SELECT * FROM students WHERE track = ? AND age < ?", ("backend", 23))
    backend_students = cur.fetchall()
    print("\nBackend students younger than 23:")
    for student in backend_students:
        print(student)

    conn.close()


if __name__ == "__main__":
    main()
