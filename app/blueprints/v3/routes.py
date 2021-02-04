from . import bp as v3_interface
from flask import render_template, redirect, url_for, jsonify, request
import requests
from app import db
from datetime import datetime as dt
from .models import V3_Page, V3_Component, V3_Navbar, V3_Link, V3_Image, V3_Article, V3_Section

# Route Functions
def get_content(content_type, content_id):
    content_data = {

    }
    if content_type == 'navbar':
        this_content = V3_Navbar.query.get(content_id)
        content_data = this_content.to_dict()
    
    return content_data

# Page Routes

@v3_interface.route('/create_page')
def create_page():
    new_page = V3_Page()
    page_name = request.args.get('page_name')
    page_type = request.args.get('page_type')
    page_data = {
        'name':page_name,
        'page_type':page_type
    }
    new_page.set_attributes(page_data)
    new_page.save()

    this_page = V3_Page.query.filter_by(name=new_page.name).first()
    
    if len(request.args.get('page_components')) > 0:
        component_ids = request.args.get('page_components').split(', ')
        for component_id in component_ids:
            this_component = V3_Component.query.get(component_id)
            this_page.components.append(this_component)

    this_page.update()

    return jsonify(this_page.to_dict())

@v3_interface.route('/edit_page')
def edit_page():
    page_id = request.args.get('page_id')
    this_page = V3_Page.query.get(page_id)

    if request.args.get('delete') == 'yes':
        this_page.delete()
        return f'{this_page} deleted'

    page_name = this_page.name
    page_type = this_page.page_type
    new_name = request.args.get('new_name')
    new_type = request.args.get('new_type')

    if len(new_name) > 0:
        page_name = new_name
    if len(new_type) > 0:
        page_type = new_type

    page_data = {
        'name':page_name,
        'page_type':page_type,
        'edited_on':dt.utcnow(),
    }

    this_page.set_attributes(page_data)
    this_page.update()

    if len(request.args.get('page_components')) > 0:
        component_ids = request.args.get('page_components').split(', ')
        for component_id in component_ids:
            this_component = V3_Component.query.get(component_id)
            this_page.components.append(this_component)

    this_page.update()
    
    return jsonify(this_page.to_dict())

@v3_interface.route('/all_pages')
def all_pages():
    all_pages = V3_Page.query.all()
    page_data = [page.to_dict() for page in all_pages]
    for page in page_data:
        for component in page['components']:
            component['content'] = get_content(component['content_type'], component['content_id'])
    return jsonify(page_data)

@v3_interface.route('/page')
def get_page():
    page_id = request.args.get('page_id')
    this_page = V3_Page.query.get(page_id).to_dict()
    for component in this_page['components']:
        component['content'] = get_content(component['content_type'], component['content_id'])
    return jsonify(this_page)

# Component Routes

@v3_interface.route('/create_component')
def create_component():
    new_component = V3_Component()
    component_name = request.args.get('component_name')
    component_value = request.args.get('component_value')
    content_type = request.args.get('content_type')
    content_id = request.args.get('content_id')

    component_data = {
        'name':component_name,
        'value':component_value,
        'content_type':content_type,
        'content_id':content_id
    }

    new_component.set_attributes(component_data)
    new_component.save()

    this_component = V3_Component.query.filter_by(name=new_component.name).first()

    return jsonify(this_component.to_dict())

@v3_interface.route('/edit_component')
def edit_component():
    component_id = request.args.get('component_id')
    this_component = V3_Component.query.get(component_id)

    if len(request.args.get('component_name')) > 0:
        this_component.name = request.args.get('component_name')
    if len(request.args.get('component_value')) > 0:
        this_component.value = request.args.get('component_value')
    if len(request.args.get('content_type')) > 0:
        this_component.content_type = request.args.get('content_type')
    if len(request.args.get('content_id')) > 0:
        this_component.content_id = request.args.get('content_id')
    
    this_component.edited_on = dt.utcnow()

    this_component.update()

    component_data = this_component.to_dict()
    component_data['content'] = get_content(this_component.content_type, this_component.content_id)
    
    return jsonify(component_data)

@v3_interface.route('/all_components')
def all_components():
    all_components = V3_Component.query.all()
    component_data = [component.to_dict() for component in all_components]
    for component in component_data:
        component['content'] = get_content(component['content_type'], component['content_id'])

    return jsonify(component_data)

