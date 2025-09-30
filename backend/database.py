import sqlite3

def setup_database():
    conn = sqlite3.connect('/data/portfolios.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        risk_score INTEGER NOT NULL UNIQUE,
        expected_return REAL NOT NULL,
        standard_deviation REAL NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        asset_name TEXT NOT NULL UNIQUE
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS portfolio_assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        portfolio_id INTEGER NOT NULL,
        asset_id INTEGER NOT NULL,
        allocation_percentage REAL NOT NULL,
        FOREIGN KEY (portfolio_id) REFERENCES portfolios (id),
        FOREIGN KEY (asset_id) REFERENCES assets (id)
    )
    ''')
    conn.commit()

    # List of assets to insert
    assets_to_insert = [
        'Apple Inc.', 'Microsoft Corporation', 'NVIDIA Corporation', 'Alphabet Inc.', 'Amazon.com, Inc.',
        'Meta Platforms Inc.', 'Tesla Inc.', 'Reliance Industries Ltd.', 'Tata Consultancy Services',
        'HDFC Bank Ltd.', 'Larsen & Toubro Ltd.', 'ITC', 'Persistent Systems Ltd.', 'Zomato', 'Trent Ltd.',
        'Dixon Technologies (India) Ltd.', 'Polycab India Ltd.', 'Sobha Ltd.', 'LT Foods Ltd.',
        'Mama Earth', 'PCBL Chemical Ltd.', 'Cholamandalam Financial Holdings Ltd.', 'Bitcoin',
        'Ethereum', 'Solana', 'Govt Bond', 'Gold', 'Copper', 'US Dollar'
    ]

    # Insert assets
    for asset in assets_to_insert:
        cursor.execute('''
            INSERT OR IGNORE INTO assets (asset_name)
            VALUES (?)
        ''', (asset,))
    conn.commit()
    print("✅ Assets inserted successfully!")

    # Portfolio data
    risk_scores = list(range(-10, 11))
    expected_returns = [
        10.856, 11.384, 11.919, 12.472, 13.031, 13.608, 14.193, 14.789, 15.403, 16.029,
        16.663, 17.308, 17.960, 18.659, 19.385, 20.099, 20.820, 21.558, 22.304, 23.072, 23.837
    ]
    standard_deviations = [
        0.9469, 0.9717, 0.9993, 1.0298, 1.0629, 1.0986, 1.1367, 1.1770, 1.2199, 1.2649,
        1.3117, 1.3603, 1.4103, 1.4643, 1.5211, 1.5781, 1.6364, 1.6967, 1.7582, 1.8220, 1.8862
    ]
    allocations_list = [
        [1.429] * 7 + [2.000] * 5 + [1.000] * 10 + [0.000] * 3 + [25.000, 20.000, 10.000, 15.000],
        [1.429] * 7 + [2.134] * 5 + [1.134] * 10 + [0.0833] * 3 + [23.750, 19.500, 9.490, 15.000],
        [1.429] * 7 + [2.256] * 5 + [1.272] * 10 + [0.167] * 3 + [22.500, 19.000, 9.000, 15.000],
        [1.429] * 7 + [2.366] * 5 + [1.418] * 10 + [0.250] * 3 + [21.250, 18.500, 8.490, 15.000],
        [1.429] * 7 + [2.464] * 5 + [1.568] * 10 + [0.333] * 3 + [20.000, 18.000, 8.000, 15.000],
        [1.429] * 7 + [2.550] * 5 + [1.726] * 10 + [0.417] * 3 + [18.750, 17.500, 7.490, 15.000],
        [1.429] * 7 + [2.624] * 5 + [1.888] * 10 + [0.500] * 3 + [17.500, 17.000, 7.000, 15.000],
        [1.429] * 7 + [2.700] * 5 + [2.000] * 10 + [0.583] * 3 + [16.250, 16.500, 6.500, 15.000],
        [1.429] * 7 + [2.750] * 5 + [2.200] * 10 + [0.667] * 3 + [15.000, 16.000, 6.000, 15.000],
        [1.429] * 7 + [2.800] * 5 + [2.400] * 10 + [0.750] * 3 + [13.750, 15.500, 5.500, 15.000],
        [1.429] * 7 + [2.850] * 5 + [2.600] * 10 + [0.833] * 3 + [12.500, 15.000, 5.000, 15.000],
        [1.429] * 7 + [2.814] * 5 + [2.786] * 10 + [0.917] * 3 + [11.750, 14.500, 4.570, 14.500],
        [1.429] * 7 + [2.816] * 5 + [2.976] * 10 + [1.000] * 3 + [11.000, 14.000, 4.160, 14.000],
        [1.429] * 7 + [2.818] * 5 + [3.176] * 10 + [1.083] * 3 + [10.250, 13.500, 3.750, 14.000],
        [1.429] * 7 + [2.820] * 5 + [3.376] * 10 + [1.167] * 3 + [9.500, 13.000, 3.330, 14.000],
        [1.429] * 7 + [2.822] * 5 + [3.576] * 10 + [1.250] * 3 + [8.750, 12.500, 3.000, 13.500],
        [1.429] * 7 + [2.824] * 5 + [3.776] * 10 + [1.333] * 3 + [8.000, 12.000, 2.500, 13.500],
        [1.429] * 7 + [2.826] * 5 + [3.976] * 10 + [1.417] * 3 + [7.250, 11.500, 2.000, 13.500],
        [1.429] * 7 + [2.828] * 5 + [4.176] * 10 + [1.500] * 3 + [6.500, 11.000, 1.500, 13.500],
        [1.429] * 7 + [2.830] * 5 + [4.376] * 10 + [1.583] * 3 + [5.750, 10.500, 1.000, 13.500],
        [1.429] * 7 + [2.832] * 5 + [4.576] * 10 + [1.667] * 3 + [5.000, 10.000, 0.500, 13.500]
    ]

    # Insert portfolios
    cursor.execute('SELECT id, asset_name FROM assets')
    assets = cursor.fetchall()
    num_assets = len(assets)

    for i in range(len(risk_scores)):
        risk_score = risk_scores[i]
        expected_return = expected_returns[i]
        standard_deviation = standard_deviations[i]
        allocations = allocations_list[i]

        cursor.execute('''
            INSERT OR IGNORE INTO portfolios (risk_score, expected_return, standard_deviation)
            VALUES (?, ?, ?)
        ''', (risk_score, expected_return, standard_deviation))

        portfolio_id = cursor.lastrowid

        if portfolio_id:
            for j in range(num_assets):
                if j < len(allocations):
                    allocation = allocations[j]
                    asset_id = assets[j][0]
                    cursor.execute('''
                        INSERT INTO portfolio_assets (portfolio_id, asset_id, allocation_percentage)
                        VALUES (?, ?, ?)
                    ''', (portfolio_id, asset_id, allocation))
            print(f"✅ Portfolio for risk score {risk_score} inserted successfully!")
        else:
            print(f"✅ Portfolio for risk score {risk_score} already exists. Skipping.")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    setup_database()