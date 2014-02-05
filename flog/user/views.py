from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify, abort)

from flask.ext.security import current_user, login_required

from .models import User


user = Blueprint('user', __name__, url_prefix='/user')


@login_required
@user.route('/')
def index():
    return abort(404)
