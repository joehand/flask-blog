from flask import (Blueprint, render_template, jsonify, request,
                   g, flash, redirect, url_for)

from flask.ext.security import current_user, login_required, roles_required
from flask.ext.classy import FlaskView, route

from ..blog import Post, Article, Note, PostForm
from ..blog import POST_TYPES

import json
import sys

admin = Blueprint('admin', __name__, url_prefix='/admin')

class PostAdmin(FlaskView):
    """ Post Admin View """

    route_base = '/' 
    decorators = [roles_required('admin')]

    def before_request(self, name, *args , **kwargs):
        g.all_pages = Post.objects()
        g.pages = Post.objects(kind__in=['page'])
        g.posts = Post.objects(kind__in=['note', 'article'])
        g.POST_TYPES = POST_TYPES

        for post in g.all_pages:
            post.form = PostForm(prefix=str(post.id), kind=post.kind, slug=post.slug)

    @route('/')
    def index(self):
        """ Main admin dashboard view """
        form = PostForm(request.form)
        return render_template('admin/index.html', newForm=form)

    @route('/<slug>', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        post = Post.objects(slug=slug).first_or_404()
        post.form = PostForm(request.form)
        return render_template('admin/post_edit.html', post=post)

    def post(self):
        form = PostForm(request.form)
        if form.validate_on_submit():
            print 'posting'
            title = form.title.data.strip()
            kind = form.kind.data
            if kind == 'static':
                post = Post(title=title, user_ref=current_user.id, kind=kind)
            elif kind == 'note':
                post = Note(title=title, user_ref=current_user.id, kind=kind)
                link_url = form.link_url.data
                if link_url:
                    post.link_url = link_url
            else:
                post = Article(title=title, user_ref=current_user.id, kind='article')
                category = form.category.data.strip()
                if category:
                    post.category = category
            post.save()
            slug = post.slug
            return redirect(url_for('admin.post', slug=slug))
        else:
            print form.errors
            flash('Error with form')
            return render_template('admin/index.html', newForm=form)

    def put(self, id):
        try:
            post = Post.objects(id=id).first()
            post = post.validate_json(json.loads(request.data))
            return post.to_dict()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            # TODO Make these more helpful
            return jsonify(status='error', error=''), 400

    def delete(self, id):
        try:
            post = Post.objects(id=id).first_or_404()
            post.delete()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            # TODO Make these more helpful
            return jsonify(), 400
        return jsonify( { 'result': True } )


#Register our View Class
PostAdmin.register(admin)