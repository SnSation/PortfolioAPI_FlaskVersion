from app import db
from datetime import datetime as dt


# Association Tables

project_tags = db.Table('project_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'))
)

blogpost_tags = db.Table('blogpost_tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('blogpost_id', db.Integer, db.ForeignKey('blog_post.id'))
)

# Database Tables

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(500)) # Needs Hash
    email = db.Column(db.String(100))
    role = db.Column(db.Integer, db.ForeignKey('role.id'))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    last_edit = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<User | ID: {self.id} | Role: {self.role}>'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'created_on':self.created_on,
            'role':self.role,
            'last_edit':self.last_edit
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['username', 'password', 'email', 'role', 'last_edit']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def new_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()

    def update_in_database(self):
        db.session.commit()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __repr__(self):
        return f'<Role | ID: {self.id} | Name: {self.name}>'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def new_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()

    def update_in_database(self):
        db.session.commit()

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(250))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    github = db.Column(db.String(100))
    last_edit = db.Column(db.DateTime, default=dt.utcnow)
    image = db.Column(db.String(100), default='http://via.placeholder.com/300x300')
    tags = db.relationship('Tag', secondary=project_tags, backref=db.backref('projects', lazy='dynamic'))

    def __repr__(self):
        return f'<Project | ID: {self.id} | Name: {self.name}>'

    def to_dict(self):
        all_tags = []
        if len(self.tags) == 0:
            all_tags.append('None')
        else:
            for tag in self.tags:
                all_tags.append(tag.name)
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'description':self.description,
            'created_on':self.created_on,
            'github':self.github,
            'last_edit':self.last_edit,
            'tags':all_tags,
            'image':self.image
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name', 'description', 'github', 'last_edit', 'image']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def new_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()

    def update_in_database(self):
        db.session.commit()

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(250))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))
    last_edit = db.Column(db.DateTime, default=dt.utcnow)
    tags = db.relationship('Tag', secondary=blogpost_tags, backref=db.backref('blogposts', lazy='dynamic'))

    def __repr__(self):
        return f'<Blog Post | ID: {self.id} | Title: {self.title}>'

    def to_dict(self):
        all_tags = []
        if len(self.tags) == 0:
            all_tags.append('None')
        else:
            for tag in self.tags:
                all_tags.append(tag.name)
        attributes_dict = {
            'id':self.id,
            'title':self.title,
            'content':self.content,
            'created_on':self.created_on,
            'author':self.author,
            'last_edit':self.last_edit,
            'tags':all_tags
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['title', 'content', 'author', 'last_edit']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def new_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()

    def update_in_database(self):
        db.session.commit()

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    created_on = db.Column(db.DateTime, default=dt.utcnow)

    def __repr__(self):
        return f'<Tag | ID: {self.id} | Name: {self.name}>'

    def to_dict(self):
        attributes_dict = {
            'id':self.id,
            'name':self.name,
            'created_on':self.created_on
        }
        return attributes_dict

    def set_attributes(self, data):
        for attribute in ['name']:
            if attribute in data:
                setattr(self, attribute, data[attribute])

    def new_to_database(self):
        db.session.add(self)
        db.session.commit()

    def remove_from_database(self):
        db.session.delete(self)
        db.session.commit()

    def update_in_database(self):
        db.session.commit()

# class Article(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(50))
#     summary = db.Column(db.String(250))
#     content = db.Column(db.String(5000))
#     # tags = Many to Many association table
