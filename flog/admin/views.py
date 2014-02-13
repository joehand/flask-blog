from urlparse import urlparse
from hashlib import sha1
import sys, json, time, os, base64, hmac, urllib

from flask import (Blueprint, render_template, jsonify, request, Response,
                   g, flash, redirect, url_for, current_app, make_response)

from flask.ext.security import current_user, login_required, roles_required
from flask.ext.classy import FlaskView, route

from ..blog import Post, PostForm
from ..blog import POST_TYPES
from .upload import process_upload
from ..utils import s3_upload


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
        form = PostForm()
        return render_template('admin/index.html', newForm=form)

    @route('/<slug>', endpoint='post')
    def get(self, slug):
        """ View for a single post"""
        post = Post.objects(slug=slug).first_or_404()
        post.form = PostForm()
        return render_template('admin/post_edit.html', post=post)

    @route("/upload/", methods=['GET', 'POST'], endpoint='upload')
    def upload(self):
        posts = []
        if request.method == 'POST':
            uploaded_files = request.files.getlist("file")
            print uploaded_files
            posts = process_upload(uploaded_files)

            for post in posts:
                post.form = PostForm(prefix=str(post.id), kind=post.kind, slug=post.slug)
        return render_template('admin/upload.html', posts=posts)

    @route("/export/", endpoint='export')
    @route("/export/<slug>", endpoint='export')
    def export(self, slug=None):
        if slug:
            post_export = Post.objects(slug=slug).first_or_404().generate_export()
            response = make_response(post_export['content'])
            response.headers["Content-Disposition"] = "attachment; filename=%s.md" % post_export['filename']
            return respose
        else:
            posts = Post.objects()

            urls = []

            for post in posts:
                post_export = post.generate_export()
                url = s3_upload(post_export['filename'], post_export['content'])
                urls.append(url)
        return render_template('admin/export.html', urls=urls)

    def post(self):
        form = PostForm(request.form)
        if form.validate_on_submit():
            print 'posting'
            title = form.title.data.strip()
            kind = form.kind.data
            if kind == 'page':
                post = Post(title=title, user_ref=current_user.id, kind=kind)
            elif kind == 'note':
                post = Post(title=title, user_ref=current_user.id, kind=kind)
                link_url = form.category.data
                if link_url:
                    post.link_url = urlparse(link_url).geturl()
            else:
                post = Post(title=title, user_ref=current_user.id, kind='article')
                category = form.category.data.strip().lower()
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

    @route('/sign_s3/', endpoint='signS3')
    def sign_s3(self):
        AWS_ACCESS_KEY = current_app.config['AWS_ACCESS_KEY_ID']
        AWS_SECRET_KEY =  current_app.config['AWS_SECRET_ACCESS_KEY']
        S3_BUCKET =  current_app.config['S3_BUCKET_NAME']

        object_name = request.args.get('s3_object_name')
        mime_type = request.args.get('s3_object_type')

        expires = int(time.time()+20)
        amz_headers = "x-amz-acl:public-read"

        put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)

        signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha1).digest())
        signature = urllib.quote_plus(signature.strip())

        url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)

        return json.dumps({
            'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' \
                % (url, AWS_ACCESS_KEY, expires, signature),
            'url': url
            })



#Register our View Class
PostAdmin.register(admin)