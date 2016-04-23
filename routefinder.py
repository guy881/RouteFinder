# -*- coding: utf-8
from flask import Flask, request, render_template
from werkzeug.debug import DebuggedApplication
from heapq import heappush, heappop
from collections import OrderedDict
import json, requests

app = Flask(__name__)
app.secret_key = '@#Q@#@KDXAXAXd'
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)
r = requests.get("http://edi.iem.pw.edu.pl/muchap1/route/cities/")
miasta = r.json()
print miasta


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', cities=miasta)
    if request.method == 'POST':
        print request.form
        z = request.form['z']
        do = request.form['do']
        zid = 0
        doid = 0
        for miasto in miasta:  # dostajemy nazwe, a potrzebujemy id
            if miasto['nazwa'] == z:
                zid = miasto['id']
            if miasto['nazwa'] == do:
                doid = miasto['id']
        # droga uslugo, dawaj trase
        req = requests.get("http://edi.iem.pw.edu.pl/muchap1/route/" + str(zid) + "/" + str(doid) + "/")
        trasa = req.json()
        print trasa
        dlugosc = trasa['dlugosc']
        trasa.__delitem__('dlugosc')
        trasa_ord = OrderedDict(sorted(trasa.items()))
        # potrzebujemy wsporzednych, nie id
        wspolrzedne = []
        for index in trasa_ord:
            wspolrzedne.append((miasta[int(trasa[index])]['h'], miasta[int(trasa[index])]['w']))  # krotka ( h, w )
        return render_template('index.html', cities=miasta, wspolrzedne=wspolrzedne, dlugosc=dlugosc)


# @app.route(app_url/connections, methods=['GET']) #zwraca link do mapy ze wszystkimi polaczeniami
# def polaczenia():
#   wspolrzedne = []
#   for sciezka in sciezki:
#      wspolrzedne.append( ( miasta[int(sciezka['od'])]['h'], miasta[int(sciezka['do'])]['w'] )) #krotka ( h, w )
#   return render_template( 'index.html', cities = miasta, wspolrzedne = wspolrzedne )

if __name__ == '__main__':
    app.run()
