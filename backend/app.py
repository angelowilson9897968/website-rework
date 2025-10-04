4. Update the app.py File
Replace the entire content of your backend/app.py file with this "smart" version that can connect to both SQLite and PostgreSQL.

Python

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__)
CORS(app)

# This will use the DATABASE_URL from your hosting service (like Render)
# OR it will use the DATABASE_URL from your local .env file.
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set. Check your .env file or hosting environment variables.")

engine = create_engine(DATABASE_URL)

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        score = data.get('score')
        time_taken = data.get('time_taken')

        if score is None or time_taken is None:
            return jsonify({"error": "Score or time_taken is missing"}), 400

        with engine.connect() as conn:
            conn.execute(text("INSERT INTO results (risk_score, time_taken_seconds) VALUES (:score, :time)"), {"score": score, "time": time_taken})
            conn.commit()

            portfolio_query = conn.execute(text("SELECT id, expected_return, standard_deviation FROM portfolios ORDER BY ABS(risk_score - :score) LIMIT 1"), {"score": score})
            portfolio = portfolio_query.fetchone()

            if not portfolio: return jsonify({"error": "Portfolio not found"}), 404
            portfolio_id, expected_return, std_dev = portfolio

            assets_query = conn.execute(text("SELECT a.asset_name, pa.allocation_percentage FROM portfolio_assets pa JOIN assets a ON pa.asset_id = a.id WHERE pa.portfolio_id = :p_id"), {"p_id": portfolio_id})
            assets = assets_query.fetchall()

        response = {
            "score": score,
            "expected_return": f"{expected_return:.2f}%",
            "standard_deviation": f"{std_dev:.2f}%",
            "assets": [{"name": asset[0], "allocation": f"{asset[1]:.2f}%"} for asset in assets]
        }
        return jsonify(response)
    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)