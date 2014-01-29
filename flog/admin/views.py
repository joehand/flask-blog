from flask import (Blueprint, render_template, jsonify, request)

from flask.ext.security import login_required

admin = Blueprint('admin', __name__, url_prefix='/admin')

@login_required
@admin.route('/')
def index():
    return render_template('admin/index.html')
