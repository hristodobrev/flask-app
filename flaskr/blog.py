from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, author_id, u.username, created"
        " FROM post p JOIN user u ON u.id == p.author_id"
        " ORDER BY created DESC"
    ).fetchall()

    likes = {}
    for post in posts:
        likes[post['id']] = db.execute(
            "SELECT u.id, u.username FROM like l"
            " JOIN user u ON u.id == l.user_id"
            " WHERE l.post_id = ?",
            (post['id'],)
        ).fetchall()

    return render_template('blog/index.html', posts=posts, likes=likes)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id) VALUES (?, ?, ?)",
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/delete/<int:id>', methods=('POST',))
@login_required
def delete(id):
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id,))
    db.commit()

    return redirect(url_for('blog.index'))


@bp.route('/like/<int:post_id>', methods=('POST',))
@login_required
def like_post(post_id):
    user_id = g.user['id']
    db = get_db()

    like = db.execute(
        "SELECT * FROM like WHERE user_id = ? AND post_id = ?",
        (user_id, post_id)
    ).fetchone()

    if like is None:
        db.execute(
            "INSERT INTO like (user_id, post_id) VALUES (?, ?)", (user_id, post_id))
        db.commit()

    return redirect(url_for('blog.index'))


def get_post(id, check_author=True):
    db = get_db()
    post = db.execute(
        "SELECT p.id, title, body, author_id, username, created"
        " FROM post p JOIN user u ON u.id == p.author_id"
        " WHERE p.id = ?",
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f'Post with id {id} does not exist')

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post
