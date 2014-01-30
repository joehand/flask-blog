from flask import (Blueprint, render_template, flash, abort,
                    request, redirect, url_for, jsonify)

from flask.ext.security import current_user, roles_required
from flask.ext.classy import FlaskView, route
from flask.ext.mongoengine.wtf import model_form

from models import Post

import json
import sys

blog = Blueprint('blog', __name__, url_prefix='')

PostForm = model_form(Post)

class PostView(FlaskView):
    """ Our base ViewClass for any Post related endpoints 
    """
    route_base = '/archive'

    def index(self):
        """ Our main index view """
        posts = Post.objects()
        return render_template('index.html', posts=posts)

    @route('/<slug>', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        posts = Post.objects()
        post = Post.objects(slug=slug).first_or_404()
        return render_template('post.html', posts=posts, post=post)

    @roles_required('admin')
    def put(self, id):
        try:
            post = Post.objects(id=id).first()

            postJSON = json.loads(request.data)

            #TODO: Put this validation elsewhere
            for key, val in postJSON.items():
                if key == 'content':
                    val = val.encode('utf-8')
                if key == 'title':
                    val = val.strip()
                if key == 'slug':
                    val = val.strip().replace(' ', '-')
                if key in ['title', 'slug', 'content', 'published', 'kind']:
                    post[key] = val

            post.save()
            return jsonify( post.to_dict() )
        except:
            print "Unexpected error:", sys.exc_info()[0]
            # TODO Make these more helpful
            return jsonify(status='error', error=''), 400

    @roles_required('admin')
    def delete(self, id):
        try:
            post = Post.objects(id=id).first_or_404()
            post.delete()
        except:
            print "Unexpected error:", sys.exc_info()[0]
            # TODO Make these more helpful
            jsonify()
        return jsonify( { 'result': True } )


#Register our View Classes
PostView.register(blog)

