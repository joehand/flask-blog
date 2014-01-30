from flask import (Blueprint, render_template, jsonify, request,
                   g, flash, redirect, url_for)

from flask.ext.security import current_user, login_required, roles_required
from flask.ext.classy import FlaskView, route

from ..blog import Post, Article, Link, PostForm

import json
import sys
import datetime

admin = Blueprint('admin', __name__, url_prefix='/admin')

class PostAdmin(FlaskView):
    """ Post Admin View """

    route_base = '/'
    decorators = [roles_required('admin')]

    def before_request(self, name, *args , **kwargs):
        g.pages = Post.objects(kind__in=['static'])
        g.posts = Post.objects(kind__in=['link', 'article'])

    @route('/')
    def index(self):
        """ Main admin dashboard view """
        form = PostForm(request.form)
        return render_template('admin/index.html', form=form)

    @route('/<slug>', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        post = Post.objects(slug=slug).first_or_404()
        return render_template('post.html', post=post)

    def put(self, id):
        try:
            post = Post.objects(id=id).first()
            postJSON = json.loads(request.data)

            #TODO: Put this validation elsewhere
            for key, val in postJSON.items():
                if key == 'content':
                    val = val
                if key == 'title':
                    val = val.strip()
                if key == 'slug':
                    val = val.strip().replace(' ', '-')
                if key == 'published':
                    if val == 'False':
                        val = False
                    elif val == 'True':
                        val = True
                if key in ['title', 'slug', 'content', 'published', 'kind']:
                    post[key] = val

            post.save()
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
PostAdmin.register(admin)