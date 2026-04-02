"""Problem 07: Create and read data with SQLAlchemy.

Task:
1. Open a SQLAlchemy Session on `school.db`.
2. Create one Assignment for an existing student.
3. Read all students.
4. Read students with age >= 22 sorted by age descending.
5. Read assignments with joined student names.

Starter:
- Reuse `Student` and `Assignment` from `db_models.py`.
- Use `select(...)` queries.
"""

from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db_models import Assignment, Student

DB_PATH = Path(__file__).resolve().parent.parent / "school.db"
DB_URL = f"sqlite:///{DB_PATH}"


def main() -> None:
    engine = create_engine(DB_URL, echo=False)

    with Session(engine) as session:
        # TODO 1: add an assignment for an existing student
        first_student = session.scalars(select(Student).order_by(Student.id)).first()
        if first_student is not None:
            assignment = Assignment(
                title="SQLAlchemy basics",
                score=95,
                student_id=first_student.id,
            )
            session.add(assignment)

        # TODO 2: read all students
        all_students = session.scalars(select(Student)).all()
        print("All students:")
        for student in all_students:
            print(student.id, student.name, student.age, student.email, student.track)

        # TODO 3: read filtered + sorted students
        filtered_students = session.scalars(
            select(Student).where(Student.age >= 22).order_by(Student.age.desc())
        ).all()
        print("\nStudents age >= 22 ordered by age desc:")
        for student in filtered_students:
            print(student.id, student.name, student.age, student.email, student.track)

        # TODO 4: read assignments with student data
        assignment_rows = session.execute(
            select(Assignment, Student).join(Student, Assignment.student_id == Student.id)
        ).all()
        print("\nAssignments with student data:")
        for assignment, student in assignment_rows:
            print(assignment.id, assignment.title, assignment.score, student.name)

        session.commit()


if __name__ == "__main__":
    main()
