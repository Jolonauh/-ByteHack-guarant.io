import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO warranty (brand, name, price, website, startdate, enddate, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Company 1', 'Warranty for iPhone', 300, 'www.example.com', '2020-05-29', '2023-05-29', 'Phone')
            )

cur.execute("INSERT INTO warranty (brand, name, price, website, startdate, enddate, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Company 2', 'Warranty for Samsung Galaxy', 250, 'www.example.com', '2020-05-29', '2021-05-29', 'Phone')
            )

cur.execute("INSERT INTO warranty (brand, name, price, website, startdate, enddate, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Company 3', 'Warranty for Google Pixel', 300, 'www.example.com', '2020-05-29', '2022-05-29', 'Phone')
            )

cur.execute("INSERT INTO warranty (brand, name, price, website, startdate, enddate, category) VALUES (?, ?, ?, ?, ?, ?, ?)",
            ('Company 3', 'Warranty for Toyota Prius', 3000, 'www.example.com', '2020-05-29', '2025-05-29', 'Car')
            )

cur.execute("INSERT INTO users (name, warranties) VALUES (?, ?)",
            ('Jeremiah', '1,3'
            ))

cur.execute("INSERT INTO users (name, warranties) VALUES (?, ?)",
            ('Nigel', '1,2'
            ))

connection.commit()
connection.close()