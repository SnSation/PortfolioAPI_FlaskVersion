from . import bp as database
from flask import render_template, redirect, url_for, jsonify, request
import requests
from app import db
from .models import User, Role, Project, BlogPost, Tag
from datetime import datetime as dt

@database.route('/', methods=['GET'])
def main():
    return render_template('database/main.html')

# Database Row Creation

@database.route('/new_entities', methods=['GET', 'POST'])
def new_entities():
    return render_template('database/new_entities.html')

@database.route('/create_role', methods=['GET'])
def create_role():
    new_role = Role()
    role_data = {
        'name' : request.args.get('role_name', None)
    }
    new_role.set_attributes(role_data)
    new_role.new_to_database()
    this_role = Role.query.filter_by(name=new_role.name).first().to_dict()
    return jsonify(this_role)

@database.route('/roles', methods=['GET'])
def roles():
    all_roles = [role.to_dict() for role in Role.query.all()]
    return jsonify(all_roles)

@database.route('/create_user', methods=['GET'])
def create_user():
    new_user = User()
    user_data = {
        'username' : request.args.get('username', None),
        'password' : request.args.get('password', None),
        'email' : request.args.get('email', None),
        'role' : request.args.get('role_id', None),
    }
    new_user.set_attributes(user_data)
    new_user.new_to_database()
    this_user = User.query.filter_by(username=new_user.username).first().to_dict()
    return jsonify(this_user)

@database.route('/users', methods=['GET'])
def users():
    all_users = [user.to_dict() for user in User.query.all()]
    return jsonify(all_users)

@database.route('/create_project', methods=['GET'])
def create_project():
    new_project = Project()
    project_data = {
        'name':request.args.get('project_name', None),
        'description':request.args.get('project_description', None),
        'github':request.args.get('project_github', None)
    }
    new_project.set_attributes(project_data)
    new_project.new_to_database()
    this_project = Project.query.filter_by(name=new_project.name).first().to_dict()
    return jsonify(this_project)

@database.route('/projects', methods=['GET'])
def projects():
    all_projects = [project.to_dict() for project in Project.query.all()]
    return jsonify(all_projects)

@database.route('/create_blogpost', methods=['GET'])
def create_blogpost():
    new_blogpost = BlogPost()
    blogpost_data = {
        'title': request.args.get('blogpost_title', None),
        'content': request.args.get('blogpost_content', None),
        'author': request.args.get('blogpost_author', None)
    }
    new_blogpost.set_attributes(blogpost_data)
    new_blogpost.new_to_database()
    this_blogpost = BlogPost.query.filter_by(title=new_blogpost.title).first().to_dict()
    return jsonify(this_blogpost)

@database.route('/blogposts', methods=['GET'])
def blogposts():
    all_blogposts = [blogpost.to_dict() for blogpost in BlogPost.query.all()]
    return jsonify(all_blogposts)

@database.route('/create_tag', methods=['GET'])
def create_tag():
    new_tag = Tag()
    tag_data = {
        'name': request.args.get('tag_name', None)
    }
    new_tag.set_attributes(tag_data)
    new_tag.new_to_database()
    this_tag = Tag.query.filter_by(name=new_tag.name).first().to_dict()
    return jsonify(this_tag)

@database.route('/tags', methods=['GET'])
def tags():
    all_tags = [tag.to_dict() for tag in Tag.query.all()]
    return jsonify(all_tags)

# Database Row Manipulation
@database.route('/edit_entities', methods=['GET', 'POST'])
def edit_entities():
    context = {
        'blog_posts':[blog_post for blog_post in BlogPost.query.all()],
        'users': [user for user in User.query.filter(User.id > 1).all()],
        'projects': [project for project in Project.query.all()]
    }
    return render_template('database/edit_entities.html', **context)

