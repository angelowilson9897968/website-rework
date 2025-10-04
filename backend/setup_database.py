import os
from sqlalchemy import create_engine, text

# Get the database connection URL from the environment variable
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set.")

engine = create_engine(DATABASE_URL)

def setup_db():
    with engine.connect() as conn:
        print("Creating tables...")
        # Create all tables if they don't exist
        # Using SERIAL for PostgreSQL auto-incrementing primary key
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS assets (
                id SERIAL PRIMARY KEY,
                asset_name TEXT NOT NULL UNIQUE
            );
            CREATE TABLE IF NOT EXISTS portfolios (
                id SERIAL PRIMARY KEY,
                risk_score INTEGER NOT NULL,
                expected_return REAL NOT NULL,
                standard_deviation REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS portfolio_assets (
                id SERIAL PRIMARY KEY,
                portfolio_id INTEGER REFERENCES portfolios(id),
                asset_id INTEGER REFERENCES assets(id),
                allocation_percentage REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS results (
                id SERIAL PRIMARY KEY,
                risk_score INTEGER NOT NULL,
                time_taken_seconds REAL NOT NULL,
                submission_timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """))
        conn.commit()
        print("Tables created successfully.")

        # Clear existing data to prevent duplicates when script is re-run
        print("Clearing existing portfolio data...")
        conn.execute(text("DELETE FROM portfolio_assets;"))
        conn.execute(text("DELETE FROM portfolios;"))
        conn.execute(text("DELETE FROM assets;"))
        conn.commit()
        print("Existing data cleared.")

        print("Inserting new data...")
        # Insert assets
        assets = [
            'US Stocks', 'International Stocks', 'Bonds', 'Real Estate', 'Commodities',
            'Emerging Market Stocks', 'High-Yield Bonds', 'T-Bills', 'Gold'
        ]
        for asset in assets:
            # ON CONFLICT is a PostgreSQL feature to avoid errors on duplicates
            conn.execute(text("INSERT INTO assets (asset_name) VALUES (:name) ON CONFLICT (asset_name) DO NOTHING;"), {"name": asset})
        
        # Define portfolio data
        portfolios_data = [
            (1, 4.5, 6.0), (2, 5.5, 8.0), (3, 6.5, 10.0),
            (4, 7.5, 12.0), (5, 8.5, 14.0), (6, 9.5, 16.0),
            (7, 10.5, 18.0), (8, 11.5, 20.0), (9, 12.5, 22.0), (10, 14.0, 25.0)
        ]
        for p in portfolios_data:
            conn.execute(text("INSERT INTO portfolios (risk_score, expected_return, standard_deviation) VALUES (:rs, :er, :sd);"), 
                         {"rs": p[0], "er": p[1], "sd": p[2]})

        # Define allocations for some key portfolios
        allocations_data = [
            (1, 'US Stocks', 20), (1, 'International Stocks', 10), (1, 'Bonds', 50), (1, 'T-Bills', 20),
            (5, 'US Stocks', 35), (5, 'International Stocks', 20), (5, 'Bonds', 25), (5, 'Real Estate', 10), (5, 'Gold', 10),
            (10, 'US Stocks', 40), (10, 'International Stocks', 25), (10, 'Emerging Market Stocks', 15), (10, 'High-Yield Bonds', 10), (10, 'Commodities', 10)
        ]

        # Insert allocations by looking up the correct IDs
        for p_id, asset_name, percent in allocations_data:
            asset_id_query = conn.execute(text("SELECT id FROM assets WHERE asset_name = :name;"), {"name": asset_name})
            asset_id = asset_id_query.fetchone()[0]
            
            portfolio_id_query = conn.execute(text("SELECT id FROM portfolios WHERE risk_score = :rs;"), {"rs": p_id})
            portfolio_id = portfolio_id_query.fetchone()[0]

            conn.execute(text("INSERT INTO portfolio_assets (portfolio_id, asset_id, allocation_percentage) VALUES (:p_id, :a_id, :percent);"),
                         {"p_id": portfolio_id, "a_id": asset_id, "percent": percent})
        
        conn.commit()
        print("Data inserted successfully.")

if __name__ == "__main__":
    setup_db()