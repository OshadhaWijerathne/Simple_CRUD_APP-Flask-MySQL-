from flask import Flask, render_template, request, redirect, url_for,flash
import pymysql

app = Flask(__name__)
app.secret_key = 'flash message'

# MySQL connection configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'crudapplication'
app.config['MYSQL_PORT'] = 3307  # Replace with your custom port

# Using pymysql to connect to the MySQL database
def get_db_connection():
    connection = pymysql.connect(host=app.config['MYSQL_HOST'],
                                  user=app.config['MYSQL_USER'],
                                  password=app.config['MYSQL_PASSWORD'],
                                  db=app.config['MYSQL_DB'],
                                  port=app.config['MYSQL_PORT'])  # Include the port here)
    return connection

@app.route('/')
def Index():

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('index.html',students = data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']  # Fixed: was using 'name' instead of 'email'
        phone = request.form['phone']  # Fixed: was using 'name' instead of 'phone'

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('Index'))
    
@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name=%s, email=%s, phone=%s WHERE id=%s", (name, email, phone, id_data))
        flash("Data Updated Successfully")
        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('Index'))    
@app.route('/delete/<string:id_data>',methods = ['POST', 'GET'])
def delete(id_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM students where id=%s", (id_data))
    flash("Data Deleted Successfully")
    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(debug=True)