@v3_interface.route('/component')
def get_component():
    component_id = request.args.get('component_id')
    this_component = V3_Component.query.get(component_id)
    component_data = this_component.to_dict()
    component_data['content'] = get_content(component_data['content_type'], component_data['content_id'])
    
    return jsonify(component_data)

# Navbar Routes

@v3_interface.route('/all_navbars')
def all_navbars():
    all_navbars = V3_Navbar.query.all()
    navbar_data = [navbar.to_dict() for navbar in all_navbars]

    return jsonify(navbar_data)

@v3_interface.route('/navbar')
def get_navbar():
    this_navbar = V3_Navbar.query.get(request.args.get('navbar_id'))
    navbar_data = this_navbar.to_dict()

    return jsonify(navbar_data)

@v3_interface.route('/create_navbar')
def create_navbar():
    new_navbar = V3_Navbar()
    navbar_data = {
        'name':request.args.get('navbar_name'),
    }
    new_navbar.set_attributes(navbar_data)
    new_navbar.save()

    if request.args.get('link_ids'):
        link_ids = request.args.get('link_ids').split(', ')
        for link_id in link_ids:
            this_link = V3_Link.query.get(link_id)
            new_navbar.links.append(this_link)
    new_navbar.update()
    
    this_navbar = V3_Navbar.query.filter_by(name=new_navbar.name).first()

    return jsonify(this_navbar.to_dict())

@v3_interface.route('/edit_navbar')
def edit_navbar():
    this_navbar = V3_Navbar.query.get(request.args.get('navbar_id'))
    navbar_name = this_navbar.name
    navbar_icon = this_navbar.icon

    if len(request.args.get('navbar_name')) > 0:
        navbar_name = request.args.get('navbar_name')
    if len(request.args.get('navbar_icon')) > 0:
        navbar_icon = request.args.get('navbar_icon')

    navbar_data = {
        'name':navbar_name,
        'icon':navbar_icon,
        'edited_on':dt.utcnow()
    }

    this_navbar.set_attributes(navbar_data)
    this_navbar.update()

    if len(request.args.get('link_ids')) > 0:
        link_ids = request.args.get('link_ids').split(', ')
        for link_id in link_ids:
            this_link = V3_Link.query.get(link_id)
            this_navbar.links.append(this_link)
    this_navbar.update()

    return jsonify(this_navbar.to_dict())

# Link Routes

@v3_interface.route('/create_link')
def create_link():
    new_link = V3_Link()

    link_data = {
        'name':request.args.get('link_name'),
        'value':request.args.get('link_value'),
        'destination':request.args.get('link_destination')
    }

    new_link.set_attributes(link_data)
    new_link.save()

    this_link = V3_Link.query.filter_by(name=new_link.name).first()

    return jsonify(this_link.to_dict())

@v3_interface.route('/all_links')
def all_links():
    all_links = V3_Link.query.all()
    link_data = [link.to_dict() for link in all_links]
    
    return jsonify(link_data)

@v3_interface.route('/link')
def get_link():
    this_link = V3_Link.query.get(request.args.get('link_id'))

    return jsonify(this_link.to_dict())

@v3_interface.route('/edit_link')
def edit_link():
    this_link = V3_Link.query.get(request.args.get('link_id'))
    link_name = this_link.name
    link_value = this_link.value
    link_destination = this_link.destination

    if len(request.args.get('link_name')) > 0:
        link_name = request.args.get('link_name')
    if len(request.args.get('link_value')) > 0:
        link_value = request.args.get('link_value')
    if len(request.args.get('link_destination')) > 0:
        link_destination = request.args.get('link_destination')
    
    link_data = {
        'name' : link_name,
        'value' : link_value,
        'destination' : link_destination,
        'edited_on' : dt.utcnow()
    }

    this_link.set_attributes(link_data)
    this_link.update()

    return jsonify(this_link.to_dict())

# Image Routes

@v3_interface.route('/create_image')
def create_image():
    new_image = V3_Image()
    
    image_data = {
        'name':request.args.get('image_name'),
        'description':request.args.get('image_description'),
        'location':request.args.get('image_location')
    }

    new_image.set_attributes(image_data)
    new_image.save()

    this_image = V3_Image.query.filter_by(name=new_image.name).first()

    return jsonify(this_image.to_dict())

