from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import mariadb, sys, yaml

app = Flask(__name__)
app.config.from_object(__name__)

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

@app.route('/add', methods=['GET', 'POST'])
def test():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        personData = request.get_json()
        vorname = personData['vorname']
        nachname = personData['nachname']
        cur = conn.cursor()
        cur.execute("INSERT INTO Person(vorname, nachname) VALUES({}, {})".format(vorname, nachname))
        conn.commit()
        cur.close()
        response_object['message'] = 'Kursleiter hinzugefügt!'
    return jsonify(response_object)

@app.route('/remove/<instructor_id>', methods=['DELETE'])
def delete_instructor(instructor_id):
    response_object = {'status': 'success'}
    if request.method == 'DELETE':
        cur = conn.cursor()
        cur.execute("DELETE FROM Person WHERE ID={}".format(instructor_id))
        conn.commit()
        cur.close()
        response_object['message'] = 'Kursleiter gelöscht!'
    return jsonify(response_object)
        
@app.route('/edit/<instructor_id>', methods=['PUT'])
def edit_instructor(instructor_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        personData = request.get_json()
        vorname = personData['vorname']
        nachname = personData['nachname']
        cur = conn.cursor()
        cur.execute("UPDATE Person SET Vorname='{}', Nachname='{}' WHERE ID={}".format(vorname, nachname, instructor_id))
        conn.commit()
        cur.close()
        response_object['message'] = 'Kursleiter editiert!'
    return jsonify(response_object)

@app.route('/liste', methods=['GET'])
def test2_db():
    cur = conn.cursor()
    cur.execute('SELECT * FROM Person')
    data = cur.fetchall()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)