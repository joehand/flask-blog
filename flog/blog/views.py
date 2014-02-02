from flask import (Blueprint, render_template, flash, g,
                    request, redirect, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user

from models import Post

from datetime import datetime

blog = Blueprint('blog', __name__, url_prefix='')

class PostView(FlaskView):
    """ Our base ViewClass for any Post related endpoints 
    """
    route_base = '/'

    def before_request(self, name, *args, **kwargs):
        if current_user.has_role('admin'):
            g.pages = Post.objects(kind__in=['page'])
            g.posts = Post.objects(kind__in=['note', 'article'])
        else:
            g.pages = Post.objects(kind__in=['page'], 
                published=True, pub_date__lte=datetime.now())
            g.posts = Post.objects(kind__in=['note', 'article'], 
                published=True, pub_date__lte=datetime.now())

    def index(self):
        """ Our main index view """
        return render_template('blog/index.html')
    
    @route('/archive/', endpoint='archive')
    def archive(self):
        """ Archive View """
        return render_template('blog/archive.html')

    @route('/notes/', endpoint='notes')
    def notes(self):
        """ Notes View """
        return render_template('blog/notes.html')

    @route('/<slug>', endpoint='page')
    @route('/archive/<slug>', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        post = Post.objects(slug=slug).first_or_404()
        if not 'archive' in request.url and post.kind != 'page':
            return redirect(url_for('.post', slug=slug))

        posts = Post.objects()
        return render_template('blog/post.html', post=post)

#Register our View Classes
PostView.register(blog)