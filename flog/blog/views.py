from flask import (Blueprint, render_template, flash, g,
                    request, redirect, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user

from models import Post

blog = Blueprint('blog', __name__, url_prefix='')

class PostView(FlaskView):
    """ Our base ViewClass for any Post related endpoints 
    """
    route_base = '/'

    def before_request(self, name, *args, **kwargs):
        if current_user.has_role('admin'):
            g.pages = Post.objects(kind__in=['static'])
            g.posts = Post.objects(kind__in=['link', 'article'])
        else:
            g.pages = Post.objects(kind__in=['static'], published=True)
            g.posts = Post.objects(kind__in=['link', 'article'], published=True)

    def index(self):
        """ Our main index view """
        post = Post.objects(kind__in=['link', 'article']).first()
        return render_template('index.html', post=post)
    
    @route('/archive/', endpoint='archive')
    def archive(self):
        """ Archive View """
        return render_template('index.html')

    @route('/<slug>', endpoint='page')
    @route('/archive/<slug>', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        post = Post.objects(slug=slug).first_or_404()
        if not 'archive' in request.url and post.kind != 'static':
            return redirect(url_for('.post', slug=slug))

        posts = Post.objects()
        return render_template('post.html', post=post)

#Register our View Classes
PostView.register(blog)