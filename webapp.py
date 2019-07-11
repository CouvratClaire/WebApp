import flask
from sqlalchemy import null

app = flask.Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


@app.route("/")
def index():
    return flask.render_template("login.html.jinja2")


@app.route("/identification", methods=["POST"])
def process_inscription():
    from database import Employee
    print(flask.request.form)
    identifiant = flask.request.form["identifiant"]
    print("l'identifiant est %s" % (identifiant))
    employee = Employee.query.filter_by(id=identifiant).first()

    if employee is None:
        return flask.render_template("mauvais_identifiant.html.jinja2")

    print("le type est %s" % (employee.type))
    if employee.type == 0:
        return flask.redirect(flask.url_for("accueil_etude", identifiant=identifiant))
    else:
        return flask.redirect(flask.url_for("accueil_affaire"))


@app.route("/new_employee")
def generate_for_new_employee():
    from database import Competence
    competences = Competence.query.all()
    return flask.render_template("employee_form.html.jinja2", competences=competences)


@app.route("/process_employee_form", methods=["POST"])
def process_employee_form_function():
    from database import db, Employee, Competence
    print(flask.request.form)
    firstname = flask.request.form["firstname"]
    lastname = flask.request.form["lastname"]
    id_competence1 = flask.request.form.get('id_competence1')
    id_competence2 = flask.request.form.get('id_competence2')
    id_competence3 = flask.request.form.get('id_competence3')
    competence1 = Competence.query.filter_by(id=id_competence1).first()
    competence2 = Competence.query.filter_by(id=id_competence2).first()
    competence3 = Competence.query.filter_by(id=id_competence3).first()



    new_employee = Employee()
    new_employee.firstname = firstname
    new_employee.lastname = lastname
    new_employee.type=0
    new_employee.project='null'
    new_employee.nb_mission="0"
    new_employee.competences.append(competence1)
    new_employee.competences.append(competence2)
    new_employee.competences.append(competence3)

    db.session.add(new_employee)
    db.session.commit()


    return flask.redirect(flask.url_for("accueil_affaire"))


@app.route("/update_employee/<employee_id>")
def update_employee(employee_id):
    from database import Employee

    employee = Employee.query.filter_by(id=employee_id).first()

    if employee is None:
        return flask.redirect(flask.url_for("index", 404))

    return flask.render_template("employee_form.html.jinja2",
                                 firstname=employee.firstname,
                                 lastname=employee.lastname,
                                 division=employee.division,
                                 employee_id=employee.id)


@app.route("/affaires")
def accueil_affaire():
    from database import Project, Employee
    projects = Project.query.all()
    employees = Employee.query.filter_by(type='0')
    return flask.render_template("index.html.jinja2", projects=projects, employees=employees)


@app.route("/affaires/missions")
def gerer_les_missions():
    from database import Project, Employee, Competence
    projects = Project.query.all()
    employees = Employee.query.all()
    return flask.render_template("missions.html.jinja2", projects=projects, employees=employees, Competence=Competence)


@app.route("/nouvelleMission")
def generate_for_new_mission():
    from database import Competence
    competences = Competence.query.all()
    return flask.render_template("mission_form.html.jinja2", competences=competences)


@app.route("/process_mission_form", methods=["POST"])
def process_mission_form_function():
    from database import db, Project, Competence
    nom = flask.request.form["nom"]
    description = flask.request.form["description"]
    id_competence1 = flask.request.form.get('id_competence1')
    id_competence2 = flask.request.form.get('id_competence2')
    competence1 = Competence.query.filter_by(id=id_competence1).first()
    competence2 = Competence.query.filter_by(id=id_competence2).first()

    project = Project()

    if project is None:
        flask.redirect(flask.url_for("index"), 404)
    else:

        project.name = nom
        project.description = description
        project.id_employee = "<null>"
        project.state = 0
        project.competences.append(competence1)
        project.competences.append(competence2)

        db.session.add(project)
        db.session.commit()

    return flask.redirect(flask.url_for("accueil_affaire"))


@app.route("/supprimerMission/<project_id>")
def supress_mission(project_id):
    from database import Project

    project = Project.query.filter_by(id=project_id).first()

    if project is None:
        return flask.redirect(flask.url_for("index", 404))

    return flask.render_template("supress_mission.html.jinja2", project_id=project.id, name=project.name)


