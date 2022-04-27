from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from config import get_config

db = SQLAlchemy()
config = dict()
config = get_config()
migrate = Migrate()


class FyyurModel():
    def insert(self) -> None:
        db.session.add(self)

    def delete(self) -> None:
        db.session.delete(self)

    def stage(self) -> None:
        db.session.flush()

    def save(self) -> None:
        db.session.commit()

    def refresh(self) -> None:
        db.session.refresh(self)

    def rollback(self) -> None:
        db.session.rollback()

    def dispose(self) -> None:
        db.session.close()


class Person(db.Model, FyyurModel):
    __tablename__ = 'person'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def format(self) -> dict:
        return {'id': self.id, 'name': self.name}
