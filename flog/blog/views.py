from flask import (Blueprint, render_template, flash, abort,
                    request, redirect, url_for, jsonify)

from flask.ext.security import current_user, login_required
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
    route_base = '/'

    @route('/')
    def index(self):
        """ Our main index view """
        posts = Post.objects()
        return render_template('index.html', posts=posts)

    @route('/archive/<slug>', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        post = Post.objects(slug=slug).first_or_404()
        return render_template('post.html', post=post)

    @login_required
    @route('/edit/<id>', methods=['PUT'])
    def put(self, id):
        if 'content' in request.data:
            try:
                content = json.loads(request.data)['content']
                post = Post.objects(id=id).first()
                post.content = content.encode('utf-8')
                post.save()
                return jsonify( post.to_dict() )
            except:
                print "Unexpected error:", sys.exc_info()[0]
                # TODO Make these more helpful
                abort(400)
        return abort(400)


#Register our View Classes
PostView.register(blog)

