from . import bp as database
from flask import render_template, redirect, url_for, jsonify, request
import requests
from app import db
from .models import User, Role, Project, BlogPost, Tag, Page, PageCategory, PageComponent, ComponentElement
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

###################
## Site API V0.2 ##
###################

# Start: Entity Selection

@database.route('/v2_new_entities', methods=['GET', 'POST'])
def v2_new_entities():
    return render_template('database/v2_new_entities.html')

@database.route('/v2_edit_entities', methods=['GET', 'POST'])
def v2_edit_entities():
    context = {
        'pages':Page.query.all(),
        'categories':PageCategory.query.all(),
        'components':PageComponent.query.all(),
        'elements':ComponentElement.query.all()
    }
    return render_template('database/v2_edit_entities.html', **context)


# End: Entity Selection

####################

# Start: Page Routes

# @database.route('/create_page_form', methods=['GET', 'POST'])
# def create_page_form():
#     return render_template('database/create_page_form.html')

@database.route('/create_page', methods=['GET'])
def create_page():
    page_name = request.args.get('page_name')

    page_data = {
        'name':page_name,
    }

    if len(request.args.get('page_category')) > 0:
        this_category = PageCategory.query.filter_by(name=request.args.get('page_category')).first()
        page_data['page_category'] = this_category.id

    new_page = Page()
    new_page.set_attributes(page_data)
    new_page.new_to_database()
    this_page = Page.query.filter_by(name=new_page.name).first()

    page_components = []
    if len(request.args.get('page_components')) > 0:
        page_components = request.args.get('page_components').split(', ')

    for component in page_components:
        print(PageComponent.query.filter_by(name=component).first())
        try:
            this_component = PageComponent.query.filter_by(name=component).first()
            this_page.components.append(this_component)
            db.session.commit()
        except:
            print(f'Component Not Found: {component}')
            continue
    
    return jsonify(Page.query.filter_by(name=this_page.name).first().to_dict())

@database.route('/edit_page_form', methods=['GET', 'POST'])
def edit_page_form():
    context = {
        'page':Page.query.get(request.args.get('page_id'))
    }

    return render_template('database/edit_page_form.html', **context)

@database.route('/edit_page', methods=['GET'])
def edit_page():
    this_page = Page.query.get(request.args.get('page_id'))

    # # Delete?
    # if request.args.get('delete') == 'yes':
    #     this_page.remove_from_database()
    #     return f'{this_page.name} deleted from database'

    # Edit?
    page_name = this_page.name
    page_category = this_page.category

    if len(request.args.get('page_name')) > 0:
        page_name = request.args.get('page_name')

    if len(request.args.get('page_category')) > 0:
        page_category = request.args.get('page_category')

    page_data = {
        'name':page_name,
        'category':page_category,
        'last_edit':dt.utcnow()
    }

    this_page.set_attributes(page_data)

    if len(request.args.get('page_components')) > 0:
        components = request.args.get('page_components').split(', ')
        for component in components:
            try:
                this_component = PageComponent.query.filter_by(name=component).first()
                this_page.components.append(this_component)
            except:
                print(f'Component Not Found: {component}')
                continue

    this_page.update_in_database()

    return jsonify(Page.query.filter_by(name=this_page.name).first().to_dict())

# End: Page Routes

####################

# Start: Page Category Routes

# @database.route('/create_page_category_form', methods=['GET', 'POST'])
# def create_page_category_form():
#     return render_template('database/create_page_category_form.html')

@database.route('/create_page_category', methods=['GET'])
def create_page_category():
    category_name = request.args.get('category_name')

    category_data = {
        'name':category_name
    }

    new_category = PageCategory()
    new_category.set_attributes(category_data)
    new_category.new_to_database()

    this_category = PageCategory.query.filter_by(name=new_category.name).first()

    return jsonify(this_category.to_dict())

@database.route('edit_page_category_form', methods=['GET', 'POST'])
def edit_page_category_form():
    context = {
        'category': PageCategory.query.get(request.args.get('category_id'))
    }
    return render_template('database/edit_page_category_form.html', **context)

