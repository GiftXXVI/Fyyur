from flask import Flask, request, abort, jsonify, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import model
from model import db, migrate, config, Student


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    db.init_app(app)
    migrate = Migrate(app, db)
    return app


app = create_app()

# SELECT * FROM student;

@app.route('/students', methods=['GET'])
def index() -> jsonify:
    students = Student.query.all()
    students_f = [student.format() for student in students]
    return render_template('pages/students.html', students=students_f)

    return jsonify({
        'success': True,
        'persons': [student.format() for student in students]
    })

# START TRANSACTION;
# INSERT INTO students(name) VALUES('VALUE');
# INSERT INTO student_interests(student_id,interest_id) VALUES('1','1');
# COMMIT;

# START TRANSACTION;
# DELETE FROM student;
# SELECT * FROM student;
# ROLLBACK;

# SELECT * FROM student;

@app.route('/students', methods=['POST'])
def create() -> jsonify:
    body = request.get_json()
    if body is not None:
        name = body.get('name', None)
        if name is not None:
            student = Student(name=name)
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
                    return jsonify({
                        'success': True,
                        'created': student.id
                    })
                else:
                    abort(500)
        else:
            abort(400)
    else:
        abort(400)





@app.errorhandler(400)
def error_400(error):
    return jsonify({
        'success': False,
        'error': error.code,
        'message': error.name
    })


@app.errorhandler(500)
def error_500(error):
    return jsonify({
        'success': False,
        'error': error.code,
        'message': error.name
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
