from app import socketio, db
from flask_socketio import emit, leave_room, join_room
from app.forum.models import post, thread
from app.auth.models import User

@socketio.on('join')
def join_room_(data):
    join_room(data['room'])
    socketio.emit('status', data, room=data['room'], dif_user=0)

@socketio.on('leave')
def leave_room_(data):
    leave_room(data['room'])
    print('User gonna leave')
    socketio.emit('left_room_announcement', data, room=data['room'], dif_user=0)

@socketio.on('send_message')
def send_message(data):
    user_ = User.query.filter_by(username=data['username']).first()
    thread_ = thread.query.filter_by(subject=data['room']).first()
    p = post(message=data['message'], user_id=user_.id, thread_id=thread_.id)
    db.session.add(p)
    db.session.commit()
    p = post.query.filter_by(message=data['message'], user_id=user_.id, thread_id=thread_.id).first()
    socketio.emit('received_message', {'room': data['room'], 'user_id': p.user_id, 'username': user_.username, 'msg': p.message, 'post_id': p.id, 'thread_id': thread_.id}, room=data['room'], dif_user=p.user_id)

@socketio.on('remove')
def remove_post(data):
    id = int(data['post_id'].split('f')[1])
    post_ = post.query.filter_by(id=id).first()
    db.session.delete(post_)
    db.session.commit()
    socketio.emit('confirm_remove', {"id": data['post_id']}, room=data['room'])
