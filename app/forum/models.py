from app import app, db
from datetime import datetime


class thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    description = db.Column(db.String(100))
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    posts = db.relationship('post', backref='BelongsTo', lazy='dynamic')

    def __repr__(self):
        return '<Thread by {} {}>'.format(self.user_id, self.created)


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(150))
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))

    def __repr__(self):
        return '<Post in thread {} by {}>'.format(self.thread_id, self.user_id)
