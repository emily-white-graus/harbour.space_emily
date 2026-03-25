   CREATE TABLE IF NOT EXISTS students (
       id INTEGER PRIMARY KEY,
       name TEXT NOT NULL,
       age INTEGER NOT NULL,
       email TEXT UNIQUE NOT NULL,
       track TEXT NOT NULL
   );

---

STUDENTS = [
    ("Ana", 21, "ana@example.com", "backend"),
    ("Omar", 24, "omar@example.com", "data"),
    ("Lina", 22, "lina@example.com", "backend"),
    ("Marta", 20, "marta@example.com", "frontend"),
    ("Ivan", 23, "ivan@example.com", "data"),
]
conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executemany(
        "INSERT INTO students (name, age, email, track) VALUES (?, ?, ?, ?)",
        STUDENTS,
    )

    conn.commit()
    print("Inserted rows:", len(STUDENTS))
    conn.close()

---

cur.execute("SELECT * FROM students")
    rows = cur.fetchall()

