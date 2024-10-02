from flask import Flask, session, request, abort
from flask_socketio import SocketIO, send, join_room, leave_room
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

db_config = {
    'user': 'your_db_user',
    'password': 'your_db_password',
    'host': '127.0.0.1',
    'database': 'your_db_name',
    'raise_on_warnings': True
}

@socketio.on('connect', namespace='/test')
def test_connect():
    if 'username' in session:
        admin_id = get_admin_id_from_username(session['username'])
        pc = request.args.get('pc')
        if has_access(admin_id, pc):
            join_room(pc)
        else:
            abort(403)
    else:
        abort(401)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    pc = request.args.get('pc')
    leave_room(pc)

@socketio.on('screenshot', namespace='/test')
def screenshot(data):
    pc = data['pc']
    admin_id = get_admin_id_from_username(session['username'])
    if has_access(admin_id, pc):
        send({'image': data['image']}, room=pc)

def get_admin_id_from_username(username):
    # 实现根据用户名获取管理员ID的函数
    pass

def has_access(admin_id, pc):
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    query = "SELECT access_granted FROM admin_pc_access WHERE admin_id = %s AND pc = %s"
    cursor.execute(query, (admin_id, pc))
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    return result and result

if __name__ == '__main__':
    socketio.run(app)
