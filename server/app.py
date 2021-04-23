from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
import mariadb, sys, yaml, json
from hashlib import sha256
from datetime import timedelta

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key="alsjd374t82troksan87rt29efh983ra"

#Connect to MariaDB Platform
'''db = yaml.load(open('db.yaml'))
app.config['MARIADB_HOST'] = db['mariadb_host']
app.config['MARIADB_USER'] = db['mariadb_user']
app.config['MARIADB_PASSWORD'] = db['mariadb_password']
app.config['MARIADB_DB'] = db['mariadb_db']'''

try:
    conn = mariadb.connect(
        user="admin",
        password="Password123!",
        host="localhost",
        database="SurveyDB"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


CORS(app, resources={r'/*': {'origins': '*'}})

class User:
    def __init__(self, login, vorname, nachname, rolle):
        self.login = login
        self.vorname = vorname
        self.nachname = nachname
        self.rolle = rolle

@app.route('/add', methods=['GET', 'POST'])
def add_user():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        personData = request.get_json()
        login = personData['login']
        vorname = personData['vorname']
        nachname = personData['nachname']
        rolle = personData['rolle']
        password = personData['passwort']
        h = sha256()
        h.update(('%s' % (password)).encode('utf-8'))
        h_password = h.hexdigest()
        cur = conn.cursor()
        cur.execute("INSERT INTO Users(UserLogin, UserFirstName, UserLastName, UserRole, UserPassword) VALUES('{}', '{}', '{}', '{}', '{}')".format(login, vorname, nachname, rolle, h_password))
        conn.commit()
        cur.close()
        response_object['message'] = 'User hinzugefügt!'
    return jsonify(response_object)

@app.route('/remove/<user_login>', methods=['DELETE'])
def delete_user(user_login):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        cur = conn.cursor()
        cur.execute("DELETE FROM Users WHERE UserLogin='{}'".format(user_login))
        conn.commit()
        cur.close()
        response_object['message'] = 'User gelöscht!'
    return jsonify(response_object)
        
@app.route('/edit/<user_login>', methods=['PUT'])
def edit_user(user_login):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        personData = request.get_json()
        login = personData['login']
        vorname = personData['vorname']
        nachname = personData['nachname']
        rolle = personData['rolle']
        password = personData['passwort']
        cur = conn.cursor()
        cur.execute("START TRANSACTION;")
        if (login):
            cur.execute("UPDATE Users SET UserLogin='{}' WHERE UserLogin='{}'".format(login, user_login))
        if (vorname):
            cur.execute("UPDATE Users SET UserFirstName='{}' WHERE UserLogin='{}'".format(vorname, user_login))
        if (nachname):
            cur.execute("UPDATE Users SET UserLastName='{}' WHERE UserLogin='{}'".format(nachname, user_login))
        if (rolle):
            cur.execute("UPDATE Users SET UserRole='{}' WHERE UserLogin='{}'".format(rolle, user_login))
        if (password):
            h = sha256()
            h.update(('%s' % (password)).encode('utf-8'))
            h_password = h.hexdigest()
            cur.execute("UPDATE Users SET UserPassword='{}' WHERE UserLogin='{}'".format(h_password, user_login))
        cur.execute("COMMIT;")
        conn.commit()
        cur.close()
        response_object['message'] = 'User editiert!'
    return jsonify(response_object)

@app.route('/change_password/<user_login>', methods=['PUT'])
def change_password(user_login):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        passwordData = request.get_json()
        old_password = passwordData['old_password']
        new_password_1 = passwordData['new_password_1']
        new_password_2 = passwordData['new_password_2']
        if (new_password_1 == new_password_2):
            h = sha256()
            h.update(('%s' % (old_password)).encode('utf-8'))
            h_old_password = h.hexdigest()
            cur = conn.cursor()
            cur.execute("START TRANSACTION;")
            cur.execute("SELECT UserPassword FROM Users WHERE UserLogin='{}'".format(user_login))
            old_password_data = cur.fetchall()
            if (old_password_data[0][0] == h_old_password):
                h = sha256()
                h.update(('%s' % (new_password_1)).encode('utf-8'))
                h_new_password = h.hexdigest()
                cur.execute("UPDATE Users SET UserPassword='{}' WHERE UserLogin='{}'".format(h_new_password, user_login))
                cur.execute("COMMIT;")
                conn.commit()
                response_object['message'] = "Passwort geändert!"
                cur.close()
                return jsonify(response_object), 200
            else:
                cur.close()
                return jsonify(response_object), 400
        else:
            cur.close()
            return jsonify(response_object), 400
        




@app.route('/liste', methods=['GET'])
def list_users():
    cur = conn.cursor()
    cur.execute('SELECT UserLogin, UserFirstName, UserLastName, UserRole FROM Users')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/login', methods=['POST', 'GET'])
def login_user():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        personData = request.get_json()
        login = personData['login']
        password = personData['password']
        h = sha256()
        h.update(('%s' % (password)).encode('utf-8'))
        h_password = h.hexdigest()
        cur = conn.cursor()
        cur.execute("SELECT UserPassword FROM Users WHERE UserLogin='{}'".format(login))
        user_pw = cur.fetchall()
        cur.close()
        if (h_password == user_pw[0][0]):
           user(login)
           response_object['message'] = 'Login erfolgreich!'
           return jsonify(response_object)
        else:
            login = ''
            password = ''
            return jsonify(response_object), 400

@app.route('/user/<login>', methods=['GET'])
def user(login):
        cur = conn.cursor()
        cur.execute("SELECT UserLogin, UserFirstName, UserLastName, UserRole FROM Users WHERE UserLogin='{}'".format(login))
        userData = cur.fetchall()
        cur.close()
        user = User(userData[0][0], userData[0][1], userData[0][2], userData[0][3])
        session["user"] = json.dumps(user.__dict__)
        return jsonify(session["user"])

@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    response_object = {'status': 'success'}
    session.pop("user", None)
    return jsonify(response_object)

@app.route('/course/add', methods=['POST'])
def add_course():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        courseData = request.get_json()
        title = courseData['title']
        description = courseData['description']
        startdate = courseData['startdate']
        enddate = courseData['enddate']
        instructor = courseData['instructor']
        cur = conn.cursor()
        cur.execute("INSERT INTO Course(CourseTitle, CourseDescription, CourseStart, CourseEnd, CourseUser) VALUES('{}', '{}', '{}', '{}', '{}')".format(title, description, startdate, enddate, instructor))
        conn.commit()
        cur.close()
        response_object['message'] = 'Kurs hinzugefügt!'
    return jsonify(response_object)

@app.route('/course/list/<user_login>', methods=['GET'])
def list_courses(user_login):
    cur = conn.cursor()
    cur.execute("SELECT CourseID, CourseTitle, CourseDescription, CourseStart, CourseEnd FROM Course WHERE CourseUser='{}'".format(user_login))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/course/list/all', methods=['GET'])
def list_all_courses():
    cur = conn.cursor()
    cur.execute("SELECT CourseID, CourseTitle, CourseDescription, CourseStart, CourseEnd FROM Course")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/course/delete/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        cur = conn.cursor()
        cur.execute("DELETE FROM Course WHERE CourseID='{}'".format(course_id))
        conn.commit()
        cur.close()
        response_object['message'] = 'Kurs gelöscht!'
    return jsonify(response_object)

@app.route('/course/edit/<course_id>', methods=['PUT'])
def edit_course(course_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        courseData = request.get_json()
        title = courseData['title']
        description = courseData['description']
        startdate = courseData['startdate']
        enddate = courseData['enddate']
        cur = conn.cursor()
        cur.execute("START TRANSACTION;")
        if (title):
            cur.execute("UPDATE Course SET CourseTitle='{}' WHERE CourseID='{}'".format(title, course_id))
        if (description):
            cur.execute("UPDATE Course SET CourseDescription='{}' WHERE CourseID='{}'".format(description, course_id))
        if (startdate):
            cur.execute("UPDATE Course SET CourseStart='{}' WHERE CourseID='{}'".format(startdate, course_id))
        if (enddate):
            cur.execute("UPDATE Course SET CourseEnd='{}' WHERE CourseID='{}'".format(enddate, course_id))
        cur.execute("COMMIT;")
        conn.commit()
        cur.close()
        response_object['message'] = 'Kurs editiert!'
    return jsonify(response_object)

@app.route('/questions/list', methods=['GET'])
def list_questions():
    cur = conn.cursor()
    cur.execute('SELECT QuestionID, QuestionText, QuestionType FROM Question')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/survey/add', methods=['POST'])
def add_survey():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        surveyData = request.get_json()
        title = surveyData['title']
        description = surveyData['description']
        password = surveyData['password']
        courseID = surveyData['courseID']
        questionList = surveyData['questionList']
        h = sha256()
        h.update(('%s' % (password)).encode('utf-8'))
        h_password = h.hexdigest()
        cur = conn.cursor()
        cur.execute("START TRANSACTION;")
        cur.execute("INSERT INTO Survey(SurveyTitle, SurveyDescription, SurveyPassword, CourseID) VALUES('{}', '{}', '{}', '{}');".format(title, description, h_password, courseID))
        cur.execute("SELECT @SurveyID:=SurveyID FROM Survey ORDER BY SurveyID DESC LIMIT 1;")
        for questionID in questionList:
            cur.execute("INSERT INTO Survey_Question(SurveyID, QuestionID) VALUES(@SurveyID, '{}');".format(questionID))
        cur.execute("COMMIT;")
        conn.commit()
        cur.close()
        response_object['message'] = 'Kurs hinzugefügt!'
    return jsonify(response_object)

@app.route('/survey/list/<user_login>', methods=['GET'])
def list_surveys(user_login):
    cur = conn.cursor()
    cur.execute("SELECT SurveyID, SurveyTitle, SurveyDescription, Survey.CourseID FROM Survey INNER JOIN Course ON Survey.CourseID = Course.CourseID WHERE Course.CourseUser='{}'".format(user_login))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/survey/list/all', methods=['GET'])
def list_all_surveys():
    cur = conn.cursor()
    cur.execute("SELECT SurveyID, SurveyTitle, SurveyDescription, Survey.CourseID FROM Survey INNER JOIN Course ON Survey.CourseID = Course.CourseID")
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/survey/delete/<survey_id>', methods=['DELETE'])
def delete_survey(survey_id):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        cur = conn.cursor()
        cur.execute("DELETE FROM Survey WHERE SurveyID='{}'".format(survey_id))
        conn.commit()
        cur.close()
        response_object['message'] = 'Umfrage gelöscht!'
    return jsonify(response_object)

@app.route('/survey/edit/<survey_id>', methods=['PUT'])
def edit_survey(survey_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        surveyData = request.get_json()
        title = surveyData['title']
        description = surveyData['description']
        password = surveyData['password']
        cur = conn.cursor()
        cur.execute("START TRANSACTION;")
        if (title):
            cur.execute("UPDATE Survey SET SurveyTitle='{}' WHERE SurveyID='{}'".format(title, survey_id))
        if (description):
            cur.execute("UPDATE Survey SET SurveyDescription='{}' WHERE SurveyID='{}'".format(description, survey_id))
        if (password):
            h = sha256()
            h.update(('%s' % (password)).encode('utf-8'))
            h_password = h.hexdigest()
            cur.execute("UPDATE Survey SET SurveyPassword='{}' WHERE SurveyID='{}'".format(h_password, survey_id))
        cur.execute("COMMIT;")
        conn.commit()
        cur.close()
        response_object['message'] = 'Kurs editiert!'
    return jsonify(response_object)

@app.route('/survey/password/<survey_id>', methods=['POST'])
def survey_verify(survey_id):
    response_object = {'status': 'success'}
    if request.method == 'POST':
        surveyData = request.get_json()
        surveyID = survey_id
        password = surveyData['password']
        h = sha256()
        h.update(('%s' % (password)).encode('utf-8'))
        h_password = h.hexdigest()
        cur = conn.cursor()
        cur.execute("SELECT SurveyPassword FROM Survey WHERE SurveyID='{}'".format(surveyID))
        survey_pw = cur.fetchall()
        cur.close()
        if (h_password == survey_pw[0][0]):
           #get_survey_data(survey_id)
           response_object['message'] = 'Erfolgreich!'
           return jsonify(response_object)
        else:
            password = ''
            return jsonify(response_object), 400

@app.route('/survey/questions/<survey_id>', methods=['GET'])
def get_question_data(survey_id):
    cur = conn.cursor()
    #cur.execute('SELECT Survey.SurveyID, Survey.SurveyTitle, Survey.SurveyDescription, Question.QuestionID, Question.QuestionText, Question.QuestionType, AnswerOption.AnswerOptionID, AnswerOption.AnswerOptionText FROM Survey_Question INNER JOIN Survey ON Survey_Question.SurveyID = Survey.SurveyID INNER JOIN Question ON Survey_Question.QuestionID = Question.QuestionID INNER JOIN AnswerOption ON Survey_Question.QuestionID = AnswerOption.QuestionID WHERE Survey.SurveyID={};'.format(survey_id))
    cur.execute('SELECT Question.QuestionID, Question.QuestionText, Question.QuestionType FROM Survey_Question INNER JOIN Survey ON Survey_Question.SurveyID = Survey.SurveyID INNER JOIN Question ON Survey_Question.QuestionID = Question.QuestionID INNER JOIN AnswerOption ON Survey_Question.QuestionID = AnswerOption.QuestionID WHERE Survey.SurveyID={} GROUP BY Question.QuestionID;'.format(survey_id))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)


@app.route('/survey/answeroptions/<survey_id>', methods=['GET'])
def get_answeroption_data(survey_id):
    cur = conn.cursor()
    cur.execute('SELECT AnswerOption.QuestionID, AnswerOption.AnswerOptionText, AnswerOption.AnswerOptionID FROM Survey_Question INNER JOIN Survey ON Survey_Question.SurveyID = Survey.SurveyID INNER JOIN Question ON Survey_Question.QuestionID = Question.QuestionID INNER JOIN AnswerOption ON Survey_Question.QuestionID = AnswerOption.QuestionID WHERE Survey.SurveyID={};'.format(survey_id))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)


@app.route('/survey/send', methods=['POST'])
def survey_send():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        AnswerData = request.get_json()
        surveyID = AnswerData['survey']
        answers = AnswerData['answers']
        cur = conn.cursor()
        cur.execute("START TRANSACTION;")
        for answer in answers:
            cur.execute("INSERT INTO Answer(SurveyID, AnswerOptionID) VALUES('{}', '{}');".format(surveyID, answer))
        cur.execute("COMMIT;")
        conn.commit()
        cur.close()
    return jsonify(response_object)

if __name__ == '__main__':
    app.run(debug=True)