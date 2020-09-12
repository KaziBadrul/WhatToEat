from flask import Flask, render_template, redirect, request, url_for
import requests

app = Flask(__name__)

def get_response(place, meter_range, cost, lat, lng):
    import json, requests
    url = 'https://api.foursquare.com/v2/venues/explore'

    params = dict(
    client_id='EOTMB0ZO4OY5TEH3DSCY0534DLT51D0H0D50OVWLQ4UL3MMO',
    client_secret='HVAA2GDMYPG3ZXZBB2XESKHMXF5UVFJ2QM5HLI1IRJ2YNSDA',
    v='20180323',
    ll=f'{lat},{lng}',
    query=place,
    radius=meter_range,
    price=cost,
    limit=30
    )
    resp = requests.get(url=url, params=params)
    data = resp.json()["response"]

    li = []
    for shop in data['groups'][0]["items"]:
        name = shop["venue"]["name"]
        distance = shop["venue"]["location"]["distance"]
        li.append({"name":name, "distance":distance})
    return li

def get_location(address):
    url = "https://trueway-geocoding.p.rapidapi.com/Geocode"

    querystring = {"language":"en","address":address}

    headers = {
        'x-rapidapi-host': "trueway-geocoding.p.rapidapi.com",
        'x-rapidapi-key': "cc8a2e13a8msh45078ac7d97e1abp1f29f2jsn55f4b2ee380c"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    return response.json()["results"][0]["location"]
    

@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        pr = request.form['prefer']
        sw = request.form['sweetness']
        sp = request.form['spicyness']
        h = request.form['healthy']
        pl = request.form['place']
        r = request.form['range'] 
        address = request.form['address']
        location = get_location(address)
        lat = location["lat"]
        lng = location["lng"]
        return redirect(url_for("searching", preference=pr, sweetness=sw, spicyness=sp, 
                                                healthyness=h, place=pl, meter_range=r, lat=lat, lng=lng, address=address))
    return render_template('form.html')

@app.route('/searching/<preference>/<sweetness>/<spicyness>/<healthyness>/<place>/<meter_range>/<lat>/<lng>/<address>')
def searching(preference, sweetness, spicyness, healthyness, place, meter_range, lat, lng, address):
    
    place_rendered = ""
    if (preference == "vegetarian"):
        place_rendered = "salad"
    elif (place == "cafe"):
        if (sweetness == "salty"):
            place_rendered = "bar"
        else:
            place_rendered = "cafe"
    elif (place == "restaurant"):
        if (spicyness == "less"):
            place_rendered = "restaurant"
        elif (spicyness == "moderate"):
            place_rendered = "chinese"
        elif (spicyness == "high"):
            place_rendered = "indian"
    elif (place == "fast foods"):
        if (healthyness == "healthy"):
            place_rendered = "salad"
        elif (healthyness == "moderate_healthy"):
            if (sweetness == "sweet"):
                place_rendered = "bakery"
            elif (sweetness == "salty"):
                place_rendered = "pizza"
        elif (healthyness == "unhealthy"):
            place_rendered = "burger"

    places = get_response(place_rendered, meter_range, 1, lat, lng)
    return render_template("shops.html", shop_list=places, place=place_rendered, address=address)

if __name__ == "__main__":
    app.run(debug=True)