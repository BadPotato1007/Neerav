from flask import Flask, render_template, request, jsonify
import mysql.connector as sql
from mysql.connector import Error

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/questions', methods=['GET'])
def get_data():
    try:
        # Establish connection to the database
        connection = sql.connect(host="localhost", passwd="deens", user="root", database="runes")
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM questions")
            results = cursor.fetchall()
            return jsonify(results)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Close connection
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/data', methods=['POST'])
def post_data():
    try:
        data = request.json
        name = data.get('name')
        value = data.get('value')

        # Establish connection to the database
        connection = sql.connect(host="localhost", passwd="deens", user="root", database="runes")
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("INSERT INTO questions (name, value) VALUES (%s, %s)", (name, value))
            connection.commit()
            return jsonify({"message": "Data inserted successfully!"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Close connection
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)