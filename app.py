from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Konfigurasi database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_db'

mysql = MySQL(app)

# Route untuk halaman utama (index)
@app.route("/")
def home():
    return render_template("index.html")

# CREATE - Tambah HP
@app.route('/hp', methods=['POST'])
def add_hp():
    try:
        data = request.json
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO hp (merek_hp, tipe, ram, rom, prosesor)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['merek_hp'], data['tipe'], data['ram'], data['rom'], data['prosesor']))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'HP added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ - Ambil semua data HP
@app.route('/hp', methods=['GET'])
def get_all_hp():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM hp")
        rows = cursor.fetchall()
        cursor.close()
        result = []
        for row in rows:
            result.append({
                'id': row[0],
                'merek_hp': row[1],
                'tipe': row[2],
                'ram': row[3],
                'rom': row[4],
                'prosesor': row[5]
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# READ - Ambil HP berdasarkan ID
@app.route('/hp/<int:id>', methods=['GET'])
def get_hp_by_id(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM hp WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()
        if row:
            result = {
                'id': row[0],
                'merek_hp': row[1],
                'tipe': row[2],
                'ram': row[3],
                'rom': row[4],
                'prosesor': row[5]
            }
            return jsonify(result)
        else:
            return jsonify({'message': 'HP not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# UPDATE - Ubah data HP
@app.route('/hp/<int:id>', methods=['PUT'])
def update_hp(id):
    try:
        data = request.json
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE hp SET merek_hp = %s, tipe = %s, ram = %s, rom = %s, prosesor = %s
            WHERE id = %s
        """, (data['merek_hp'], data['tipe'], data['ram'], data['rom'], data['prosesor'], id))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'HP updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# DELETE - Hapus data HP
@app.route('/hp/<int:id>', methods=['DELETE'])
def delete_hp(id):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM hp WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return jsonify({'message': 'HP deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run server
if __name__ == '__main__':
    app.run(debug=True)