@app.route("/cloreMission/<project_id>")
def clore_mission(project_id):
    from database import Project

    project = Project.query.filter_by(id=project_id).first()

    if project is None:
        return flask.redirect(flask.url_for("index", 404))

    return flask.render_template("clore_mission.html.jinja2", project_id=project.id, name=project.name,
                                 project_description=project.description)


@app.route("/updateMission/<project_id>")
def update_mission(project_id):
    from database import Project, Employee, Competence

    project = Project.query.filter_by(id=project_id).first()
    employees_wish = Employee.query.filter_by(wish=project_id)
    employees_comp=[]
    comp=[]

    for compet in project.competences:
        # for competence in competences:
        comp += [compet]
    employees = Employee.query.all()
    for employee in employees:
        if all(elem in employee.competences for elem in comp):
            employees_comp += [employee]



    if project is None:
        return flask.redirect(flask.url_for("accueil_affaire", 404))

    return flask.render_template("attribuer_mission.html.jinja2", project_id=project.id, name=project.name,
                                 project_description=project.description, employees_wish=employees_wish,
                                 employees_comp=employees_comp)


@app.route("/process_attribution_form/<project_id>", methods=["POST"])
def process_attribution_form_function(project_id):
    from database import db, Project, Employee

    id = flask.request.form.get('id_select')

    employee = Employee.query.filter_by(id=id).first()
    employee.project = project_id
    if employee.nb_mission is None:
        employee.nb_mission="0"
    else :
        employee.nb_mission += int(1)

    project = Project.query.filter_by(id=project_id).first()
    project.state = '-1'

    db.session.commit()

    return flask.redirect(flask.url_for("accueil_affaire"))


@app.route("/process_supress_mission/<mission_id>")
def process_supress_mission_function(mission_id):
    from database import db, Project

    project = Project.query.filter_by(id=mission_id).first()  # Behaviour (2)

    if project is None:
        flask.redirect(flask.url_for("index"), 404)
    else:

        db.session.delete(project)
        db.session.commit()

    return flask.redirect(flask.url_for("accueil_affaire"))


@app.route("/process_close_mission/<mission_id>")
def process_close_mission_function(mission_id):
    print(flask.request.form)
    from database import db, Project, Employee

    project = Project.query.filter_by(id=mission_id).first()

    if project is None:
        flask.redirect(flask.url_for("index"), 404)
    else:

        project.state = -1
        db.session.commit()

    return flask.redirect(flask.url_for('accueil_affaire'))


@app.route("/supprimerEtude/<employee_id>")
def supress_employee(employee_id):
    from database import Employee

    employee = Employee.query.filter_by(id=employee_id).first()

    if employee is None:
        return flask.redirect(flask.url_for("index", 404))

    return flask.render_template("supress_employee.html.jinja2", firstname=employee.firstname, name=employee.lastname,
                                 employee_id=employee_id)


@app.route("/process_supress_employee/<employee_id>")
def process_supress_employee_function(employee_id):
    from database import db, Employee

    employee = Employee.query.filter_by(id=employee_id).first()

    if employee is None:
        flask.redirect(flask.url_for("index"), 404)
    else:

        db.session.delete(employee)
        db.session.commit()

    return flask.redirect(flask.url_for("accueil_affaire"))


@app.route("/profilEtude/<employee_id>")
def profil_employee(employee_id):
    from database import Employee, Project, Competence

    employee = Employee.query.filter_by(id=employee_id).first()

    if employee is None:
        return flask.redirect(flask.url_for("index", 404))

    employee_nb=employee.nb_mission
    print(employee_nb)
    voeux_id = employee.wish

    wish = Project.query.filter_by(id=voeux_id).first()

    if wish is None:
        voeux = "Aucun"

    else:
        voeux = wish.name

    if employee.project is None:
        project_name=None
        project_state=None
        project_description=None
    else:
        project = Project.query.filter_by(id=employee.project).first()
        if project is None:
            project_name=None
            project_description=None
            project_state=None
        else:
            project_name = project.name
            project_description = project.description
            if project.state == 1:
                project_state = "effectuee"
            else:
                project_state = "en cours"

    return flask.render_template("profil_employee2.html.jinja2", employee_nb=employee_nb, employee=employee, firstname=employee.firstname,
                                 name=employee.lastname, identifiant=employee_id, project_name=project_name,
                                 description=project_description, project_state=project_state, voeux=voeux)


