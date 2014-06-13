from datetime import datetime

from flask import (abort, Blueprint, flash, g, redirect,
                    render_template, request, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user
from bleach import clean, linkify
from markdown import Markdown

from .constants import ALLOWED_COMMENT_TAGS
from .forms import CommentForm
from .models import Comment, Post

blog = Blueprint('blog', __name__, url_prefix='')

md = Markdown()

class PostView(FlaskView):
    ''' Our base ViewClass for any Post related endpoints
    '''
    route_base = '/'

    def _clean_text(self, text):
        """ Cleans up submitted text from users
        """
        return linkify(clean(md.convert(text),
                tags=ALLOWED_COMMENT_TAGS, strip=True))

    def index(self):
        ''' Our main index view '''
        post = Post.objects(kind__in=['note', 'article'],
                published=True, pub_date__lte=datetime.now()).first()
        home = Post.objects(kind__in=['page'], slug='home',
                published=True, pub_date__lte=datetime.now()).first()
        return render_template('blog/home.html', post=post, home=home)

    @route('/archive/', endpoint='archive',)
    def archive(self):
        ''' Archive View '''
        g.posts = Post.objects(kind__in=['article', 'note'],
                published=True, pub_date__lte=datetime.now())
        return render_template('blog/archive.html')

    @route('/blog/', endpoint='blog')
    @route('/blog/<int:page_num>', endpoint='blog')
    def blog(self, page_num=1):
        ''' Blog View '''
        g.posts = Post.objects(kind__in=['article', 'note'],
            published=True,
            pub_date__lte=datetime.now()).paginate(
            page=page_num, per_page=3)
        return render_template('blog/blog.html')

    @route('/category/<category>/', endpoint='category')
    @route('/category/<category>/<int:page_num>/', endpoint='category')
    def category(self, category, page_num=1):
        ''' Category Page'''
        if category == 'note':
            g.posts = Post.objects(kind__in=['note'], published=True,
                pub_date__lte=datetime.now()).paginate(page=page_num,
                per_page=10)
            return render_template('blog/category.html',
                    category = category)

        g.posts = Post.objects(kind__in=['article'],
                published=True, category = category,
                pub_date__lte=datetime.now()).paginate(page=page_num,
                per_page=10)
        if len(g.posts.items) == 0:
            flash('Sorry, there are no posts in the <b>%s</b> category.' % category)
            return abort(404)
        return render_template('blog/category.html', category=category)

    @route('/<slug>/', endpoint='page')
    @route('/archive/<slug>/', endpoint='post')
    def get(self, slug):
        ''' View for a single post'''
        form = CommentForm()
        post = Post.objects(slug=slug, published=True).first_or_404()
        if not 'archive' in request.url and post.kind != 'page':
            return redirect(url_for('.post', slug=slug))
        return render_template('blog/post.html', post=post, form=form)

    @route('/archive/<slug>/', methods=['POST'])
    def post(self, slug):
        ''' Post action for comment'''
        form = CommentForm(request.form)
        post = Post.objects(slug=slug, published=True).first_or_404()
        if form.validate_on_submit():
            name = clean(form.name.data.strip(), tags=[], strip=True)
            content = self._clean_text(form.content.data)
            email = form.email.data
            comment = Comment(name=name, content=content, email=email)
            post.update(push__comments=comment)
            flash('Thanks for the comment!')
            return redirect(url_for('.post', slug=slug))
        flash('Errors on comment form')
        return render_template('blog/post.html', post=post, form=form)

#Register our View Classes
PostView.register(blog)
