from flask import (
    Blueprint,
    render_template
)

from flaskr.auth import admin_required
from flaskr.db import get_db

bp = Blueprint('user', __name__,url_prefix='/users')

@bp.route('/', methods=('GET',))
@admin_required
def users():
    db = get_db()
    users = db.execute('SELECT * FROM user').fetchall()

    return render_template('user/index.html', users=users)