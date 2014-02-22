from datetime import datetime, date
import json
import sys

from flask import (Blueprint, current_app, flash, g, jsonify,
                    redirect, render_template, request, url_for)

from flask.ext.classy import FlaskView, route
from flask.ext.security import current_user, roles_required

from .forms import SettingsForm
from .models import Daily, Settings
from ..utils import validate_date

writer = Blueprint('writer', __name__, url_prefix='/admin/writer')

class DailyAdmin(FlaskView):
    ''' Daily Writing View '''

    route_base = '/' 
    decorators = [roles_required('admin')]

    def before_request(self, name, *args , **kwargs):
        g.today = date.today()
        g.posts = Daily.objects(user_ref=current_user.id)
        g.word_goal = Settings.objects(user_ref=current_user.id).first().word_goal

    @route('/', endpoint='index')
    def index(self):
        ''' '''
        return redirect(url_for('.today'))

    @route('/today', endpoint='today')
    @route('/<post_date>', endpoint='daily')
    def get(self, post_date=None):
        ''' Daily Writing View
        '''
        if 'today' in request.path:
            post_date = g.today
        else:
            post_date = datetime.strptime(post_date, '%d-%b-%Y')
        is_today = True if post_date == g.today else False
        post = Daily.objects(user_ref=current_user.id, date=post_date).first()
        if post is None:
            if is_today:
                # create a new post for today
                post = Daily(user_ref=current_user.id, date=g.today)
                post.save()
            else:
                flash('No post found for date: %s' % post_date.strftime('%d-%b-%Y'))
                return redirect(url_for('.today'))
        return render_template('admin/writer.html', post=post, is_today=is_today)

    def put(self, id):
        try:
            post = Daily.objects(id=id).first()
            post = post.validate_json(json.loads(request.data))
            return post.to_dict()
        except:
            print 'Unexpected error:', sys.exc_info()[0]
            # TODO Make these more helpful
            return jsonify(status='error', error=''), 400

    @route('/settings', methods=['GET', 'POST'])
    def settings(self):
        ''' '''
        form = SettingsForm(request.form)
        settings = Settings.objects(user_ref=current_user.id).first()
        if form.validate_on_submit():
            if not settings:
                settings = Settings(user_ref=current_user.id)
            settings.word_goal = form.data['word_goal']
            settings.save()
        elif settings:
            form.word_goal.data = settings.word_goal
        return render_template('admin/writer_settings.html', form=form)


#Register our View Class
DailyAdmin.register(writer)