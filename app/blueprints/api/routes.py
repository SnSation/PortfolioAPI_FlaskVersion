from . import bp as api
from flask import render_template, redirect, url_for, jsonify, request
import requests
from app import db
from app.blueprints.database.models import User, Role, Project, BlogPost, Tag

@api.route('/', methods=['GET'])
def main():
    context = {
        'users': User.query.all(),
        'blogposts': BlogPost.query.all(),
        'projects': Project.query.all(),
        'tags': Tag.query.all()
    }
    return render_template('api/main.html', **context)

@api.route('/all_users', methods=['GET'])
def all_users():
    all_users = [user.to_dict() for user in User.query.all()]
    return jsonify(all_users)

@api.route('/single_user', methods=['GET'])
def single_user():
    this_user = User.query.get(request.args.get('user_id')).to_dict()
    return jsonify(this_user)

@api.route('/all_blogposts', methods=['GET'])
def all_blogposts():
    all_blogposts = [blogpost.to_dict() for blogpost in BlogPost.query.all()]
    return jsonify(all_blogposts)

@api.route('/single_blogpost', methods=['GET'])
def single_blogpost():
    this_blogpost = BlogPost.query.get(request.args.get('blogpost_id')).to_dict()
    return jsonify(this_blogpost)

@api.route('/all_projects', methods=['GET'])
def all_projects():
    all_projects = [project.to_dict() for project in Project.query.all()]
    return jsonify(all_projects)

@api.route('/single_project', methods=['GET'])
def single_project():
    this_project = Project.query.get(request.args.get('project_id')).to_dict()
    return jsonify(this_project)

@api.route('/all_tags', methods=['GET'])
def all_tags():
    all_tags = [tag.to_dict() for tag in Tag.query.all()]
    return jsonify(all_tags)

@api.route('/single_tag', methods=['GET'])
def single_tag():
    this_tag = Tag.query.get(request.args.get('tag_id')).to_dict()
    return jsonify(this_tag)