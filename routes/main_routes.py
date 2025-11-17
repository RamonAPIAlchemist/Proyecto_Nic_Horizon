from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def inicio():
    return render_template("index.html")

@main_bp.route('/index')
def index():
    return render_template("index.html")

@main_bp.route('/contactopost')
def contactopost():
   
    return render_template("contactopost.html")

@main_bp.route('/acercade')
def acercade():
    return render_template("acercade.html")
