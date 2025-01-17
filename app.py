from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.config['MYSQL_HOST'] = '138.41.20.102'
app.config['MYSQL_PORT'] = 53306
app.config['MYSQL_USER'] = 'ospite'
app.config['MYSQL_PASSWORD'] = 'ospite'
app.config['MYSQL_DB'] = 'w3schools'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("home.html", titolo = "Home")

@app.route("/registrati/",methods=["GET","POST"])
def registrati():
    if request.method == 'GET':
        return render_template("register.html", titolo = "Registrati")

    cursor = mysql.connection.cursor()

    nome = request.form.get("nome","")
    cognome = request.form.get("cognome","")
    username = request.form.get("userName","")
    password = request.form.get("pass","")
    confirmPass = request.form.get("confirmPass","")

    if nome == "" or cognome == "" or username == "" or password == "" or confirmPass == "":
        flash("Errore, almeno un campo è vuoto")
        return redirect(url_for("registrati"))
    elif password != confirmPass:
        flash("Le password non concindono")
        return redirect(url_for("registrati"))

    
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query,(username,))
    if cursor.fetchone():
        flash("Username già presente")
        return redirect(url_for("registrati"))


    query = "INSERT INTO users (username,password,nome,cognome) VALUES(%s,%s,%s,%s)"
    cursor.execute(query,(username,generate_password_hash(password),nome,cognome))
    mysql.connection.commit()
    cursor.close()
    flash('Utente registrato con successo')
    return redirect(url_for("home"))
    
@app.route("/login/",methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", titolo = "Accedi")
    
    cursor = mysql.connection.cursor()

    username = request.form.get("nome","")
    password = request.form.get("pass","")
    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    hashPass = cursor.fetchone()

    if hashPass and check_password_hash(hashPass, password):
        flash("Login effettuato")
        return redirect(url_for("home"))
    
    flash("Credenziali errate")
    return redirect(url_for("login"))




app.run(debug=True)
