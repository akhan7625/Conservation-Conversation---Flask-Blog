import flask_login
import paginate as paginate
import sqlalchemy
from flask import render_template, flash, redirect, url_for, request, abort
from sqlalchemy import create_engine

from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, PostForm
from flaskblog.models import User, Post, Comments
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail,Message

engine = create_engine("mysql+mysqlconnector://admin3:@GitPa$$w0rd#@54.74.234.11/finalproject_group3")
Post.metadata.bind = engine

DBSession = sqlalchemy.orm.sessionmaker(bind=engine)
session = DBSession()
mail = Mail(app)

@app.route('/')
@app.route('/home_page')
def home_page():

    sendTestEmail()

    return render_template('home_page.html')

@app.route('/blog_archive')
def blog_archive():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)
    title = "Our Blog"

    return render_template('blog_archive.html', posts=posts, title=title)


# Route for search results
@app.route('/results')
def results():
    q = request.args.get('q')
    title = "Search Results"

    if q:
        posts= session.query(Post).filter(Post.title.contains(q) |
                                           Post.content.contains(q)).order_by(Post.date_posted.desc()).limit(3).all()
        return render_template('results.html', posts=posts, title=title)
    else:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=3)

        return render_template('blog_archive.html', posts=posts, title=title)


@app.route('/articles')
def articles():
    return render_template('articles.html', title='Article')

@app.route('/article-1')
def article_1():
    return render_template('article-1.html', title='Article1')

@app.route('/article-2')
def article_2():
    return render_template('article-2.html', title='Article2')

@app.route('/article-3')
def article_3():
    return render_template('article-3.html', title='Article3')

@app.route('/article-4')
def article_4():
    return render_template('article-4.html', title='Article4')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    comments = Comments.query.filter_by(post_id=post.id).all()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        comment = Comments(name=name, email=email, message=message, post_id=post.id)
        db.session.add(comment)
        post.comments += 1
        flash('Your comment has been submitted', 'success')
        db.session.commit()

        return redirect(request.url)
    return render_template('post.html', title=post.title, post=post, comments=comments)


# @app.route("/post/<int:post_id>", methods=['POST'])
# def post(post_id):
#     name = request.form.get('name')
#     email = request.form.get('email')
#     message = request.form.get('message')
#     comment = Comments(name=name, email=email, message=message, post_id=post.id)
#     db.session.add(comment)
#     post.comments += 1
#     flash('Your comment has been submitted', 'success')
#     db.session.commit()
#
#     return redirect(request.url)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=request.form['title'], content=request.form['content'], author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('blog_archive'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('blog_archive'))


def sendTestEmail():
    msg = Message("Our first Python Email",
                  sender="ctrl.alt.elite.2021@gmail.com",
                  recipients=["ctrl.alt.elite.2021@gmail.com"])

    msg.body = """ 
    Hello there,

    I am sending this message from python.

    say Hello

    regards,
    Me
    """


    msg.html = """

    <div>
    <h5>Hello there</h5>
    <br>

    <p>
    I am sending this message from Python 
    <br>
    Say hello 
    <br>
    Regards
    </p>
    </div>

    """

    # mail.send(msg)


def sendContactForm(result):
    msg = Message("New Message",
                  sender="ctrl.alt.elite.2021@gmail.com",
                  recipients=["ctrl.alt.elite.2021@gmail.com"])

    msg.body = """
    Hello there,

    You just received a contact form.

    Name: {}
    Email: {}
    Subject: {}
    Message: {}


    Kind Regards,
    Admin

    """.format(result['name'], result['email'],result['subject'],result['message'])

    mail.send(msg)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        result = {}

        result['name'] = request.form['name']
        result['email'] = request.form['email'].replace(' ', '').lower()
        result['subject'] = request.form['subject']
        result['message'] = request.form['message']

        sendContactForm(result)



        return redirect(url_for('home_page'))


    return render_template('contact-form.html', **locals())


# Route for Like/Unlike
@app.route('/post/<int:post_id>/<action>', methods=['GET', 'POST'])
# @login_required
def like_action(post_id, action):
    post = Post.query.get_or_404(post_id)
    if action == 'like':
        current_user.like_post(post)
        post.likes += 1
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        post.likes -= 1
        db.session.commit()
    return redirect(request.referrer)


# Route for most likes
@app.route('/most_liked', methods=['GET', 'POST'])
def most_liked():
    posts = Post.query.order_by(Post.likes.desc()).limit(3).all()
    title = "Most liked blog posts!"

    return render_template('most_popular.html', posts=posts, title=title)


# Route for most commented
@app.route('/most_commented', methods=['GET', 'POST'])
def most_commented():
    posts = Post.query.order_by(Post.comments.desc()).limit(3).all()
    title = "Most commented blog posts!"

    return render_template('most_popular.html', posts=posts, title=title)


# Route for most recent
@app.route('/most_recent', methods=['GET', 'POST'])
def most_recent():
    posts = Post.query.order_by(Post.date_posted.desc()).limit(3).all()
    title = "Most recent blog posts!"

    return render_template('most_popular.html', posts=posts, title=title)
