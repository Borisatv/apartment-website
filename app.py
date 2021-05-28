from flask import Flask, render_template, url_for, request, session, redirect
from flaskext.mysql import MySQL
import pymysql

from createPost import Post

app = Flask(__name__)

app.secret_key = 'SECRET_KEY'

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = 'Borisatv'
app.config['MYSQL_DATABASE_PASSWORD'] = '21436587boris'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'
mysql.init_app(app)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
  
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'passwords' in request.form:
        username = request.form['username']
        password = request.form['passwords']
        cursor.execute('''SELECT * FROM users WHERE username = %s AND passwords = %s''', (username, password))
        users = cursor.fetchone()

        if users:
            session['loggedin'] = True
            session['id'] = users['id']
            session['username'] = users['username']
            return render_template('registered.html')
        else:
            msg = 'Incorrect username or password!'
    
    return render_template('account.html', msg = msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = mysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'passwords' in request.form and 'email' in request.form:
        fullname = request.form['fullname']
        username = request.form['username']
        password = request.form['passwords']
        email = request.form['email']
   
        cursor.execute('''SELECT * FROM users WHERE username = %s''', (username))
        users = cursor.fetchone()

        if users:
            msg = 'Account alredy exists!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('''INSERT INTO users(fullname, email, username, passwords) VALUES (%s, %s, %s, %s)''', (fullname, email, username, password))  
            conn.commit()

            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return render_template('register.html', msg = msg)

@app.route('/')
def home():
    if 'loggedin' in session:
        
        return render_template('registered.html', username = session['username'])
    return redirect(url_for('login'))

@app.route('/postAd', methods=['GET', 'POST'])
def postAd():
    if request.method == 'POST':
        price = request.form.get('price')
        apartmentType = request.form.get('apartmentType')
        quadrature = request.form.get('quadrature')
        city = request.form.get('city')
        Post.createPost(price, apartmentType, quadrature, city)
    return render_template('post.html')

@app.route('/main')
def showAds():
    data = Post.showPosts
    render_template('registered.html', data=data)

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)