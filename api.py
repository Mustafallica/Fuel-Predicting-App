import sqlite3

from flask import Flask, jsonify, request, render_template, redirect, url_for, flash, session

from func import checkInClient, getaddress, addFuel, sign_login
from priceModule import getprice, getTotal

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "bhenchod"


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
      return render_template("login.html")
    if request.method == 'POST':

          username = request.form["email"]
          password = request.form["pass"]
          completion = validate(username, password)
          if completion == False:
              error = 'Invalid Credentials. Please try again.'
              print(error)
              return redirect(url_for('login'))
          else:
              session['signup_user'] = username
              return redirect(url_for('profile', username=username))


def validate(username, password):
    con = sqlite3.connect('client1.db')
    completion = False
    with con:
                cur = con.cursor()
                cur.execute("SELECT * FROM User")
                rows = cur.fetchall()
                for row in rows:
                    dbUser = row[1]
                    dbPass = row[2]

                    if dbUser == username:
                        if dbPass == password:
                            completion = True

    return completion


@app.route('/profile/fuelquote', methods=['GET', 'POST'])
def fuelquote():
    mix = ""
    if request.method == 'GET':
      error = "Your profile is Up"
      username = session.get('signup_user', None)

      yn = checkInClient(username)
      if yn == False:
          error = 'Please first make profile!'
      if yn == True:
          mix = getaddress(username)
          session['my_var2'] = mix
      return render_template("fuelquote.html", error=error, mix=mix, username=username)

    if request.method == 'POST':

        if request.form['action'] == 'calculate':

         reqGallon = request.form["inputreq"]
         date = request.form["date"]
         my_var2 = session.get('my_var2', None)
         username = session.get('signup_user', None)
         session['date'] = date
         price = getprice(reqGallon, my_var2, username, date)

         session['reqgallon'] = reqGallon

         session['address'] = my_var2
         session['price'] = price

         getTotalPrice = getTotal(reqGallon, price)
         session['totalp'] = getTotalPrice
         mix = my_var2
         return render_template("fuelquote.html", reqGallon=reqGallon, date=date, price=price, getTotalPrice=getTotalPrice, mix=mix, username=username)

        if request.form['action'] == 'submit':
           reqGallon = session.get('reqgallon', None)
           date = session.get('date', None)
           mix = session.get('address', None)
           email = session.get('signup_user', None)
           price = session.get('price', None)
           getTotalPrice = session.get('totalp', None)
           username = session.get('signup_user', None)
           addFuel(reqGallon, date, mix, price, getTotalPrice, email)

           return render_template("fuelquote.html", reqGallon=reqGallon, date=date, mix=mix, price=price, getTotalPrice=getTotalPrice, username=username)


@app.route('/profile/fuelqotehistory', methods=['GET', 'POST'])
def fuelqotehistory():
    if request.method == 'GET':
        con = sqlite3.connect('client1.db')
        price = []
        date = []
        totalgallon = []
        totalprice = []

        with con:
            cur = con.cursor()
            my_var = session.get('signup_user', None)
            cur.execute("SELECT * FROM FuelQoute1 where email=?", (my_var,))

            rows = cur.fetchall()
            for row in rows:
                g = row[1]
                d = row[5]
                p = row[6]
                tp = row[7]
                date.append(d)
                price.append(p)
                totalgallon.append(g)
                totalprice.append(tp)

        username = session.get('signup_user', None)

    return render_template("fuelqotehistory.html", price=price, date=date, totalprice=totalprice, totalgallon=totalgallon, username=username)


@app.route('/signup/profile', methods=['GET', 'POST'])
@app.route('/login/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'GET':
      username = session.get('signup_user', None)
      return render_template("profile.html", username=username)
    if request.method == 'POST':

        username = session.get('signup_user', None)

        Firstname = request.form["text-input1"]

        Lastname = request.form["text-input2"]
        Address = request.form["text-input4"]
        Address1 = request.form["text-input5"]
        city = request.form["text-input6"]
        state = request.form["text-input7"]
        zipcode = request.form["text-input8"]

        if Firstname == '' and Lastname == '' and Address == '' and Address1 == '' and city == '' and state == '' and zipcode == '':
            error = "please fill this form completely"
            print(error)
            return render_template("profile.html", username=username, error=error)
        else:
         try:
          con = sqlite3.connect('client1.db')

          with con:
            cur = con.cursor()
            cur.execute(''' INSERT INTO ClientInfo(Firstname,Lastname,Email,Address,Address1,city,state,zipcode)
            VALUES(?,?,?,?,?,?,?,?) ''', (str(Firstname), str(Lastname), str(username), str(Address), str(Address1), str(city), str(state), str(zipcode)))
            con.commit()
            msg = "Record successfully added"
         except:
            con.rollback()
            msg = "error in insert operation"

         finally:
             con.close()
             username = username
             return render_template("profile.html", Firstname=Firstname, Lastname=Lastname, Address=Address, Address1=Address1, city=city, state=state, zipcode=zipcode, username=username)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
      return render_template("signup.html")
    if request.method == 'POST':

        username = request.form["email"]
        password = request.form["pass"]
        sign_login(username, password)
        completion = validate(username, password)
        session['signup_user'] = username
        if completion == True:
            return redirect(url_for('profile', username=username))


if __name__ == '__main__':
    app.run(debug=True)
