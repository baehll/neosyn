from flask import Blueprint, render_template, request, jsonify, send_from_directory
import requests

views = Blueprint('views', __name__)

# @views.route('/')
# def index():
#     media_id = 18006078842062541
#     access_token = "EAAJtrkmf9eYBO2TQojC7Wcg7ZCOrzEqVAdcZBSyZBeZBw8PO5pZCa5NCQv6ezUpjpozbHIBLIcZAoBGAhW0yPjBwZBfmyXUMb8xb4ZCFvOfb3z37a5waeuxbLoXwvGU7gT902zerhJw9HOcOFjV11lQ8jh0ImW3TBmDrruOMYJHk4a9AsZBpCBSQ0ZCgTWXgEGA4GY9UfWlLsGXWdoBzlUxeCjQQMQTGSEoAZDZD"
    
#     comments = get(media_id, access_token)['comments']['data']

#     return render_template("home.html", comments=comments, user=None)

# @views.route('/prices')
# @views.route('/chatting')
# @views.route('/about')
@views.route('/')
def index():
    return send_from_directory('static', 'index.html')

@views.route('/assets/<path:filename>')
def serve_static_assets(filename):
    return send_from_directory('static/assets', filename)

 