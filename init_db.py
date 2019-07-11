# coding=utf-8
import sys

from flask import session
from pip._vendor.certifi import where
from sqlalchemy import create_engine, MetaData, Binary
from sqlalchemy.engine import Engine

import database
from database import db
from  sqlalchemy.sql.expression import func
import random
#!/usr/bin/python2.6

# -*-coding:Latin-1 -*


first_names = ["Bob", "Edward", "Jane", "Maria", "Susan", "Nick"]
last_names = ["Hendricks", "Norrington", "Doe", "Sullivan", "Brice", "Henry"]
competence_name = ["Leadership", "CSS", "HTML", "Connaissance en art", "Communication", "Imagination", "Teamwork"]
project_name_prefix = ["Incredible", "Fantastic", "Big", "Magic", "Better"]
project_name_suffix = ["Leap", "Jump", "Revolution", "World", "Configuration"]
project_description = ["Programmer un site pour aider les startups à trouver des financements", "Design d'un jeu pour adolescent", "Programmer une application pour prévenir des problèmes écologiques", "Débat sur le futur de la compagnie"]


if __name__ == "__main__":
    # Create the DB
    from database import db
    print("creating database")
    db.create_all()
    print("database created")

    employees = []

    # Create some competences
    for i in range(0, 7):
        competence = database.Competence()
        competence.name = competence_name[i]
        competence.description = "-"

        db.session.add(competence)
        db.session.commit()

    # Create few employees
    for i in range(0, 10):
        employee = database.Employee()
        employee.firstname = random.choice(first_names)
        employee.lastname = random.choice(last_names)
        employee.division = "business" if (i % 2 == 0) else "coder"
        employee.type = "1" if (employee.division == "business") else "0"
        employee.project = "1" if (i==1) else "null"
        employee.wish = "2" if (i==4) else "null"
        employee.nb_mission="1" if (i==1) else "0"

        for j in range(0,3):
           comp__ = database.Competence.query.order_by(func.random()).first()  # type: object
           employee.competences.append(comp__)


        employees += [employee]
        db.session.add(employee)
        db.session.commit()


    # Create few projects
    for i in range(0, 4):
        project = database.Project()
        project.name = "{prefix} {suffix}".format(prefix=random.choice(project_name_prefix),
                                                  suffix=random.choice(project_name_suffix))
        project.state = "-1" if (i==1) else "0"
        project.description = random.choice(project_description)
        project.id_manager = database.Employee.query \
            .filter_by(type="1") \
            .order_by(func.random()) \
            .first().id
        project.id_employee = database.Employee.query \
            .filter_by(type="0") \
            .order_by(func.random()) \
            .first().id
       # comps = []

        for i in range(0,2):
            #engine = create_engine()  # type: Engine
            #metadata = MetaData(bind=engine)
            comp__ = database.Competence.query.order_by(func.random()).first()
            project.competences.append(comp__)


        db.session.add(project)
        db.session.commit()




    # Assign few competence to employees
    #for i in range(0, 4):
      #  asso1 = database.association_table2()
      #  asso1.employee_id=database.Employee.query \
           # .filter_by(type="0") \
           # .order_by(func.random()) \
           # .first().id
       # asso1.competence = random.choice(competences)

       # db.session.add(project)
       # db.session.commit()

    sys.exit(0)
