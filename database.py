import os
import sqlite3
from datetime import datetime

N_CHANNELS = 24  # 36


class Database():
    def __init__(self):
        self.create_db()

    def create_db(self):
        conn = self.get_db_connection()
        cur = conn.cursor()

        #cur.execute('''GRANT postgres TO carol;''')

        #cur.execute('''CREATE DATABASE serial_data;''')
        cur.execute(
            "CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY AUTOINCREMENT, user_name VARCHAR(40) not null)")
        conn.commit()

        cur.execute('CREATE TABLE IF NOT EXISTS raw_data(timestamp TIME PRIMARY KEY,' +
                    ','.join([f'ch{i} FLOAT NOT NULL' for i in range(0, N_CHANNELS)]) + ');')
        conn.commit()

        cur.close()
        conn.close()

    def get_db_connection(self):
        conn = sqlite3.connect('database.db')
        return conn

    def get_all_data(self, table):
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM {table};')
        res = cur.fetchall()
        cur.close()
        conn.close()
        # json.dumps(res,  default=str) #jsonify({"hello": "world"})
        return res

    def get_users(self):
        conn = self.get_db_connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('SELECT * FROM users;')
        res = cur.fetchall()
        cur.close()
        conn.close()
        # json.dumps(res,  default=str) #jsonify({"hello": "world"})
        return [{key: item[key] for key in item.keys()} for item in res]

    def save_data(self, new_values):
        conn = self.get_db_connection()
        cur = conn.cursor()

        cmd = 'INSERT INTO  raw_data (timestamp,' + ','.join([f'ch{i}' for i in range(
            0, N_CHANNELS)]) + ') VALUES (' + ', '.join(['?']*(N_CHANNELS+1)) + ')'
        cur.execute(cmd, (datetime.now().strftime("%H:%M:%S"), *new_values))

        conn.commit()
        cur.close()
        conn.close()

    def save_user(self, user_name):
        try:
            conn = self.get_db_connection()
            cur = conn.cursor()

            cur.execute(
                "INSERT INTO users (user_name) VALUES (?);", (user_name,))

            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(str(e))

    def get_user_by_id(self, user_id):

        try:

            conn = self.get_db_connection()
            #conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id=?;", (user_id,))
            res = cur.fetchone()
            cur.close()
            conn.close()
            id, name = res
            # json.dumps(res,  default=str) #jsonify({"hello": "world"})
            return {"user_id": id, "user_name": name}

        except Exception as e:
            print(str(e))

    def update_user(self, user_id, user_name):
        conn = self.get_db_connection()
        cur = conn.cursor()

        cur.execute("UPDATE users SET user_name=? WHERE user_id=?;",
                    (user_name, user_id))

        conn.commit()
        cur.close()
        conn.close()

    def delete_user(self, user_id):
        try:
            print("Deletando:")
            conn = self.get_db_connection()
            cur = conn.cursor()

            cur.execute("DELETE FROM users WHERE user_id=?;", (user_id,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    db = Databroker()
