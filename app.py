import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/viewList')
def list():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row

    cur = connection.cursor()
    cur.execute('select * from users')

    rows = cur.fetchall()
    return render_template("/list.html", rows = rows)


@app.route('/adduserecord', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            name = request.form['name']
            dbName = request.form['dbName']
            logInfo = request.form['logInfo']
            metricInfo = request.form['metricInfo']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                cur.execute('INSERT INTO users (name,dbName,logInfo,metricInfo) VALUES(?, ?, ?, ?)',
                                (name,dbName,logInfo,metricInfo))

                con.commit()
                msg = "User Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("/result.html", msg=msg)
            con.close()

    return "success"

@app.route('/register')
def new_entry():
    return render_template('user.html')

if __name__ == "__main__":
        app.run(debug=True)