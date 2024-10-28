import sqlite3
from flask import Flask,jsonify

app = Flask(__name__)

def connection():
    name = "cars.db"
    con = sqlite3.connect(name)
    return con

#Create any database with sqlite
def create_table(car_name, engine, price, year):
    con = connection()
    cursor = con.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cars(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        car_name TEXT,
        engine TEXT,
        price INTEGER,
        year INTEGER)''')

    cursor.execute('''
    INSERT INTO cars (car_name, engine, price, year) 
    VALUES (?, ?, ?, ?)''',
    (car_name, engine, price, year))

    con.commit()

#Read txt file and input infos in database
def infos():
    with open("cars.txt", "r") as f:
        for info in f:
            inf = info.split(",")
            car_name = inf[0]
            engine = inf[1]
            price = inf[2]
            year = inf[3]
            create_table(car_name, engine, price, year)
    

def read_database():
    con = connection()
    cursor = con.cursor()
    cursor.execute('''SELECT * from cars''')
    rows = cursor.fetchall()

    description = [] 
    for i in cursor.description:
        description.append(i[0])

    result_dict = []
    for row in rows:
        row_dict = {}
        for i in range(len(description)):
            row_dict[description[i]] = row[i]
        result_dict.append(row_dict)
        
    con.close()
    return result_dict
    
@app.route("/")
def index():
    return "Please enter this url to get database:http://127.0.0.1:5000/cars"

@app.route("/cars")
def add_db(): 
    return jsonify(read_database())
    
    
if __name__ == "__main__":
    app.run(debug=True) 