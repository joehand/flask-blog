from datetime import date
import json
import sys
from urlparse import urlparse

from flask import (Blueprint, current_app, flash, g, make_response,
                    jsonify, redirect, render_template,
                    request, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import (current_user, login_required,
                                roles_required)

from ..blog import Comment, Post, PostForm
from ..blog import POST_TYPES
from ..daily import Daily
from .upload import process_upload
from ..utils import s3_upload, s3_signer

admin = Blueprint('admin', __name__, url_prefix='/admin')

class PostAdmin(FlaskView):
    ''' Post Admin View '''

    route_base = '/'
    decorators = [login_required, roles_required('admin')]

    @login_required
    def before_request(self, name, *args , **kwargs):
        g.all_pages = Post.objects(user_ref=current_user.id)
        g.POST_TYPES = POST_TYPES

        for post in g.all_pages:
            post.form = PostForm(prefix=str(post.id),
                                kind=post.kind,
                                slug=post.slug)

    def before_index(self, *args, **kwargs):
        g.daily = Daily.objects(user_ref=current_user.id)
        if (len(g.daily) and
                g.daily[0].is_today() and
                g.daily[0].goal_met()):
            g.wrote_today = True
        else:
            g.wrote_today = False
        g.streak = 1 if g.wrote_today else 0
        for i, day in enumerate(g.daily):
            d1 = day.date.date()
            if day.is_today():
                continue
            elif not day.goal_met():
                break
            elif i > 0:
                d0 = g.daily[i-1]
                d0 = d0.date.date()
                delta = d0 - d1
                if delta.days == 1: g.streak += 1

        g.comments = []
        for post in g.all_pages:
            if post.comments:
                print 'getting comments for %s' % post.title
                for comment in post.comments:
                    print 'comment %s' % comment.name
                    comment.post_slug = post.slug
                    g.comments.append(comment)


    @route('/', endpoint='index')
    def index(self):
        ''' Main admin post view '''
        form = PostForm()
        return render_template('admin/dashboard.html', newForm=form)

    @route('/posts/', endpoint='post_list')
    def post_list(self):
        ''' Post List '''
        form = PostForm()
        return render_template('admin/post_list.html', newForm=form)

    @route('/<slug>', endpoint='post')
    def get(self, slug):
        ''' View for a single post '''
        post = Post.objects(slug=slug).first_or_404()
        post.form = PostForm()
        return render_template('admin/post_edit.html', post=post)

    @route('/upload/', methods=['GET', 'POST'], endpoint='upload')
    def upload(self):
        ''' Upload View '''
        posts = []
        if request.method == 'POST':
            uploaded_files = request.files.getlist('file')
            posts = process_upload(uploaded_files)
            for post in posts:
                post.form = PostForm(prefix=str(post.id),
                                    kind=post.kind, slug=post.slug)
        return render_template('admin/upload.html', posts=posts)

    @route('/export/', endpoint='export')
    @route('/export/<slug>', endpoint='export')
    def export(self, slug=None):
        '''Export View '''
        if slug:
            post_export = Post.objects(
                    slug=slug).first_or_404().generate_export()
            response = make_response(post_export['content'])
            response.headers['Content-Disposition'] = 'attachment; filename=%s.md' % post_export['filename']
            return response

        posts = Post.objects()
        urls = []
        for post in posts:
            post_export = post.generate_export()
            url = s3_upload(post_export['filename'], post_export['content'])
            urls.append(url)
        return render_template('admin/export.html', urls=urls)

    def post(self):
        ''' POST Request to create new Post() '''
        form = PostForm(request.form)
        if form.validate_on_submit():
            # TODO: Move this to model
            print 'posting'
            title = form.title.data.strip()
            kind = form.kind.data
            if kind == 'page':
                post = Post(title=title,
                        user_ref=current_user.id, kind=kind)
            elif kind == 'note':
                post = Post(title=title,
                        user_ref=current_user.id, kind=kind)
                link_url = form.category.data
                if link_url:
                    post.link_url = urlparse(link_url).geturl()
            else:
                post = Post(title=title,
                        user_ref=current_user.id, kind='article')
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
            print 'Unexpected error:', sys.exc_info()[0]
            # TODO Make these more helpful
            return jsonify(status='error', error=''), 400

    def delete(self, id):
        try:
            post = Post.objects(id=id).first_or_404()
            post.delete()
        except:
            print 'Unexpected error:', sys.exc_info()[0]
            # TODO Make these more helpful
            return jsonify(), 400
        return jsonify( { 'result': True } )

    @route('/comments/', endpoint='comments')
    @route('/comments/<slug>/', endpoint='comments')
    def comments(self, slug=None):
        if slug:
            posts = [Post.objects(slug=slug).first_or_404()]
        else:
            posts = Post.objects(user_ref=current_user.id,
                    kind__in=['note', 'article'])
        return render_template('admin/comments.html', posts=posts)

    @route('/comments/<slug>/<comment_id>',
            methods=['GET', 'DELETE'], endpoint='delete_comment')
    def delete_comment(self, slug, comment_id):
        Post.objects(slug=slug).update_one(
                pull__comments__id=Comment(id=comment_id).id)
        return redirect(request.referrer)


@roles_required('admin')
@admin.route('/sign_s3/', endpoint='signS3')
def sign_s3():
    return s3_signer(request)

#Register our View Class
PostAdmin.register(admin)
