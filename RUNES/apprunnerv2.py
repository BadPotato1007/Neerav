from flask import Flask, request, jsonify, render_template, redirect, url_for, make_response, Response
import json
import mysql.connector
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'user': 'runes',
    'password': 'root',
    'host': '192.168.100.133',
    'database': 'runes'
}

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'adicomp05@gmail.com'  # Sender email (must be a Gmail account)
app.config['MAIL_PASSWORD'] = 'lmao'                 # Use an App Password, not your actual password
app.config['MAIL_DEFAULT_SENDER'] = 'adicomp05@gmail.com'
mail = Mail(app)

@app.route('/send_mail', methods=['GET', 'POST'])
def send_mail():
    if request.method == 'POST':
        sender_name = request.form['name']
        sender_email = request.form['email']
        message_body = request.form['message']

        msg = Message(
            subject=f"[RUNES] Contact Form: {sender_name}",
            recipients=['runes@gmail.com'],
            body=f"Name: {sender_name}\nEmail: {sender_email}\n\nMessage:\n{message_body}"
        )

        try:
            mail.send(msg)
            return "Message sent successfully!"
        except Exception as e:
            return f"Failed to send email: {str(e)}"

@app.route('/')
def home():
    username = request.cookies.get('username')
    if username:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Fetch correctq, totalq, and subject attempts
        cursor.execute("""
            SELECT username, correctq AS C, totalq AS T, 
                phy_attempted AS phy,
                chem_attempted AS chem,
                math_attempted AS math
            FROM userdata 
            WHERE username = %s
        """, (username,))
        
        userdata = cursor.fetchone()
        cursor.close()
        conn.close()

        if not userdata:
            return "User not found", 404

        # Compute accuracy
        correct = userdata.get('C', 0) or 0
        total = userdata.get('T', 0) or 0
        accuracy = correct / total if total else 0

        # Add fields needed by template
        userdata['totalq'] = total
        userdata['acc'] = round(accuracy * 100, 2)  # in %
        userdata['phy'] = userdata.get('phy', 0)
        userdata['chem'] = userdata.get('chem', 0)
        userdata['math'] = userdata.get('math', 0)
        return render_template('index.html', username=username, userdata=userdata)
    
    return redirect(url_for('signup_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/signup', methods=['GET'])
def signup_page():
    return render_template('signup.html')

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    pass1 = data.get('pass1')
    email = data.get('email')

    if not username or not pass1 or not email:
        return jsonify({'error': 'Missing username, email or password'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userdata (username, email, pass) VALUES (%s, %s, %s)", (username, email, pass1))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'User created successfully!'})
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    pass1 = data.get('pass1')

    if not username or not pass1:
        return jsonify({'error': 'Missing username or password'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT pass FROM userdata WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result and result[0] == pass1:
        resp = make_response(jsonify({'message': 'Login successful'}))
        resp.set_cookie('username', username)
        return resp
    return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/trivia_start')
def trivia_start():
    username = request.cookies.get('username')
    if not username:
        return redirect(url_for('login_page'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT username, correctq AS C, totalq AS T FROM userdata WHERE username = %s", (username,))
    userdata = cursor.fetchone()

    if not userdata:
        return "User not found", 404

    # Compute accuracy and inject it into userdata
    C = userdata['C'] or 0
    T = userdata['T'] or 0
    accuracy = C / T if T else 0
    accuracy = round(accuracy * 100, 2)  
    userdata['acc'] = accuracy

    userdata['totalq'] = T

    cursor.close()
    conn.close()

    return render_template('quiz_main.html', username=username, userdata=userdata)

@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login_page')))
    resp.delete_cookie('username')
    return resp

@app.route('/api/profile', methods=['GET'])
def profile():
    username = request.cookies.get('username')
    if not username:
        return jsonify({'error': 'Not logged in'}), 401

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM userdata WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if user:
        return jsonify({'username': user[0]})
    return jsonify({'error': 'User not found'}), 404

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing username, email, or password'}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO userdata (username, email, pass) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Registration successful!'})
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Username already exists'}), 400

def get_user_attempt_number(username, sub):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    column_name = f"{sub.lower()}_attempted"
    print(f"[DEBUG] Fetching attempt number for user '{username}' and subject '{sub}' using column '{column_name}'")

    try:
        # Dynamically insert the column name, but parameterize the value
        query = f"SELECT {column_name} FROM userdata WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        attempt_number = result[column_name] if result and column_name in result else 0
    except mysql.connector.Error as e:
        print("[ERROR] Database error while fetching attempt number:", e)
        attempt_number = 0
    finally:
        cursor.close()
        connection.close()

    return attempt_number

def get_next_question(subject, username):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    if subject == "phy":
        cursor.execute("SELECT phy_attempted FROM userdata WHERE username = %s", (username,))
        db_subject = "Physics"
    elif subject == "math":
        cursor.execute("SELECT math_attempted FROM userdata WHERE username = %s", (username,))
        db_subject = "Maths"
    elif subject == "chem":
        cursor.execute("SELECT chem_attempted FROM userdata WHERE username = %s", (username,))
        db_subject = "Chemistry"
    else:
        cursor.close()
        connection.close()
        return None  # Invalid subject

    result = cursor.fetchone()
    print("[DEBUG]  RESULT FROM THE DATABASE: ", result)

    current_attempt_number = result.get(f"{subject}_attempted", 0) if result else 0
    next_question_number = current_attempt_number + 1
    print("[DEBUG] curr, next question numbers", current_attempt_number, next_question_number)

    if next_question_number > 50:  # Replace 50 with your actual limit
        print("[DEBUG] No more questions available for subject:", subject)
        cursor.close()
        connection.close()
        return None

    # Properly parameterized query
    query = "SELECT * FROM questions WHERE sub = %s AND qno = %s"
    cursor.execute(query, (db_subject, next_question_number))

    question = cursor.fetchone()
    print("[DEBUG] Question fetched from DB:", question if question else "No question found")

    cursor.close()
    connection.close()
    return question




@app.route("/api/submit-answer", methods=["POST"])
def submit_answer():
    data = request.get_json()
    username = request.cookies.get('username')
    if not username:
        return jsonify({'status': 'error', 'message': 'User not logged in'}), 401

    qno = data.get("qno")
    subject = data.get("subject")
    correct = data.get("correct")

    if not qno or not subject:
        return jsonify({'status': 'error', 'message': 'Missing qno or subject'}), 400

    subject_column = f"{subject}_attempted"
    update_fields = ["totalq = totalq + 1"]

    if correct == "True":
        update_fields.append("correctq = correctq + 1")
    elif correct == "False":
        update_fields.append("wrongq = wrongq + 1")

    update_fields.append(f"{subject_column} = {subject_column} + 1")

    update_query = f"UPDATE userdata SET {', '.join(update_fields)} WHERE username = %s"

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(update_query, (username,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Answer submitted and stats updated.'})
    except mysql.connector.Error as e:
        print("[ERROR] Failed to update userdata:", e)
        return jsonify({'status': 'error', 'message': 'Database error'}), 500







@app.route('/api/next-question', methods=['GET'])
def next_question():
    sub = request.args.get('subject')
    username = request.cookies.get('username')

    if not sub or not username:
        return jsonify({
            'status': 'error',
            'message': f'Subject and username are required. Got subject={sub}, username={username}'
        }), 400

    attempt_number = get_user_attempt_number(username, sub)
    if attempt_number is None:
        return jsonify({'status': 'error', 'message': f'Could not find attempt data for sub: {sub}'}), 404

    question = get_next_question(sub, username)
    if not question:
        return jsonify({'status': 'error', 'message': 'No more questions available'}), 404

    return Response(
        json.dumps({
            'status': 'success',
            'data': question,
            'question_number': int(attempt_number) + 1
        }, ensure_ascii=False),
        content_type='application/json; charset=utf-8'
    )
@app.route('/leaderboard')
def leaderboard():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT username, correctq AS C, totalq AS T FROM userdata")
    users = cursor.fetchall()

    if not users:
        return "No user data available."

    valid_C_values = [user['C'] for user in users if user['C'] is not None]
    C_max = max(valid_C_values) if valid_C_values else 1

    for user in users:
        C = user['C'] or 0
        T = user['T'] or 0
        accuracy = C / T if T else 0
        normalized_correct = C / C_max if C_max else 0
        user['score'] = 50 * (accuracy + normalized_correct)

    users.sort(key=lambda x: x['score'], reverse=True)

    cursor.close()
    conn.close()
    return render_template('leaderboard.html', data=users)

@app.route('/trivia')
def trivia():
    subject = request.args.get('sub')
    print(f"Subject received: {subject}")
    return render_template('trivia.html', subject=subject)








# ===============================
# ✅ ADMIN PAGE + QUESTION CRUD
# ===============================

@app.route('/admin')
def admin_page():
    username = request.cookies.get('username')
    # You can add proper admin authentication here later
    return render_template('admin.html')

@app.route("/api/questions", methods=["GET"])
def get_questions():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(questions)
    except mysql.connector.Error as e:
        print("[ERROR] Failed to fetch questions:", e)
        return jsonify({"error": "Database error"}), 500

@app.route("/api/questions", methods=["POST"])
def add_question():
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            INSERT INTO questions (sub, qno, question_text, option_a, option_b, option_c, option_d, correct_option)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data["sub"],
            data["qno"],
            data["question_text"],
            data["option_a"],
            data["option_b"],
            data["option_c"],
            data["option_d"],
            data["correct_option"]
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Question added successfully!"})
    except mysql.connector.Error as e:
        print("[ERROR] Failed to add question:", e)
        return jsonify({"error": "Database error"}), 500

@app.route("/api/questions/<int:id>", methods=["PUT"])
def edit_question(id):
    data = request.get_json()
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
            UPDATE questions
            SET sub=%s, qno=%s, question_text=%s,
                option_a=%s, option_b=%s, option_c=%s, option_d=%s, correct_option=%s
            WHERE id=%s
        """
        cursor.execute(query, (
            data["sub"],
            data["qno"],
            data["question_text"],
            data["option_a"],
            data["option_b"],
            data["option_c"],
            data["option_d"],
            data["correct_option"],
            id
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Question updated successfully!"})
    except mysql.connector.Error as e:
        print("[ERROR] Failed to update question:", e)
        return jsonify({"error": "Database error"}), 500

@app.route("/api/questions/<int:id>", methods=["DELETE"])
def delete_question(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Question deleted successfully!"})
    except mysql.connector.Error as e:
        print("[ERROR] Failed to delete question:", e)
        return jsonify({"error": "Database error"}), 500














if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)