from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Function to get the portfolio data from the database
def get_portfolio_from_db(score):
    conn = sqlite3.connect('/data/portfolios.db')
    cursor = conn.cursor()

    # Find the closest portfolio based on the user's score
    cursor.execute('''
        SELECT id, expected_return, standard_deviation
        FROM portfolios
        ORDER BY ABS(risk_score - ?) LIMIT 1
    ''', (score,))
    portfolio = cursor.fetchone()

    if not portfolio:
        conn.close()
        return None

    portfolio_id, expected_return, std_dev = portfolio

    cursor.execute('''
        SELECT a.asset_name, pa.allocation_percentage
        FROM portfolio_assets pa
        JOIN assets a ON pa.asset_id = a.id
        WHERE pa.portfolio_id = ?
    ''', (portfolio_id,))
    assets = cursor.fetchall()

    conn.close()

    response = {
        "score": score,
        "expected_return": f"{expected_return:.2f}%",
        "standard_deviation": f"{std_dev:.2f}%",
        "assets": [{"name": asset[0], "allocation": f"{asset[1]:.2f}%"} for asset in assets]
    }
    return response

# Home Route
@app.route('/')
def home():
    return "Backend is running!"

# Endpoint to Handle Risk Score Submission
@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        score = data.get('score')
        # Get the time_taken value from the request
        time_taken = data.get('time_taken')

        if score is None or time_taken is None:
            return jsonify({"error": "Score or time_taken is missing"}), 400

        # --- NEW: Save the submission data to the 'results' table ---
        conn = sqlite3.connect('/data/portfolios.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO results (risk_score, time_taken_seconds)
            VALUES (?, ?)
        ''', (score, time_taken))
        conn.commit()
        conn.close()
        # --- END of data saving code ---

        # Now, we use the function to get the portfolio details
        portfolio_data = get_portfolio_from_db(score)

        if portfolio_data is None:
            return jsonify({"error": "Portfolio not found for the given score"}), 404

        return jsonify(portfolio_data)

    except Exception as e:
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)