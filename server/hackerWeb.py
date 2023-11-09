from flask import Flask, app, request
import sqlite3

app.config['DATABASE'] = 'database.db'

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/api', methods=['POST'])
def receive_message():
    data = request.get_json()
    message = data.get('message')

    # Lưu thông điệp vào cơ sở dữ liệu
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO messages (message) VALUES (?)', (message,))
    conn.commit()
    conn.close()

    return 'Message received and saved to database!'

if __name__ == '__main__':
    app.run(debug=True)
