from flask import Flask
import psycopg2
import os
import socket

app = Flask(__name__)

# PostgreSQL connection
def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")
    )
    return conn

@app.route("/")
def hello():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, count INTEGER);")
    cur.execute("INSERT INTO visits (count) VALUES (1) ON CONFLICT DO NOTHING;")
    cur.execute("UPDATE visits SET count = count + 1 WHERE id = 1;")
    cur.execute("SELECT count FROM visits WHERE id = 1;")
    visits = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    return f"""
    <h3>Hello {os.getenv('NAME', 'world')}!</h3>
    <b>Hostname:</b> {socket.gethostname()}<br/>
    <b>Visits:</b> {visits}
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0")