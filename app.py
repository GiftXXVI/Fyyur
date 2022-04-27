from flask import Flask, request, abort, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import model
from model import db, migrate, config, Person


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config["SQLALCHEMY_DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config["SQLALCHEMY_TRACK_MODIFICATIONS"]
    db.init_app(app)
    migrate = Migrate(app, db)
    return app


app = create_app()


@app.route('/persons', methods=['GET'])
def index() -> jsonify:
    persons = Person.query.all()

    return jsonify({
        'success': True,
        'persons': [person.format() for person in persons]
    })


@app.route('/persons', methods=['POST'])
def create() -> jsonify:
    body = request.get_json()
    if body is not None:
        name = body.get('name', None)
        if name is not None:
            person = Person(name=name)
            success = False
            try:
                person.insert()
                person.save()
                person.refresh()
                success = True
            except BaseException:
                person.rollback()
            finally:
                person.dispose()
                if success:
                    return jsonify({
                        'success': True,
                        'created': person.id
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
