from flask import Flask,request,redirect, url_for,render_template
import sqlite3

app = Flask(__name__)
DBNAME = 'library'
BOOK_T = 'book_t'

conn = sqlite3.connect(f'{DBNAME}.db')
print("Opened database successfully")

conn.execute(f'CREATE TABLE IF NOT EXISTS {BOOK_T} (title,category,isbn,language,edition,description,pagenumber)')
print("Table created successfully")
conn.close()

@app.route('/')
def index():
   con = sqlite3.connect(f'{DBNAME}.db')
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute(f'select * from {BOOK_T}')
   
   rows = cur.fetchall(); 
   return render_template("index.html", rows=rows)


@app.route('/add',methods = ['POST'])
def add():
    try:
        title = request.form['title']
        category = request.form['category']
        isbn = request.form['isbn']
        language = request.form['language']
        edition = request.form['edition']
        description = request.form['description']
        pagenumber = request.form['pagenumber']
        
        with sqlite3.connect(f'{DBNAME}.db') as con:
            cur = con.cursor()
            cur.execute(f'INSERT INTO {BOOK_T} (title,category,isbn,language,edition,description,pagenumber) VALUES (?,?,?,?,?,?,?)', (title,category,isbn,language,edition,description,pagenumber))
            con.commit()
            print("added new row")
    except Exception as err:
        con.rollback()
        print(f'SQLite error: {err}')
    finally:
        con.close()
        return redirect(url_for("index"))

if __name__=='__main__':
    app.run(debug=True)      