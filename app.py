from flask import Flask, render_template, session, request, redirect
from flask_session import Session
from helper import getloc, find_dis
# Configure application
app = Flask(__name__)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        sym = request.form.get("loc")
        if sym == '0':
            return render_template("apology.html", err = "Unknown error occurred, please close and try again after sometime")
        elif sym == '1':
            return render_template("apology.html", err = "Looks like you didnt allow the location, please close and try again after sometime")
        elif sym == '2':
            return render_template("apology.html", err = "Postition unavailabe currently, please close and try again after sometime")
        elif sym == '3':
            return render_template("apology.html", err = "Server timed out, please close and try again after sometime")
        else:
            sym = str(sym)
            lat = sym[:sym.find(' '):]
            lng = sym[sym.find(' ')::]
            session['places'] = getloc(lat, lng)
            return render_template("play.html", lat=float(lat), lng=float(lng), places = session['places'])
    else:
        if 'location' not in session:
            session['places'] = []
        return render_template("index.html")

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        dist = []
        ans = []
        coord = []
        ctr = 0
        for i in session['places']:
            lat1 = float(i['loc']['lat'])
            lng1 = float(i['loc']['lng'])
            ans.append(lat1)
            ans.append(lng1)
            pos = request.values.get(str(ctr))
            lat2 = float(pos[pos.find('(')+1:pos.find(','):])
            lng2 = float(pos[pos.find(',')+2:pos.find(')'):])
            coord.append(lat2)
            coord.append(lng2)
            dist.append(find_dis(lat1, lat2, lng1, lng2))
            ctr += 1
        return render_template("result.html", dist=dist, lat=lat1, lng=lng1, places=session['places'], coord=coord, ans=ans)
    else:
        return render_template("apology.html", err = "Something's wrong please try again later")
