import requests
from flask import Flask, request, jsonify
import sqlite3
base_url = 'http://localhost:5000/users'

users_to_add = [
    {
        'first_name': 'John',
        'last_name': 'Doe',
        'age': 25,
        'gender': 'Male',
        'email': 'john@example.com',
        'phone': '1234567890',
        'birth_date': '1998-05-10'
    },
    {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'age': 30,
        'gender': 'Female',
        'email': 'jane@example.com',
        'phone': '9876543210',
        'birth_date': '1991-02-15'
    },
    {
        'first_name': 'Michael',
        'last_name': 'Johnson',
        'age': 40,
        'gender': 'Male',
        'email': 'michael@example.com',
        'phone': '5555555555',
        'birth_date': '1982-09-20'
    },
   
    {
        'first_name': 'David',
        'last_name': 'Williams',
        'age': 33,
        'gender': 'Male',
        'email': 'david@example.com',
        'phone': '6666666666',
        'birth_date': '1990-11-30'
    }
]

for user in users_to_add:
    response = requests.post(base_url, json=user)
    print(response.json())



app = Flask(__name__)
DATABASE = 'user_db.sqlite'

def create_user_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, age INTEGER, gender TEXT, email TEXT, phone TEXT, birth_date TEXT)''')
    conn.commit()
    conn.close()

@app.route('/users', methods=['GET'])
def get_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    user_list = []
    for user in users:
        user_list.append({'id': user[0],'first_name': user[1],'last_name': user[2],'age': user[3],'gender': user[4],'email': user[5],'phone': user[6],'birth_date': user[7]})
    return jsonify(user_list)

@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (first_name, last_name, age, gender, email, phone, birth_date) VALUES (?, ?, ?, ?, ?, ?, ?)''', (new_user['first_name'],new_user['last_name'],new_user['age'],new_user['gender'],new_user['email'],new_user['phone'],new_user['birth_date']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User created successfully'})

@app.route('/api/users', methods=['GET'])
def search_users():
    first_name = request.args.get('first_name')
    if not first_name:
        return jsonify({'message': 'Missing mandatory query parameter: first_name'}), 400
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE first_name LIKE ?', (first_name + '%',))
    users = cursor.fetchall()
    conn.close()
    user_list = []
    for user in users:
        user_list.append({'id': user[0],'first_name': user[1],'last_name': user[2],'age': user[3],'gender': user[4],'email': user[5],'phone': user[6],'birth_date': user[7]})
    return jsonify({'users': user_list,'total': len(user_list),'skip': 0,'limit': 0})

if __name__ == '__main__':
    create_user_table()
    app.run(debug=True)

