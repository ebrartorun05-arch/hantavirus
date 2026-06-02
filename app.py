from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "hantavirus_ozel_anahtar"

# Veritabanı
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///veritabani.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================
# VERİTABANI MODELİ
# ==========================
class Kullanici(db.Model):
    __tablename__ = "kullanici"

    id = db.Column(db.Integer, primary_key=True)
    isim = db.Column(db.String(50), nullable=False)
    eposta = db.Column(db.String(100), unique=True, nullable=False)
    sifre = db.Column(db.String(200), nullable=False)

# Veritabanını oluştur
with app.app_context():
    db.create_all()
    print("Veritabanı ve tablolar oluşturuldu.")

# ==========================
# KAYIT
# ==========================
@app.route("/kayit", methods=["GET", "POST"])
def kayit():

    if request.method == "POST":

        isim = request.form.get("isim")
        eposta = request.form.get("eposta")
        sifre = request.form.get("sifre")

        mevcut_user = Kullanici.query.filter_by(eposta=eposta).first()

        if mevcut_user:
            flash("Bu e-posta zaten kayıtlı!")
            return redirect(url_for("kayit"))

        hashed_sifre = generate_password_hash(sifre)

        yeni = Kullanici(
            isim=isim,
            eposta=eposta,
            sifre=hashed_sifre
        )

        db.session.add(yeni)
        db.session.commit()

        flash("Başarıyla kayıt oldunuz!")
        return redirect(url_for("login"))

    return render_template("register.html")

# ==========================
# GİRİŞ
# ==========================
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        eposta = request.form.get("eposta")
        sifre = request.form.get("sifre")

        user = Kullanici.query.filter_by(eposta=eposta).first()

        if user and check_password_hash(user.sifre, sifre):
            session["user_id"] = user.id
            session["user_name"] = user.isim
            return redirect(url_for("ana_sayfa"))

        flash("Giriş bilgileri hatalı!")
        return redirect(url_for("login"))

    return render_template("login.html")

# ==========================
# ANA SAYFA
# ==========================
@app.route("/")
def ana_sayfa():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "index.html",
        isim=session["user_name"]
    )

# ==========================
# ÇIKIŞ
# ==========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ==========================
# ÇALIŞTIR
# ==========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
