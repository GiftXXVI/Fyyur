from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import model
from model import Interest, db, migrate, config, Student
from forms import StudentForm, InterestForm


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    db.init_app(app)
    migrate = Migrate(app, db)
    return app


app = create_app()

# list
# SELECT * FROM student LIMIT 5 OFFSET 0 ORDER BY id DESC;


@app.route('/students', methods=['GET'])
def view_students(limit=5, offset=0):
    students = Student.query.order_by(
        Student.id.desc()).limit(limit).offset(offset).all()
    students_f = [student.format() for student in students]
    return render_template('pages/students/list.html', students=students_f)


@app.route('/interests', methods=['GET'])
def view_interests(limit=5, offset=0):
    interests = Interest.query.order_by(
        Interest.id.desc()).limit(limit).offset(offset).all()
    interests_f = [interest.format() for interest in interests]
    return render_template('pages/interests/list.html', students=interests_f)

# create


@app.route('/student/create', methods=['GET'])
def create_student_form():
    student_form = StudentForm()
    return render_template('forms/students/add.html')


@app.route('/student/create', methods=['GET'])
def create_interest_form():
    return render_template('forms/interests/add.html')

# START TRANSACTION;
# INSERT INTO students(name) VALUES('VALUE');
# INSERT INTO student_interests(student_id,interest_id) VALUES('1','1');
# COMMIT;

# START TRANSACTION;
# DELETE FROM student;
# SELECT * FROM student;
# ROLLBACK;

# SELECT * FROM student;


@app.route('/students/create', methods=['POST'])
def create_student():
    if len(request.form) > 0:
        name = request.form.get('name', None)
        interests = request.form.get('interests', None)
        if name is not None:
            student = Student(name=name, interests=[Interest.query.filter(
                Interest.id == interest) for interest in interests])
            success = False
            try:
                student.add()
                student.commit()
                student.refresh()
                success = True
            except SQLAlchemyError:
                student.rollback()
            finally:
                student.dispose()
                if success:
                    return redirect(url_for('students'))
                else:
                    abort(500)
        else:
            abort(400)
    else:
        abort(400)


@app.route('/interests/create', methods=['POST'])
def create_interest():
    if len(request.form) > 0:
        name = request.form.get('name', None)
        if name is not None:
            interest = Interest(name=name)
            success = False
            try:
                interest.add()
                interest.commit()
                interest.refresh()
                success = True
            except SQLAlchemyError:
                interest.rollback()
            finally:
                interest.dispose()
                if success:
                    return redirect(url_for('interests'))
                else:
                    abort(500)
        else:
            abort(400)
    else:
        abort(400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
