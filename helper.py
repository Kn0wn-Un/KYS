from flask import Flask, render_template, session, request, redirect
from flask_session import Session
import requests
import urllib.request
from math import radians, cos, sin, asin, sqrt

def getloc(lat, lng):
    try:
        response = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=' + lat + ',' + lng + '&radius=1500&rankby=prominence&key=AIzaSyBFweg0RNel-43y0l85djHglrUwH4BxkTQ')
        response.raise_for_status()
    except requests.RequestException:
        return render_template("apology.html", err = "Something's wrong please try again later")

    quote = response.json()

    x = []
    temp = {'name': '', 'loc': {}}
    try:
        for i in quote['results']:
            if 'user_ratings_total' in i:
                if i['rating'] > 3.5:
                    temp['name'] = i['name']
                    temp['loc'] = i['geometry']['location']
                    x.append(temp)
                    temp = {'name': '', 'loc': {}}
    except IndexError:
        return render_template("apology.html", err = "Something's wrong please try again later")
    except Exception:
        return render_template("apology.html", err = "Something's wrong please try again later")
    info = []

    for i in range(5):
        info.append(x[i])
    return info

def find_dis(lat1, lat2, lon1, lon2):  
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = abs(lon2 - lon1) 
    dlat = abs(lat2 - lat1)
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))  

    return(round(c * 6371, 2))
      