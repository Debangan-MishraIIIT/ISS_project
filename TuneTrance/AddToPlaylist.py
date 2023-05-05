from flask import jsonify,request, Flask
import sqlite3 
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)
# Connect to the database

@app.route('/add_to_playlist', methods=['POST'])
def add_to_playlist():
    song_id = request.form.get('song_id')

    # Check if the song is already in the playlist
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM playlist WHERE SongID=?", (song_id,))
    result = cursor.fetchone()
    if result[0] > 0:
        cursor.close()
        conn.close()
        return jsonify({'success': False})

    # Insert the song into the playlist
    cursor.execute("INSERT INTO playlist (SongId) VALUES (?)", (song_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)