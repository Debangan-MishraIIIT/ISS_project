from flask import Flask, render_template, redirect,jsonify,request
import sqlite3

app = Flask(__name__)

def get_items():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM playlist")
    items = c.fetchall()
    
    mainlist=[]
    for item in items:
        text= item[0]
        q1=f"select * from songs where SongId='{text}'"
        c.execute(q1)
        itval= c.fetchall()
        sublist=[]
        sublist.append(itval[0][1])
        sublist.append(itval[0][3])
        sublist.append(itval[0][2])
        sublist.append(itval[0][0])
        
        mainlist.append(sublist)
    
    c.close()
    conn.close()
    return mainlist

@app.route("/")
def index():
    items = get_items()
    return render_template("index.html", val=items)

@app.route("/delete/<string:item_id>", methods=["POST"])
def delete_item(item_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("DELETE FROM playlist WHERE SongId = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect("/")

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


if __name__ == "__main__":
    app.run(debug=True)
