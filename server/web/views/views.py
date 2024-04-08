from flask import Blueprint, render_template, request, jsonify, send_from_directory
import requests

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return send_from_directory('static', 'index.html')

@views.route('/assets/<path:filename>')
def serve_static_assets(filename):
    return send_from_directory('static/assets', filename)

@views.route("/app.html")
def app_html():
    return send_from_directory("static", "app.html")

@views.route("/registration.html")
def registration():
    return send_from_directory("static", "registration.html")