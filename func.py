import sqlite3

from flask import flash


def checkInClient(myvar):
    con = sqlite3.connect('client1.db')
    completion = False
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ClientInfo")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[3]

            if dbUser == myvar:
                completion = True

    return completion


def getaddress(myvar):
    con = sqlite3.connect('client1.db')
    address = ""
    state = ""

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ClientInfo")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[3]

            if dbUser == myvar:
                address = row[4]
                state = row[7]

    mix = (address+','+state)

    return mix


def addFuel(reqGallon, date, address, price, totalp, email):
    con = sqlite3.connect('client1.db')
    try:
      with con:
         cur = con.cursor()
         cur.execute(''' INSERT INTO FuelQoute1(gallonreq,email,Address,City,date,price,totalprice)
               VALUES(?,?,?,?,?,?,?) ''', (
             reqGallon, str(email), str(address), str('tax'), str(date), price, totalp))
         con.commit()
         msg = "Record successfully added"

    except:
       con.rollback()
       msg = "error in insert operation"

    finally:
       con.close()
       print("Done")
       flash('Congratulations,client successfully saved')


def sign_login(username, password):
    try:
      con = sqlite3.connect('client1.db')

      with con:
         cur = con.cursor()
         cur.execute(''' INSERT INTO user(email,password)
                    VALUES(?,?) ''', (str(username), str(password)))
         con.commit()
         msg = "Record successfully added"

    except:
      con.rollback()
      msg = "error in insert operation"

    finally:
       con.close()
