from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

# HTML + Tailwind Template for Leaderboard
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Leaderboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 font-sans">
  <div class="max-w-3xl mx-auto py-10">
    <h1 class="text-3xl font-bold text-center mb-6">🏆 Leaderboard</h1>
    <table class="w-full table-auto bg-white shadow-md rounded-xl overflow-hidden">
      <thead class="bg-blue-600 text-white">
        <tr>
          <th class="p-4 text-left">S. No</th>
          <th class="p-4 text-left">Username</th>
          <th class="p-4 text-left">Score</th>
        </tr>
      </thead>
      <tbody id="leaderboard" class="text-gray-700">
        {% for i, user in enumerate(data, 1) %}
        <tr class="border-b hover:bg-gray-100 transition">
          <td class="p-4">{{ i }}</td>
          <td class="p-4">{{ user['username'] }}</td>
          <td class="p-4">{{ '{:.2f}'.format(user['score']) }}</td>
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</body>
</html>
"""

@app.route('/')
def leaderboard():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='your_username',      # 🔁 Replace with your MySQL username
        password='your_password',  # 🔁 Replace with your MySQL password
        database='your_database'   # 🔁 Replace with your MySQL database name
    )
    cursor = conn.cursor(dictionary=True)

    # Get user data from 'userdata' table
    cursor.execute("SELECT username, correctq AS C, totalq AS T FROM userdata")
    users = cursor.fetchall()

    if not users:
        return "No user data available."

    # Calculate max correct answers
    C_max = max(user['C'] for user in users) or 1  # Prevent divide-by-zero

    # Compute scores
    for user in users:
        C = user['C']
        T = user['T']
        accuracy = C / T if T else 0
        normalized_correct = C / C_max
        user['score'] = 50 * (accuracy + normalized_correct)

    # Sort users by score descending
    users.sort(key=lambda x: x['score'], reverse=True)

    # Clean up and render
    cursor.close()
    conn.close()
    return render_template_string(HTML_TEMPLATE, data=users)

if __name__ == '__main__':
    app.run(debug=True)
