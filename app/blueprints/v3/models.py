from app import db
from datetime import datetime as dt

v3_page_components = db.Table('v3_page_components',
    db.Column('component_id', db.Integer, db.ForeignKey('v3__component.id')),
    db.Column('page_id', db.Integer, db.ForeignKey('v3__page.id'))
)

v3_navbar_links = db.Table('v3_navbar_links',
    db.Column('link_id', db.Integer, db.ForeignKey('v3__link.id')),
    db.Column('navbar_id', db.Integer, db.ForeignKey('v3__navbar.id'))
)

v3_article_sections = db.Table('v3_article_sections',
    db.Column('section_id', db.Integer, db.ForeignKey('v3__section.id')),
    db.Column('article_id', db.Integer, db.ForeignKey('v3__article.id'))
)

class V3_Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=dt.utcnow())
    edited_on = db.Column(db.DateTime, default=dt.utcnow())
    owner = db.Column(db.Integer)
    page_type = db.Column(db.String(50), default='main', nullable=False)
    components = db.relationship(
        'V3_Component',
        secondary=v3_page_components,
        backref=db.backref('pages', lazy='dynamic', cascade="all, delete"))

    def __repr__(self):
        return f'< V3 Page | ID: {self.id} | Name: {self.name} >'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'page_type':self.page_type,
            'created_on':self.created_on,
            'edited_on':self.edited_on,
            'owner':self.owner,
            'components':[component.to_dict() for component in self.components]
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name', 'page_type', 'edited_on', 'owner']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_components(self, components):
        for component in components:
            self.components.append(component)

    def remove_components(self, components):
        for component in components:
            self.components.remove(component)

class V3_Component(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=dt.utcnow())
    edited_on = db.Column(db.DateTime, default=dt.utcnow())
    owner = db.Column(db.Integer)
    value = db.Column(db.String(50))
    content_type = db.Column(db.String(50))
    content_id = db.Column(db.Integer)

    def __repr__(self):
        return f'< V3 Component | ID: {self.id} | Name: {self.name} >'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'created_on':self.created_on,
            'edited_on':self.edited_on,
            'owner':self.owner,
            'value':self.value,
            'content_type':self.content_type,
            'content_id':self.content_id,
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name', 'title', 'edited_on', 'owner', 'value', 'content_type', 'content_id']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

class V3_Navbar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=dt.utcnow())
    edited_on = db.Column(db.DateTime, default=dt.utcnow())
    owner = db.Column(db.Integer)
    icon = db.Column(db.Integer, db.ForeignKey('v3__image.id'))
    links = db.relationship(
        'V3_Link',
        secondary=v3_navbar_links,
        backref=db.backref('navbars', lazy='dynamic', cascade="all, delete"))

    def __repr__(self):
        return f'< V3 Navbar | ID: {self.id} | Name: {self.name} >'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'created_on':self.created_on,
            'edited_on':self.edited_on,
            'icon': V3_Image.query.get(self.icon).to_dict(),
            'links':[link.to_dict() for link in self.links]
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name', 'edited_on', 'owner', 'icon']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

    def add_links(self, links):
        for link in links:
            self.links.append(link)
        db.session.commit()

class V3_Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=dt.utcnow())
    edited_on = db.Column(db.DateTime, default=dt.utcnow())
    owner = db.Column(db.Integer)
    value = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(500), nullable=False, default='/')

    def __repr__(self):
        return f'< V3 Link | ID: {self.id} | Name: {self.name} >'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'created_on':self.created_on,
            'edited_on':self.edited_on,
            'owner':self.owner,
            'value':self.value,
            'destination':self.destination
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name', 'edited_on', 'owner', 'value', 'destination']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

class V3_Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=dt.utcnow())
    edited_on = db.Column(db.DateTime, default=dt.utcnow())
    owner = db.Column(db.Integer)
    description = db.Column(db.String(500))
    location = db.Column(db.String(500))

    def __repr__(self):
        return f'< V3 Image | ID: {self.id} | Name: {self.name} >'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'created_on':self.created_on,
            'edited_on':self.edited_on,
            'owner':self.owner,
            'description':self.description,
            'location':self.location
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name', 'edited_on', 'owner', 'description', 'location']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

class V3_Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=dt.utcnow())
    edited_on = db.Column(db.DateTime, default=dt.utcnow())
    owner = db.Column(db.Integer)
    title = db.Column(db.String(100))
    summary = db.Column(db.String(3000))
    lead = db.Column(db.String(250))
    thumbnail = db.Column(db.Integer, db.ForeignKey('v3__image.id'))
    sections = db.relationship(
        'V3_Section',
        secondary=v3_article_sections,
        backref=db.backref('articles', lazy='dynamic', cascade="all, delete"))
    # tags

    def __repr__(self):
        return f'< V3 Article | ID: {self.id} | Name: {self.name} >'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'created_on':self.created_on,
            'edited_on':self.edited_on,
            'owner':self.owner,
            'title':self.title,
            'summary' : self.summary,
            'lead':self.lead,
            'thumbnail':V3_Image.query.get(self.thumbnail).to_dict(),
            # 'tags': [tag.to_dict() for tag in self.tags],
            'sections' : [section.to_dict() for section in self.sections]
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name', 'edited_on', 'owner', 'title', 'summary', 'lead', 'thumbnail']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)

class V3_Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=dt.utcnow())
    edited_on = db.Column(db.DateTime, default=dt.utcnow())
    owner = db.Column(db.Integer)
    title = db.Column(db.String(100))
    text = db.Column(db.String(9999))
    thumbnail = db.Column(db.Integer, db.ForeignKey('v3__image.id'))

    def set_attributes(self, data):
        for attribute in ['name', 'edited_on', 'owner', 'title', 'text']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'created_on':self.created_on,
            'edited_on':self.edited_on,
            'owner':self.owner,
            'title':self.title,
            'text' : self.text,
            'thumbnail':V3_Image.query.get(self.thumbnail).to_dict(),
            # 'tags': [tag.to_dict() for tag in self.tags],
        }
        return attributes_dict

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)