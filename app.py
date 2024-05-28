import os
from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, jsonify, session
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
import bcrypt
from os.path import join,dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get('MONGODB_URI')
DB_NAME = os.environ.get('DB_NAME')
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    msg = request.args.get('msg')
    project = list(db.project.find({}))
    return render_template('portfolio/index.html', project=project, msg = msg)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    if 'username' in session:
        return render_template('admin_panel/dashboards/dashboard.html')
    else:
        return redirect(url_for('home'))


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password'].encode('utf-8')
        user = user.lower()
        psw = password.lower()
        login_user = db.pengguna.find_one({'username': user})

        if login_user:
            db_pass = login_user['password']
            if bcrypt.checkpw(psw, db_pass):
                session['username'] = login_user['username']
                return redirect(url_for('dashboard'))
            else:
                return 'Email tidak terdaftar!'
        else:
            json_response = 'Email Tidak terdaftar'
            return render_template('login/login.html', json_response=json_response)
    return render_template('login/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        psw = request.form['password']

        user = user.lower()
        psw = psw.lower()

        hashpass = bcrypt.hashpw(psw.encode('utf-8'), bcrypt.gensalt())
        db.pengguna.insert_one({
            'username': user,
            'password': hashpass,
        })
        session['username'] = user
        return redirect(url_for('dashboard'))
    return render_template('login/register.html')


@app.route('/project', methods=['GET', 'POST'])
def project():
    if 'username' in session:
        project = list(db.project.find({}))
        return render_template('admin_panel/projects/project.html', project=project)
    else:
        return redirect(url_for('home'))


@app.route('/addproject', methods=['GET', 'POST'])
def addproject():
    if 'username' in session:
        if request.method == 'POST':
            nama = request.form['nama']
            deskripsi = request.form['deskripsi']

            gambar = request.files['gambar']
            extension = gambar.filename.split('.')[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
            gambar_name = f'gambar- {mytime}.{extension}'
            save_to = f'static/assets/Imgproject/{gambar_name}'
            gambar.save(save_to)

            doc = {
                'nama': nama,
                'deskripsi': deskripsi,
                'gambar': gambar_name
            }

            db.project.insert_one(doc)
            return redirect(url_for('project'))
        return render_template('admin_panel/projects/addproject.html')
    else:
        return redirect(url_for('home'))
    


@app.route('/editproject/<_id>', methods=['GET', 'POST'])
def editproject(_id):
    if 'username' in session:
        if request.method == 'POST':
            nama = request.form['nama']
            deskripsi = request.form['deskripsi']

            gambar = request.files['gambar']
            extension = gambar.filename.split('.')[-1]
            today = datetime.now()
            mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
            gambar_name = f'gambar- {mytime}.{extension}'
            save_to = f'static/assets/Imgproject/{gambar_name}'
            gambar.save(save_to)

            doc = {
                'nama': nama,
                'deskripsi': deskripsi,
            }

            if gambar:
                doc['gambar'] = gambar_name

            db.project.update_one({'_id': ObjectId(_id)}, {'$set': doc})
            return redirect(url_for('project'))
            return render_template('index.html')
        id = ObjectId(_id)
        data = list(db.project.find({'_id': id}))
        return render_template('admin_panel/projects/editproject.html', data=data)
    else:
        return redirect(url_for('home'))


@app.route('/deleteproject/<_id>', methods=['GET', 'POST'])
def deleteproject(_id):

    id = ObjectId(_id)
    projectdata = db.project.find_one({'_id': id})

    if projectdata:
        lokasi_file = os.path.join(
            'static/assets/Imgproject/', projectdata['gambar'])
        if os.path.exists(lokasi_file):
            os.remove(lokasi_file)

    db.project.delete_one({'_id': id})
    return redirect(url_for('project'))

# ACHIEVEMENT


@app.route('/achievement', methods=['GET', 'POST'])
def achievement():
        
        achievement = list(db.achievement.find({}))
        return render_template('portfolio/achievement.html', achievement=achievement)

@app.route('/achiev', methods=['GET', 'POST'])
def achiev():
    achievement = list(db.achievement.find({}))
    return render_template('admin_panel/achievements/achiev.html', achievement=achievement)


@app.route('/addachievement', methods=['GET', 'POST'])
def addachievement():
    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']

        gambar = request.files['gambar']
        extension = gambar.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name = f'gambar- {mytime}.{extension}'
        save_to = f'static/assets/Imgachievement/{gambar_name}'
        gambar.save(save_to)

        doc = {
            'nama': nama,
            'deskripsi': deskripsi,
            'gambar': gambar_name
        }

        db.achievement.insert_one(doc)
        return redirect(url_for('achiev'))
    return render_template('admin_panel/achievements/addachievement.html')


@app.route('/editachievement/<_id>', methods=['GET', 'POST'])
def editachievement(_id):
    if request.method == 'POST':
        nama = request.form['nama']
        deskripsi = request.form['deskripsi']

        gambar = request.files['gambar']
        extension = gambar.filename.split('.')[-1]
        today = datetime.now()
        mytime = today.strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name = f'gambar- {mytime}.{extension}'
        save_to = f'static/assets/Imgachievement/{gambar_name}'
        gambar.save(save_to)

        doc = {
            'nama': nama,
            'deskripsi': deskripsi,
        }

        if gambar:
            doc['gambar'] = gambar_name

        db.achievement.update_one({'_id': ObjectId(_id)}, {'$set': doc})
        return redirect(url_for('achievement'))
    id = ObjectId(_id)
    data = list(db.achievement.find({'_id': id}))
    return render_template('admin_panel/achievements/editachievement.html', data=data)


@app.route('/deleteachievement/<_id>', methods=['GET', 'POST'])
def deleteachievement(_id):

    id = ObjectId(_id)
    achievementdata = db.achievement.find_one({'_id': id})

    if achievementdata:
        lokasi_file = os.path.join(
            'static/assets/Imgachievement/', achievementdata['gambar'])
        if os.path.exists(lokasi_file):
            os.remove(lokasi_file)

    db.achievement.delete_one({'_id': id})
    return redirect(url_for('achievement'))


@app.route('/hubungi', methods=['GET', 'POST'])
def hubungi():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        keterangan = request.form['keterangan']

        doc = {
            'nama': nama,
            'email': email,
            'keterangan': keterangan
        }

        db.kontak.insert_one(doc)
        msg = 'success'
        return redirect(url_for('home', msg = msg))
    else:
        data_kontak = list(db.kontak.find({}))
        return render_template('admin_panel/contact/kontak.html', kontak=data_kontak)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    # DEBUG is SET to TRUE. CHANGE FOR PROD
    app.secret_key = 'rahasia'
    app.run('0.0.0.0', port=5000, debug=True)




