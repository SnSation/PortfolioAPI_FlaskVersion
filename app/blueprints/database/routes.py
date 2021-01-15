from . import bp as database
from flask import render_template, redirect, url_for, jsonify
import requests
from app import db

@database.route('/', methods=['GET'])
def main():
    return render_template('database/main.html')