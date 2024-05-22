from flask import Blueprint, render_template, request, jsonify, send_from_directory, redirect
from flask_login import login_required, current_user
import requests

views = Blueprint('views', __name__)

@views.route('/', defaults={"path":""})
@views.route("/<path:path>")
def catch_all(path):
    return send_from_directory('static', "index.html")

@views.route('/assets/<path:filename>')
def serve_static_assets(filename):
    return send_from_directory('static/assets', filename)

@views.route("/login.html")
def login():
    # if current_user.is_authenticated:
    #     return redirect("/app.html")
    return send_from_directory("static", "login.html")

@views.route("/app.html")
@login_required
def app_html():
    return send_from_directory("static", "app.html")

@views.route("/registration.html")
@login_required
def registration():
    return send_from_directory("static", "registration.html")