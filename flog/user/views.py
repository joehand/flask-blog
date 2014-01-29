from flask import (Blueprint, render_template, url_for, flash, 
                    redirect, session, request, jsonify)

from flask.ext.security import current_user

from .models import User


user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/')
def index():
    return jsonify(user=current_user.to_dict())


@user.route('/clear')
def clear():
    current_user.services = None
    current_user.save()
    return jsonify(user=current_user.to_dict())