@v3_interface.route('/all_images')
def all_images():
    all_images = V3_Image.query.all()
    image_data = [image.to_dict() for image in all_images]

    return jsonify(image_data)

@v3_interface.route('/image')
def get_image():
    this_image = V3_Image.query.get(request.args.get('image_id'))

    return jsonify(this_image.to_dict())

@v3_interface.route('/edit_image')
def edit_image():
    this_image = V3_Image.query.get(request.args.get('image_id'))

    image_name = this_image.name
    image_description = this_image.description
    image_location = this_image.location

    if len(request.args.get('image_name')) > 0:
        image_name = request.args.get('image_name')
    if len(request.args.get('image_description')) > 0:
        image_description = request.args.get('image_description')
    if len(request.args.get('image_location')) > 0:
        image_location = request.args.get('image_location')

    image_data = {
        'name':image_name,
        'description': image_description,
        'location': image_location,
        'edited_on': dt.utcnow()
    }

    this_image.set_attributes(image_data)
    this_image.update()

    return jsonify(this_image.to_dict())

# Article Routes

@v3_interface.route('/create_article')
def create_article():
    new_article = V3_Article()
    article_name = request.args.get('article_name')
    article_title = request.args.get('article_title')
    article_summary = request.args.get('article_summary')
    article_lead = request.args.get('article_lead')
    article_thumbnail = request.args.get('article_thumbnail')

    article_data = {
        'name':article_name,
        'title':article_title,
        'summary':article_summary,
        'lead':article_lead,
        'thumbnail':article_thumbnail
    }

    new_article.set_attributes(article_data)
    new_article.save()

    this_article = V3_Article.query.filter_by(name=new_article.name).first()

    return jsonify(this_article.to_dict())

@v3_interface.route('/all_articles')
def all_articles():
    all_articles = V3_Article.query.all()

    article_data = [article.to_dict() for article in all_articles]

    return jsonify(article_data)

@v3_interface.route('/article')
def get_article():
    this_article = V3_Article.query.get(request.args.get('article_id'))

    return jsonify(this_article.to_dict())

@v3_interface.route('/edit_article')
def edit_article():
    this_article = V3_Article.query.get(request.args.get('article_id'))
    article_name = this_article.name
    article_title = this_article.title
    article_summary = this_article.summary
    article_lead = this_article.lead
    article_thumbnail = this_article.thumbnail

    if len(request.args.get('article_name')) > 0:
        article_name = request.args.get('article_name')
    if len(request.args.get('article_title')) > 0:
        article_title = request.args.get('article_title')
    if len(request.args.get('article_lead')) > 0:
        article_lead = request.args.get('article_lead')
    if len(request.args.get('article_thumbnail')) > 0:
        article_thumbnail = request.args.get('article_thumbnail')

    article_data = {
        'name':article_name,
        'title':article_title,
        'summary':article_summary,
        'lead':article_lead,
        'thumbnail':article_thumbnail,
        'edited_on':dt.utcnow()
    }

    this_article.set_attributes(article_data)

    if len(request.args.get('article_sections')) > 0:
        section_ids = request.args.get('article_sections').split(', ')
        for section_id in section_ids:
            this_section = V3_Section.query.get(section_id)
            this_article.sections.append(this_section)

    this_article.update()

    return jsonify(this_article.to_dict())

@v3_interface.route('/create_section')
def create_section():
    new_section = V3_Section()
    section_name = request.args.get('section_name')
    section_title = request.args.get('section_title')
    section_text = request.args.get('section_text')
    section_thumbnail = request.args.get('section_thumbnail')

    section_data = {
        'name':section_name,
        'title':section_title,
        'text':section_text,
        'thumbnail':section_thumbnail
    }

    new_section.set_attributes(section_data)
    new_section.save()

    this_section = V3_Section.query.filter_by(name=new_section.name).first()

    return jsonify(this_section.to_dict())

@v3_interface.route('/all_sections')
def all_sections():
    all_sections = V3_Section.query.all()

    section_data = [section.to_dict() for section in all_sections]

    return jsonify(section_data)

@v3_interface.route('/section')
def get_section():
    this_section = V3_Section.query.get(request.args.get('section_id'))

    return jsonify(this_section.to_dict())

