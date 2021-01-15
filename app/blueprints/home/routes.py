from . import bp as home
from flask import jsonify, request, url_for, redirect, render_template
import requests

@home.route('/', methods=['GET'])
def main():
    return render_template('home/main.html')