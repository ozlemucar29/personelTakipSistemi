from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'  # Güvenlik için değiştirin
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    soyad = db.Column(db.String(100), nullable=False)
    pozisyon = db.Column(db.String(100), nullable=False)
    ise_baslama = db.Column(db.String(20))
    maas = db.Column(db.Float)

class GirisCikis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personel_id = db.Column(db.Integer, db.ForeignKey('personel.id'), nullable=False)
    giris_saati = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cikis_saati = db.Column(db.DateTime, nullable=True)
    personel = db.relationship('Personel', backref=db.backref('giris_cikislar', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/personel')
@login_required
def personel():
    personeller = Personel.query.all()
    return render_template('personel.html', personeller=personeller)

@app.route('/personel/ekle', methods=['GET', 'POST'])
@login_required
def personel_ekle():
    if request.method == 'POST':
        ad = request.form.get('ad')
        soyad = request.form.get('soyad')
        pozisyon = request.form.get('pozisyon')
        ise_baslama = request.form.get('ise_baslama')
        maas = request.form.get('maas')
        try:
            maas = float(maas)
        except (TypeError, ValueError):
            maas = 0
        if not pozisyon:
            flash('Pozisyon seçilmedi!')
            return render_template('personel_ekle.html')
        yeni_personel = Personel(ad=ad, soyad=soyad, pozisyon=pozisyon, ise_baslama=ise_baslama, maas=maas)
        db.session.add(yeni_personel)
        db.session.commit()
        return redirect(url_for('personel'))
    return render_template('personel_ekle.html')

@app.route('/personel/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def personel_duzenle(id):
    personel = Personel.query.get_or_404(id)
    if request.method == 'POST':
        personel.ad = request.form['ad']
        personel.soyad = request.form['soyad']
        personel.pozisyon = request.form['pozisyon']
        personel.ise_baslama = request.form.get('ise_baslama')
        maas = request.form.get('maas')
        try:
            personel.maas = float(maas)
        except (TypeError, ValueError):
            personel.maas = 0
        db.session.commit()
        return redirect(url_for('personel'))
    return render_template('personel_duzenle.html', personel=personel)

@app.route('/personel/sil/<int:id>', methods=['POST'])
@login_required
def personel_sil(id):
    personel = Personel.query.get_or_404(id)
    db.session.delete(personel)
    db.session.commit()
    return redirect(url_for('personel'))

@app.route('/raporlar')
@login_required
def raporlar():
    personeller = Personel.query.all()
    # Her personelin son giriş-çıkış kaydını bul
    son_giris_cikis = {}
    for p in personeller:
        kayit = GirisCikis.query.filter_by(personel_id=p.id).order_by(GirisCikis.giris_saati.desc()).first()
        son_giris_cikis[p.id] = kayit
    return render_template('raporlar.html', personeller=personeller, son_giris_cikis=son_giris_cikis)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten alınmış!')
            return render_template('register.html')
        hashed_password = generate_password_hash(password)
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Kayıt başarılı! Giriş yapabilirsiniz.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/profil', methods=['GET', 'POST'])
@login_required
def profil():
    if request.method == 'POST':
        yeni_kullanici_adi = request.form.get('username')
        eski_sifre = request.form.get('old_password')
        yeni_sifre = request.form.get('new_password')
        # Kullanıcı adı güncelle
        if yeni_kullanici_adi and yeni_kullanici_adi != current_user.username:
            if User.query.filter_by(username=yeni_kullanici_adi).first():
                flash('Bu kullanıcı adı zaten alınmış!')
                return render_template('profil.html')
            current_user.username = yeni_kullanici_adi
        # Şifre güncelle
        if eski_sifre and yeni_sifre:
            if check_password_hash(current_user.password, eski_sifre):
                current_user.password = generate_password_hash(yeni_sifre)
                flash('Şifreniz güncellendi.')
            else:
                flash('Eski şifreniz yanlış!')
                return render_template('profil.html')
        db.session.commit()
        flash('Bilgileriniz güncellendi.')
        return render_template('profil.html')
    return render_template('profil.html')

@app.route('/personel/giris/<int:id>', methods=['POST'])
@login_required
def personel_giris(id):
    yeni_giris = GirisCikis(personel_id=id, giris_saati=datetime.now())
    db.session.add(yeni_giris)
    db.session.commit()
    flash('Giriş kaydedildi.')
    return redirect(url_for('personel'))

@app.route('/personel/cikis/<int:id>', methods=['POST'])
@login_required
def personel_cikis(id):
    kayit = GirisCikis.query.filter_by(personel_id=id, cikis_saati=None).order_by(GirisCikis.giris_saati.desc()).first()
    if kayit:
        kayit.cikis_saati = datetime.now()
        db.session.commit()
        flash('Çıkış kaydedildi.')
    else:
        flash('Açık giriş kaydı bulunamadı!')
    return redirect(url_for('personel'))

@app.route('/personel/detay/<int:id>')
@login_required
def personel_detay(id):
    personel = Personel.query.get_or_404(id)
    giris_cikislar = GirisCikis.query.filter_by(personel_id=id).order_by(GirisCikis.giris_saati.desc()).all()
    return render_template('personel_detay.html', personel=personel, giris_cikislar=giris_cikislar)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 