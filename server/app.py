from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS
import mariadb, sys, yaml, json
from hashlib import sha256

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
        database="test_db"
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
        cur.execute("INSERT INTO User(login, vorname, nachname, rolle, passwort) VALUES('{}', '{}', '{}', '{}', '{}')".format(login, vorname, nachname, rolle, h_password))
        conn.commit()
        cur.close()
        response_object['message'] = 'User hinzugefügt!'
    return jsonify(response_object)

@app.route('/remove/<user_login>', methods=['DELETE'])
def delete_user(user_login):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        cur = conn.cursor()
        cur.execute("DELETE FROM User WHERE Login='{}'".format(user_login))
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
        if (login):
            cur.execute("UPDATE User SET Login='{}' WHERE Login='{}'".format(login, user_login))
        if (vorname):
            cur.execute("UPDATE User SET Vorname='{}' WHERE Login='{}'".format(vorname, user_login))
        if (nachname):
            cur.execute("UPDATE User SET Nachname='{}' WHERE Login='{}'".format(nachname, user_login))
        if (rolle):
            cur.execute("UPDATE User SET Rolle='{}' WHERE Login='{}'".format(rolle, user_login))
        if (password):
            h = sha256()
            h.update(('%s' % (password)).encode('utf-8'))
            h_password = h.hexdigest()
            cur.execute("UPDATE User SET Passwort='{}' WHERE Login='{}'".format(h_password, user_login))
        conn.commit()
        cur.close()
        response_object['message'] = 'User editiert!'
    return jsonify(response_object)

@app.route('/liste', methods=['GET'])
def list_users():
    cur = conn.cursor()
    cur.execute('SELECT Login, Vorname, Nachname, Rolle FROM User')
    data = cur.fetchall()
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
        cur.execute("SELECT Passwort FROM User WHERE Login='{}'".format(login))
        user_pw = cur.fetchall()
        if (h_password == user_pw[0][0]):
           print("Login erfolgreich!")
           user(login)
           response_object['message'] = 'Login erfolgreich!'
        return jsonify(response_object)

@app.route('/user/<login>', methods=['GET'])
def user(login):
        cur = conn.cursor()
        cur.execute("SELECT Login, Vorname, Nachname, Rolle FROM User WHERE Login='{}'".format(login))
        userData = cur.fetchall()
        user = User(userData[0][0], userData[0][1], userData[0][2], userData[0][3])
        session["user"] = json.dumps(user.__dict__)
        print(session["user"])
        return jsonify(session["user"])



if __name__ == '__main__':
    app.run(debug=True)