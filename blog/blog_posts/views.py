# blog post views
from flask import (
    render_template, url_for, redirect, 
    flash, request, Blueprint, abort)
from flask_login import login_required, current_user
from blog import db
from blog.models import BlogPost
from blog.blog_posts.forms import BlogPostForm

blog_posts = Blueprint('blog_posts', __name__)

# create post
@blog_posts.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    
    if form.validate_on_submit():
        post = BlogPost(title=form.title.data,
                        text=form.text.data,
                        user_id=current_user.id)
        
        db.session.add(post)
        db.session.commit()
        flash('Blog post created!')
        
        return redirect(url_for('blog_posts.blog_post',
                                blog_post_id=post.id))
    
    return render_template('create_post.html', form=form)
    
# view post by the id taken as an integer parameter
@blog_posts.route('/<int:blog_post_id>')
def blog_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html',
                           title=blog_post.title,
                           text=blog_post.text,
                           date=blog_post.date,
                           post=blog_post)
    
# update post
@blog_posts.route('/<int:blog_post_id>/update', methods=['GET', 'POST'])
@login_required
def update(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # if the logged in user is not the author of the post 
        # we throw 403 error,denying their access to updating the post
        abort(403)
    
    form = BlogPostForm()
    
    if form.validate_on_submit():
        blog_post.title = form.title.data
        blog_post.text = form.text.data
        
        db.session.commit()
        
        flash('Blog post updated!')
        
        return redirect(url_for('blog_posts.blog_post',
                                blog_post_id=blog_post_id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.text.data = blog_post.text
    
    return render_template('create_post.html', title='Updating', form=form)

# delete post
@blog_posts.route('/<int:blog_post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        # if the logged in user is not the author of the post 
        # we throw 403 error,denying their access to updating the post
        abort(403)
    
    db.session.delete(blog_post)
    db.session.commit()
    flash('Post Deleted')
    return redirect(url_for('core.index'))

