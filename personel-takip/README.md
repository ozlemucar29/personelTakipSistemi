# ÖZLEM UÇAR 

## 1. Projenin Amacı

Bu proje, bir kurum ya da şirket bünyesindeki personellerin kayıtlarının tutulduğu, kullanıcı girişleriyle erişim sağlanan basit bir **personel takip sistemidir**. Gerçek dünyada İK (İnsan Kaynakları) departmanlarında kullanılan uygulamaların basit bir örneğidir. Proje, kullanıcıların kayıt olmasını, giriş yapmasını ve sisteme personel ekleyip yönetmesini mümkün kılar. Böylece kullanıcı, manuel kayıt defterlerine gerek duymadan dijital olarak verileri takip edebilir.

## 2. Projenin Kapsamı ve Özellikleri

**Yapabildikleri:**
- Kullanıcı kayıt olma ve giriş yapma
- Yeni personel ekleme
- Mevcut personel bilgilerini görüntüleme
- Personel bilgilerini düzenleme
- Personel silme işlemleri
- Raporlama sayfası

**Yapamadıkları / Kapsam Dışı:**
- Çoklu kullanıcı yönetimi (admin ve normal kullanıcı ayrımı yok)
- Gelişmiş rol tabanlı yetkilendirme
- Mobil uyumluluk / API desteği
- Görsel yükleme desteği

## 3. Kullanılan Teknolojiler

- **Programlama Dili:** Python
- **Framework:** Flask
- **Veritabanı:** SQLite (`site.db`)
- **Frontend:** HTML (Jinja2 templating)
- **Ekstra:** Bootstrap (template’lerde stil için), Flask-Login

## 4. Kurulum ve Çalıştırma Talimatları

1. Python 3 yüklü olmalı.
2. Terminal'den proje klasörüne gidin:
   ```bash
   cd özlem
   ```
3. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
4. Uygulamayı çalıştırın:
   ```bash
   python app.py
   ```
5. Uygulama `http://127.0.0.1:5000` adresinde çalışacaktır.

## 5. Dosya Yapısı ve Açıklamaları

| Dosya / Klasör | Açıklama |
|----------------|----------|
| `app.py` | Flask uygulamasının ana dosyası |
| `requirements.txt` | Proje bağımlılıkları |
| `site.db` | SQLite veritabanı |
| `templates/` | HTML arayüz dosyaları |
| `base.html` | Ortak HTML şablonu |
| `index.html` | Anasayfa |
| `login.html`, `register.html` | Giriş ve kayıt ekranları |
| `personel.html`, `personel_ekle.html`, `personel_duzenle.html`, `personel_detay.html` | Personel işlemleri sayfaları |


## 7. Zorluklar ve Öğrenilenler

Projeyi geliştirirken:
- Flask Login yapısını kurarken sorunlar yaşadım, oturum yönetimini tam anlamak zaman aldı.
- Veritabanı işlemlerinde hata ayıklama süreci öğretici oldu.
- HTML ve Jinja2 ile dinamik veri aktarımı pratiği kazandım.

Bu proje sayesinde Flask yapısını baştan sona bir proje içinde kullanmayı öğrendim.

## 8. Geliştirilebilir Yönler

- Yetkilendirme sistemi geliştirilebilir (Admin kullanıcı, normal kullanıcı ayrımı).
- Dosya yükleme özelliği (personel fotoğrafı gibi) eklenebilir.
- Veritabanı MySQL gibi daha güçlü bir yapıya geçirilebilir.
- Grafiksel raporlama (chart.js) entegre edilebilir.