@database.route('/choose_blogpost', methods=['GET', 'POST'])
def choose_blogpost():
    context = {
        'selected_post': BlogPost.query.get(request.args.get('blogpost_id'))
    }
    return render_template('database/edit_blogpost.html', **context)

@database.route('/edit_blogpost', methods=['GET'])
def edit_blogpost():
    this_post = BlogPost.query.get(request.args.get('blogpost_id'))
    if request.args.get('delete') == 'yes':
        this_post.remove_from_database()
        return f'Blog Post - {this_post.title} - Deleted'
    else:
        new_data = {
            'title': request.args.get('edited_blogpost_title', None),
            'content': request.args.get('edited_blogpost_content', None),
            'last_edit': dt.utcnow()
        }
        this_post.set_attributes(new_data)
        this_post.update_in_database()
        return f'Blog Post - {this_post.title} - Edited'

@database.route('/choose_user', methods=['GET', 'POST'])
def choose_user():
    context = {
        'selected_user': User.query.get(request.args.get('user_id')),
        'roles': Role.query.all()
    }
    return render_template('database/edit_user.html', **context)

@database.route('/edit_user', methods=['GET'])
def edit_user():
    this_user = User.query.get(request.args.get('user_id'))
    if request.args.get('delete') == 'yes':
        this_user.remove_from_database()
        return f'User - {this_user.username} - Deleted'
    else:
        new_data = {
            'username':request.args.get('edited_username', None),
            'password':request.args.get('edited_password', None),
            'role':request.args.get('edited_role', None),
            'last_edit': dt.utcnow()
        }
        this_user.set_attributes(new_data)
        this_user.update_in_database()
        return f'User - {this_user.username} - Edited'

@database.route('/choose_project', methods=['GET', 'POST'])
def choose_project():
    context = {
        'selected_project': Project.query.get(request.args.get('project_id')),
    }
    return render_template('database/edit_project.html', **context)

@database.route('/edit_project', methods=['GET'])
def edit_project():
    this_project = Project.query.get(request.args.get('project_id'))
    if request.args.get('delete') == 'yes':
        this_project.remove_from_database()
        return f'Project - {this_project.name} - Deleted'
    else:
        new_data = {
            'name':request.args.get('edited_name', None),
            'description':request.args.get('edited_description', None),
            'github':request.args.get('edited_github', None),
            'last_edit': dt.utcnow()
        }
        this_project.set_attributes(new_data)
        this_project.update_in_database()
        return f'Project - {this_project.name} - Edited'

@database.route('/change_tags', methods=['GET'])
def change_tags():
    tag_arguments = request.args.get('new_tags').lower().split(', ')
    tag_list = []
    for tag_name in tag_arguments:
        if Tag.query.filter_by(name=tag_name).first() == None:
            new_tag = Tag()
            tag_data = {
                'name': tag_name
            }
            new_tag.set_attributes(tag_data)
            new_tag.new_to_database()
            tag_list.append(Tag.query.filter_by(name=tag_name).first())
        else:
            tag_list.append(Tag.query.filter_by(name=tag_name).first())
    if request.args.get('object_type') == 'project':
        this_object = Project.query.get(request.args.get('object_id'))
        this_object.tags = tag_list
        db.session.commit()
    elif request.args.get('object_type') == 'blogpost':
        this_object = BlogPost.query.get(request.args.get('object_id'))
        this_object.tags = tag_list
        db.session.commit()
    return redirect(url_for('database.main'))

@database.route('/edit_tags', methods=['GET', 'POST'])
def edit_tags():
    selection_list = []
    selection_type = ''
    if request.args.get('object_type') == 'project':
        selection_type = "project"
        selection_list = Project.query.all()
    elif request.args.get('object_type') == 'blogpost':
        selection_type = "blogpost"
        selection_list = BlogPost.query.all()
    context = {
        'selection_type':selection_type,
        'selection_options':selection_list,
        'selection_tags':[]
    }
    return render_template('database/edit_tags.html', **context)
