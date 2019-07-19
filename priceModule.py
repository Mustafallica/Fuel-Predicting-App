import sqlite3
from datetime import date, datetime


def getprice(reqgallon, address, email, date):

    state = 'Texas'
    current_price = 1.50
    oneper = 0.01

    comanyprofit = (oneper*10)
    print(comanyprofit)
    userstate = address.split(',')  # index1
    locationfactor = 0
    ratehistoryfactor = 0
    gallonrequiredfield = 0
    ratefluctuation = 0
    print(userstate[1])
    if(state == userstate[1] or 'texas' == userstate[1] or 'taxas' == userstate[1]):
        locationfactor = 0.02
        print(locationfactor)
    else:
        locationfactor = (oneper * 4)
        print('else location', locationfactor)

    yn = calculate_ratehistory(email)
    if yn == True:
        ratehistoryfactor = oneper
        print(ratehistoryfactor)
    else:
        ratehistoryfactor = 0
        print(ratehistoryfactor)

    if int(reqgallon) >= 1000:
        gallonrequiredfield = (oneper*2)
        print(gallonrequiredfield)
    else:
        gallonrequiredfield = (oneper*3)
        print(gallonrequiredfield)

    season = calculaterate_f(date)
    if season == 'summer':
        ratefluctuation = (oneper * 4)
        print(ratefluctuation)
    else:
        ratefluctuation = (oneper*3)
        print(ratefluctuation)

    Price_Diff = sumPrice(current_price, locationfactor, ratehistoryfactor,
                          gallonrequiredfield, comanyprofit, ratefluctuation)
    suggestedprice = current_price+Price_Diff

    return round(suggestedprice, 5)


def calculate_ratehistory(email):
    con = sqlite3.connect('client1.db')
    address = ""
    state = ""

    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM FuelQoute1")
        rows = cur.fetchall()
        for row in rows:
            dbUser = row[2]

            if dbUser == email:
                return True
    return False


def calculaterate_f(date):
    datesplit = date.split('-')

    if datesplit[1] == 6 or datesplit[1] == 7 or datesplit[1] == 8 or datesplit[1] == 9:
        return 'summer'

    return 'wint'


def getTotal(reqgallon, price):
    total = (int(reqgallon) * price)
    return total


def sumPrice(current_price, locationfactor, ratehistoryfactor, gallonrequiredfield, comanyprofit, ratefluctuation):
    margin = (current_price * ((locationfactor-ratehistoryfactor) +
                               gallonrequiredfield+comanyprofit+ratefluctuation))
    return margin
