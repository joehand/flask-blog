from flask import (Blueprint, abort)

from flask.ext.security import login_required

from .models import User


user = Blueprint('user', __name__, url_prefix='/user')


@login_required
@user.route('/')
def index():
    return abort(404)
