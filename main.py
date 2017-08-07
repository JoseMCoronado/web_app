#main.py
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *#Table, Column, Integer, String, Date, Float, ForeignKey, DateTime
import os, sys
import urllib2
import requests
import json


app = Flask(__name__)
app.config.from_object(__name__)

def geturl(user, password, db, host='localhost', port=5432):
    url = 'postgresql://{}:{}@{}:{}/{}'
    url = url.format(user, password, host, port, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
if app.config['SQLALCHEMY_DATABASE_URI'] == None:
    print "Need database config"
    sys.exit(1)

db = SQLAlchemy(app)

import models

@app.route("/", methods=['GET','POST'])
def show_home_page():
    pastes = models.Paste.query.order_by("date desc").limit(10)
    if pastes == None:
        raise Exception("No pastes in db")
    return render_template("home.html", pastes=pastes)

@app.route("/temp_clear")
def temp_clear():
    models.Paste.query.delete()
    return "TERMINATION DONE"

@app.route('/search', methods=["POST"])
def display_messages_by():
        field = request.form["field"]
        field = field.encode("ascii", errors="ignore")
        value = request.form["value"]
        value = value.encode("ascii", errors="ignore")
        return search_result(field,value)

@app.route('/search/<field>/<value>')
def search_result(field,value):
        #MULTIPLE SEARCH CRITERIA
        #criteria = (('id', 2), ('paste', 1) ,('poster', 353))
        #query = session.query(tablename)
        #for _filter, value in criteria:
        #    query = query.filter(getattr(tablename, _filter) == value)
        #result = query.all()
        return render_template("home.html", pastes = (models.Paste.query.filter(getattr(models.Paste, field) == value).all()))

@app.route("/submit", methods=["POST"])
def submit():
    text = request.form["paste"]
    text = text.encode("ascii", errors="ignore")
    poster = request.form["poster"]
    poster = poster.encode("ascii", errors="ignore")
    value = request.form["value"]

    paste = models.Paste(text, poster, value)

    db.session.add(paste)
    db.session.commit()

    print "added paste by %s with id %s" % (paste.poster, paste.id)
    #route to other page
    #return render_template("success.html", id=paste.id)
    #reroute to home
    pastes = models.Paste.query.order_by("date desc").limit(10)
    if pastes == None:
        raise Exception("No pastes in db")
    return render_template("home.html", pastes=pastes)

@app.route("/all")
def showall():
    pastes = models.Paste.query.order_by("date desc").all()
    if pastes == None:
        raise Exception("No pastes in db")
    return render_template("allpastes.html", pastes=pastes)

#api endpoints
@app.route('/api/all')
def api_all():
  events = models.Paste.query.all()
  return jsonify([p.serialize for p in events])

@app.route('/api/alljsonlist')
def api_all_json_list():
    events = models.Paste.query.all()
    return jsonify(json_list = [p.serialize for p in events])

@app.route('/api/<event_type>')
def api_by_event_type(event_type):
  events = models.Paste.query.filter_by(poster = event_type).all()
  return jsonify(json_list = [p.serialize for p in events])

@app.route("/chart")
def chart():
    return render_template("chart.html")

@app.route("/data/dataforchart")
def data_for_chart():
    pastes = models.Paste.query.order_by("date desc").all()
    d = dict()
    for p in pastes:
        key = p.poster
        if key in d:
            d[key][0] += p.value
            d[key][1] += 1
        else:
            d[key] = [p.value, 1]
    listdict = list()
    for sec in d.items():
        x = dict()
        x['name'] = sec[0]
        x['tot'] = sec[1][0]
        x['tot2'] = sec[1][1]
        listdict.append(x)
    return json.dumps(listdict)

@app.route("/oldfaith")
def old():
    pastes = models.Paste.query.order_by("date desc").all()
    json_list = [p.serialize for p in pastes]
    return json.dumps(json_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
