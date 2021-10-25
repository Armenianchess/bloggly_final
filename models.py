from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

"""Models for Blogly."""

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "posts_tags"
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    """Tag that can be added to posts."""
   
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )


def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """
    db.app = app
    db.init_app(app)