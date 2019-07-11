from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, Column
from sqlalchemy.orm import relationship

from webapp import app

#!/usr/bin/python2.6

# -*-coding:Latin-1 -*

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table1 = db.Table('association_project_competence',
                             db.Column('competence_id', db.Integer, db.ForeignKey('competence.id')),
                             db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
                             )

association_table2 = db.Table('association_employee_competence',
                             db.Column('competence_id', db.Integer, db.ForeignKey('competence.id')),
                             db.Column('employee_id', db.Integer, db.ForeignKey('employee.id'))
                             )


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text)
    lastname = db.Column(db.Text)
    type = db.Column(db.Integer)
    #division = db.Column(db.Integer)
    project = db.Column (db.Integer)
    wish = db.Column(db.Integer)
    nb_mission =  db.Column(db.Integer)

   # competences = db.Column(db.Integer)

    #children2 = relationship("Wishes", back_populates="parent2")
    competences = db.relationship('Competence', secondary=association_table2, lazy='subquery',
                                  backref=db.backref('employees', lazy=True))
    #division = Column(Integer, db.ForeignKey('division.id'))
    #parent4 = relationship("Division", back_populates="children4")
    #child5 = relationship("Project", uselist=False, back_populates="parent5")
    wish = Column(Integer, db.ForeignKey('project.id'))
    project = Column(Integer, db.ForeignKey('project.id'))
    parent6 = relationship("Project", foreign_keys=[project], back_populates="children6")
    parent7 = relationship("Project", foreign_keys=[wish], back_populates="children7")


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    #id_division = db.Column(db.Text)
    competences = db.Column(db.Integer)
    state = db.Column(db.Integer)
    description = db.Column(db.Text)
    #id_employee = db.Column(db.Integer)
    #id_manager = db.Column(db.Integer)


    #children1 = relationship("Wishes", back_populates="parent1")
    competences = db.relationship('Competence', secondary=association_table1, lazy='subquery',
                                  backref=db.backref('projects', lazy=True))
    #id_division = Column(Integer, db.ForeignKey('division.id'))
    #parent3 = relationship("Division",back_populates="children3")
    #id_employee = Column(Integer, ForeignKey('employee.id'))
    #parent5 = relationship("Employee", back_populates="child5")
    children7 = relationship("Employee", foreign_keys=[Employee.wish], back_populates="parent7")
    children6 = relationship("Employee", foreign_keys=[Employee.project], back_populates="parent6")

# #class Wishes(db.Model):
#     #id_employee = db.Column(db.Integer, primary_key=True)
#     numero_wishes = db.Column(db.Integer, primary_key=True)
#     id_project = db.Column(db.Integer)
#
#     id_project = Column(Integer, ForeignKey('project.id'))
#     parent1 = relationship("Project", back_populates="children1")
#     id_employee = Column(Integer, ForeignKey('employee.id'))
#     parent2 = relationship("Employee", back_populates="children2")


# class Division(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Text)
#     description = db.Column(db.Text)
#
#     children3 = relationship("Project", back_populates="parent3")
#     children4 = relationship("Employee",back_populates="parent4")


class Competence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)


