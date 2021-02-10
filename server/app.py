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


#mariadb = mariadb(app)
'''try:
    conn = mariadb.connect(
        user="",
        password="",
        host="",
        port="",
        database=""
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)'''


CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['GET', 'POST'])
def test():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        personDetails = request.form
        vorname = personDetails['vorname']
        nachname = personDetails['nachname']
        cur = conn.cursor()
        cur.execute("INSERT INTO Person(vorname, nachname) VALUES(%s, %s)",(vorname, nachname))
        conn.commit()
        cur.close()
        response_object['message'] = 'Kursleiter hinzugefügt!'
    return jsonify(response_object)
        




@app.route('/test', methods=['GET', 'POST'])
def test_db():
    if request.method == 'POST':
        personDetails = request.form
        vorname = personDetails['vorname']
        nachname = personDetails['nachname']
        cur = conn.cursor()
        cur.execute("INSERT INTO Person(vorname, nachname) VALUES(%s, %s)",(vorname, nachname))
        conn.commit()
        cur.close()
        return 'success'
    return render_template('test.html')

@app.route('/liste', methods=['GET'])
def test2_db():
    cur = conn.cursor()
    cur.execute('SELECT * FROM Person')
    data = cur.fetchall()
    return jsonify(data)
    #return render_template('liste.html', output_data=data)

INSTRUCTORS = [
    {
        'ID': '1',
        'vorname': 'Max',
        'nachname': 'Mustermann'
    },
    {
        'ID': '2',
        'vorname': 'Susi',
        'nachname': 'Silber'
    }
]

@app.route('/instructor', methods=['GET'])
def all_instructor():
    return jsonify({
        'status': 'success',
        'instructors': INSTRUCTORS
    })

if __name__ == '__main__':
    app.run(debug=True)