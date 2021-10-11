from flask import Flask, render_template, request
import pymongo

app = Flask(__name__)
app.secret_key = 'bizim cok zor gizli sozcugumuz'
app.config["DEBUG"] = True

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["INP102"]
mesajlar_tablousu = mydb["mesajlar"]
kullanicilar_tablosu = mydb["kullanicilar"]



@app.route('/')
def baslangic():
    return render_template("anasayfa.html")


@app.route('/meyveler')
def meyveler():
    return render_template("meyveler.html")

@app.route('/sebzeler')
def sebzeler():
    return render_template("Sebzeler.html")

@app.route('/kuruyemis')
def kuruyemis():
    return render_template("kuruyemis.html")

@app.route('/cipsler')
def cipsler():
    return render_template("cipsler.html")


@app.route('/iletisim')
def iletisim():
    return render_template("Iletisim.html")

@app.route('/icecekler')
def icecekler():
    return render_template("icecekler.html")

@app.route('/uyeol', methods=['GET','POST'])
def uyeol():
    if request.method == 'POST':
        kayit = dict(request.form)
        kullanicilar_tablosu.insert_one(kayit)
        return redirect("/giris", code=302)
    else:
        return render_template("uyeol.html")

@app.route('/cikis')
def cikis():
    session.clear()
    return redirect("/", code=302)



@app.route('/mesajkaydet', methods=['POST'])
def mesaj_kaydet():
    adsoyad = request.form.get('adsoyad')
    eposta = request.form.get('eposta')
    mesaj = request.form.get('mesaj')

    kayit = {"adsoyad": adsoyad, "eposta": eposta, "mesaj":mesaj}
    kaydedilmis = mesajlar_tablousu.insert_one(kayit)
    return "Sayın " + adsoyad + ". Mesajınız için teşekkürler."

@app.route('/mesajlar')
def mesajlar():
    mesaj_listesi = list(mesajlar_tablosu.find())
    return render_template("mesajlar.html", mesaj_listesi=mesaj_listesi)

if __name__ == "__main__":
    app.run()