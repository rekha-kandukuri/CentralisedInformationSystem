from app import app, db, socketio
from app.forum.models import thread, post
from app.course.models import Courses
from app.auth.models import User


# Flask Shell Command Gives Access to DataBase Manipulation Facilated Through Flask SQLAlchemy
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'thread': thread, 'post': post, 'course': Courses}


if __name__ == '__main__':
    socketio.run(app, debug=True, log_output=True, port=8000)
