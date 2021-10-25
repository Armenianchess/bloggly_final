from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ihaveasecret'

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# toolbar = DebugToolbarExtension(app)

connect_db(app)

# first route
@app.route('/')
def home():
    get_all_users = User.query.all()
    print(get_all_users)
    return render_template('index.html',get_all_users = get_all_users)


# second route
@app.route('/users/new')
def add_user():
    return render_template('add-user.html')


# third route
@app.route('/users')
def show_users():
    return render_template('all-users.html')


# fourth route
@app.route('/user/new',methods=['GET','POST'])
def create_user():
    print ('here is new user')
    print (request.form)

    new_user = User(
    first_name =request.form['first_name'],
    last_name =request.form['last_name'],
    image_url =request.form['img'] or None)


    db.session.add(new_user)
    db.session.commit()


    return redirect('/users')


# fifth route
@app.route('/users/<int:user_id>')
def create_user_id(user_id):
    filter_user = User.query.filter_by(id=user_id).first()
    filter_post = Post.query.filter_by(user_id=user_id).all()
    return render_template('user-id.html',filter_user = filter_user,filter_post=filter_post)

# sixth route
@app.route('/user/<int:user_id>/edit',methods=['GET','POST'])
def edit_user(user_id):
    user_edit = User.query.filter_by(id=user_id).first()
    if request.method == 'POST':
        first_name =request.form['first_name']
        last_name =request.form['last_name']
        image_url =request.form['img']
        user_edit.first_name = first_name
        user_edit.last_name = last_name
        user_edit.image_url = image_url
        db.session.flush()
        db.session.commit()
    return render_template('user-edit.html',user_edit=user_edit)


# seventh route
@app.route('/users/<int:user_id>/delete',methods=['GET'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect ('/')

@app.route('/users/<int:user_id>/posts/new',methods=['GET','POST'])
def add_post(user_id):
    tags=Tag.query.all()
    if request.method=='POST':
            title =request.form['title']
            content =request.form['content']
            tag_list=[]
            for tag in tags:
                try:
                    request.form[str(tag.id)]
                    tag_list.append(tag.id)
                except:
                    pass
            
            tags = Tag.query.filter(Tag.id.in_(tag_list)).all()
            print("------------------")
            print(tags)
            new_post = Post(
                    title=title,
                    content = content,
                    user_id = user_id,
                    tags=tags)
            db.session.add(new_post)
            db.session.commit()
            return redirect(f'/users/{user_id}')

    return render_template('add-post.html',tags=tags)

@app.route('/posts/<int:post_id>/detail',methods=['GET','POST'])
def post_detail(post_id):
    filter_post = Post.query.filter_by(id=post_id).first()
    return render_template('post-detail.html',post=filter_post)


@app.route('/posts/<int:post_id>/edit',methods=['GET','POST'])
def post_edit(post_id):
    tags=Tag.query.all()
    filter_post = Post.query.filter_by(id=post_id).first()
    if request.method=='POST':
            title =request.form['title']
            content =request.form['content']
            filter_post.title=title
            filter_post.content=content
            tag_list=[]
            for tag in tags:
                try:
                    request.form[str(tag.id)]
                    tag_list.append(tag.id)
                except:
                    pass
            
            tags = Tag.query.filter(Tag.id.in_(tag_list)).all()
            filter_post.tags = tags
            db.session.flush()
            db.session.commit()
            return redirect(f'/users/{filter_post.user_id}')

    return render_template('post-edit.html',post=filter_post,tags=tags)

@app.route('/posts/<int:post_id>/delete',methods=['GET'])
def delete_posts(post_id):
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect ('/')

@app.route('/tags',methods=['GET'])
def tags():
    tags=Tag.query.all()
    return render_template('tags.html',tags=tags)

@app.route('/tags/<int:tag_id>',methods=['GET'])
def tags_detail(tag_id):
    tag=Tag.query.filter_by(id=tag_id).first()
    posts=Post.query.all() 
    return render_template('tag-detail.html',tag=tag,posts=posts)

@app.route('/tags/new',methods=['GET','POST'])
def add_tag():
    if request.method == 'POST':
            new_post = Tag(
                    name = request.form['name'],
                    )
            db.session.add(new_post)
            db.session.commit()
            return redirect('/')
    return render_template('add-tag.html')

@app.route('/tags/<int:tag_id>/edit',methods=['GET','POST'])
def edit_tag(tag_id):
    filter_tag=Tag.query.filter_by(id=tag_id).first()
    if request.method=='POST':
            name =request.form['name']

            filter_tag.name=name
            db.session.flush()
            db.session.commit()  
            return redirect('/tags')
    return render_template('edit-tag.html',tag=filter_tag) 

@app.route('/tags/<int:tag_id>/delete',methods=['GET'])
def delete_tag(tag_id):
    Tag.query.filter_by(id=tag_id).delete()
    db.session.commit()
    return redirect('/tags')