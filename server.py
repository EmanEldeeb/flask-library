from flask import Flask,request,redirect, url_for,render_template
import sqlite3

app = Flask(__name__)
DBNAME = 'lib2'
BOOK_T = 'Book'

conn = sqlite3.connect(f'{DBNAME}.db')
print("Opened database successfully")

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
    con = sqlite3.connect(f'{DBNAME}.db')
    try:
        title = request.form['title']
        category = request.form['category']
        isbn = request.form['isbn']
        language = request.form['language']
        edition = request.form['edition']
        description = request.form['description']
        pagenumber = request.form['pagenumber']
        
        cur = con.cursor()
        cur.execute(f'INSERT INTO {BOOK_T} (BookTitle,BookCategory,BookIsbn,BookLanguage,BookEdition,BookDescription,BookPagesNo) VALUES (?,?,?,?,?,?,?)', (title,category,isbn,language,edition,description,pagenumber))
        con.commit()
        print("added new row")
    except Exception as err:
        con.rollback()
        print(f'SQLite error: {err}')
    finally:
        con.close()
        return redirect(url_for("index"))

@app.route('/edit', methods = ['POST'])
def edit():
    con = sqlite3.connect(f'{DBNAME}.db')
    try:
        title = request.form['title']
        category = request.form['category']
        isbn = request.form['isbn']
        language = request.form['language']
        edition = request.form['edition']
        description = request.form['description']
        pagenumber = request.form['pagenumber']
        
        cur = con.cursor()
        cur.execute(f'UPDATE {BOOK_T} SET BookTitle=?,BookCategory=?,BookIsbn=?,BookLanguage=?,BookEdition=?,BookDescription=?,BookPagesNo=? WHERE BookTitle=?', (title,category,isbn,language,edition,description,pagenumber,title))
        con.commit()
        print("updated new row")
    except Exception as err:
        con.rollback()
        print(f'SQLite error: {err}')
    finally:
        con.close()
        return redirect(url_for("index"))

if __name__=='__main__':
    app.run(debug=True)      