@app.route("/profil/modifier", methods=["POST"])
def process_modification_employee_function():
    print(flask.request.form)
    from database import Employee, db
    identifiant = flask.request.form["identifiant"]
    prenom = flask.request.form["firstname"]
    nom = flask.request.form["lastname"]

    employee = Employee.query.filter_by(id=identifiant).first()

    if employee is None:
        return flask.redirect(flask.url_for("index", 404))

    else:
        employee.firstname = prenom
        employee.lastname = nom
        db.session.commit()

    return flask.redirect(flask.url_for("profil_employee", employee_id=identifiant))


@app.route("/affaires/ingenieurs_etude")
def gerer_les_ingenieurs_d_etude():
    from database import Employee, Project

    projects = Project.query.all()
    employees = Employee.query.all()

    return flask.render_template("etudes.html.jinja2", employees=employees, projects=projects)




@app.route("/etudes/<identifiant>")
def accueil_etude(identifiant):
    from database import Employee
    from database import Project
    employee= Employee.query.filter_by(id=identifiant).first()

    voeux_id = employee.wish

    wish = Project.query.filter_by(id=voeux_id).first()

    if wish is None:
        voeux = "Aucun"

    else:
        voeux = wish.name


    if employee.project is None:
        project_name = None
        project_state = None
        project_description = None
    else:
        project = Project.query.filter_by(id=employee.project).first()
        if (project is not None):
            project_name = project.name
            project_description = project.description
            if project.state == 0:
                project_state = "En cours"
            else:
                project_state = "Finie"
        else :
            project_name = None
            project_state = None
            project_description = None



    return flask.render_template("profil_employee2.html.jinja2", voeux=voeux, employee=employee, identifiant=identifiant, project_name=project_name, project_description=project_description,project_state=project_state)

@app.route("/etudes/liste_missions/<identifiant>")
def liste_missions(identifiant):
    from database import Project
    from database import Competence
    projects = Project.query.all()
    competences = Competence.query.all()
    return flask.render_template("liste_missions.html.jinja2", projects=projects, competences=competences, identifiant=identifiant)

@app.route("/etudes/voeux/<identifiant>")
def voeux(identifiant):
    from database import Employee
    from database import Project
    from database import Competence
    employee = Employee.query.filter_by(id=identifiant)
    competences = Competence.query.all()
    comp = []
    for compet in employee.one().competences:
        # for competence in competences:
        comp += [compet]
    projects = Project.query.all()
    proj = []
    for project in projects:
        if all(elem in comp for elem in project.competences):
            proj +=[project]

    return flask.render_template("voeux.html.jinja2", identifiant=identifiant, employee=employee, competences=competences, projects=projects, comp=comp, proj=proj)


@app.route("/process_wish_form/<identifiant>",  methods=["POST"])
def process_wish_function(identifiant):
    from database import Employee, db
    id_project = flask.request.form.get('id_select')
    employee = Employee.query.filter_by(id=identifiant).first()

    employee.wish=id_project
    db.session.commit()

    return flask.redirect(flask.url_for("profil_employee", employee_id=identifiant))
@app.route("/profil/modifier/etudes", methods=["POST"])
def process_modification_employee_function2():
    print(flask.request.form)
    from database import Employee, db
    identifiant = flask.request.form["identifiant"]
    prenom = flask.request.form["firstname"]
    nom = flask.request.form["lastname"]

    employee = Employee.query.filter_by(id=identifiant).first()

    if employee is None:
        return flask.redirect(flask.url_for("accueil_etude", 404))

    else:
        employee.firstname = prenom
        employee.lastname = nom
        db.session.commit()

    return flask.redirect(flask.url_for("accueil_etude", identifiant=identifiant))



@app.route("/test")
def testHTML():
    from database import Project
    projects = Project.query.all()
    return flask.render_template("index.html.jinja2", projects = projects
                                 )



#if __name__ == "__main__":
    # Create the DB
   # from database import db
   # print("creating database")
   # db.create_all()
   # print("database created")

    print("Running the main program")
    app.jinja_env.auto_reload = True
    app.run(host="0.0.0.0", port=5000, debug=True)

