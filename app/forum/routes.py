from .models import thread, post
from app import app
from flask_login import login_required
from flask import render_template
from app.forum import forum

@forum.route('/forum')
@login_required
def forum_home():
    threads = thread.query.all()
    return render_template('forumhome.html', title='Forum', threads=threads)

@forum.route('/thread/<int:thread_id>', methods=['POST', 'GET'])
@login_required
def forum_(thread_id):
    posts = post.query.filter_by(thread_id=thread_id).order_by(post.time.asc())
    thread_name = thread.query.filter_by(id=thread_id).first().subject
    return render_template('forum.html', title='Forum', posts=posts, room=thread_name)
