from flask import (Blueprint, render_template, jsonify, request,
                   flash, redirect, url_for)

from flask.ext.security import current_user, login_required, roles_required
from flask.ext.classy import FlaskView, route

from ..blog import Post, Article, Link, PostForm

admin = Blueprint('admin', __name__, url_prefix='/admin')

class PostAdminView(FlaskView):
    """ Post Admin View """

    route_base = '/'
    decorators = [roles_required('admin')]

    @route('/')
    def index(self):
        """ Main admin dashboard view """
        posts = Post.objects()
        form = PostForm(request.form)
        return render_template('admin/index.html', posts=posts, form=form)

    def post(self):
        form = PostForm(request.form)
        if form.validate_on_submit():
            print 'posting'
            title = form.title.data.strip()
            kind = form.kind.data
            if kind == 'article':
                post = Article(title=title, user_ref=current_user.id, kind=kind)
            elif kind == 'link':
                post = Link(title=title, user_ref=current_user.id, kind=kind)
            else:
                post = Post(title=title, user_ref=current_user.id, kind=kind)
            post.save()
            slug = post.slug
            return redirect(url_for('blog.post', slug=slug))
        else:
            print form.errors
            flash('some error')
            return render_template('admin/index.html', form=form)


#Register our View Class
PostAdminView.register(admin)