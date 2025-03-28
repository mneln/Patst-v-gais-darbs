from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
db = TinyDB('db.json')

@app.route("/")
def home():
    import matplotlib.pyplot as plt
    from collections import Counter

    # paņem no TinyDB datubazes
    records = db.all()

    # izņem zvaigznes un pārvērš par int
    zvaigznes_values = [int(record['zvaigznes']) for record in records if record['zvaigznes'].isdigit()]

    # saskaita daudzumu zvaigznu vert.
    Skaits = Counter(zvaigznes_values)

    # histogramma
    plt.bar(Skaits.keys(), Skaits.values(), color='blue', edgecolor='black')
    plt.title('Histogram of Zvaigznes')
    plt.xlabel('Zvaigznes')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)

    # histogram ka bilde
    plt.savefig('static/images/histogram.png')  # parbauda ka eksiste folderis
    plt.close()

    # izņem ediens ailes
    ediens_values = [record['ediens'] for record in records if 'ediens' in record and record['ediens']]

    # saskaita ediens biezumu
    ediens_counts = Counter(ediens_values)

    # apļa diagr.
    plt.figure(figsize=(8, 8))
    plt.pie(ediens_counts.values(), labels=ediens_counts.keys(), autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title('Pie Chart of Ediens')

    # saglaba bildi
    plt.savefig('static/images/pie_chart.png')  # parbauda ka eksiste folderis
    plt.close()

    return render_template("home.html")
#par lapa
@app.route("/about/")
def about():
    return render_template("about.html")
#atsauksmju lapa
@app.route("/review/")
def review():
    return render_template("review.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )
#parada atsauksmes
@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")
#panem info paradresē uz atsauksmju lapu 
@app.route('/submit', methods=['POST'])
def submit():
    vards = request.form.get('vards')
    zvaigznes = request.form.get('zvaigznes')
    ediens = request.form.get('ediens')
    dzeriens = request.form.get('dzeriens')
    apkalposana = request.form.get('apkalposana')
    atmosfera = request.form.get('atmosfera')
    komentars = request.form.get('komentars')
    ieteikumi = request.form.get('ieteikumi')
    
    db.insert({
        'zvaigznes': zvaigznes,
        'dzeriens': dzeriens,
        'ediens': ediens,
        'apkalposana': apkalposana,
        'atmosfera': atmosfera,
        'ieteikumi': ieteikumi,
        'vards': vards,
        'komentars': komentars
    })
    
    
    return redirect(url_for('results'))

@app.route("/results")
def results():
    # filtrē rezultātus pēc zvaigznēm 
    zvaigznes_high = db.search(Query().zvaigznes == '5')  
    zvaigznes_low = db.search(Query().zvaigznes != '5')  

    return render_template("result.html", high_ratings=zvaigznes_high, low_ratings=zvaigznes_low)

if __name__ == '__main__':
    app.run(debug=True)

