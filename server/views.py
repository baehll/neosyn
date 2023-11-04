from flask import Blueprint, render_template, request
import requests


views = Blueprint('views', __name__)

@views.route('/')
def index():
    media_id = 18006078842062541
    access_token = "EAAJtrkmf9eYBO2TQojC7Wcg7ZCOrzEqVAdcZBSyZBeZBw8PO5pZCa5NCQv6ezUpjpozbHIBLIcZAoBGAhW0yPjBwZBfmyXUMb8xb4ZCFvOfb3z37a5waeuxbLoXwvGU7gT902zerhJw9HOcOFjV11lQ8jh0ImW3TBmDrruOMYJHk4a9AsZBpCBSQ0ZCgTWXgEGA4GY9UfWlLsGXWdoBzlUxeCjQQMQTGSEoAZDZD"
    
    comments = get(media_id, access_token)['comments']['data']

    return render_template("home.html", comments=comments, user=None)


def get(media_id, access_token):
    url = "https://graph.facebook.com/v18.0/" + str(media_id)


    params = {
        "fields": "comments_count,comments{text, username, replies{username, text}}",
        "transport": "cors",
        "access_token": access_token
    }

    response = requests.get(url, params=params)
    return response.json()

@views.route('/token')
def token():
    name = request.args.get('name')
    value = request.args.get('value')
    print(value)