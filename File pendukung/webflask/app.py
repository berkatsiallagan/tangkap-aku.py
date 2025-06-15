from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializations
app = Flask(__name__)

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbpolibatam'
mysql = MySQL(app)

# APP secret key (bebas)
app.secret_key = "4cc645e832bc2ed0869da6d3a9bdc0ea"

# routes
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/mahasiswa')
def data_mahasiswa():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, nim, nama_lengkap, alamat, program_studi FROM students')
    data = cur.fetchall()
    cur.close()
    return render_template('mahasiswa/data-mahasiswa.html', mahasiswa=data)

@app.route('/mahasiswa/tambah', methods=['GET'])
def tambah_mahasiswa():
    return render_template('mahasiswa/tambah-mahasiswa.html')

@app.route('/mahasiswa/insert', methods=['POST'])
def add_mahasiswa():
    if request.method == 'POST':
        nim = request.form['nim']
        nama_lengkap = request.form['nama_lengkap']
        alamat = request.form['alamat']
        program_studi = request.form['program_studi']  # New field for program_studi
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (nim, nama_lengkap, alamat, program_studi) VALUES (%s, %s, %s, %s)", 
                    (nim, nama_lengkap, alamat, program_studi))
        mysql.connection.commit()
        flash('Data mahasiswa berhasil ditambahkan!')
        return redirect(url_for('data_mahasiswa'))

@app.route('/mahasiswa/edit/<int:id>', methods=['GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM students WHERE id = {id}")
    data = cur.fetchall()
    cur.close()
    return render_template('mahasiswa/ubah-mahasiswa.html', contact=data[0])

@app.route('/mahasiswa/update/<int:id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        nim = request.form['nim']
        nama_lengkap = request.form['nama_lengkap']
        alamat = request.form['alamat']
        program_studi = request.form['program_studi']  # New field for program_studi
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE students
            SET nim = %s, nama_lengkap = %s, alamat = %s, program_studi = %s
            WHERE id = %s
        """, (nim, nama_lengkap, alamat, program_studi, id))
        mysql.connection.commit()
        flash('Data mahasiswa berhasil diubah!')
        return redirect(url_for('data_mahasiswa'))

@app.route('/mahasiswa/delete/<int:id>', methods=['POST', 'GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Data mahasiswa berhasil dihapus!')
    return redirect(url_for('data_mahasiswa'))

# starting the app
if __name__ == "__main__":
    app.run(port=9999, debug=True)
