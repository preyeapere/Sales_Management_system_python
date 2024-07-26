from flask import Flask
from flask import render_template
from flask import request
import sqlite3

app = Flask(__name__)

# Home Page route
@app.route("/")
def home():
    return render_template("home.html")

# Route to form used to add a new Sales to the database
@app.route("/enternew")
def enternew():
    return render_template("sales.html")

# Route to add a new record (INSERT) sales data to the database
@app.route("/addrec", methods = ['POST', 'GET'])
def addrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            product_nm = request.form['product_nm']
            category = request.form['category']
            quantity = request.form['quantity']
            price = request.form['price']

            # Connect to SQLite3 database and execute the INSERT
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO sales (product_nm, category, quantity, price) VALUES (?,?,?,?)",(product_nm, category, quantity, price))

                con.commit()
                msg = "product information successfully added to database, thanks"
        except:
            con.rollback()
            msg = "Error in the INSERT"

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route to SELECT all data from the database and display in a table      
@app.route('/list')
def list():
    # Connect to the SQLite3 datatabase and 
    # SELECT rowid and all Rows from the Sales table.
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("SELECT rowid, * FROM sales")

    rows = cur.fetchall()
    con.close()
    # Send the results of the SELECT to the List.html page
    return render_template("list.html",rows=rows)

# Route that will SELECT a specific row in the database then load an Edit form 
@app.route("/edit", methods=['POST','GET'])
def edit():
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            id = request.form['id']
            # Connect to the database and SELECT a specific rowid
            con = sqlite3.connect("database.db")
            con.row_factory = sqlite3.Row

            cur = con.cursor()
            cur.execute("SELECT rowid, * FROM sales WHERE rowid = " + id)

            rows = cur.fetchall()
        except:
            id=None
        finally:
            con.close()
            # Send the specific record of data to edit.html
            return render_template("edit.html",rows=rows)

# Route used to execute the UPDATE statement on a specific record in the database
@app.route("/editrec", methods=['POST','GET'])
def editrec():
    # Data will be available from POST submitted by the form
    if request.method == 'POST':
        try:
            # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['rowid']
            product_nm = request.form['product_nm']
            category = request.form['category']
            quantity = request.form['quantity']
            price = request.form['price']

            # UPDATE a specific record in the database based on the rowid
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE sales SET product_nm='"+product_nm+"', category='"+category+"', quantity='"+quantity+"', price='"+price+"' WHERE rowid="+rowid)

                con.commit()
                msg = "Sales information successfully edited in the database"
        except:
            con.rollback()
            msg = "Error in the Edit: UPDATE sales SET product_nm="+product_nm+"', category='"+category+"', quantity='"+quantity+"', price='"+price+"' WHERE rowid="+rowid

        finally:
            con.close()
            # Send the transaction message to result.html
            return render_template('result.html',msg=msg)

# Route used to DELETE a specific record in the database    
@app.route("/delete", methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        try:
             # Use the hidden input value of id from the form to get the rowid
            rowid = request.form['id']
            # Connect to the database and DELETE a specific record based on rowid
            with sqlite3.connect('database.db') as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM sales WHERE rowid="+rowid)

                    con.commit()
                    msg = "Sales information successfully deleted from the database"
        except:
            con.rollback()
            msg = "Error in the DELETE"

        finally:
            con.close()
            # Send the transaction message to Result.html
            return render_template('result.html',msg=msg)
        
if __name__ == '__main__':
      
         app.run(debug = True,port=5006)