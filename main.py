#main.py
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, String, Date, Float, ForeignKey, DateTime
import os, sys


app = Flask(__name__)
app.config.from_object(__name__)


#def geturl(user, password, db, host='localhost', port=5432):
#    url = 'postgresql://{}:{}@{}:{}/{}'
#    url = url.format(user, password, host, port, db)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
if app.config['SQLALCHEMY_DATABASE_URI'] == None:
    print "Need database config"
    sys.exit(1)

db = SQLAlchemy(app)
import models
# main.py

@app.route("/")
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

    paste = models.Paste(text, poster)

    db.session.add(paste)
    db.session.commit()

    print "added paste by %s with id %s" % (paste.poster, paste.id)
    #return render_template("success.html", id=paste.id)
    pastes = models.Paste.query.order_by("date desc").limit(10)
    if pastes == None:
        raise Exception("No pastes in db")
    return render_template("home.html", pastes=pastes)

@app.route("/<id>")
def show(id):
    pastes = models.Paste.query.filter_by(id=id)
    prepaste = pastes.first()
    pasteid = prepaste.id
    pastecontent = prepaste.paste

    if prepaste == None:
        raise Exception("No such paste by id %s" % id)

    return render_template("paste.html", pasteid=pasteid, pastecontent=pastecontent)



@app.route("/all")
def showall():
    pastes = models.Paste.query.order_by("date desc").all()
    if pastes == None:
        raise Exception("No pastes in db")
    return render_template("allpastes.html", pastes=pastes)

if __name__ == "__main__":
    app.run(debug=True)
