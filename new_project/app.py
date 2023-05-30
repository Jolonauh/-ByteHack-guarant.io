from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn





@app.route('/warranties', methods = ['GET'])
def index():
    args = request.args.to_dict()
    conn = get_db_connection()
    string = 'SELECT * FROM warranty'
    delimiter = " AND "
    query_list = []

    if not args.get('category') is None:
        query_list.append(f'category="{args.get("category")}"')
    if not args.get('low') is None:
        query_list.append(f'price >= {args.get("low")}')
    if not args.get('high') is None:
        query_list.append(f'price <= {args.get("high")}')
    
    if len(query_list) != 0:
        string += " WHERE " + delimiter.join(query_list)

    warranties = conn.execute(string).fetchall()
    conn.close()
    result = [dict(row) for row in warranties]
    resp = Response(str(result))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/user/<username>', methods = ['GET'])
def user(username):
    conn = get_db_connection()
    users = conn.execute(f'SELECT * FROM users WHERE name="{username}"').fetchall()
    userdata = dict(users[0])["warranties"].split(",")
    print(userdata)
    result = []
    for id in userdata:
        if id == '':
            continue
        warranty = conn.execute(f'SELECT * FROM warranty WHERE id="{id}"').fetchall()
        result.append(dict(warranty[0]))
    conn.close()
    return result

@app.route('/user/<username>', methods = ['POST'])
def update(username):
    data = request.get_json()
    conn = get_db_connection()
    string = "INSERT INTO warranty (brand, name, price, website, startdate, enddate, category) VALUES "
    cursor = conn.cursor()
    warranty_list = []
    for warranty in data.get('warranties'):
        update = f"('{warranty.get('brand')}', '{warranty.get('name')}', {warranty.get('price')}, '{warranty.get('datawebsite')}', '{warranty.get('startdate')}', '{warranty.get('enddate')}', '{warranty.get('category')}')"
        cursor.execute(string + update)
        conn.commit()
        warranty_list.append(str(cursor.lastrowid))
    user = dict(conn.execute(f'SELECT * FROM users WHERE name="{username}"').fetchall()[0])
    user_id = user.get("id")
    old_warranties = user.get("warranties").split(",")
    warranty_list.extend(old_warranties)
    new_warranties = ','.join(warranty_list)
    conn.execute(f'UPDATE users SET warranties="{new_warranties}" WHERE id={user_id}')
    conn.commit()
    conn.close()
    return "Success! Added a new warranty!"


@app.route('/register', methods = ['POST'])
def register():
    data = request.args.to_dict()
    conn = get_db_connection()
    if not data.get('username') is None:
        username=data.get('username')
        conn.execute(f"INSERT INTO users (name, warranties) VALUES ('{username}', '')")
        conn.commit()
        return "Success! Registered"
    return "No username given in query"

@app.route('/user/<username>/tracking', methods = ['POST'])
def add_tracking(username):
    data = request.args.to_dict()
    conn = get_db_connection()
    if not data.get('id') is None:
        id=data.get('id')
        user = dict(conn.execute(f'SELECT * FROM users WHERE name="{username}"').fetchall()[0])
        user_id = user.get("id")
        old_warranties = user.get("warranties").split(",")
        old_warranties.append(f'{id}')
        new_warranties = ','.join(old_warranties)
        conn.execute(f'UPDATE users SET warranties="{new_warranties}" WHERE id={user_id}')
        conn.commit()
        return "Success! Added to tracking list"
    return "No id given in query"