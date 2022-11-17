from flask_admin import Admin
from flask_login import current_user
from flask import redirect, url_for, request
from app import app, db, login
from flask_admin.contrib.sqla import ModelView
from app.auth.models import User
from app.forum.models import thread, post
from app.course.models import Courses
from flask_admin.model import typefmt
from datetime import date
from wtforms import DateTimeField

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


class adminmodelview(ModelView):
    def is_accessible(self):
        return (current_user.is_authenticated and current_user.is_admin)

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('home.index'))

class UserAdminModel(adminmodelview):
    can_view_details = True
    form_overrides = dict(last_seen=DateTimeField)

class PostAdminModel(adminmodelview):
    can_view_details = True
    form_overrides = dict(time=DateTimeField)

class ThreadAdminModel(adminmodelview):
    can_view_details = True
    form_overrides = dict(created=DateTimeField)

class CourseAdminModel(adminmodelview):
    can_view_details = True
    form_overrides = dict(created=DateTimeField)


admin = Admin(app, name='celis', template_mode='bootstrap3')
admin.add_view(UserAdminModel(User, db.session))
admin.add_view(PostAdminModel(post, db.session))
admin.add_view(ThreadAdminModel(thread, db.session))
admin.add_view(CourseAdminModel(Courses, db.session))
