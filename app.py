from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = 'hantavirus_ozel_anahtar' 

# Veritabanı Yolu
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'veritabani.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Kullanici(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(50), nullable=False)
    eposta = db.Column(db.String(100), unique=True, nullable=False)
    sifre = db.Column(db.String(200), nullable=False)

@app.route('/kayit', methods=['GET', 'POST'])
def kayit():
    if request.method == 'POST':
        # Kullanıcı zaten var mı kontrolü (opsiyonel ama iyi olur)
        mevcut_user = Kullanici.query.filter_by(eposta=request.form.get('eposta')).first()
        if mevcut_user:
            flash("Bu e-posta zaten kayıtlı!")
            return redirect(url_for('kayit'))
            
        hashed_sifre = generate_password_hash(request.form.get('sifre'))
        yeni = Kullanici(isim=request.form.get('isim'), eposta=request.form.get('eposta'), sifre=hashed_sifre)
        db.session.add(yeni)
        db.session.commit()
        flash("Başarıyla kayıt oldunuz! Şimdi giriş yapabilirsiniz.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Kullanici.query.filter_by(eposta=request.form.get('eposta')).first()
        if user and check_password_hash(user.sifre, request.form.get('sifre')):
            session['user_id'] = user.id
            session['user_name'] = user.isim
            return redirect(url_for('ana_sayfa'))
        else:
            # GÖRSELDEKİ KIRMIZI YAZIYI BURASI ÇALIŞTIRIR
            flash("Giriş bilgileri hatalı!")
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/')
def ana_sayfa():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', isim=session['user_name'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)