from flask import (Blueprint, render_template, flash, g, abort,
                    request, redirect, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user

from models import Post, Article

from datetime import datetime

blog = Blueprint('blog', __name__, url_prefix='')

class PostView(FlaskView):
    """ Our base ViewClass for any Post related endpoints 
    """
    route_base = '/'

    def index(self):
        """ Our main index view """
        post = Post.objects(kind__in=['note', 'article'], 
                published=True, pub_date__lte=datetime.now()).first()
        return render_template('blog/index.html', post=post)
    
    @route('/archive/', endpoint='archive',)
    def archive(self):
        """ Archive View """
        g.posts = Post.objects(kind__in=['article'], 
                published=True, pub_date__lte=datetime.now())

        return render_template('blog/archive.html')

    @route('/category/<category>/', endpoint='category')
    @route('/category/<category>/<int:page_num>/', endpoint='category')
    def category(self, category, page_num=1):
        """ Category Page"""
        if category == 'note':
            g.posts = Post.objects(kind__in=['note'], published=True, 
                pub_date__lte=datetime.now()).paginate(page=page_num, per_page=10)
            return render_template('blog/category.html', category = category)
        g.posts = Article.objects(kind__in=['article'], published=True, category = category,
                pub_date__lte=datetime.now()).paginate(page=page_num, per_page=10)
        if len(g.posts.items) == 0:
            flash('Sorry, there are no posts in the <b>%s</b> category.' % category)
            return abort(404)
        return render_template('blog/category.html', category = category)

    @route('/<slug>/', endpoint='page')
    @route('/archive/<slug>/', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        post = Post.objects(slug=slug, published=True).first_or_404()
        if not 'archive' in request.url and post.kind != 'page':
            return redirect(url_for('.post', slug=slug))

        return render_template('blog/post.html', post=post)


#Register our View Classes
PostView.register(blog)