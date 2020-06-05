# core views of the blog
from flask import render_template, request, Blueprint
from blog.models import BlogPost

core = Blueprint('core', __name__)


@core.route('/')
def index():
    # paginate
    page = request.args.get('page', 1, type=int)
    # get posts sorted by date
    posts = BlogPost.query.order_by(BlogPost.date.desc()).paginate(
        page=page, per_page=2)
    
    return render_template('index.html', posts=posts)


@core.route('/info')
def info():
    return render_template('info.html')