@database.route('/edit_page_category', methods=['GET'])
def edit_page_category():
    this_category = PageCategory.query.get(request.args.get('category_id'))
    category_name = this_category.name

    if len(request.args.get('category_name')) > 0:
        category_name = request.args.get('category_name')

    category_data = {
        'name':category_name,
        'last_edit':dt.utcnow()
    }

    this_category.set_attributes(category_data)
    this_category.update_in_database()

    return jsonify(PageCategory.query.filter_by(name=this_category.name).first().to_dict())

# End: Page Category Routes

####################

# Start: Page Component Routes

# @database.route('/create_page_component_form', methods=['GET', 'POST'])
# def create_page_component_form():
#     return render_template('database/create_page_component_form.html')

@database.route('/create_page_component', methods=['GET'])
def create_page_component():
    component_name = request.args.get('component_name')
    component_type = request.args.get('component_type')
    
    component_data = {
        'name':component_name,
        'component_type':component_type
    }

    new_component = PageComponent()
    new_component.set_attributes(component_data)
    new_component.new_to_database()

    this_component = PageComponent.query.filter_by(name=new_component.name).first()

    if len(request.args.get('component_elements')) > 0:
        elements = request.args.get('component_elements').split(', ')
        for element in elements:
            try:
                this_element = ComponentElement.query.filter_by(name=element).first()
                this_component.elements.append(this_element)
                db.session.commit()
            except:
                print(f'Element Not Found: {element}')
                continue
    
    return jsonify(PageComponent.query.filter_by(name=this_component.name).first().to_dict())

@database.route('/edit_page_component_form', methods=['GET', 'POST'])
def edit_page_component_form():
    context = {
        'component':PageComponent.query.get(request.args.get('component_id'))
    }
    return render_template('database/edit_page_component_form.html', **context)
    
@database.route('/edit_page_component', methods=['GET', 'POST'])
def edit_page_component():
    this_component = PageComponent.query.get(request.args.get('component_id'))
    component_name = this_component.name

    if len(request.args.get('component_name')) > 0:
        component_name = request.args.get('component_name')

    component_data = {
        'name':component_name,
        'last_edit':dt.utcnow()
    }

    this_component.set_attributes(component_data)

    if len(request.args.get('component_elements')) > 0:
        elements = request.args.get('component_elements').split(', ')
        new_elements = []
        for element in elements:
            try:
                this_element = ComponentElement.query.filter_by(name=element).first()
                if this_element != None:
                    new_elements.append(this_element)
            except:
                print(f'Element Not Found: {element}')
                continue
        print(new_elements)
        this_component.elements = new_elements
                
    this_component.update_in_database()

    return jsonify(PageComponent.query.filter_by(name=this_component.name).first().to_dict())

# End: Page Component Routes

####################

# Start: Component Element Routes

# @database.route('/create_component_element_form', methods=['GET', 'POST'])
# def create_component_element_form():
#     return render_template('database/create_component_element_form.html')

@database.route('/create_component_element', methods=['GET'])
def create_component_element():
    element_name = request.args.get('element_name')
    element_content = request.args.get('element_content')
    element_type = request.args.get('element_type')

    element_data = {
        'name':element_name,
        'content':element_content,
        'element_type':element_type
    }

    new_element = ComponentElement()
    new_element.set_attributes(element_data)
    new_element.new_to_database()

    return jsonify(ComponentElement.query.filter_by(name=new_element.name).first().to_dict())

@database.route('/edit_component_element_form', methods=['GET'])
def edit_component_element_form():
    context = {
        'element':ComponentElement.query.get(request.args.get('element_id'))
    }
    return render_template('database/edit_component_element_form.html', **context)

@database.route('/edit_component_element', methods=['GET'])
def edit_component_element():
    this_element = ComponentElement.query.get(request.args.get('element_id'))
    element_name = this_element.name
    element_content = this_element.content
    element_type = this_element.element_type

    if len(request.args.get('element_name')) > 0:
        element_name = request.args.get('element_name')
    if len(request.args.get('element_content')) > 0:
        element_content = request.args.get('element_content')
    if len(request.args.get('element_type')) > 0:
        element_type = request.args.get('element_type')

    element_data = {
        'name':element_name,
        'content':element_content,
        'element_type':element_type,
        'last_edit':dt.utcnow()
    }

    this_element.set_attributes(element_data)
    this_element.update_in_database()

    return jsonify(ComponentElement.query.filter_by(name=this_element.name).first().to_dict())


