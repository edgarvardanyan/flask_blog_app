# views for users
from flask import (
    render_template, url_for, flash,
    redirect, request, Blueprint)
from flask_login import (
    login_user, current_user, logout_user, login_required)
from blog import db
from blog.models import User, BlogPost
from blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from blog.users.picture_handler import add_profile_pic

# registering the blueprint
users = Blueprint('users', __name__)


# register view
@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')

        return redirect(url_for('users.login'))
    
    return render_template('register.html', form=form)


# login view
@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash("Logged in succesfully!")
            
            next = request.args.get('next')
            
            if next is None or next[0] != '/':
                next = url_for('core.index')
            
            return redirect(next)
    
    return render_template('login.html', form=form)


# logout view
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))


# account(update UserForm)
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUserForm()
    
    if form.validate_on_submit():
        
        # if a new picture is uploaded
        if form.picture.data:
            username = current_user.username
            # pic is the path of the saved image
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic
        
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account information updated!')
        
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        # grabbing current info of they have not submitted yet
        form.username.data = current_user.username
        form.email.data = current_user.email
    
    profile_image = url_for(
        'static',
        filename=('profile_pics/' + current_user.profile_image))
    
    return render_template('account.html',
                           profile_image=profile_image,
                           form=form)


# user's list of blogposts
# take the username as argument and put that in the url
@users.route("/<username>")
def user_posts(username):
    # grab their current page
    page = request.args.get('page', 1, type=int)
    # return 404 error in case wrong url is specified mannualy
    user = User.query.filter_by(username=username).first_or_404()
    # filter the blog post by author,
    # order them by the descending order of the datetime,
    # and show 5 posts per page
    blog_posts = BlogPost.query.filter_by(
        author=user).order_by(BlogPost.date.desc()).paginate(page=page,
                                                             per_page=5)

    return render_template('user_blog_posts.html',
                           blog_posts=blog_posts,
                           user=user)
    
    
