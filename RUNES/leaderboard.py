from flask import Flask, render_template_string
import mysql.connector

app = Flask(__name__)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Leaderboard | RUNES</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap" rel="stylesheet" />
  <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet" />
  <style>
    @font-face {
      font-family: 'norse';
      src: url('/static/fonts/norse.otf') format('opentype');
    }

    body {
      background: linear-gradient(135deg, rgba(75, 0, 130, 0.8), rgba(0, 0, 255, 0.5));
      font-family: 'Quicksand', sans-serif;
      background-image: url('https://i.ibb.co/9mf6y34K/1111-Photoroom.png');
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
    }

    .frosted {
      backdrop-filter: blur(70px);
      background: rgba(255, 255, 255, 0.1);
      border-radius: 15px;
      border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .frostednav {
      backdrop-filter: blur(70px);
      background: rgba(255, 255, 255, 0.1);
    }

    .customfont {
      font-family: 'norse', sans-serif;
    }
  </style>
</head>
<body class="text-white">

  <!-- Navbar -->
  <nav class="w-full px-6 py-4 bg-transparent flex justify-between items-center frostednav fixed top-0 shadow-md z-10">
    <div class="flex items-center space-x-4">
      <img src="https://i.ibb.co/F1CK3wq/logo.png" alt="Runes Logo" class="w-12 h-12 shadow-md" />
      <span class="text-3xl text-white customfont">R U N E S</span>
    </div>
  </nav>

  <!-- Leaderboard Section -->
  <div class="pt-24 max-w-4xl mx-auto px-4">
    <div class="frosted p-6 shadow-lg">
      <h1 class="text-3xl font-bold text-center mb-6">🏆 Leaderboard</h1>
      <div class="overflow-x-auto rounded-lg">
        <table class="w-full text-left border-collapse text-white">
          <thead class="bg-purple-700 bg-opacity-30">
            <tr>
              <th class="p-4">S. No</th>
              <th class="p-4">Username</th>
              <th class="p-4">Score</th>
            </tr>
          </thead>
          <tbody>
            {% for user in data %}
            <tr class="border-b border-white border-opacity-10 hover:bg-white hover:bg-opacity-10 transition">
              <td class="p-4">{{ loop.index }}</td>
              <td class="p-4">{{ user.username }}</td>
              <td class="p-4">{{ '%.2f' % user.score }}</td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
      </div>
    </div>
  </div>

</body>
</html>"""

@app.route('/')
def leaderboard():
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='192.168.100.82',
        user='runes',       # 🔁 Replace with your MySQL username
        password='root',    # 🔁 Replace with your MySQL password
        database='runes'    # 🔁 Replace with your MySQL database name
    )
    cursor = conn.cursor(dictionary=True)

    # Get user data from 'userdata' table
    cursor.execute("SELECT username, correctq AS C, totalq AS T FROM userdata")
    users = cursor.fetchall()

    if not users:
        return "No user data available."

    # Calculate max correct answers to normalize
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

    # Render the leaderboard
    cursor.close()  
    conn.close()
    return render_template_string(HTML_TEMPLATE, data=users)

if __name__ == '__main__':
    app.run(debug=True)
